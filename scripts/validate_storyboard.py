#!/usr/bin/env python3
"""Validate V2 storyboard gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


EVIDENCE_TYPES = {"real_ui_demo", "screenshot_proof"}
BEAT_REQUIRED = ["voice_fragment", "visual_action", "caption", "proof_or_explanation", "motion_trigger"]


def motion_layer_count(motion: dict[str, Any]) -> int:
    keys = ["background_motion", "foreground_motion", "callout_motion", "transition"]
    return sum(1 for key in keys if str(motion.get(key, "")).strip() and str(motion.get(key)).lower() != "none")


def validate(data: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []
    scenes = data.get("scenes", [])
    if len(scenes) < 6:
        issues.append("storyboard must contain at least 6 scenes")
    first_five_changes = 0
    elapsed = 0.0
    evidence_runtime = 0.0
    total_runtime = 0.0
    visual_change_times: list[float] = []
    retention_times: list[float] = []
    for scene in scenes:
        duration = float(scene.get("duration_target") or 0)
        total_runtime += duration
        if elapsed < 5:
            first_five_changes += 1
        visual_change_times.append(elapsed)
        elapsed += duration
        for key in ["scene_id", "voice", "caption", "on_screen_text", "visual", "motion", "sync", "safe_zone", "qa_notes"]:
            if key not in scene:
                issues.append(f"{scene.get('scene_id', 'unknown')} missing {key}")
        beat_map = scene.get("beat_map", [])
        if not beat_map:
            issues.append(f"{scene.get('scene_id', 'unknown')} missing beat_map")
        for index, beat in enumerate(beat_map, start=1):
            retention_times.append(elapsed - duration)
            for key in BEAT_REQUIRED:
                if not str(beat.get(key, "")).strip():
                    issues.append(f"{scene.get('scene_id', 'unknown')} beat {index} missing {key}")
            voice_fragment = str(beat.get("voice_fragment", "")).strip()
            voice = str(scene.get("voice", ""))
            if voice_fragment and voice_fragment not in voice:
                warnings.append(f"{scene.get('scene_id', 'unknown')} beat {index} voice_fragment not found verbatim in voice")
            if not any(term in str(beat.get("proof_or_explanation", "")) for term in ["对比", "证明", "错误", "模板", "结果", "清单", "真实", "保存"]):
                warnings.append(f"{scene.get('scene_id', 'unknown')} beat {index} should name proof, contrast, template, result, or save value")
        if motion_layer_count(scene.get("motion", {})) < 2:
            issues.append(f"{scene.get('scene_id', 'unknown')} needs at least 2 motion layers")
        visual = scene.get("visual", {})
        if visual.get("scene_type") in EVIDENCE_TYPES:
            evidence_runtime += duration
        if duration > 8:
            issues.append(f"{scene.get('scene_id', 'unknown')} duration is too long; split or add reveal/build/focus")
        if duration > 5 and len(beat_map) < 2:
            warnings.append(f"{scene.get('scene_id', 'unknown')} is longer than 5s and should include at least 2 beat_map items")
    if first_five_changes < 2:
        issues.append("first 5 seconds must contain at least 2 visual changes")
    for previous, current in zip(visual_change_times, visual_change_times[1:]):
        if current - previous > 5:
            issues.append("visual changes must happen every 3-5 seconds")
            break
    ratio = evidence_runtime / total_runtime if total_runtime else 0
    if ratio < 0.5:
        issues.append("evidence runtime ratio must be at least 0.5")
    if ratio < 0.6:
        warnings.append("evidence runtime ratio is publishable but below the V3 high-quality target of 0.6")
    if total_runtime >= 8:
        retention_times = retention_times or visual_change_times
        retention_times = sorted(set(round(item, 3) for item in retention_times))
        if not retention_times:
            issues.append("retention beats are missing")
        for previous, current in zip(retention_times, retention_times[1:]):
            if current - previous > 8:
                issues.append("retention beats must appear every 6-8 seconds")
                break
    return {
        "status": "passed" if not issues else "failed",
        "issues": issues,
        "warnings": warnings,
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
