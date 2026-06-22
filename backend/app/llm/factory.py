"""
Hangi adapter kullanılacağını config.yaml'dan okur.
Yeni sağlayıcı eklemek için yalnızca yeni adapter + bu factory'e kayıt yeterli.
"""
from app.llm.adapter import LLMAdapter
from app.core.settings import get_config
from functools import lru_cache


@lru_cache
def get_llm_adapter() -> LLMAdapter:
    cfg = get_config()
    provider = cfg["llm"]["provider"]

    if provider == "claude":
        from app.llm.claude_adapter import ClaudeAdapter
        return ClaudeAdapter()
    # Faz 2: elif provider == "azure_openai": ...
    raise ValueError(f"Unknown LLM provider: {provider}")
