# src/utils.py
import logging

logger = logging.getLogger("discord_bot")

def should_block(guild):
    # Implement logic to determine if the bot should block messages in the given guild
    return False

def close_thread(thread):
    # Implement logic to close a thread
    pass

def is_last_message_stale(interaction_message, last_message, bot_id):
    # Implement logic to check if the last message is stale
    return False

def discord_message_to_message(discord_message):
    # Convert a Discord message to a custom Message object
    return Message(user=discord_message.author.name, text=discord_message.content)
