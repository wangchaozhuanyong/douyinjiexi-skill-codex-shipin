#!/usr/bin/env python3
"""Build the single publish package after QA and text checks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from artifact_fingerprint import verify_report_inputs, write_report_with_fingerprints
from validate_project import artifact_path, load_json


def existing(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def normalized_topic(value: Any) -> str:
    return str(value or "").strip().lstrip("#").strip()


def checked_input_paths(report: dict[str, Any], project: Path) -> list[Path]:
    paths: list[Path] = []
    for raw in report.get("checked_files") or []:
        if not isinstance(raw, str) or raw == "stdin":
            continue
        path = Path(raw)
        if path.is_absolute():
            paths.append(path)
            continue
        cwd_candidate = path.resolve()
        project_candidate = (project / path).resolve()
        if cwd_candidate.is_file():
            paths.append(cwd_candidate)
        elif project_candidate.is_file():
            paths.append(project_candidate)
        else:
            paths.append(cwd_candidate)
    return paths


def platform_visible_message(report: dict[str, Any]) -> str:
    direct = str(report.get("visible_result") or "").strip()
    if direct:
        return direct
    final_check = report.get("final_check")
    if isinstance(final_check, dict):
        return str(final_check.get("message") or "").strip()
    return ""


def platform_result_passed(report: dict[str, Any]) -> bool:
    status = str(report.get("status") or "")
    if status not in {"passed", "user_override_accepted"}:
        return False
    final_check = report.get("final_check")
    if isinstance(final_check, dict) and final_check.get("status") != "passed":
        return False
    return bool(platform_visible_message(report))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--video")
    parser.add_argument("--cover")
    parser.add_argument("--platform-check")
    parser.add_argument("--out")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    script = load_json(artifact_path(project, "script.json"), [])
    script_path = artifact_path(project, "script.json")
    qa_path = artifact_path(project, "qa_report.json")
    qa = load_json(qa_path, [])
    publish = script.get("publish") if isinstance(script.get("publish"), dict) else {}
    video = Path(args.video).resolve() if args.video else project / "render" / "final.mp4"
    cover = Path(args.cover).resolve() if args.cover else project / "render" / "cover.png"
    text_check_path = project / "public_text_check.json"
    text_check = load_json(text_check_path, []) if text_check_path.exists() else {}
    platform_path = Path(args.platform_check).resolve() if args.platform_check else project / "platform_text_check.json"
    platform_check = load_json(platform_path, []) if platform_path.exists() else {}

    issues: list[str] = []
    if qa.get("status") != "passed":
        issues.append("qa_report.status must be passed")
    if not existing(video):
        issues.append(f"video missing or empty: {video}")
    if not existing(cover):
        issues.append(f"cover missing or empty: {cover}")
    for field in ("title", "caption", "topics"):
        value = publish.get(field)
        if not value or (field == "topics" and not isinstance(value, list)):
            issues.append(f"script.publish.{field} is required")
    if text_check.get("status") != "passed":
        issues.append("public_text_check.status must be passed")
    checked_paths = checked_input_paths(text_check, project)
    if not checked_paths:
        issues.append("public_text_check.checked_files must contain final public text files")
    else:
        issues.extend(
            f"public_text_check is stale: {issue}"
            for issue in verify_report_inputs(text_check, checked_paths)
        )
        checked_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in checked_paths
            if path.is_file()
        )
        title = str(publish.get("title") or "").strip()
        caption = str(publish.get("caption") or "").strip()
        if title and title not in checked_text:
            issues.append("script.publish.title was not included in public_text_check")
        if caption and caption not in checked_text:
            issues.append("script.publish.caption was not included in public_text_check")
        for topic in publish.get("topics") or []:
            normalized = normalized_topic(topic)
            if normalized and normalized not in checked_text and f"#{normalized}" not in checked_text:
                issues.append(
                    f"script.publish topic was not included in public_text_check: {normalized}"
                )

    if not platform_result_passed(platform_check):
        issues.append(
            "platform_text_check must contain a passed real visible result before publishing"
        )
    checked_fields = platform_check.get("checked_fields") or platform_check.get("fields_checked") or []
    if not {"title", "caption", "topics"}.issubset(set(checked_fields)):
        issues.append("platform_text_check must cover title, caption and topics")
    if not str(platform_check.get("checked_at") or "").strip():
        issues.append("platform_text_check.checked_at is required")
    if str(platform_check.get("final_title") or "").strip() != str(
        publish.get("title") or ""
    ).strip():
        issues.append("platform_text_check.final_title does not match script.publish.title")
    if str(platform_check.get("final_caption") or "").strip() != str(
        publish.get("caption") or ""
    ).strip():
        issues.append("platform_text_check.final_caption does not match script.publish.caption")
    platform_topics = [
        normalized_topic(item) for item in platform_check.get("final_topics") or []
    ]
    publish_topics = [normalized_topic(item) for item in publish.get("topics") or []]
    if platform_topics != publish_topics:
        issues.append("platform_text_check.final_topics do not match script.publish.topics")

    package: dict[str, Any] = {
        "version": 1,
        "project": str(project),
        "script": str(script_path),
        "video": str(video),
        "cover": str(cover),
        "title": str(publish.get("title") or ""),
        "caption": str(publish.get("caption") or ""),
        "topics": publish.get("topics") if isinstance(publish.get("topics"), list) else [],
        "qa_report": str(qa_path),
        "text_check": {"path": str(text_check_path), "status": text_check.get("status") or "not_run"},
        "platform_check": {
            "path": str(platform_path),
            "status": "passed" if platform_result_passed(platform_check) else "not_passed",
            "source_status": platform_check.get("status") or "not_run",
            "checked_at": platform_check.get("checked_at") or "",
        },
        "gate": {"status": "passed" if not issues else "blocked", "issues": issues},
    }
    inputs = [video, cover, qa_path, script_path, text_check_path, platform_path]
    write_report_with_fingerprints(package, [path for path in inputs if existing(path)])
    out = Path(args.out) if args.out else artifact_path(project, "publish_package.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(package, ensure_ascii=False, indent=2))
    return 0 if package["gate"]["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
