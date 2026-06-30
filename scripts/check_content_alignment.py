#!/usr/bin/env python3
"""Check source-copy-visual alignment for AI Douyin video packages."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


MISSING_SOURCE_VALUES = {"", "无", "none", "n/a", "待补充", "todo", "unknown"}
PROOF_TYPES = {"fact", "news", "source", "official", "data", "release", "事实", "新闻", "来源", "官方", "数据"}
PROOF_STAGE_TERMS = {"proof", "evidence", "example", "demo", "证明", "证据", "例子", "演示", "对比"}
GENERIC_VISUAL_TERMS = [
    "generic ai",
    "tech background",
    "technology background",
    "premium tech",
    "futuristic",
    "neon",
    "abstract",
    "科技感",
    "高级科技",
    "未来感",
    "抽象背景",
    "数字空间",
    "炫酷背景",
]
MOTION_BEAT_FIELDS = ("beat_map", "visual_beats", "beat_points", "timeline_beats", "micro_beats")
SFX_CUE_FIELDS = ("sfx_cues", "audio_cues", "icon_audio_cues")
NO_SFX_TERMS = ("no_sfx", "no sfx", "without sfx", "无音效", "不要音效", "静音")
ALLOWED_ENGLISH_TOKENS = {
    "ai",
    "api",
    "cli",
    "ui",
    "ux",
    "tts",
    "sfx",
    "mp4",
    "json",
    "md",
    "html",
    "css",
    "js",
    "url",
    "openai",
    "chatgpt",
    "gpt",
    "codex",
    "gemini",
    "google",
    "github",
    "browser",
    "hugging",
    "face",
    "developers",
    "hyperframes",
    "remotion",
    "imagegen",
    "heygen",
    "ffmpeg",
    "skill",
    "prompt",
    "agent",
    "agents",
    "workflow",
}


def load_json(path: Path | None) -> dict[str, Any]:
    if not path or not path.exists() or path.stat().st_size == 0:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_source(value: Any) -> str:
    return str(value or "").strip()


def source_present(value: Any) -> bool:
    return normalize_source(value).lower() not in MISSING_SOURCE_VALUES


def cjk_chars(text: str) -> list[str]:
    return re.findall(r"[\u4e00-\u9fff]", text)


def english_tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z0-9+._-]*", text)


def is_language_exception(path: str, text: str) -> bool:
    lowered_path = path.lower()
    lowered_text = text.lower()
    if any(part in lowered_path for part in ("source_url", "asset_path", "file", "path")):
        return True
    tokens = [token.lower().strip("._-+") for token in english_tokens(text)]
    real_tokens = [token for token in tokens if len(token) > 1]
    return bool(real_tokens) and all(token in ALLOWED_ENGLISH_TOKENS for token in real_tokens)


def text_values(value: Any, prefix: str) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    if isinstance(value, str):
        if value.strip():
            items.append((prefix, value.strip()))
    elif isinstance(value, list):
        for index, item in enumerate(value, start=1):
            items.extend(text_values(item, f"{prefix}[{index}]"))
    elif isinstance(value, dict):
        for key, item in value.items():
            items.extend(text_values(item, f"{prefix}.{key}" if prefix else str(key)))
    return items


def public_text_items(copy_json: dict[str, Any], storyboard: dict[str, Any] | None = None) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    broad_copy_fields = ["title_options", "cover_text_options", "scene_captions", "on_screen_text", "publish_caption", "hashtags"]
    for field in broad_copy_fields:
        if field in copy_json:
            items.extend(text_values(copy_json[field], f"copy_package.{field}"))
    for field in ("first_3_seconds_hook", "first_5_seconds_hook"):
        hook = copy_json.get(field)
        if isinstance(hook, dict):
            for key in ("line", "visual", "caption"):
                items.extend(text_values(hook.get(key), f"copy_package.{field}.{key}"))
            items.extend(text_values(hook.get("visual_changes"), f"copy_package.{field}.visual_changes"))
    for index, item in enumerate(copy_json.get("first_5_seconds_hooks") or [], start=1):
        if not isinstance(item, dict):
            continue
        for key in ("line", "visual", "caption"):
            items.extend(text_values(item.get(key), f"copy_package.first_5_seconds_hooks[{index}].{key}"))
    for index, item in enumerate(copy_json.get("copy_progression_plan") or [], start=1):
        if isinstance(item, dict):
            items.extend(text_values(item.get("new_information_job"), f"copy_package.copy_progression_plan[{index}].new_information_job"))
    for index, item in enumerate(copy_json.get("content_alignment_map") or [], start=1):
        if not isinstance(item, dict):
            continue
        for key in ("claim", "copy_line", "visual_job", "allowed_on_screen_text"):
            items.extend(text_values(item.get(key), f"copy_package.content_alignment_map[{index}].{key}"))

    if storyboard:
        title = storyboard.get("title")
        if isinstance(title, str) and title.strip():
            items.append(("storyboard.title", title.strip()))
        for index, shot in enumerate(storyboard.get("director_shots") or [], start=1):
            if not isinstance(shot, dict):
                continue
            for field in ("visual_subject", "primary_action", "viewer_focus", "on_screen_text"):
                items.extend(text_values(shot.get(field), f"director_shots[{index}].{field}"))
        for index, scene in enumerate(storyboard.get("scenes") or [], start=1):
            if not isinstance(scene, dict):
                continue
            scene_id = str(scene.get("scene_id") or f"S{index:02d}")
            for field in ("voice", "caption", "on_screen_text", "primary_read_text", "text_layers"):
                items.extend(text_values(scene.get(field), f"scenes[{scene_id}].{field}"))
    return items


def chinese_first_issues(copy_json: dict[str, Any], storyboard: dict[str, Any] | None = None) -> tuple[list[str], dict[str, Any]]:
    issues: list[str] = []
    checked = 0
    exception_count = 0
    for path, text in public_text_items(copy_json, storyboard):
        tokens = [token for token in english_tokens(text) if len(token) > 1]
        if not tokens:
            continue
        checked += 1
        chinese_count = len(cjk_chars(text))
        english_letter_count = sum(len(token) for token in tokens)
        if is_language_exception(path, text):
            exception_count += 1
            continue
        if chinese_count == 0 and english_letter_count >= 4:
            issues.append(f"{path} visible text must be Chinese-first or declare an allowed product/code exception: {text}")
        elif english_letter_count > max(10, chinese_count * 2):
            issues.append(f"{path} uses too much non-essential English for a Chinese-first video: {text}")
    return issues, {
        "checked_text_items": checked,
        "language_exception_count": exception_count,
        "chinese_first_issue_count": len(issues),
    }


def claim_records(copy_json: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    raw_map = copy_json.get("content_alignment_map")
    if isinstance(raw_map, dict):
        raw_entries = raw_map.get("claims") or raw_map.get("items") or raw_map.get("scenes") or []
    else:
        raw_entries = raw_map if isinstance(raw_map, list) else []
    for index, item in enumerate(raw_entries, start=1):
        if not isinstance(item, dict):
            continue
        source_ids = item.get("source_ids")
        if not isinstance(source_ids, list):
            source_ids = [item.get("source_id") or item.get("source") or item.get("source_title")]
        records.append(
            {
                "claim_id": str(item.get("claim_id") or item.get("id") or f"C{index:02d}"),
                "claim": str(item.get("claim") or item.get("copy_line") or item.get("narration_line") or "").strip(),
                "type": str(item.get("type") or item.get("claim_type") or "fact").strip().lower(),
                "source_ids": [normalize_source(source) for source in source_ids if source_present(source)],
                "source": normalize_source(item.get("source") or item.get("source_title") or item.get("evidence")),
                "scene_id": normalize_source(item.get("scene_id")),
                "visual_job": normalize_source(item.get("visual_job") or item.get("information_job")),
            }
        )

    if records:
        return records

    ledger = copy_json.get("claim_ledger")
    if isinstance(ledger, list):
        for index, item in enumerate(ledger, start=1):
            if not isinstance(item, dict):
                continue
            source = item.get("source")
            records.append(
                {
                    "claim_id": str(item.get("claim_id") or f"C{index:02d}"),
                    "claim": str(item.get("claim") or "").strip(),
                    "type": str(item.get("type") or "fact").strip().lower(),
                    "source_ids": [normalize_source(source)] if source_present(source) else [],
                    "source": normalize_source(source),
                    "scene_id": normalize_source(item.get("scene_id")),
                    "visual_job": normalize_source(item.get("proof_visual") or item.get("visual_job")),
                }
            )

    proof_plan = copy_json.get("proof_visual_plan")
    if isinstance(proof_plan, list):
        start = len(records) + 1
        for offset, item in enumerate(proof_plan, start=start):
            if not isinstance(item, dict):
                continue
            evidence = item.get("source") or item.get("proof_visual") or item.get("asset_needed")
            records.append(
                {
                    "claim_id": str(item.get("claim_id") or f"C{offset:02d}"),
                    "claim": str(item.get("claim") or "").strip(),
                    "type": "proof_visual",
                    "source_ids": [normalize_source(evidence)] if source_present(evidence) else [],
                    "source": normalize_source(evidence),
                    "scene_id": normalize_source(item.get("scene_id") or item.get("scene")),
                    "visual_job": normalize_source(item.get("proof_visual")),
                }
            )
    return records


def source_claim_issues(copy_json: dict[str, Any]) -> tuple[list[str], list[str], dict[str, Any]]:
    issues: list[str] = []
    warnings: list[str] = []
    records = claim_records(copy_json)
    if not records:
        warnings.append("copy_package.json should include content_alignment_map or claim_ledger before storyboard")
        return issues, warnings, {"claim_count": 0, "sourced_claim_count": 0}

    sourced = 0
    for item in records:
        claim = item["claim"] or item["claim_id"]
        proof_required = item["type"] in PROOF_TYPES or item["type"] not in {"opinion", "advice", "经验", "建议"}
        has_source = bool(item["source_ids"] or source_present(item["source"]))
        if has_source:
            sourced += 1
        if proof_required and not has_source:
            issues.append(f"{item['claim_id']} claim has no source/evidence binding: {claim}")
        if not item["claim"]:
            issues.append(f"{item['claim_id']} content alignment claim text is empty")
    return issues, warnings, {"claim_count": len(records), "sourced_claim_count": sourced}


def token_set(text: str) -> set[str]:
    lowered = text.lower()
    cjk_terms = set(re.findall(r"[\u4e00-\u9fff]{2,}", lowered))
    ascii_terms = {
        token
        for token in re.findall(r"[a-z][a-z0-9+._-]{2,}", lowered)
        if token not in ALLOWED_ENGLISH_TOKENS
    }
    return cjk_terms | ascii_terms


def similarity(left: str, right: str) -> float:
    left_terms = token_set(left)
    right_terms = token_set(right)
    if not left_terms or not right_terms:
        return 0.0
    return len(left_terms & right_terms) / max(1, min(len(left_terms), len(right_terms)))


def progression_entries(copy_json: dict[str, Any], storyboard: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    raw = copy_json.get("copy_progression_plan")
    entries: list[dict[str, Any]] = []
    if isinstance(raw, list):
        for index, item in enumerate(raw, start=1):
            if not isinstance(item, dict):
                continue
            entries.append(
                {
                    "id": str(item.get("scene_id") or item.get("id") or f"P{index:02d}"),
                    "stage": str(item.get("stage") or item.get("information_stage") or "").strip(),
                    "job": str(item.get("new_information_job") or item.get("job") or item.get("line") or "").strip(),
                    "reuse_allowed": item.get("reuse_allowed") is True,
                }
            )
    elif isinstance(copy_json.get("retention_beats"), list):
        for index, item in enumerate(copy_json["retention_beats"], start=1):
            if not isinstance(item, dict):
                continue
            entries.append(
                {
                    "id": str(item.get("scene") or item.get("time_range") or f"B{index:02d}"),
                    "stage": str(item.get("type") or "").strip(),
                    "job": str(item.get("line") or item.get("visual") or "").strip(),
                    "reuse_allowed": False,
                }
            )

    if not entries and storyboard:
        for index, scene in enumerate(storyboard.get("scenes") or [], start=1):
            if not isinstance(scene, dict):
                continue
            entries.append(
                {
                    "id": str(scene.get("scene_id") or f"S{index:02d}"),
                    "stage": str(scene.get("information_stage") or "").strip(),
                    "job": str(scene.get("new_information_job") or scene.get("concept") or scene.get("voice") or "").strip(),
                    "reuse_allowed": scene.get("reuse_allowed") is True,
                }
            )
    return entries


def copy_progression_issues(copy_json: dict[str, Any], storyboard: dict[str, Any] | None = None) -> tuple[list[str], list[str], dict[str, Any]]:
    issues: list[str] = []
    warnings: list[str] = []
    entries = progression_entries(copy_json, storyboard)
    if not entries:
        warnings.append("copy progression plan is missing; add copy_progression_plan before storyboard")
        return issues, warnings, {"progression_entry_count": 0, "duplicate_pair_count": 0}

    duplicate_pairs = 0
    for previous, current in zip(entries, entries[1:]):
        previous_job = previous["job"]
        current_job = current["job"]
        if not current_job:
            issues.append(f"{current['id']} new_information_job is empty")
            continue
        sim = similarity(previous_job, current_job)
        same_stage = previous["stage"] and previous["stage"] == current["stage"]
        proof_stage = any(term in current["stage"].lower() for term in PROOF_STAGE_TERMS) or any(
            term in current["stage"] for term in PROOF_STAGE_TERMS
        )
        repeated_exact_job = previous_job and current_job and previous_job == current_job
        if (repeated_exact_job or (sim >= 0.82 and same_stage)) and not current["reuse_allowed"] and not proof_stage:
            duplicate_pairs += 1
            issues.append(
                f"{current['id']} repeats the previous information job instead of adding new information: {current_job}"
            )
    return issues, warnings, {
        "progression_entry_count": len(entries),
        "duplicate_pair_count": duplicate_pairs,
    }


def scene_claim_ids(scene: dict[str, Any]) -> list[str]:
    values: list[Any] = []
    for key in ("claim_ids", "source_claim_ids", "copy_line_ids"):
        raw = scene.get(key)
        if isinstance(raw, list):
            values.extend(raw)
        elif raw:
            values.append(raw)
    visual = scene.get("visual") if isinstance(scene.get("visual"), dict) else {}
    for key in ("claim_ids", "source_claim_ids", "copy_line_ids"):
        raw = visual.get(key)
        if isinstance(raw, list):
            values.extend(raw)
        elif raw:
            values.append(raw)
    return [str(value).strip() for value in values if str(value).strip()]


def list_item_count(value: Any) -> int:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        return 1
    if isinstance(value, str) and value.strip():
        return 1
    return 0


def scene_duration_seconds(scene: dict[str, Any]) -> float:
    for key in ("duration_target", "duration_sec", "duration"):
        try:
            value = float(scene.get(key) or 0)
        except (TypeError, ValueError):
            value = 0.0
        if value > 0:
            return value
    timing = scene.get("timing") if isinstance(scene.get("timing"), dict) else {}
    try:
        start = float(timing.get("start") or scene.get("start") or 0)
        end = float(timing.get("end") or scene.get("end") or 0)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, end - start)


def scene_motion_count(scene: dict[str, Any]) -> int:
    visual = scene.get("visual") if isinstance(scene.get("visual"), dict) else {}
    total = 0
    for field in MOTION_BEAT_FIELDS:
        total += list_item_count(scene.get(field))
        total += list_item_count(visual.get(field))
    for field in ("animation_cues", "motion_phases", "component_motion", "transition_motion"):
        total += list_item_count(scene.get(field))
        total += list_item_count(visual.get(field))
    return total


def scene_sfx_count(scene: dict[str, Any]) -> int:
    visual = scene.get("visual") if isinstance(scene.get("visual"), dict) else {}
    sync = scene.get("sync") if isinstance(scene.get("sync"), dict) else {}
    total = 0
    for field in SFX_CUE_FIELDS:
        total += list_item_count(scene.get(field))
        total += list_item_count(visual.get(field))
        total += list_item_count(sync.get(field))
    return total


def storyboard_requires_sfx(storyboard: dict[str, Any]) -> bool:
    quality = storyboard.get("quality_spec") if isinstance(storyboard.get("quality_spec"), dict) else {}
    decision = storyboard.get("audio_music_decision") if isinstance(storyboard.get("audio_music_decision"), dict) else {}
    if decision.get("sfx_required") is False:
        return False
    policy_text = " ".join(
        str(value)
        for value in (
            quality.get("sfx_policy"),
            storyboard.get("sfx_policy"),
            decision,
        )
        if value
    ).lower()
    if any(term in policy_text for term in NO_SFX_TERMS):
        return False
    if "sfx" in policy_text or "音效" in policy_text:
        return True
    scenes = storyboard.get("scenes")
    return isinstance(scenes, list) and len(scenes) >= 3


def visual_alignment_issues(storyboard: dict[str, Any] | None, known_claim_ids: set[str]) -> tuple[list[str], list[str], dict[str, Any]]:
    issues: list[str] = []
    warnings: list[str] = []
    if not storyboard:
        warnings.append("storyboard is unavailable for visual alignment check")
        return issues, warnings, {"scene_alignment_count": 0, "scene_count": 0}
    scenes = storyboard.get("scenes")
    if not isinstance(scenes, list):
        return ["storyboard.scenes must be an array for content alignment"], warnings, {"scene_alignment_count": 0, "scene_count": 0}

    aligned = 0
    generic_count = 0
    dynamic_scene_count = 0
    static_scene_count = 0
    sfx_scene_count = 0
    missing_sfx_scene_count = 0
    sfx_required = storyboard_requires_sfx(storyboard)
    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            continue
        scene_id = str(scene.get("scene_id") or f"S{index:02d}")
        visual = scene.get("visual") if isinstance(scene.get("visual"), dict) else {}
        visual_job = str(
            scene.get("visual_job")
            or visual.get("information_job")
            or visual.get("description")
            or visual.get("proof_chain")
            or ""
        ).strip()
        new_job = str(scene.get("new_information_job") or scene.get("concept") or scene.get("voice") or "").strip()
        if not new_job:
            issues.append(f"{scene_id} must state new_information_job or a concrete one-idea concept")
        if not visual_job:
            issues.append(f"{scene_id} visual must state a visual_job/information_job/description tied to the current copy")

        ids = scene_claim_ids(scene)
        missing_ids = sorted({claim_id for claim_id in ids if known_claim_ids and claim_id not in known_claim_ids})
        if missing_ids:
            issues.append(f"{scene_id} references unknown claim ids: {', '.join(missing_ids)}")
        evidence_source = str(visual.get("evidence_source") or visual.get("asset_path") or visual.get("proof_chain") or "").strip()
        has_binding = bool(ids or evidence_source or visual.get("proof_chain"))
        if has_binding and visual_job and new_job:
            aligned += 1

        visual_blob = json.dumps(
            {
                "scene_type": visual.get("scene_type"),
                "description": visual.get("description"),
                "evidence_source": visual.get("evidence_source"),
                "design_layers": visual.get("design_layers"),
            },
            ensure_ascii=False,
        ).lower()
        is_generic = any(term in visual_blob for term in GENERIC_VISUAL_TERMS)
        if is_generic:
            generic_count += 1
        if is_generic and not has_binding:
            issues.append(f"{scene_id} visual looks generic and has no source/copy claim binding")
        if not has_binding and visual.get("asset_source_type") in {"support", "generated"}:
            warnings.append(f"{scene_id} support/generated visual should carry explicit claim_ids or proof_chain")
        if visual_job and new_job and similarity(visual_job, new_job) == 0 and not has_binding:
            issues.append(f"{scene_id} visual_job is not semantically tied to the scene copy")

        duration = scene_duration_seconds(scene)
        motion_count = scene_motion_count(scene)
        required_motion_count = max(1, math.ceil(duration / 5.0)) if duration > 0 else 1
        if motion_count >= required_motion_count:
            dynamic_scene_count += 1
        else:
            static_scene_count += 1
            issues.append(
                f"{scene_id} has {motion_count} visual beat/motion cue(s) for {duration:.2f}s; "
                f"needs at least {required_motion_count} to avoid static-page narration"
            )

        sfx_count = scene_sfx_count(scene)
        if sfx_count:
            sfx_scene_count += 1
        elif sfx_required:
            missing_sfx_scene_count += 1
            issues.append(f"{scene_id} missing sfx_cues/audio_cues for the planned dynamic transition")
    return issues, warnings, {
        "scene_count": len(scenes),
        "scene_alignment_count": aligned,
        "generic_visual_count": generic_count,
        "dynamic_scene_count": dynamic_scene_count,
        "static_scene_count": static_scene_count,
        "sfx_scene_count": sfx_scene_count,
        "missing_sfx_scene_count": missing_sfx_scene_count,
    }


def build_report(
    copy_text: str = "",
    copy_json: dict[str, Any] | None = None,
    storyboard: dict[str, Any] | None = None,
) -> dict[str, Any]:
    copy_json = copy_json or {}
    blocking_issues: list[str] = []
    warnings: list[str] = []

    source_issues, source_warnings, source_signals = source_claim_issues(copy_json)
    progression_issues, progression_warnings, progression_signals = copy_progression_issues(copy_json, storyboard)
    known_claim_ids = {item["claim_id"] for item in claim_records(copy_json)}
    visual_issues, visual_warnings, visual_signals = visual_alignment_issues(storyboard, known_claim_ids)
    language_issues, language_signals = chinese_first_issues(copy_json, storyboard)

    blocking_issues.extend(source_issues)
    blocking_issues.extend(progression_issues)
    blocking_issues.extend(visual_issues)
    blocking_issues.extend(language_issues)
    warnings.extend(source_warnings)
    warnings.extend(progression_warnings)
    warnings.extend(visual_warnings)

    return {
        "status": "passed" if not blocking_issues else "failed",
        "checks": {
            "source_claim_alignment": "passed" if not source_issues else "failed",
            "copy_progression": "passed" if not progression_issues else "failed",
            "visual_alignment": "passed" if not visual_issues else "failed",
            "visual_rhythm": "passed" if not any("static-page narration" in issue for issue in visual_issues) else "failed",
            "sfx_cues": "passed" if not any("missing sfx_cues" in issue for issue in visual_issues) else "failed",
            "chinese_first_text": "passed" if not language_issues else "failed",
        },
        "blocking_issues": blocking_issues,
        "warnings": warnings,
        "signals": {
            **source_signals,
            **progression_signals,
            **visual_signals,
            **language_signals,
            "copy_text_chars": len(copy_text),
        },
    }


def review_copy_package_alignment(text: str, copy_json: dict[str, Any]) -> dict[str, Any]:
    report = build_report(copy_text=text, copy_json=copy_json, storyboard=None)
    report["warnings"] = [
        warning
        for warning in report.get("warnings", [])
        if "storyboard is unavailable" not in warning
    ]
    return report


def review_storyboard_alignment(storyboard: dict[str, Any]) -> dict[str, Any]:
    return build_report(copy_text="", copy_json={}, storyboard=storyboard)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check source-copy-visual alignment for AI video packages.")
    parser.add_argument("--copy", help="copy_package.md path")
    parser.add_argument("--copy-json", help="copy_package.json path")
    parser.add_argument("--storyboard", help="storyboard.json path")
    parser.add_argument("--out", help="content_alignment_report.json path")
    args = parser.parse_args()

    copy_path = Path(args.copy) if args.copy else None
    copy_text = copy_path.read_text(encoding="utf-8") if copy_path and copy_path.exists() else ""
    copy_json = load_json(Path(args.copy_json) if args.copy_json else None)
    storyboard = load_json(Path(args.storyboard) if args.storyboard else None)
    report = build_report(copy_text=copy_text, copy_json=copy_json, storyboard=storyboard)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
