#!/usr/bin/env python3
"""Validate asset_manifest.json before HyperFrames QA."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Optional, Tuple


EVIDENCE_TYPES = {
    "real_ui_screenshot",
    "real_ui_recording",
    "terminal_output",
    "code_or_file_proof",
    "official_doc_screenshot",
}
ASSET_SOURCE_TYPES = {"proof", "support", "generated", "free_stock", "audio", "subtitle"}
BACKGROUND_PROMPT_PACK_NAMES = ("background_prompt_pack.md", "ai_asset_prompt_pack.md")
LOCAL_SUMMARY_CARD_TERMS = {
    "official_source_card_local_render",
    "source card",
    "summary card",
    "local original card",
    "local render",
    "本地原创证据卡",
    "原创证据卡",
    "自制摘要卡",
}
FORBIDDEN_PROVIDER_TERMS = {
    "elevenlabs",
    "runway",
    "kling",
    "heygen",
    "ressemble",
    "veo",
    "paid stock",
    "paid design",
    "paid video",
    "subscription asset",
    "pinterest",
    "付费素材",
    "付费设计",
    "付费视频",
    "订阅素材",
}
APPROVAL_TERMS = {"explicit user approval", "approved paid exception", "用户明确批准", "用户批准"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def resolve_asset_path(raw_path: str, manifest_path: Path, project: Optional[Path]) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path
    if project:
        candidate = project / path
        if candidate.exists():
            return candidate
    return manifest_path.parent / path


def parse_resolution(value: str) -> Optional[Tuple[int, int]]:
    match = re.search(r"(\d{2,5})\s*x\s*(\d{2,5})", value, flags=re.IGNORECASE)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def has_forbidden_provider(text: str) -> bool:
    lowered = text.lower()
    if any(term in lowered for term in APPROVAL_TERMS):
        return False
    return any(term in lowered for term in FORBIDDEN_PROVIDER_TERMS)


def is_local_summary_card(asset: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(asset.get("type", "")),
            str(asset.get("provider", "")),
            str(asset.get("source", "")),
            str(asset.get("source_note", "")),
            str(asset.get("qa_notes", "")),
        ]
    ).lower()
    if any(term in text for term in LOCAL_SUMMARY_CARD_TERMS):
        return True
    return "not an official screenshot" in text or "summarizing official" in text


def is_background_plate(asset: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(asset.get("asset_role", "")),
            str(asset.get("role", "")),
            str(asset.get("type", "")),
            str(asset.get("source", "")),
            str(asset.get("source_note", "")),
            str(asset.get("qa_notes", "")),
        ]
    ).lower()
    return "background_plate" in text or "background plate" in text or "背景" in text


def background_prompt_pack_exists(manifest_path: Path) -> bool:
    internal = manifest_path.parent
    return any((internal / name).exists() and (internal / name).stat().st_size > 0 for name in BACKGROUND_PROMPT_PACK_NAMES)


def validate(manifest: dict[str, Any], manifest_path: Path, project: Optional[Path]) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []
    assets = manifest.get("assets", [])
    scene_usage: dict[str, int] = {}
    evidence_count = 0
    source_class_count = 0
    provider_count = 0
    background_plate_count = 0
    background_plate_valid_count = 0

    if manifest.get("background_plate_required", True) is not False and not background_prompt_pack_exists(manifest_path):
        issues.append("background_prompt_pack.md is required before AI knowledge video asset generation")

    if not isinstance(assets, list):
        issues.append("assets must be an array")
        assets = []

    for index, asset in enumerate(assets, start=1):
        asset_id = str(asset.get("asset_id") or f"asset_{index}")
        asset_type = str(asset.get("type", ""))
        asset_source_type = str(asset.get("asset_source_type", "")).strip()
        provider = str(asset.get("provider", "")).strip()
        raw_path = str(asset.get("path", ""))
        asset_path = resolve_asset_path(raw_path, manifest_path, project) if raw_path else manifest_path

        if asset_source_type in ASSET_SOURCE_TYPES:
            source_class_count += 1
        else:
            issues.append(f"{asset_id}: asset_source_type must be proof/support/generated/free_stock/audio/subtitle")

        background_plate = is_background_plate(asset)
        if background_plate:
            background_plate_count += 1

        if provider:
            provider_count += 1
        else:
            issues.append(f"{asset_id}: provider is required")

        provider_surface = " ".join(
            [
                provider,
                str(asset.get("source", "")),
                str(asset.get("source_note", "")),
                raw_path,
            ]
        )
        if has_forbidden_provider(provider_surface):
            issues.append(f"{asset_id}: disabled paid/scraping provider used without explicit approval")

        if not raw_path:
            issues.append(f"{asset_id}: missing path")
        elif not exists(asset_path):
            issues.append(f"{asset_id}: asset file missing or empty: {raw_path}")

        for scene_id in asset.get("used_in_scenes", []) or []:
            scene_usage[scene_id] = scene_usage.get(scene_id, 0) + 1

        is_evidence = bool(asset.get("is_evidence"))
        if is_evidence:
            evidence_count += 1
            if asset_type not in EVIDENCE_TYPES:
                issues.append(f"{asset_id}: evidence asset must use a real proof type, not {asset_type}")
            if asset_source_type != "proof":
                issues.append(f"{asset_id}: evidence asset must use asset_source_type=proof")
            if is_local_summary_card(asset):
                issues.append(
                    f"{asset_id}: local summary/designed cards cannot be counted as proof; use real UI/doc/terminal proof or classify as support"
                )
        elif asset_source_type == "proof" and is_local_summary_card(asset):
            issues.append(f"{asset_id}: local summary/designed cards cannot use asset_source_type=proof")
        if asset_type == "generated_visual" and is_evidence:
            issues.append(f"{asset_id}: AI-generated visual cannot be counted as real evidence")
        if asset_type == "generated_visual" and asset_source_type == "proof":
            issues.append(f"{asset_id}: generated visual cannot use asset_source_type=proof")
        if asset_source_type == "free_stock" and is_evidence:
            issues.append(f"{asset_id}: free_stock assets cannot be counted as evidence")

        resolution = parse_resolution(str(asset.get("resolution", "")))
        if not resolution:
            warnings.append(f"{asset_id}: resolution is missing or not formatted as WIDTHxHEIGHT")
        elif resolution[0] < 720 or resolution[1] < 720:
            warnings.append(f"{asset_id}: resolution may be too low for readable mobile video")

        if asset.get("contains_private_info") is True:
            issues.append(f"{asset_id}: contains private information")
        if asset.get("contains_contact_info") is True:
            issues.append(f"{asset_id}: contains contact information")
        if asset.get("contains_qr_code") is True:
            issues.append(f"{asset_id}: contains QR code")
        if asset.get("risk") == "high":
            issues.append(f"{asset_id}: high-risk asset requires replacement or documented approval")

        copyright_status = str(asset.get("copyright_status", ""))
        if copyright_status == "unknown":
            warnings.append(f"{asset_id}: copyright status is unknown")
        source_note = str(asset.get("source_note", ""))
        if asset_type == "generated_visual" and any(term in source_note for term in ["官方", "真实", "截图", "评价", "认证"]):
            issues.append(f"{asset_id}: generated visual appears to claim real or official proof")

        if background_plate:
            if asset_type != "generated_visual":
                issues.append(f"{asset_id}: background_plate must use type=generated_visual")
            if asset_source_type != "generated":
                issues.append(f"{asset_id}: background_plate must use asset_source_type=generated")
            if is_evidence:
                issues.append(f"{asset_id}: background_plate must not be counted as evidence")
            if resolution != (1920, 1080):
                issues.append(f"{asset_id}: background_plate must be 1920x1080 for AI knowledge videos")
            boundary_text = f"{source_note} {asset.get('qa_notes', '')}".lower()
            if not any(term in boundary_text for term in ["not official", "not factual proof", "support background", "support visual", "非证据", "不作为证据"]):
                issues.append(f"{asset_id}: background_plate must document that it is support-only, not evidence")
            if (
                asset_type == "generated_visual"
                and asset_source_type == "generated"
                and not is_evidence
                and resolution == (1920, 1080)
            ):
                background_plate_valid_count += 1

    repeated_scenes = [scene_id for scene_id, count in scene_usage.items() if count > 4]
    for scene_id in repeated_scenes:
        warnings.append(f"{scene_id}: many assets reference the same scene; verify duplicate usage is intentional")

    if assets and evidence_count == 0:
        issues.append("asset manifest has no real evidence assets")
    if manifest.get("background_plate_required", True) is not False and background_plate_valid_count == 0:
        issues.append("AI knowledge asset manifest must include at least one valid generated text-free 1920x1080 background_plate")

    return {
        "status": "passed" if not issues else "failed",
        "asset_count": len(assets),
        "evidence_asset_count": evidence_count,
        "source_class_count": source_class_count,
        "provider_count": provider_count,
        "background_plate_count": background_plate_count,
        "background_plate_valid_count": background_plate_valid_count,
        "blocking_issues": issues,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate asset manifest safety and evidence quality.")
    parser.add_argument("--manifest", required=True, help="asset_manifest.json path")
    parser.add_argument("--project", help="Optional project root for relative asset paths")
    parser.add_argument("--out", help="Output asset_validation.json path")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    project = Path(args.project) if args.project else None
    report = validate(load_json(manifest_path), manifest_path, project)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
