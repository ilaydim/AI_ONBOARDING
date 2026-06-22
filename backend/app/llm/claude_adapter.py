"""
Claude (Anthropic) Adapter — Faz 1'de kullanılan tek adapter.
"""
import anthropic
from app.llm.adapter import LLMAdapter
from app.core.settings import get_settings
from app.core.settings import get_config


class ClaudeAdapter(LLMAdapter):
    def __init__(self):
        settings = get_settings()
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        cfg = get_config()
        self._model = cfg["llm"]["model"]
        self._max_tokens = cfg["llm"]["max_tokens"]

    def send_message(
        self,
        system_prompt: str,
        conversation_history: list[dict],
        user_message: str,
    ) -> str:
        messages = conversation_history + [{"role": "user", "content": user_message}]
        response = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text
