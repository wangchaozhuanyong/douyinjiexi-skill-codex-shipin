#!/usr/bin/env python3
"""Promote a QA-passed draft package into the public final folder."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def first_existing(*paths: Path) -> Path:
    for path in paths:
        if exists(path):
            return path
    return paths[0]


def require_passed(report: dict[str, Any]) -> None:
    if report.get("status") != "passed":
        raise SystemExit("qa_report.status must be passed before promotion")
    if report.get("blocking_issues"):
        raise SystemExit("qa_report.blocking_issues must be empty before promotion")
    hard_gates = report.get("hard_gates", {})
    if not hard_gates or not all(bool(value) for value in hard_gates.values()):
        raise SystemExit("all qa_report.hard_gates must be true before promotion")


def require_provider_usage_audit(report: dict[str, Any]) -> None:
    if report.get("status") != "passed":
        raise SystemExit("provider_usage_audit.status must be passed before promotion")
    if report.get("issues"):
        raise SystemExit("provider_usage_audit.issues must be empty before promotion")


def normalize_text(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.strip().splitlines()).strip()


def checked_fields(report: dict[str, Any]) -> set[str]:
    raw = (
        report.get("checked_fields")
        or report.get("checked_text_fields")
        or report.get("checked", {}).get("fields")
        or []
    )
    if not isinstance(raw, list):
        return set()
    return {str(item).strip().lower() for item in raw if str(item).strip()}


def require_publish_keyword_check(report: dict[str, Any], publish_copy: str) -> None:
    if report.get("status") != "passed":
        raise SystemExit("qingdou_keyword_check.status must be passed before promotion")

    final_check = report.get("final_check")
    if not isinstance(final_check, dict):
        raise SystemExit("qingdou_keyword_check.final_check is required before promotion")

    message = str(final_check.get("message") or "")
    final_status = str(final_check.get("status") or "")
    if final_status != "passed" and "未检查到敏感词" not in message:
        raise SystemExit("qingdou_keyword_check.final_check must prove no sensitive keywords")
    if final_check.get("items"):
        raise SystemExit("qingdou_keyword_check.final_check.items must be empty")

    missing_fields = {"title", "caption", "topics"} - checked_fields(report)
    if missing_fields:
        raise SystemExit(
            "qingdou_keyword_check must include title, caption, and topics; missing: "
            + ", ".join(sorted(missing_fields))
        )

    title = str(report.get("final_title") or report.get("title") or "").strip()
    caption = str(report.get("final_caption") or report.get("caption") or "").strip()
    topics = report.get("final_topics") or report.get("topics") or []
    if not title:
        raise SystemExit("qingdou_keyword_check.final_title is required")
    if not caption:
        raise SystemExit("qingdou_keyword_check.final_caption is required")
    if not isinstance(topics, list) or not any(str(item).strip() for item in topics):
        raise SystemExit("qingdou_keyword_check.final_topics must list the checked topics")
    if publish_copy and normalize_text(caption) != normalize_text(publish_copy):
        raise SystemExit("qingdou_keyword_check.final_caption must match publish_copy.txt")


def promote(project: Path, qa_report: Path, provider_audit: Path, keyword_check: Path) -> dict[str, str]:
    internal = project / "internal"
    final = project / "final"
    report = load_json(qa_report)
    require_passed(report)
    if not exists(provider_audit):
        raise SystemExit(f"provider usage audit missing or empty: {provider_audit}")
    require_provider_usage_audit(load_json(provider_audit))

    sources = {
        "final.mp4": first_existing(internal / "draft.mp4", project / "draft.mp4"),
        "metadata.json": internal / "metadata.json",
        "cover.png": first_existing(internal / "cover.png", project / "cover.png"),
        "publish_copy.txt": first_existing(internal / "publish_copy.txt", project / "publish_copy.txt"),
    }
    missing = [f"{name} source missing or empty: {path}" for name, path in sources.items() if not exists(path)]
    if missing:
        raise SystemExit("\n".join(missing))
    if not exists(keyword_check):
        raise SystemExit(f"qingdou keyword check missing or empty: {keyword_check}")
    require_publish_keyword_check(load_json(keyword_check), sources["publish_copy.txt"].read_text(encoding="utf-8"))

    final.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, str] = {}
    for name, source in sources.items():
        target = final / name
        shutil.copy2(source, target)
        outputs[name] = str(target)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote QA-passed draft artifacts to final/.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic>")
    parser.add_argument("--qa-report", help="Defaults to <project>/internal/qa_report.json")
    parser.add_argument("--provider-audit", help="Defaults to <project>/internal/provider_usage_audit.json")
    parser.add_argument("--keyword-check", help="Defaults to <project>/internal/qingdou_keyword_check.json")
    parser.add_argument("--out", help="Optional promotion_report.json path")
    args = parser.parse_args()

    project = Path(args.project)
    qa_report = Path(args.qa_report) if args.qa_report else project / "internal" / "qa_report.json"
    provider_audit = Path(args.provider_audit) if args.provider_audit else project / "internal" / "provider_usage_audit.json"
    keyword_check = Path(args.keyword_check) if args.keyword_check else project / "internal" / "qingdou_keyword_check.json"
    if not exists(qa_report):
        raise SystemExit(f"qa report missing or empty: {qa_report}")
    outputs = promote(project, qa_report, provider_audit, keyword_check)
    result = {"status": "promoted", "outputs": outputs}
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
