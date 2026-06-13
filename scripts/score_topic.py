#!/usr/bin/env python3
"""Score AI-circle topic candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


WEIGHTS = {
    "pain_score": 0.25,
    "novelty_score": 0.15,
    "save_score": 0.25,
    "comment_score": 0.10,
    "visual_score": 0.15,
    "compliance_safety_score": 0.10,
}

CONTENT_FORMATS = {
    "mistake_correction",
    "three_step_tutorial",
    "before_after",
    "news_explain",
    "tool_stack",
    "prompt_template",
    "case_breakdown",
    "myth_busting",
}

REQUIRED_FIELDS = [
    "topic_id",
    "title_direction",
    "core_angle",
    "content_format",
    "format_reason",
    "target_viewer",
    "viewer_pain",
    "why_now",
    "curiosity_gap",
    "save_reason",
    "comment_trigger",
    "visual_potential",
    "proof_assets_needed",
    "main_claims",
    "sources",
    "risk_flags",
]

GENERIC_TOPIC_PATTERNS = [
    "AI 工具推荐",
    "ChatGPT 很强",
    "AI 视频来了",
    "Codex 怎么用",
    "这个工具很好用",
    "AI 很厉害",
]

PROOF_TERMS = ["截图", "录屏", "真实", "UI", "输出", "命令", "文件", "官方", "文档", "结果", "对比"]


def clamp_score(value: Any) -> float:
    try:
        return max(0.0, min(10.0, float(value)))
    except Exception:
        return 0.0


def candidates_from(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict) and isinstance(data.get("candidates"), list):
        return data["candidates"]
    if isinstance(data, list):
        return data
    raise ValueError("Input must be a list or an object with candidates.")


def score_candidate(candidate: dict[str, Any]) -> float:
    scores = candidate.setdefault("scores", {})
    total = 0.0
    for key, weight in WEIGHTS.items():
        total += clamp_score(scores.get(key)) * weight
    validation = validate_candidate(candidate)
    penalty = validation["penalty"]
    scores["raw_total_score"] = round(total, 2)
    scores["total_score"] = round(max(0.0, total - penalty), 2)
    candidate["validation_issues"] = validation["issues"]
    candidate["quality_warnings"] = validation["warnings"]
    return scores["total_score"]


def is_filled(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value)
    if isinstance(value, dict):
        return bool(value)
    return value is not None


def validate_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []
    penalty = 0.0

    for field in REQUIRED_FIELDS:
        if field == "risk_flags":
            if not isinstance(candidate.get(field), list):
                issues.append("risk_flags must be an array")
                penalty += 1.0
            continue
        if not is_filled(candidate.get(field)):
            issues.append(f"missing or empty {field}")
            penalty += 1.0

    content_format = candidate.get("content_format")
    if content_format not in CONTENT_FORMATS:
        issues.append("content_format must be one of the supported V3 formats")
        penalty += 1.0

    title = str(candidate.get("title_direction", ""))
    core_angle = str(candidate.get("core_angle", ""))
    if any(pattern in title or pattern in core_angle for pattern in GENERIC_TOPIC_PATTERNS):
        issues.append("generic topic direction needs a sharper pain, proof, or format")
        penalty += 1.5

    sources = candidate.get("sources") or []
    if not isinstance(sources, list) or not sources:
        issues.append("sources must contain at least one source")
        penalty += 1.0
    else:
        for idx, source in enumerate(sources, start=1):
            for key in ["title", "url_or_note", "date", "claim_supported"]:
                if not str(source.get(key, "")).strip():
                    issues.append(f"source {idx} missing {key}")
                    penalty += 0.4

    proof_assets = candidate.get("proof_assets_needed") or []
    proof_blob = " ".join(str(item) for item in proof_assets)
    if not proof_assets:
        issues.append("proof_assets_needed must name concrete proof assets")
        penalty += 1.0
    elif not any(term in proof_blob for term in PROOF_TERMS):
        warnings.append("proof assets may be too abstract; name screenshots, recordings, outputs, files, or docs")
        penalty += 0.5

    if content_format == "news_explain":
        dated_sources = [source for source in sources if str(source.get("date", "")).strip()]
        if not dated_sources:
            issues.append("news_explain topics require dated sources")
            penalty += 1.0

    if any(term in title + core_angle for term in ["教程", "工具", "ChatGPT", "Codex", "Agent", "AI 视频"]):
        if not any(term in proof_blob for term in ["真实", "UI", "截图", "录屏", "输出", "命令", "文件", "文档"]):
            issues.append("AI tool/tutorial topics require real UI, output, command, file, or official-doc proof")
            penalty += 1.0

    return {"issues": issues, "warnings": warnings, "penalty": penalty}


def main() -> int:
    parser = argparse.ArgumentParser(description="Score topic candidates and enforce minimum threshold.")
    parser.add_argument("--input", required=True, help="topic_candidates.json")
    parser.add_argument("--out", help="Output path. Defaults to overwriting --input.")
    parser.add_argument("--min-score", type=float, default=8.0)
    args = parser.parse_args()

    path = Path(args.input)
    data = json.loads(path.read_text(encoding="utf-8"))
    candidates = candidates_from(data)
    for candidate in candidates:
        score_candidate(candidate)
    eligible = [item for item in candidates if item.get("scores", {}).get("total_score", 0) >= args.min_score]
    result = data if isinstance(data, dict) else {"candidates": candidates}
    result["eligible_topic_ids"] = [item.get("topic_id") for item in eligible]
    result["status"] = "passed" if eligible and all(not item.get("validation_issues") for item in eligible) else "failed"
    result["blocking_issues"] = [
        f"{item.get('topic_id', 'unknown')}: {issue}"
        for item in candidates
        for issue in item.get("validation_issues", [])
    ]

    out = Path(args.out) if args.out else path
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "eligible_topic_ids": result["eligible_topic_ids"]}, ensure_ascii=False))
    return 0 if eligible else 1


if __name__ == "__main__":
    raise SystemExit(main())
