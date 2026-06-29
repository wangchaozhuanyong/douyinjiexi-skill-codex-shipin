#!/usr/bin/env python3
"""Validate a concrete visual style profile."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = [
    "style_id",
    "layout_system",
    "color_system",
    "typography_system",
    "caption_system",
    "proof_panel_rules",
    "annotation_rail_rules",
    "background_rules",
    "motion_language",
    "sfx_language",
    "cover_rules",
    "negative_visual_rules",
    "douyin_delivery_strategy",
]

FORBIDDEN_VAGUE_TERMS = ["高级科技感", "炫酷", "4K", "premium tech", "科技感拉满"]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(profile: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    for field in REQUIRED_FIELDS:
        value = profile.get(field)
        if isinstance(value, list):
            if not value:
                issues.append(f"{field} must be non-empty")
        elif not str(value or "").strip():
            issues.append(f"{field} is required")
    if profile.get("style_id") == "premium_editorial_proof_board_v1":
        canvas = profile.get("canvas") if isinstance(profile.get("canvas"), dict) else {}
        if int(canvas.get("master_width") or 0) != 1920 or int(canvas.get("master_height") or 0) != 1080:
            issues.append("premium_editorial_proof_board_v1 canvas must be 1920x1080")
    blob = json.dumps(profile, ensure_ascii=False).lower()
    for term in FORBIDDEN_VAGUE_TERMS:
        if term.lower() in blob:
            issues.append(f"vague visual wording is not allowed: {term}")
    negative = profile.get("negative_visual_rules")
    if not isinstance(negative, list) or len(negative) < 5:
        issues.append("negative_visual_rules must list concrete banned visual patterns")
    return {
        "status": "passed" if not issues else "failed",
        "style_id": profile.get("style_id"),
        "blocking_issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate visual_style_profile JSON.")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()

    report = validate(load_json(Path(args.profile)))
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
