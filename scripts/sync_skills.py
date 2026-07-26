#!/usr/bin/env python3
"""Install the four-skill bundle and remove retired AI video skills."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills"
NEW_SKILLS = (
    "douyin-video-production-core",
    "douyin-ai-tool-explainer",
    "douyin-ai-news-explainer",
    "douyin-ai-list-video",
)
RETIRED_SKILLS = (
    "douyin-hyperframes-remake",
    "douyin-ai-premium-director",
)
DESTINATIONS = (
    Path.home() / ".agents" / "skills",
    Path.home() / ".codex" / "skills",
)


def sync(destination: Path) -> dict[str, list[str]]:
    destination.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    removed: list[str] = []
    for name in RETIRED_SKILLS:
        target = destination / name
        if target.exists():
            shutil.rmtree(target)
            removed.append(str(target))
    for name in NEW_SKILLS:
        source = SOURCE / name
        target = destination / name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
        installed.append(str(target))
    return {"installed": installed, "removed": removed}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        result = {
            "status": "planned",
            "install": [str(root / name) for root in DESTINATIONS for name in NEW_SKILLS],
            "remove": [str(root / name) for root in DESTINATIONS for name in RETIRED_SKILLS],
        }
    else:
        runs = [sync(root) for root in DESTINATIONS]
        result = {"status": "synced", "runs": runs}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
