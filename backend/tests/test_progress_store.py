"""NFR-5.2 atomik yazma / bozuk dosya kurtarma; FR-4.5 boşluk."""
import os
from app.content import progress_store as ps


def test_atomic_write_and_reload(tmp_path, monkeypatch):
    monkeypatch.setattr(ps, "DATA_DIR", str(tmp_path))
    ps.mark_task_completed("u1", "t1", 5)
    assert not any(f.endswith(".tmp") for f in os.listdir(tmp_path))
    assert ps.get_completion_stats("u1")["completed"] == 1


def test_corrupt_file_recovered(tmp_path, monkeypatch):
    monkeypatch.setattr(ps, "DATA_DIR", str(tmp_path))
    (tmp_path / "progress_u2.json").write_text("{broken")
    assert ps.get_completion_stats("u2")["total"] == 0
    assert (tmp_path / "progress_u2.json.corrupt").exists()


def test_gap_counts_per_topic(tmp_path, monkeypatch):
    monkeypatch.setattr(ps, "DATA_DIR", str(tmp_path))
    ps.record_gap("u3", "t1", "question_count")
    ps.record_gap("u3", "t1", "question_count")
    gaps = ps.get_gaps("u3")
    assert len(gaps) == 1 and gaps[0].count == 2
