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
