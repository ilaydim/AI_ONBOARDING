from groq import Groq
from app.llm.adapter import LLMAdapter
from app.core.settings import get_settings
from app.core.settings import get_config


class GroqAdapter(LLMAdapter):
    def __init__(self):
        settings = get_settings()
        self._client = Groq(api_key=settings.groq_api_key)
        cfg = get_config()
        self._model = cfg["llm"]["model"]
        self._max_tokens = cfg["llm"]["max_tokens"]

    def send_message(
        self,
        system_prompt: str,
        conversation_history: list[dict],
        user_message: str,
    ) -> str:
        messages = (
            [{"role": "system", "content": system_prompt}]
            + conversation_history
            + [{"role": "user", "content": user_message}]
        )
        response = self._client.chat.completions.create(
            model=self._model,
            max_tokens=self._max_tokens,
            messages=messages,
        )
        return response.choices[0].message.content
