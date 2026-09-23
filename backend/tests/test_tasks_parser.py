"""CM-3.x: tasks.md şeması."""
from app.content.task_parser import _parse_block

BLOCK = """## Task: Setup
- **ID:** backend-002
- **Level:** junior, mid
- **Dependency:** backend-001
- **Expected Output:** runs locally
- **Completion Criteria:** screenshot
- **Estimated Duration:** 2 hours
- **Skippable:** Yes
"""


def test_parse_valid_block():
    t = _parse_block(BLOCK)
    assert t.id == "backend-002"
    assert t.levels == ["junior", "mid"]
    assert t.dependency == "backend-001"
    assert t.estimated_hours == 2.0
    assert t.skippable is True


def test_dependency_none_and_not_skippable():
    t = _parse_block(BLOCK.replace("backend-001", "None").replace("Yes", "No"))
    assert t.dependency is None
    assert t.skippable is False


def test_missing_id_rejected():
    assert _parse_block(BLOCK.replace("- **ID:** backend-002\n", "")) is None


def _task(title, expected="", skippable=True):
    from app.models.task import Task
    return Task(id="backend-009", title=title, levels=["junior"], expected_output=expected,
                completion_criteria="c", estimated_hours=1, skippable=skippable)


def test_verified_note_matches_title_keyword():
    from app.content.task_parser import is_covered_by_verified_note
    assert is_covered_by_verified_note(_task("Containerize the Service with Docker"), {"docker"})
    assert is_covered_by_verified_note(_task("Servisi Docker ile Konteynerleştir"), {"docker"})


def test_verified_note_matches_expected_output():
    from app.content.task_parser import is_covered_by_verified_note
    assert is_covered_by_verified_note(_task("Setup", expected="Docker image is built"), {"docker"})


def test_verified_note_ignores_unrelated_and_partial_words():
    from app.content.task_parser import is_covered_by_verified_note
    assert not is_covered_by_verified_note(_task("Learn Kubernetes"), {"docker"})
    assert not is_covered_by_verified_note(_task("Write a Dockerfile"), {"docker"})


def test_non_skippable_task_never_removed_by_note():
    from app.content.task_parser import is_covered_by_verified_note
    assert not is_covered_by_verified_note(_task("Docker basics", skippable=False), {"docker"})


def test_verified_keys_only_verified_notes():
    from app.content.task_parser import verified_keys
    notes = [{"key": " Docker ", "verified": True}, {"key": "Python", "verified": False}]
    assert verified_keys(notes) == {"docker"}


def test_describe_error_includes_status_code_but_not_message():
    from app.core.logger import describe_error

    class Boom(Exception):
        status_code = 404

    assert describe_error(Boom("secret content")) == "Boom:404"
    assert describe_error(ValueError("secret")) == "ValueError"
