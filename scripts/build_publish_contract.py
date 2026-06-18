#!/usr/bin/env python3
"""Build the single publish contract consumed by final publish gates."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def load_json(path: Path) -> dict[str, Any]:
    if not exists(path):
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def first_existing(*paths: Path) -> Path:
    for path in paths:
        if exists(path):
            return path
    return paths[0]


def status_of(path: Path) -> str:
    report = load_json(path)
    return str(report.get("status") or "missing")


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    return path.read_text(encoding="utf-8").strip()


def normalize_topic(topic: Any) -> str:
    text = str(topic or "").strip()
    if text and not text.startswith("#"):
        return "#" + text
    return text


def publish_from_reports(internal: Path, metadata: dict[str, Any], publish_copy_path: Path) -> dict[str, Any]:
    qingdou = load_json(internal / "qingdou_keyword_check.json")
    title = str(qingdou.get("final_title") or qingdou.get("title") or metadata.get("title") or "").strip()
    caption = str(qingdou.get("final_caption") or qingdou.get("caption") or read_text(publish_copy_path)).strip()
    topics_raw = qingdou.get("final_topics") or qingdou.get("topics") or []
    topics = [normalize_topic(item) for item in topics_raw if str(item or "").strip()]
    if not title and caption:
        title = caption.splitlines()[0].strip()[:30]
    return {
        "title": title,
        "caption": caption,
        "topics": topics,
        "first_topic": topics[0] if topics else "",
    }


def build_contract(project: Path) -> dict[str, Any]:
    internal = project / "internal"
    final = project / "final"
    metadata_path = internal / "metadata.json"
    publish_copy_path = first_existing(internal / "publish_copy.txt", project / "publish_copy.txt")
    metadata = load_json(metadata_path)
    text_compliance_path = first_existing(
        internal / "on_screen_and_publish_text_compliance_report.json",
        internal / "compliance_report.json",
    )
    cover_report_path = internal / "publish_cover_report.json"
    cover_report = load_json(cover_report_path)
    cover_outputs = cover_report.get("outputs") if isinstance(cover_report.get("outputs"), dict) else {}
    raw_cover_text = str(cover_outputs.get("cover_text") or "").strip()
    cover_text_path = first_existing(Path(raw_cover_text), internal / "publish_cover_text.txt") if raw_cover_text else internal / "publish_cover_text.txt"
    video_source = first_existing(internal / "draft.mp4", project / "draft.mp4")
    cover_source = first_existing(
        internal / "cover.png",
        project / "cover.png",
        project / "delivery" / "cover.png",
    )
    contract = {
        "version": 1,
        "project": str(project),
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "artifacts": {
            "video": {
                "source": str(video_source),
                "final": str(final / "final.mp4"),
            },
            "cover": {
                "source": str(cover_source),
                "vertical": str(internal / "cover_publish_vertical.png"),
                "horizontal": str(internal / "cover_publish_horizontal.png"),
                "text_source": str(cover_text_path),
                "report": str(cover_report_path),
            },
            "metadata": {
                "source": str(metadata_path),
                "final": str(final / "metadata.json"),
            },
            "publish_copy": {
                "source": str(publish_copy_path),
                "final": str(final / "publish_copy.txt"),
            },
        },
        "publish": publish_from_reports(internal, metadata, publish_copy_path),
        "checks": {
            "qa_report": {
                "path": str(internal / "qa_report.json"),
                "status": status_of(internal / "qa_report.json"),
            },
            "provider_usage_audit": {
                "path": str(internal / "provider_usage_audit.json"),
                "status": status_of(internal / "provider_usage_audit.json"),
            },
            "qingdou_keyword_check": {
                "path": str(internal / "qingdou_keyword_check.json"),
                "status": status_of(internal / "qingdou_keyword_check.json"),
            },
            "text_compliance": {
                "path": str(text_compliance_path),
                "status": status_of(text_compliance_path),
            },
            "cover": {
                "path": str(cover_report_path),
                "status": status_of(cover_report_path),
            },
        },
        "gate": {
            "status": "not_evaluated",
            "issues": [],
        },
    }
    return contract


def main() -> int:
    parser = argparse.ArgumentParser(description="Build internal/publish_contract.json.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic> project path")
    parser.add_argument("--out", help="Defaults to <project>/internal/publish_contract.json")
    args = parser.parse_args()

    project = Path(args.project)
    out = Path(args.out) if args.out else project / "internal" / "publish_contract.json"
    contract = build_contract(project)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "built", "out": str(out)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
