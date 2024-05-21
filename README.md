# Discord Bot with LLM-Based Relevance Checking

This is a Discord bot that uses a large language model (LLM) to dynamically determine the relevance of messages for response.

## Setup

1. Clone the repository:
git clone <repository-url>
cd discord_bot
2. Install the dependencies:
pip install -r requirements.txt
3. Set up your environment variables (e.g., `DISCORD_BOT_TOKEN`).
4. Run the bot:
python main.py

## Project Structure

- `main.py`: The main entry point for the bot.
- `src/`: Contains all source code and modules.
- `base.py`: Base classes like `Message`, `Conversation`, `ThreadConfig`.
- `constants.py`: Constants used across the project.
- `utils.py`: Utility functions.
- `completion.py`: Functions related to generating responses using the LLM.
- `moderation.py`: Functions for moderating messages.
- `relevance.py`: Functions for LLM-based relevance checking.

## How to Use

- The bot listens for messages and checks if they are relevant using an LLM.
- Relevant messages are processed and responded to.
- Irrelevant messages are ignored.
