#!/usr/bin/env python3
"""Fail when retired AI creative identifiers remain in active skill rules."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_ROOTS = (
    ROOT / "skills",
    Path.home() / ".agents" / "skills",
    Path.home() / ".codex" / "skills",
)
NEW_SKILLS = {
    "douyin-video-production-core",
    "douyin-ai-tool-explainer",
    "douyin-ai-news-explainer",
    "douyin-ai-list-video",
}
RETIRED_SKILLS = {"douyin-hyperframes-remake", "douyin-ai-premium-director"}
RETIRED_IDENTIFIERS = (
    "scheme_1",
    "scheme_7",
    "ant_ai",
    "fixed_template_selection",
    "director_selection",
    "style_recipe",
    "foreground_module",
    "BG_DYNAMIC_",
    "BG_FIXED_",
    "Editorial Chalkboard Evidence Lab",
    *(f"M{index:02d}" for index in range(1, 21)),
    *(f"C{index:02d}" for index in range(1, 31)),
    *(f"TR{index:02d}" for index in range(1, 9)),
)
TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".yaml", ".yml", ".py", ".js", ".html", ".css"}


def main() -> int:
    issues: list[str] = []
    scanned = 0
    for root in ACTIVE_ROOTS:
        for retired in RETIRED_SKILLS:
            if (root / retired).exists():
                issues.append(f"retired skill directory still exists: {root / retired}")
        for name in NEW_SKILLS:
            skill = root / name
            if not skill.exists():
                issues.append(f"new skill missing: {skill}")
                continue
            for path in skill.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                    continue
                scanned += 1
                text = path.read_text(encoding="utf-8", errors="ignore")
                for identifier in RETIRED_IDENTIFIERS:
                    if identifier in text:
                        issues.append(f"{identifier} found in {path}")
    result = {
        "status": "passed" if not issues else "blocked",
        "scanned_files": scanned,
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 2


if __name__ == "__main__":
    raise SystemExit(main())
