import os
from typing import Iterable

from promptist.connectors.base import ChatMessage, LLMClient
from promptist.models import Prompt


class AzureOpenAIClient(LLMClient):
    """
    Thin wrapper around OpenAI python client to talk to Azure OpenAI.
    Requires env vars (or args):
      - AZURE_OPENAI_API_KEY
      - AZURE_OPENAI_ENDPOINT (e.g., https://<resource>.openai.azure.com)
      - AZURE_OPENAI_DEPLOYMENT (the deployment name)
      - AZURE_OPENAI_API_VERSION (e.g., 2024-05-01-preview)
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        endpoint: str | None = None,
        deployment: str | None = None,
        api_version: str | None = None,
    ):
        try:
            from openai import OpenAI  # type: ignore
        except Exception as e:  # pragma: no cover
            raise RuntimeError("openai package is required. Install with 'pip install openai'.") from e

        self._OpenAI = OpenAI
        self.api_key = api_key or os.getenv('AZURE_OPENAI_API_KEY')
        self.endpoint = endpoint or os.getenv('AZURE_OPENAI_ENDPOINT')
        self.deployment = deployment or os.getenv('AZURE_OPENAI_DEPLOYMENT')
        self.api_version = api_version or os.getenv('AZURE_OPENAI_API_VERSION', '2024-05-01-preview')

        if not self.api_key:
            raise ValueError('AZURE_OPENAI_API_KEY is not set')
        if not self.endpoint:
            raise ValueError('AZURE_OPENAI_ENDPOINT is not set')
        if not self.deployment:
            raise ValueError('AZURE_OPENAI_DEPLOYMENT is not set')

        # Base URL points to the deployment root per OpenAI Python SDK Azure guidance
        self.base_url = f"{self.endpoint}/openai/deployments/{self.deployment}"

    def chat(self, *, model: str | None = None, messages: Iterable[ChatMessage], **kwargs) -> str:
        # For Azure, 'model' should be the deployment name; keep default to self.deployment if None
        model = model or self.deployment
        client = self._OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            default_query={"api-version": self.api_version},
        )
        resp = client.chat.completions.create(
            model=model,
            messages=[{'role': m.role, 'content': m.content} for m in messages],
            **kwargs,
        )
        return resp.choices[0].message.content or ''

    def complete(self, *, model: str | None = None, prompt: str | Prompt, **kwargs) -> str:
        text = prompt.text if isinstance(prompt, Prompt) else str(prompt)
        model = model or self.deployment
        client = self._OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            default_query={"api-version": self.api_version},
        )
        resp = client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': text}],
            **kwargs,
        )
        return resp.choices[0].message.content or ''


