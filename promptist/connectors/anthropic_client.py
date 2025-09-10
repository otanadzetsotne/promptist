import os
from typing import Iterable

from promptist.connectors.base import ChatMessage, LLMClient
from promptist.models import Prompt


class AnthropicClient(LLMClient):
    def __init__(self, api_key: str | None = None):
        try:
            import anthropic  # type: ignore
        except Exception as e:  # pragma: no cover
            raise RuntimeError("anthropic package is required. Install with 'pip install anthropic'.") from e
        self._anthropic = anthropic
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError('ANTHROPIC_API_KEY is not set')

    def chat(self, *, model: str, messages: Iterable[ChatMessage], **kwargs) -> str:
        client = self._anthropic.Anthropic(api_key=self.api_key)
        # Anthropics expects system separate and user/assistant turns format; we keep simple mapping
        system = "\n\n".join(m.content for m in messages if m.role == 'system') or None
        user_msgs = [m for m in messages if m.role != 'system']
        resp = client.messages.create(
            model=model,
            system=system,
            messages=[{'role': m.role, 'content': m.content} for m in user_msgs],
            **kwargs,
        )
        # anthropic sdk v0.34 returns text at content[0].text
        try:
            return resp.content[0].text  # type: ignore[attr-defined]
        except Exception:
            return ""

    def complete(self, *, model: str, prompt: str | Prompt, **kwargs) -> str:
        text = prompt.text if isinstance(prompt, Prompt) else str(prompt)
        client = self._anthropic.Anthropic(api_key=self.api_key)
        resp = client.messages.create(
            model=model,
            messages=[{"role": "user", "content": text}],
            **kwargs,
        )
        try:
            return resp.content[0].text  # type: ignore[attr-defined]
        except Exception:
            return ""


