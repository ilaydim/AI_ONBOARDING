"""
tasks.md dosyasını parse eder — SRS §6.3
"""
import re
import os
from app.models.task import Task
from app.core.settings import get_config


def parse_tasks(area: str, language: str = "tr") -> list[Task]:
    cfg = get_config()
    base_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "../../",
                     cfg["content"]["base_path"], language, "areas", area, "tasks.md")
    )
    if not os.path.exists(base_path):
        return []

    with open(base_path, encoding="utf-8") as f:
        content = f.read()

    tasks = []
    # Her ## Görev: bloğunu yakala
    blocks = re.split(r'\n(?=## Görev:|## Task:)', content)
    for block in blocks:
        if not block.strip().startswith(("## Görev:", "## Task:")):
            continue
        task = _parse_block(block)
        if task:
            tasks.append(task)
    return tasks


def _parse_block(block: str) -> Task | None:
    def get(pattern: str, default="") -> str:
        m = re.search(pattern, block, re.IGNORECASE | re.MULTILINE)
        return m.group(1).strip() if m else default

    title_m = re.match(r'## (?:Görev|Task):\s*(.+)', block)
    if not title_m:
        return None

    title = title_m.group(1).strip()
    task_id = get(r'\*\*ID:\*\*\s*(.+)')
    levels_str = get(r'\*\*(?:Seviye|Level):\*\*\s*(.+)')
    levels = [l.strip() for l in levels_str.split(",")]
    dependency = get(r'\*\*(?:Bağımlılık|Dependency):\*\*\s*(.+)') or None
    if dependency and dependency.lower() in ("yok", "none", "-"):
        dependency = None
    expected_output = get(r'\*\*(?:Beklenen Çıktı|Expected Output):\*\*\s*(.+)')
    criteria = get(r'\*\*(?:Tamamlanma Kriteri|Completion Criteria):\*\*\s*(.+)')
    duration_str = get(r'\*\*(?:Tahmini Süre|Estimated Duration):\*\*\s*(.+)')
    duration_m = re.search(r'([\d.]+)', duration_str)
    estimated_hours = float(duration_m.group(1)) if duration_m else 1.0
    skippable_str = get(r'\*\*(?:Atlanabilir|Skippable):\*\*\s*(.+)').lower()
    skippable = skippable_str not in ("hayır", "no", "false")

    if not task_id or not title:
        return None

    return Task(
        id=task_id,
        title=title,
        levels=levels,
        dependency=dependency,
        expected_output=expected_output,
        completion_criteria=criteria,
        estimated_hours=estimated_hours,
        skippable=skippable,
    )
