# src/base.py
from dataclasses import dataclass
from typing import List

@dataclass
class Message:
    user: str
    text: str

@dataclass
class Conversation:
    messages: List[Message]

@dataclass
class ThreadConfig:
    model: str
    max_tokens: int
    temperature: float
