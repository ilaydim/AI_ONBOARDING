"""
Test için sahte adapter — SRS §7.6 (NFR-6.1). Gerçek API çağrısı yapmaz.
"""
from app.llm.adapter import LLMAdapter


class MockAdapter(LLMAdapter):
    def __init__(self, reply: str = "mock reply", fail: bool = False):
        self.reply = reply
        self.fail = fail
        self.calls: list[dict] = []

    def send_message(self, system_prompt, conversation_history, user_message) -> str:
        self.calls.append({
            "system_prompt": system_prompt,
            "history": list(conversation_history),
            "user_message": user_message,
        })
        if self.fail:
            raise RuntimeError("mock LLM failure")
        return self.reply
