# main.py
import asyncio
import logging
from collections import defaultdict
from discord import Message as DiscordMessage, app_commands
import discord
from src.base import Message, Conversation, ThreadConfig
from src.constants import (
    BOT_INVITE_URL,
    DISCORD_BOT_TOKEN,
    EXAMPLE_CONVOS,
    ACTIVATE_THREAD_PREFX,
    MAX_THREAD_MESSAGES,
)
from src.utils import (
    logger,
    should_block,
    close_thread,
    is_last_message_stale,
    discord_message_to_message,
)
from src.completion import generate_completion_response, process_response
from src.moderation import (
    moderate_message,
    send_moderation_blocked_message,
    send_moderation_flagged_message,
)
from src.relevance import is_relevant_message_llm

logging.basicConfig(
    format="[%(asctime)s] [%(filename)s:%(lineno)d] %(message)s", level=logging.INFO
)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
thread_data = defaultdict()

@client.event
async def on_ready():
    logger.info(f"We have logged in as {client.user}. Invite URL: {BOT_INVITE_URL}")
    for c in EXAMPLE_CONVOS:
        messages = []
        for m in c.messages:
            if m.user == "Lenard":
                messages.append(Message(user=client.user.name, text=m.text))
            else:
                messages.append(m)
        completion.MY_BOT_EXAMPLE_CONVOS.append(Conversation(messages=messages))
    await tree.sync()

@client.event
async def on_message(message: DiscordMessage):
    try:
        if message.author == client.user:
            return

        if client.user in message.mentions or message.content.startswith('!chat'):
            user_message = message.content.replace(f'<@!{client.user.id}>', '').strip()
            response = await get_chatgpt_response(user_message)

            if isinstance(message.channel, discord.Thread):
                await message.channel.send(response)
            else:
                thread = await message.channel.create_thread(name=f"Chat with {message.author.name}", message=message)
                thread_data[thread.id] = ThreadConfig(
                    model=DEFAULT_MODEL, max_tokens=512, temperature=1.0
                )
                await thread.send(response)
            return

        if should_block(guild=message.guild):
            return

        if not isinstance(message.channel, discord.Thread):
            return

        if message.channel.archived or message.channel.locked or not message.channel.name.startswith(ACTIVATE_THREAD_PREFX):
            return

        if message.channel.id not in thread_data:
            thread_data[message.channel.id] = ThreadConfig(
                model=DEFAULT_MODEL, max_tokens=512, temperature=1.0
            )

        # Use the LLM-based relevance check
        if not await is_relevant_message_llm(message):
            return  # Skip irrelevant messages

        flagged_str, blocked_str = moderate_message(
            message=message.content, user=message.author
        )
        await send_moderation_blocked_message(
            guild=message.guild,
            user=message.author,
            blocked_str=blocked_str,
            message=message.content,
        )
        if len(blocked_str) > 0:
            try:
                await message.delete()
                await message.channel.send(
                    embed=discord.Embed(
                        description=f"❌ **{message.author}'s message has been deleted by moderation.**",
                        color=discord.Color.red(),
                    )
                )
                return
            except Exception as e:
                await message.channel.send(
                    embed=discord.Embed(
                        description=f"❌ **{message.author}'s message has been blocked by moderation but could not be deleted. Missing Manage Messages permission in this Channel.**",
                        color=discord.Color.red(),
                    )
                )
                return
        await send_moderation_flagged_message(
            guild=message.guild,
            user=message.author,
            flagged_str=flagged_str,
            message=message.content,
            url=message.jump_url,
        )
        if len(flagged_str) > 0:
            await message.channel.send(
                embed=discord.Embed(
                    description=f"⚠️ **{message.author}'s message has been flagged by moderation.**",
                    color=discord.Color.yellow(),
                )
            )

        await asyncio.sleep(1)  # Delay for 1 second
        latest_message = await message.channel.history(limit=1).flatten()
        if latest_message and latest_message[0].id != message.id:
            return  # If there is a new message, do not respond to this one

        logger.info(
            f"Thread message to process - {message.author}: {message.content[:50]} - {message.channel.name} {message.channel.jump_url}"
        )

        channel_messages = [
            discord_message_to_message(message)
            async for message in message.channel.history(limit=MAX_THREAD_MESSAGES)
        ]
        channel_messages = [x for x in channel_messages if x is not None]
        channel_messages.reverse()

        async with message.channel.typing():
            response_data = await generate_completion_response(
                messages=channel_messages,
                user=message.author,
                thread_config=thread_data[message.channel.id],
            )

        if is_last_message_stale(
            interaction_message=message,
            last_message=message.channel.last_message,
            bot_id=client.user.id,
        ):
            return

        await process_response(
            user=message.author, thread=message.channel, response_data=response_data
        )
    except Exception as e:
        logger.exception(e)

client.run(DISCORD_BOT_TOKEN)
