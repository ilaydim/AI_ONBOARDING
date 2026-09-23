"""
Kullanıcı girdisi sanitizasyonu — SRS §7.2 (NFR-2.7)
Girdi LLM'e iletilmeden önce kontrol karakterleri ve prompt sınır işaretleyicilerinden
arındırılır; uzunluk sınırlanır. Sistem promptu ayrıca girdiyi "veri" olarak ele almayı söyler.
"""
import re

MAX_INPUT_CHARS = 4000

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
# Sistem promptundaki context sınırını (---) ve rol etiketlerini taklit eden satırlar
_DELIMITER_LINE = re.compile(r"^\s*(-{3,}|={3,}|#{3,})\s*$", re.MULTILINE)
_ROLE_MARKER = re.compile(r"^\s*(system|assistant|developer)\s*:", re.IGNORECASE | re.MULTILINE)


def sanitize_user_input(text: str, max_chars: int = MAX_INPUT_CHARS) -> str:
    text = _CONTROL_CHARS.sub("", text or "")
    text = _DELIMITER_LINE.sub("", text)
    text = _ROLE_MARKER.sub(lambda m: m.group(1) + " -", text)
    return text.strip()[:max_chars]
