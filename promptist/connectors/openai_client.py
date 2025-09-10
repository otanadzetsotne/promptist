import os
from typing import Iterable

from promptist.connectors.base import ChatMessage, LLMClient
from promptist.models import Prompt


class OpenAIClient(LLMClient):
    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        try:
            from openai import OpenAI  # type: ignore
        except Exception as e:  # pragma: no cover - import-time error surfaced at runtime
            raise RuntimeError("openai package is required. Install with 'pip install openai'.") from e
        self._OpenAI = OpenAI
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = base_url or os.getenv('OPENAI_BASE_URL')
        if not self.api_key:
            raise ValueError('OPENAI_API_KEY is not set')

    def chat(self, *, model: str, messages: Iterable[ChatMessage], **kwargs) -> str:
        client = self._OpenAI(api_key=self.api_key, base_url=self.base_url)
        resp = client.chat.completions.create(
            model=model,
            messages=[{'role': m.role, 'content': m.content} for m in messages],
            **kwargs,
        )
        return resp.choices[0].message.content or ''

    def complete(self, *, model: str, prompt: str | Prompt, **kwargs) -> str:
        text = prompt.text if isinstance(prompt, Prompt) else str(prompt)
        client = self._OpenAI(api_key=self.api_key, base_url=self.base_url)
        # Use chat.completions with a single user message for text prompts
        resp = client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': text}],
            **kwargs,
        )
        return resp.choices[0].message.content or ''


