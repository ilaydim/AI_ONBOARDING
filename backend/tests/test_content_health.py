"""CM-1.5 / NFR-5.3 / CM-3.5: eksik veya hatalı md dosyası."""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.auth import get_current_user
from app.content import loader
from app.models.user import UserProfile

TASK = """## Task: T
- **ID:** x-001
- **Level:** junior
- **Dependency:** None
- **Expected Output:** o
- **Completion Criteria:** c
- **Estimated Duration:** 1 hour
- **Skippable:** No
"""


@pytest.fixture
def content(tmp_path, monkeypatch):
    monkeypatch.setattr(loader, "_get_content_path", lambda lang: str(tmp_path / lang))
    return tmp_path / "en" / "areas"


def _area(root, name, files):
    d = root / name
    d.mkdir(parents=True)
    for f, body in files.items():
        (d / f).write_text(body)


def test_missing_file_disables_only_that_area(content):
    _area(content, "good", {"overview.md": "a", "tasks.md": TASK, "resources.md": "r"})
    _area(content, "broken", {"overview.md": "a", "tasks.md": TASK})
    assert loader.list_available_areas("en") == ["good"]
    assert "resources.md is missing" in loader.validate_area("broken", "en")["errors"][0]


def test_empty_file_is_error(content):
    _area(content, "e", {"overview.md": "  ", "tasks.md": TASK, "resources.md": "r"})
    assert "empty" in loader.validate_area("e", "en")["errors"][0]


def test_invalid_task_flagged_as_warning(content):
    bad = TASK + "\n## Task: NoId\n- **Level:** junior\n"
    _area(content, "w", {"overview.md": "a", "tasks.md": bad, "resources.md": "r"})
    res = loader.validate_area("w", "en")
    assert not res["errors"] and "1 task(s) skipped" in res["warnings"][0]


def test_unknown_area_is_error(content):
    assert loader.validate_area("nope", "en")["errors"]


def test_chat_returns_friendly_503_for_broken_area(monkeypatch):
    user = UserProfile(id="u", first_name="A", last_name="B", area="nope", experience_level="junior", language="en")
    app.dependency_overrides[get_current_user] = lambda: user
    try:
        r = TestClient(app).post("/chat", json={"message": "hi"})
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 503
    assert "administrator" in r.json()["detail"]
