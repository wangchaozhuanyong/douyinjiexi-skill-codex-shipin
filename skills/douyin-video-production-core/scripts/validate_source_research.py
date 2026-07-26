#!/usr/bin/env python3
"""Validate source_research.json and selected current/hot topic references."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED_SOURCE_FIELDS = [
    "source_id",
    "title",
    "url_or_local_capture",
    "published_or_captured_date",
    "source_type",
    "claim_supported",
    "asset_potential",
]
SOURCE_TYPES = {"official_doc", "release_note", "credible_news", "local_capture", "user_reference"}
ASSET_POTENTIAL = {"screenshot", "quote_card", "timeline", "comparison", "demo"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def selected_topic_source_ids(topic: dict[str, Any]) -> set[str]:
    raw = topic.get("source_ids") or topic.get("sources") or topic.get("source_refs") or []
    ids: set[str] = set()
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                value = item.get("source_id") or item.get("id")
            else:
                value = item
            if str(value or "").strip():
                ids.add(str(value).strip())
    return ids


def is_current_or_hot(topic: dict[str, Any]) -> bool:
    blob = json.dumps(topic, ensure_ascii=False).lower()
    markers = ["current", "hot", "热点", "热榜", "today", "same-day", "当天", "最新", "新闻"]
    return any(marker in blob for marker in markers)


def validate(research: dict[str, Any], selected_topic: dict[str, Any] | None = None) -> dict[str, Any]:
    issues: list[str] = []
    sources = research.get("sources") if isinstance(research.get("sources"), list) else []
    seen_ids: set[str] = set()
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            issues.append(f"sources[{index}] must be an object")
            continue
        for field in REQUIRED_SOURCE_FIELDS:
            if not str(source.get(field) or "").strip():
                issues.append(f"sources[{index}].{field} is required")
        source_id = str(source.get("source_id") or "").strip()
        if source_id in seen_ids:
            issues.append(f"duplicate source_id: {source_id}")
        seen_ids.add(source_id)
        if source.get("source_type") not in SOURCE_TYPES:
            issues.append(f"sources[{index}].source_type is invalid")
        if source.get("asset_potential") not in ASSET_POTENTIAL:
            issues.append(f"sources[{index}].asset_potential is invalid")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(source.get("published_or_captured_date") or "")):
            issues.append(f"sources[{index}].published_or_captured_date must be YYYY-MM-DD")

    if selected_topic is not None and is_current_or_hot(selected_topic):
        refs = selected_topic_source_ids(selected_topic)
        if not sources:
            issues.append("current/hot selected_topic requires source_research.sources")
        if not refs:
            issues.append("current/hot selected_topic must reference source ids")
        missing = sorted(ref for ref in refs if ref not in seen_ids)
        if missing:
            issues.append("selected_topic references missing source ids: " + ", ".join(missing))

    return {
        "status": "passed" if not issues else "failed",
        "source_count": len(sources),
        "blocking_issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate source_research.json.")
    parser.add_argument("--source-research", required=True)
    parser.add_argument("--selected-topic")
    parser.add_argument("--out")
    args = parser.parse_args()

    research = load_json(Path(args.source_research))
    selected = load_json(Path(args.selected_topic)) if args.selected_topic else None
    report = validate(research, selected)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
