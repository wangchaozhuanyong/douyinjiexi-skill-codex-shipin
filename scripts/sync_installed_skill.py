#!/usr/bin/env python3
"""Sync this source tree into installed Codex skill locations.

The sync is intentionally allowlisted: generated videos, app builds, logs,
downloaded media, local env files, and desktop-tool runtime state are never
copied into installed skill folders.
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESTINATIONS = [
    Path.home() / ".agents" / "skills" / "douyin-hyperframes-remake",
    Path.home() / ".codex" / "skills" / "douyin-hyperframes-remake",
]

MANAGED_FILES = [
    "SKILL.md",
    "README.md",
    "requirements.txt",
]

MANAGED_DIRS = [
    "agents",
    "assets",
    "references",
    "schemas",
    "templates",
    "scripts",
    "tests",
    "examples",
]

STALE_ROOT_FILES = [
    "build_storyboard.py",
    "metadata.json",
    "metadata.schema.json",
    "premium_ai_video_source_to_hyperframes_rule.md",
    "storyboard.example.json",
    "storyboard.json",
    "storyboard.schema.json",
    "timeline_contract.md",
    "validate_storyboard.py",
    "video_technical_qa.py",
    "visual_aesthetic_review.py",
]

STALE_DIRS = [
    ".pytest_cache",
    "__pycache__",
    "build",
    "dist",
    "docs",
    "hyperframes-remakes",
    "mp3",
    "output-test",
    "outputs",
    "导出",
]

IGNORED_NAMES = {
    ".DS_Store",
    "__pycache__",
    ".pytest_cache",
    ".git",
    ".env",
}


def ignore_names(_directory: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        if name in IGNORED_NAMES or name.endswith((".pyc", ".pyo", ".log")):
            ignored.add(name)
    return ignored


def copy_file(source: Path, target: Path, dry_run: bool) -> bool:
    if not source.exists():
        return False
    changed = not target.exists() or not filecmp.cmp(source, target, shallow=False)
    if dry_run:
        return changed
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return changed


def copy_dir(source: Path, target: Path, dry_run: bool) -> bool:
    if not source.exists():
        return False
    changed = True
    if dry_run:
        return changed
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target, ignore=ignore_names)
    return changed


def remove_path(path: Path, dry_run: bool) -> bool:
    if not path.exists():
        return False
    if dry_run:
        return True
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    return True


def sync_destination(destination: Path, prune: bool, dry_run: bool) -> dict[str, list[str]]:
    summary: dict[str, list[str]] = {"copied": [], "pruned": []}
    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)

    for relative in MANAGED_FILES:
        if copy_file(ROOT / relative, destination / relative, dry_run):
            summary["copied"].append(relative)

    for relative in MANAGED_DIRS:
        if copy_dir(ROOT / relative, destination / relative, dry_run):
            summary["copied"].append(relative + "/")

    if prune:
        for relative in STALE_ROOT_FILES:
            if remove_path(destination / relative, dry_run):
                summary["pruned"].append(relative)
        for relative in STALE_DIRS:
            if remove_path(destination / relative, dry_run):
                summary["pruned"].append(relative + "/")

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync the skill source into installed Codex skill folders.")
    parser.add_argument(
        "--dest",
        action="append",
        type=Path,
        help="Destination skill folder. Can be repeated. Defaults to ~/.agents and ~/.codex skill locations.",
    )
    parser.add_argument("--prune", action="store_true", help="Remove known stale generated/runtime files from destination folders.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing files.")
    args = parser.parse_args()

    destinations = args.dest or DEFAULT_DESTINATIONS
    for destination in destinations:
        summary = sync_destination(destination.expanduser(), prune=args.prune, dry_run=args.dry_run)
        print(f"{destination.expanduser()}:")
        copied = summary["copied"] or ["(none)"]
        pruned = summary["pruned"] or ["(none)"]
        print("  copied: " + ", ".join(copied))
        print("  pruned: " + ", ".join(pruned))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
