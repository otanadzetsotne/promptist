from dataclasses import dataclass
from typing import Iterable, Literal, Protocol
from promptist.models import Prompt


Role = Literal['system', 'user', 'assistant']


@dataclass
class ChatMessage:
    role: Role
    content: str


class LLMClient(Protocol):
    def chat(self, *, model: str, messages: Iterable[ChatMessage], **kwargs) -> str:  # returns text
        ...
    def complete(self, *, model: str, prompt: str | Prompt, **kwargs) -> str:  # returns text
        ...


