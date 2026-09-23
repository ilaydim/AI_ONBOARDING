"""NFR-6.2: chunking ve chunk seçimi bağımsız test edilir."""
from app.content.loader import chunk_markdown, select_relevant_chunks


def test_chunk_empty():
    assert chunk_markdown("") == []


def test_chunk_splits_on_size_with_overlap():
    text = "\n\n".join(f"## Bölüm {i}\n" + ("kelime " * 60) for i in range(8))
    chunks = chunk_markdown(text)
    assert len(chunks) > 1
    assert all(len(c) <= 1000 + 200 + 500 for c in chunks)
    # overlap: bir chunk'ın sonu sonrakinin başında görünür
    assert chunks[0][-50:].strip() in chunks[1]


def test_select_relevant_prefers_matching_chunk():
    chunks = ["docker container image", "sprint planning agile", "database index"]
    assert select_relevant_chunks(chunks, "sprint agile")[0] == "sprint planning agile"


def test_select_relevant_falls_back_to_first():
    chunks = ["alpha", "beta"]
    assert select_relevant_chunks(chunks, "zzz") == ["alpha"]
