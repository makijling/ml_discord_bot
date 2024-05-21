# src/relevance.py
import asyncio
from transformers import pipeline

# Load a smaller model
model = pipeline('text-classification', model='distilbert-base-uncased')

async def get_llm_classification(prompt: str) -> str:
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, model, prompt)
    return result[0]['label']

async def is_relevant_message_llm(message):
    prompt = f"Is the following message relevant for a chat bot to respond to? Message: '{message.content}'"
    response = await get_llm_classification(prompt)
    return response.lower().strip() == "yes"
