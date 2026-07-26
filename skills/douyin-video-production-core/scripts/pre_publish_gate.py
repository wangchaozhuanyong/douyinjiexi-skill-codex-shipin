#!/usr/bin/env python3
"""Validate a publish_package.json immediately before promotion or upload."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from artifact_fingerprint import verify_report_inputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", required=True)
    args = parser.parse_args()

    package_path = Path(args.package).resolve()
    issues: list[str] = []
    if not package_path.is_file():
        issues.append(f"package missing: {package_path}")
        package = {}
    else:
        package = json.loads(package_path.read_text(encoding="utf-8"))
    if package.get("gate", {}).get("status") != "passed":
        issues.append("publish package gate is not passed")
    for field in ("video", "cover", "qa_report", "script"):
        path = Path(str(package.get(field) or ""))
        if not path.is_file() or path.stat().st_size == 0:
            issues.append(f"{field} missing or empty: {path}")
    if package.get("text_check", {}).get("status") != "passed":
        issues.append("local text check is not passed")
    if package.get("platform_check", {}).get("status") != "passed":
        issues.append("visible platform text check is not passed")
    expected = [
        Path(str(package.get("video") or "")),
        Path(str(package.get("cover") or "")),
        Path(str(package.get("qa_report") or "")),
        Path(str(package.get("script") or "")),
        Path(str(package.get("text_check", {}).get("path") or "")),
        Path(str(package.get("platform_check", {}).get("path") or "")),
    ]
    issues.extend(verify_report_inputs(package, [path for path in expected if path.is_file()]))
    text_check_path = Path(str(package.get("text_check", {}).get("path") or ""))
    if text_check_path.is_file():
        text_check = json.loads(text_check_path.read_text(encoding="utf-8"))
        text_inputs = [
            Path(str(path))
            for path in text_check.get("checked_files") or []
            if isinstance(path, str) and path != "stdin"
        ]
        issues.extend(
            f"local text check is stale: {issue}"
            for issue in verify_report_inputs(text_check, text_inputs)
        )
    result = {"status": "passed" if not issues else "blocked", "issues": issues}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 2


if __name__ == "__main__":
    raise SystemExit(main())
