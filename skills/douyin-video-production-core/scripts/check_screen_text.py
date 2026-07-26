#!/usr/bin/env python3
"""Proofread final on-screen text against storyboard-approved text."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PRIMARY_TEXT_ROLES = {
    "primary_title",
    "title",
    "headline",
    "cover_title",
    "cta",
    "large_caption",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(text: Any) -> str:
    return str(text or "").strip()


def approved_texts(storyboard: dict[str, Any]) -> set[str]:
    approved: set[str] = set()
    for shot in storyboard.get("director_shots", []) or []:
        if not isinstance(shot, dict):
            continue
        text = shot.get("on_screen_text", {})
        if not isinstance(text, dict):
            continue
        primary = normalize(text.get("primary"))
        if primary:
            approved.add(primary)
        for key in ["secondary", "approved_primary_text"]:
            values = text.get(key, [])
            if isinstance(values, list):
                approved.update(normalize(item) for item in values if normalize(item))
    for scene in storyboard.get("scenes", []) or []:
        if not isinstance(scene, dict):
            continue
        for key in ["caption", "voice"]:
            value = normalize(scene.get(key))
            if value:
                approved.add(value)
        values = scene.get("on_screen_text", [])
        if isinstance(values, list):
            approved.update(normalize(item) for item in values if normalize(item))
    return approved


def validate(storyboard: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []
    approved = approved_texts(storyboard)
    texts = manifest.get("texts", [])
    if not isinstance(texts, list) or not texts:
        issues.append("render_text_manifest.texts must list final on-screen text")
        texts = []

    checked = 0
    unapproved: list[dict[str, Any]] = []
    for item in texts:
        if not isinstance(item, dict):
            continue
        role = normalize(item.get("role")).lower()
        text = normalize(item.get("text"))
        if not text:
            warnings.append(f"{item.get('shot_id', 'unknown')} has empty text entry")
            continue
        if role in PRIMARY_TEXT_ROLES:
            checked += 1
            if text not in approved:
                unapproved.append(
                    {
                        "shot_id": item.get("shot_id"),
                        "role": role,
                        "text": text,
                        "start_sec": item.get("start_sec"),
                        "end_sec": item.get("end_sec"),
                    }
                )
    if checked == 0:
        issues.append("render_text_manifest must include at least one primary title/headline/CTA text entry")
    for item in unapproved:
        issues.append(
            f"{item.get('shot_id', 'unknown')} {item.get('role')} text is not approved by storyboard: {item.get('text')}"
        )

    return {
        "status": "passed" if not issues else "failed",
        "checked_primary_text_count": checked,
        "approved_text_count": len(approved),
        "unapproved_text": unapproved,
        "blocking_issues": issues,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check final render text against storyboard approvals.")
    parser.add_argument("--storyboard", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    report = validate(load_json(Path(args.storyboard)), load_json(Path(args.manifest)))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
