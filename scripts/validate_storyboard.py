#!/usr/bin/env python3
"""Validate V2 storyboard gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


EVIDENCE_TYPES = {"real_ui_demo", "screenshot_proof"}


def motion_layer_count(motion: dict[str, Any]) -> int:
    keys = ["background_motion", "foreground_motion", "callout_motion", "transition"]
    return sum(1 for key in keys if str(motion.get(key, "")).strip() and str(motion.get(key)).lower() != "none")


def validate(data: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    scenes = data.get("scenes", [])
    if len(scenes) < 6:
        issues.append("storyboard must contain at least 6 scenes")
    first_five_changes = 0
    elapsed = 0.0
    evidence_runtime = 0.0
    total_runtime = 0.0
    for scene in scenes:
        duration = float(scene.get("duration_target") or 0)
        total_runtime += duration
        if elapsed < 5:
            first_five_changes += 1
        elapsed += duration
        for key in ["scene_id", "voice", "caption", "on_screen_text", "visual", "motion", "sync", "safe_zone", "qa_notes"]:
            if key not in scene:
                issues.append(f"{scene.get('scene_id', 'unknown')} missing {key}")
        if motion_layer_count(scene.get("motion", {})) < 2:
            issues.append(f"{scene.get('scene_id', 'unknown')} needs at least 2 motion layers")
        visual = scene.get("visual", {})
        if visual.get("scene_type") in EVIDENCE_TYPES:
            evidence_runtime += duration
    if first_five_changes < 2:
        issues.append("first 5 seconds must contain at least 2 visual changes")
    ratio = evidence_runtime / total_runtime if total_runtime else 0
    if ratio < 0.5:
        issues.append("evidence runtime ratio must be at least 0.5")
    return {
        "status": "passed" if not issues else "failed",
        "issues": issues,
        "scene_count": len(scenes),
        "evidence_runtime_ratio": round(ratio, 3),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate storyboard.json gates.")
    parser.add_argument("--storyboard", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()

    data = json.loads(Path(args.storyboard).read_text(encoding="utf-8"))
    report = validate(data)
    if args.out:
        Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
