"""
LLM Adapter Layer — SRS §3.2.3, §5.1
Vendor lock-in'i önlemek için tüm LLM çağrıları bu arayüz üzerinden yapılır.
"""
from abc import ABC, abstractmethod


class LLMAdapter(ABC):
    @abstractmethod
    def send_message(
        self,
        system_prompt: str,
        conversation_history: list[dict],
        user_message: str,
    ) -> str:
        """Tüm adapter'lar bu arayüzü implemente etmek zorundadır."""
        raise NotImplementedError
