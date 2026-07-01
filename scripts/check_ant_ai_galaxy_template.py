#!/usr/bin/env python3
"""Validate the Ant AI Scheme 7 galaxy renderer contract."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "templates" / "ant_ai_hotlist_galaxy" / "renderer_config.json"
PREVIEW = ROOT / "templates" / "ant_ai_hotlist_galaxy" / "preview.html"
SAMPLE = ROOT / "templates" / "ant_ai_hotlist_galaxy" / "sample_hotlist.json"
DESIGN_CONTRACT = ROOT / "references" / "ant_ai_hotlist_galaxy_design_contract.md"
QUALITY_CHECKLIST = ROOT / "references" / "ant_ai_hotlist_galaxy_quality_checklist.md"
TOP5_TEMPLATE = ROOT / "templates" / "ai_hot_rank_top5.template.json"
SCENE_REGISTRY = ROOT / "references" / "fixed_ai_scene_motion_templates.json"
BACKGROUND_REGISTRY = ROOT / "references" / "fixed_ai_background_template_rotation.json"
DYNAMIC_MANIFEST = ROOT / "assets" / "ai_background_templates_dynamic" / "dynamic_asset_manifest.json"
ANT_DOC = ROOT / "references" / "ai_video_scheme_7_ant_ai_hotlist_extended.md"
BACKGROUND_GENERATOR = ROOT / "scripts" / "generate_ant_ai_hotlist_background.py"

ANT_PROFILE_ID = "ant_ai_hotlist_extended"
BACKGROUND_ID = "BG_FIXED_11_ANT_AI_HOTLIST_NEBULA_9X16"
DYNAMIC_ID = "BG_DYNAMIC_11"

EXPECTED_GALAXY = {
    "centerX": 0.52,
    "centerY": 0.44,
    "width": 1.18,
    "tiltDeg": -17,
    "scaleY": 0.62,
    "rotationDuration": 42,
    "opacity": 0.58,
    "blendMode": "screen",
    "maskFeather": 0.72,
    "motion_mode": "local_internal_rotation",
}

EXPECTED_CARD = {
    "backgroundAlpha": 0.26,
    "minBackgroundAlpha": 0.24,
    "maxBackgroundAlpha": 0.34,
    "blur": 5,
    "borderAlpha": 0.18,
    "innerGlowAlpha": 0.08,
    "material": "transparent_glass",
}

EXPECTED_PATHS = {
    "design_contract": "references/ant_ai_hotlist_galaxy_design_contract.md",
    "quality_checklist": "references/ant_ai_hotlist_galaxy_quality_checklist.md",
    "preview_template": "templates/ant_ai_hotlist_galaxy/preview.html",
    "renderer_config": "templates/ant_ai_hotlist_galaxy/renderer_config.json",
}

FORBIDDEN_POSITIVE_MOTION = {
    "slow push",
    "slow_push",
    "slow_nebula_push",
    "慢速推近",
    "慢速推镜",
    "整张图片 scale",
    "scale(1.02)",
    "scale(1.08)",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def close_enough(actual: Any, expected: Any) -> bool:
    if isinstance(expected, float):
        try:
            return abs(float(actual) - expected) <= 0.001
        except (TypeError, ValueError):
            return False
    return actual == expected


def validate_dict(label: str, data: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for key, value in expected.items():
        if not close_enough(data.get(key), value):
            issues.append(f"{label}.{key} must be {value!r}, got {data.get(key)!r}")
    return issues


def ant_profile_from_top5(data: dict[str, Any]) -> dict[str, Any]:
    extended = data.get("extended_profiles") if isinstance(data.get("extended_profiles"), dict) else {}
    profile = extended.get(ANT_PROFILE_ID)
    return profile if isinstance(profile, dict) else {}


def ant_profile_from_scene_registry(data: dict[str, Any]) -> dict[str, Any]:
    top5 = data.get("ai_hot_rank_top5_template") if isinstance(data.get("ai_hot_rank_top5_template"), dict) else {}
    extended = top5.get("extended_profiles") if isinstance(top5.get("extended_profiles"), dict) else {}
    profile = extended.get(ANT_PROFILE_ID)
    return profile if isinstance(profile, dict) else {}


def background_entry(data: dict[str, Any]) -> dict[str, Any]:
    entries = data.get("background_templates") or data.get("templates") or []
    for item in entries:
        if isinstance(item, dict) and item.get("id") == BACKGROUND_ID:
            return item
    return {}


def dynamic_entry(data: dict[str, Any]) -> dict[str, Any]:
    for item in data.get("assets", []):
        if isinstance(item, dict) and item.get("id") == DYNAMIC_ID:
            return item
    return {}


def positive_motion_text(entry: dict[str, Any]) -> str:
    fields = [
        entry.get("asset_generation_method"),
        entry.get("generation_method"),
        entry.get("background_implementation"),
        entry.get("motion_description"),
        entry.get("prompt"),
        " ".join(str(item) for item in entry.get("motion_affordance", []) if isinstance(item, str)),
        " ".join(str(item) for item in entry.get("motion_layers", []) if isinstance(item, str)),
    ]
    return "\n".join(str(field) for field in fields if field)


def validate_preview_html(path: Path) -> list[str]:
    issues: list[str] = []
    html = path.read_text(encoding="utf-8")
    required_tokens = [
        "BG_DYNAMIC_11_蚂蚁AI热榜星云_9x16.mp4",
        "id=\"alpha\"",
        'min="0.24"',
        'max="0.34"',
        'value="0.26"',
        "id=\"speed\"",
        "id=\"quality\"",
        "id=\"toggleCard\"",
        "id=\"exportFrame\"",
        "id=\"recordPreview\"",
        "captureStream(30)",
        "关注 蚂蚁AI",
    ]
    for token in required_tokens:
        if token not in html:
            issues.append(f"preview.html missing required token: {token}")
    if re.search(r"background(?:-color)?\s*:\s*rgba\(\s*0\s*,\s*0\s*,\s*0\s*,\s*0\.[6-9]", html):
        issues.append("preview.html contains an opaque black glass/card fill")
    return issues


def validate_generator_contract(path: Path) -> list[str]:
    issues: list[str] = []
    text = path.read_text(encoding="utf-8")
    required_tokens = [
        "GALAXY_MOTION_CONTRACT",
        '"centerX": 0.52',
        '"centerY": 0.44',
        '"width": 1.18',
        '"tiltDeg": -17.0',
        '"scaleY": 0.62',
        '"rotationDuration": 42.0',
        '"opacity": 0.58',
        '"maskFeather": 0.72',
        "galaxy_disk_mask",
        "default=42.0",
    ]
    for token in required_tokens:
        if token not in text:
            issues.append(f"generate_ant_ai_hotlist_background.py missing contract token: {token}")
    return issues


def validate() -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []
    required_files = [
        CONFIG,
        PREVIEW,
        SAMPLE,
        DESIGN_CONTRACT,
        QUALITY_CHECKLIST,
        TOP5_TEMPLATE,
        SCENE_REGISTRY,
        BACKGROUND_REGISTRY,
        DYNAMIC_MANIFEST,
        ANT_DOC,
        BACKGROUND_GENERATOR,
    ]
    for path in required_files:
        if not exists(path):
            issues.append(f"missing required file: {path.relative_to(ROOT)}")
    if issues:
        return {"status": "failed", "blocking_issues": issues, "warnings": warnings, "signals": {}}

    config = load_json(CONFIG)
    top5 = load_json(TOP5_TEMPLATE)
    scene = load_json(SCENE_REGISTRY)
    background = load_json(BACKGROUND_REGISTRY)
    dynamic = load_json(DYNAMIC_MANIFEST)
    sample = load_json(SAMPLE)

    if config.get("scheme_variant") != ANT_PROFILE_ID:
        issues.append("renderer_config scheme_variant must be ant_ai_hotlist_extended")
    fmt = config.get("format") if isinstance(config.get("format"), dict) else {}
    if fmt.get("width") != 1080 or fmt.get("height") != 1920:
        issues.append("renderer_config format must be 1080x1920")
    issues.extend(validate_dict("renderer_config.galaxy", config.get("galaxy", {}), EXPECTED_GALAXY))
    issues.extend(validate_dict("renderer_config.card", config.get("card", {}), EXPECTED_CARD))
    bg_policy = config.get("background") if isinstance(config.get("background"), dict) else {}
    for key in ("static_base_plate_locked", "full_frame_scale_forbidden", "ken_burns_forbidden", "whole_frame_pan_forbidden"):
        if bg_policy.get(key) is not True:
            issues.append(f"renderer_config.background.{key} must be true")
    for key in ("asset_path", "poster_path"):
        raw_path = bg_policy.get(key)
        if not isinstance(raw_path, str) or not raw_path.strip():
            issues.append(f"renderer_config.background.{key} must be set")
            continue
        resolved = (CONFIG.parent / raw_path).resolve()
        if not exists(resolved):
            issues.append(f"renderer_config.background.{key} missing or empty: {raw_path}")

    top5_profile = ant_profile_from_top5(top5)
    scene_profile = ant_profile_from_scene_registry(scene)
    for label, profile in (("top5_template", top5_profile), ("scene_registry", scene_profile)):
        if not profile:
            issues.append(f"{label} missing ant_ai_hotlist_extended profile")
            continue
        for key, expected in EXPECTED_PATHS.items():
            if profile.get(key) != expected:
                issues.append(f"{label}.{key} must be {expected}")
        issues.extend(validate_dict(f"{label}.galaxy_motion_contract", profile.get("galaxy_motion_contract", {}), EXPECTED_GALAXY))
        issues.extend(validate_dict(f"{label}.glass_card_contract", profile.get("glass_card_contract", {}), EXPECTED_CARD))

    bg_entry = background_entry(background)
    dyn_entry = dynamic_entry(dynamic)
    if not bg_entry:
        issues.append(f"fixed background registry missing {BACKGROUND_ID}")
    else:
        motion_contract = bg_entry.get("motion_contract") if isinstance(bg_entry.get("motion_contract"), dict) else {}
        if motion_contract.get("static_base_plate_locked") is not True:
            issues.append("fixed background motion_contract.static_base_plate_locked must be true")
        issues.extend(validate_dict("fixed_background.motion_contract.galaxy", motion_contract.get("galaxy", {}), EXPECTED_GALAXY))
        issues.extend(validate_dict("fixed_background.motion_contract.glass_card", motion_contract.get("glass_card", {}), EXPECTED_CARD))
        surface = positive_motion_text(bg_entry).lower()
        for term in FORBIDDEN_POSITIVE_MOTION:
            if term.lower() in surface:
                issues.append(f"fixed background positive motion text contains forbidden term: {term}")

    if not dyn_entry:
        issues.append(f"dynamic manifest missing {DYNAMIC_ID}")
    else:
        motion_contract = dyn_entry.get("motion_contract") if isinstance(dyn_entry.get("motion_contract"), dict) else {}
        if motion_contract.get("static_base_plate_locked") is not True:
            issues.append("dynamic manifest motion_contract.static_base_plate_locked must be true")
        issues.extend(validate_dict("dynamic_manifest.motion_contract.galaxy", motion_contract.get("galaxy", {}), EXPECTED_GALAXY))
        issues.extend(validate_dict("dynamic_manifest.motion_contract.glass_card", motion_contract.get("glass_card", {}), EXPECTED_CARD))
        checks = dyn_entry.get("checks") if isinstance(dyn_entry.get("checks"), dict) else {}
        for key in ("no_full_frame_scale_or_ken_burns", "local_galaxy_internal_rotation", "transparent_glass_card_alpha_contract"):
            if checks.get(key) is not True:
                issues.append(f"dynamic manifest checks.{key} must be true")
        surface = positive_motion_text(dyn_entry).lower()
        for term in FORBIDDEN_POSITIVE_MOTION:
            if term.lower() in surface:
                issues.append(f"dynamic manifest positive motion text contains forbidden term: {term}")

    sample_items = sample.get("items") if isinstance(sample.get("items"), list) else []
    if len(sample_items) != 5:
        issues.append("sample_hotlist.json must contain five sample items")
    if sample.get("cta") != "关注 蚂蚁AI":
        issues.append("sample_hotlist.json cta must be 关注 蚂蚁AI")

    ant_doc = ANT_DOC.read_text(encoding="utf-8")
    for token in (
        "references/ant_ai_hotlist_galaxy_design_contract.md",
        "templates/ant_ai_hotlist_galaxy/preview.html",
        "full-frame scale",
        "0.24-0.34",
        "python3 scripts/check_ant_ai_galaxy_template.py",
    ):
        if token not in ant_doc:
            issues.append(f"ant_ai_hotlist_extended doc missing token: {token}")

    issues.extend(validate_preview_html(PREVIEW))
    issues.extend(validate_generator_contract(BACKGROUND_GENERATOR))

    return {
        "status": "passed" if not issues else "failed",
        "blocking_issues": issues,
        "warnings": warnings,
        "signals": {
            "renderer_config": str(CONFIG.relative_to(ROOT)),
            "preview_template": str(PREVIEW.relative_to(ROOT)),
            "design_contract": str(DESIGN_CONTRACT.relative_to(ROOT)),
            "dynamic_background_id": DYNAMIC_ID,
            "galaxy_rotation_duration_sec": EXPECTED_GALAXY["rotationDuration"],
            "glass_card_alpha_default": EXPECTED_CARD["backgroundAlpha"],
            "sample_rank_items": len(sample_items),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Ant AI hotlist galaxy renderer contract.")
    parser.add_argument("--out", default=str(ROOT / "outputs" / "ant_ai_galaxy_template_check.json"))
    args = parser.parse_args()

    report = validate()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if report["status"] != "passed":
        for issue in report["blocking_issues"]:
            print(f"- {issue}")
        return 1
    print(f"Ant AI galaxy template check passed: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
