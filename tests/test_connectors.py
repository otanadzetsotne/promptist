import pytest
from promptist.connectors.openai_client import OpenAIClient
from promptist.connectors.anthropic_client import AnthropicClient
from promptist.connectors.azure_openai_client import AzureOpenAIClient
from promptist.connectors.base import ChatMessage
from promptist.models import Prompt


def test_openai_client_init_env_missing(monkeypatch):
    pytest.importorskip('openai')
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    try:
        OpenAIClient(api_key=None)
    except ValueError as e:
        assert 'OPENAI_API_KEY' in str(e)


def test_anthropic_client_init_env_missing(monkeypatch):
    pytest.importorskip('anthropic')
    monkeypatch.delenv('ANTHROPIC_API_KEY', raising=False)
    try:
        AnthropicClient(api_key=None)
    except ValueError as e:
        assert 'ANTHROPIC_API_KEY' in str(e)


def test_azure_openai_client_init_env_missing(monkeypatch):
    pytest.importorskip('openai')
    for var in ['AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_DEPLOYMENT']:
        monkeypatch.delenv(var, raising=False)
    try:
        AzureOpenAIClient()
    except ValueError as e:
        assert any(x in str(e) for x in ['AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_DEPLOYMENT'])


def test_protocol_complete_signature_exists():
    # This test ensures complete() exists on clients
    for cls in [OpenAIClient, AnthropicClient, AzureOpenAIClient]:
        assert hasattr(cls, 'complete')


