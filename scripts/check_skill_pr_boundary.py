#!/usr/bin/env python3
"""Keep local desktop parser files out of skill PRs."""

from __future__ import annotations

import fnmatch
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LOCAL_ONLY_PATTERNS = (
    ".env.example",
    "requirements.txt",
    "build_desktop_app.sh",
    "run_douyin_media_server.sh",
    "start_douyin_media_server.sh",
    "douyin_media_*.py",
    "douyin_to_mp3.py",
    "douyin_media_studio.spec",
    "tts_providers.py",
    "scripts/generate_ai_daily_*.py",
    "zh-Hans.lproj/**",
    "delivery/**",
    "reference_downloads/**",
    "assets/source_cosmic_backgrounds/**",
    "build/**",
    "dist/**",
    "mp3/**",
    "outputs/**",
    "output-test/**",
    "导出/**",
)
PUBLIC_CONFIG_PATTERNS = (
    "SKILL.md",
    "references/*.md",
    "references/*.json",
    "templates/*.md",
    "templates/*.json",
    "assets/ai_background_templates_dynamic/*.json",
)
PUBLIC_FORBIDDEN_REFERENCES = (
    "reference_downloads/",
    "assets/source_cosmic_backgrounds/",
)


def is_local_only_path(path: str) -> bool:
    normalized = path.strip("/")
    return any(fnmatch.fnmatchcase(normalized, pattern) for pattern in LOCAL_ONLY_PATTERNS)


def run_git(args: list[str]) -> bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True)
    return result.stdout


def decode_paths(data: bytes) -> list[str]:
    text = data.decode("utf-8", errors="surrogateescape")
    return [item for item in text.split("\0") if item]


def tracked_local_only_paths() -> list[str]:
    data = run_git(["ls-files", "-z", "--", *LOCAL_ONLY_PATTERNS])
    return sorted(path for path in decode_paths(data) if is_local_only_path(path))


def visible_untracked_local_only_paths() -> list[str]:
    data = run_git(["status", "--porcelain=v1", "-z", "--untracked-files=all"])
    records = decode_paths(data)
    paths: list[str] = []
    index = 0
    while index < len(records):
        record = records[index]
        status = record[:2]
        path = record[3:] if len(record) > 3 else ""
        if status == "??" and is_local_only_path(path):
            paths.append(path)
        if "R" in status or "C" in status:
            index += 2
        else:
            index += 1
    return sorted(paths)


def public_files_with_local_references() -> list[str]:
    issues: list[str] = []
    paths: set[Path] = set()
    for pattern in PUBLIC_CONFIG_PATTERNS:
        paths.update(path for path in ROOT.glob(pattern) if path.is_file())
    for path in sorted(paths):
        text = path.read_text(encoding="utf-8")
        for forbidden in PUBLIC_FORBIDDEN_REFERENCES:
            if forbidden in text:
                issues.append(f"{path.relative_to(ROOT)} references local-only path {forbidden}")
    return issues


def main() -> int:
    if any(arg in {"-h", "--help"} for arg in sys.argv[1:]):
        print("usage: check_skill_pr_boundary.py")
        print()
        print("Fail if local desktop parser, downloader, reference, or output files are tracked or visible to git.")
        return 0

    try:
        tracked = tracked_local_only_paths()
        untracked = visible_untracked_local_only_paths()
        public_refs = public_files_with_local_references()
    except subprocess.CalledProcessError as exc:
        print(f"Skill PR boundary check skipped: git command failed ({exc.returncode}).")
        return 0

    issues: list[str] = []
    if tracked:
        issues.append("tracked local-only paths:")
        issues.extend(f"- {path}" for path in tracked)
    if untracked:
        issues.append("visible untracked local-only paths; add them to .gitignore or move them out of the repo:")
        issues.extend(f"- {path}" for path in untracked)
    if public_refs:
        issues.append("public skill files reference local-only paths:")
        issues.extend(f"- {item}" for item in public_refs)

    if issues:
        print("Skill PR boundary check failed.")
        for issue in issues:
            print(issue)
        return 1

    print("Skill PR boundary check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
