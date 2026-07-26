#!/usr/bin/env python3
"""Dry-run or execute an SAU upload from a passed publish package."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEDULE_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")
LOCAL_SAU = Path("/Users/wangchao/Desktop/抖音解析/local_tools/social-auto-upload/.venv/bin/sau")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_sau_bin(raw: str) -> str:
    candidates = [raw, os.environ.get("DOUYIN_SAU_BIN", ""), str(LOCAL_SAU)]
    for value in candidates:
        value = value.strip()
        if not value:
            continue
        path = Path(value).expanduser()
        if path.exists():
            return str(path)
        found = shutil.which(value)
        if found:
            return found
    return shutil.which("sau") or "sau"


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--package")
    parser.add_argument("--account", required=True)
    parser.add_argument("--sau-bin", default="")
    parser.add_argument("--schedule", default="")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-immediate", action="store_true")
    parser.add_argument("--allow-title-truncate", action="store_true")
    parser.add_argument("--skip-thumbnails", action="store_true")
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    package_path = Path(args.package).resolve() if args.package else project / "publish_package.json"
    report_path = Path(args.out) if args.out else project / "douyin_sau_upload_report.json"
    issues: list[str] = []
    warnings: list[str] = []
    if not package_path.is_file():
        package: dict[str, Any] = {}
        issues.append(f"publish package missing: {package_path}")
    else:
        package = json.loads(package_path.read_text(encoding="utf-8"))

    gate = Path(__file__).with_name("pre_publish_gate.py")
    if package:
        gate_result = subprocess.run(
            [sys.executable, str(gate), "--package", str(package_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if gate_result.returncode:
            issues.append("pre-publish gate failed")

    title = str(package.get("title") or "").strip()
    caption = str(package.get("caption") or "").strip()
    topics = [str(item).lstrip("#").strip() for item in package.get("topics") or [] if str(item).strip()]
    video = Path(str(package.get("video") or ""))
    cover = Path(str(package.get("cover") or ""))
    if len(title) > 30 and not args.allow_title_truncate:
        issues.append("title exceeds Douyin 30-character upload limit")
    if args.schedule and not SCHEDULE_RE.match(args.schedule):
        issues.append("schedule must use YYYY-MM-DD HH:MM")
    if args.execute and not args.schedule and not args.allow_immediate:
        issues.append("execute requires --schedule or --allow-immediate")

    sau_bin = resolve_sau_bin(args.sau_bin)
    if args.execute and not (Path(sau_bin).exists() or shutil.which(sau_bin)):
        issues.append(f"sau binary not found: {sau_bin}")

    command = [
        sau_bin,
        "douyin",
        "upload-video",
        "--account",
        args.account,
        "--file",
        str(video),
        "--title",
        title[:30] if args.allow_title_truncate else title,
        "--desc",
        caption,
        "--tags",
        ",".join(topics),
    ]
    if args.schedule:
        command += ["--schedule", args.schedule]
    if not args.skip_thumbnails and cover.is_file():
        suffix = "--thumbnail-portrait" if package.get("cover_orientation") == "portrait" else "--thumbnail-landscape"
        command += [suffix, str(cover)]
    elif args.skip_thumbnails:
        warnings.append("thumbnail upload skipped; the checked video/cover package remains the source of truth")
    command.append("--headed" if args.headed else "--headless")
    if args.debug:
        command.append("--debug")

    report: dict[str, Any] = {
        "status": "blocked" if issues else ("planned" if not args.execute else "executing"),
        "mode": "execute" if args.execute else "dry_run",
        "checked_at": now_iso(),
        "package": str(package_path),
        "issues": issues,
        "warnings": warnings,
        "command": command,
    }
    if not issues and args.execute:
        account_check = subprocess.run(
            [sau_bin, "douyin", "check", "--account", args.account],
            capture_output=True,
            text=True,
            check=False,
        )
        report["account_check_returncode"] = account_check.returncode
        if account_check.returncode:
            report["status"] = "blocked"
            report["issues"].append("SAU account check failed")
        else:
            upload = subprocess.run(command, capture_output=True, text=True, check=False)
            report["upload_returncode"] = upload.returncode
            report["stdout"] = upload.stdout[-4000:]
            report["stderr"] = upload.stderr[-4000:]
            report["status"] = "submitted_to_sau" if upload.returncode == 0 else "failed"
            if upload.returncode:
                report["issues"].append("SAU upload command failed")
    write_json(report_path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] in {"planned", "submitted_to_sau"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
