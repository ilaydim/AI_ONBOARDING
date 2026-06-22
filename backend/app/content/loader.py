"""
İçerik Katmanı — SRS §3.2.4, §6
Markdown dosyalarını okur, chunk'lara böler, alakalı olanları seçer.
"""
import os
import re
from app.core.settings import get_config


def _get_content_path(language: str) -> str:
    cfg = get_config()
    base = cfg["content"]["base_path"]
    # config.yaml'daki relative path'i resolve et
    config_dir = os.path.join(os.path.dirname(__file__), "../../")
    return os.path.normpath(os.path.join(config_dir, base, language))


def load_markdown(filepath: str) -> str:
    if not os.path.exists(filepath):
        return ""
    with open(filepath, encoding="utf-8") as f:
        return f.read()


def load_company_content(language: str = "tr") -> str:
    base = _get_content_path(language)
    company_dir = os.path.join(base, "company")
    parts = []
    for filename in ["overview.md", "culture.md", "processes.md"]:
        fp = os.path.join(company_dir, filename)
        content = load_markdown(fp)
        if content:
            parts.append(f"## {filename}\n{content}")
    return "\n\n".join(parts)


def load_area_content(area: str, language: str = "tr") -> str:
    base = _get_content_path(language)
    area_dir = os.path.join(base, "areas", area)
    parts = []
    for filename in ["overview.md", "tasks.md", "resources.md"]:
        fp = os.path.join(area_dir, filename)
        content = load_markdown(fp)
        if content:
            parts.append(f"## {filename}\n{content}")
    return "\n\n".join(parts)


def list_available_areas(language: str = "tr") -> list[str]:
    base = _get_content_path(language)
    areas_dir = os.path.join(base, "areas")
    if not os.path.exists(areas_dir):
        return []
    return [d for d in os.listdir(areas_dir)
            if os.path.isdir(os.path.join(areas_dir, d))]


# ─── Chunking — SRS §6.4 ─────────────────────────────────────────────────────

def chunk_markdown(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """
    Başlık ve paragraf sınırlarında böl, overlap uygula.
    Cümle ortasında kesme yapma.
    """
    if not text:
        return []

    cfg = get_config()
    chunk_size = cfg["content"].get("chunk_size", chunk_size)
    overlap = cfg["content"].get("chunk_overlap", overlap)

    # Başlık ve paragrafları doğal sınırlar olarak kullan
    sections = re.split(r'\n(?=#{1,3} |\n)', text)
    sections = [s.strip() for s in sections if s.strip()]

    chunks = []
    current = ""

    for section in sections:
        if len(current) + len(section) > chunk_size and current:
            chunks.append(current.strip())
            # overlap: son overlap karakteri bir sonraki chunk'a taşı
            current = current[-overlap:] if len(current) > overlap else current
        current += "\n\n" + section

    if current.strip():
        chunks.append(current.strip())

    return chunks


def select_relevant_chunks(chunks: list[str], query: str, top_k: int = 3) -> list[str]:
    """
    TF-IDF benzeri keyword eşleştirme ile en alakalı chunk'ları seç.
    Faz 2'de vektör veritabanı ile değiştirilecek.
    """
    if not chunks:
        return []

    cfg = get_config()
    top_k = cfg["content"].get("top_k_chunks", top_k)

    query_words = set(re.findall(r'\w+', query.lower()))

    def score(chunk: str) -> int:
        chunk_words = set(re.findall(r'\w+', chunk.lower()))
        return len(query_words & chunk_words)

    scored = sorted(enumerate(chunks), key=lambda x: score(x[1]), reverse=True)
    # En az 1 chunk döndür, eğer hiç eşleşme yoksa ilk chunk'ı ver
    top = scored[:top_k]
    if all(score(c) == 0 for _, c in top):
        return [chunks[0]]
    return [chunks[i] for i, _ in top]


def build_context(area: str, query: str = "", language: str = "tr") -> str:
    """
    Şirket + alan içeriğini yükle, chunk'la, en alakalı olanları seç.
    """
    company = load_company_content(language)
    area_content = load_area_content(area, language)
    full_content = company + "\n\n" + area_content

    chunks = chunk_markdown(full_content)
    if query:
        relevant = select_relevant_chunks(chunks, query)
        return "\n\n---\n\n".join(relevant)
    return full_content
