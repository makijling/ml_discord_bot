# src/constants.py

BOT_INVITE_URL = "https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot"
DISCORD_BOT_TOKEN = "your-discord-bot-token"
EXAMPLE_CONVOS = [
    Conversation(messages=[
        Message(user="Lenard", text="Hello! How can I help you today?"),
        Message(user="User", text="I have a question about your services."),
    ])
]
ACTIVATE_THREAD_PREFX = "Chat"
MAX_THREAD_MESSAGES = 50
SECONDS_DELAY_RECEIVING_MSG = 1
AVAILABLE_MODELS = ["model1", "model2"]
DEFAULT_MODEL = "model1"
