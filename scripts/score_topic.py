#!/usr/bin/env python3
"""Score AI-circle topic candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Optional


LEGACY_WEIGHTS = {
    "pain_score": 0.25,
    "novelty_score": 0.15,
    "save_score": 0.25,
    "comment_score": 0.10,
    "visual_score": 0.15,
    "compliance_safety_score": 0.10,
}

BEGINNER_WEIGHTS = {
    "beginner_usefulness_score": 0.30,
    "visible_result_score": 0.20,
    "time_saving_score": 0.15,
    "pain_score": 0.15,
    "novelty_score": 0.10,
    "visual_score": 0.07,
    "compliance_safety_score": 0.03,
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

BEGINNER_FIELDS = [
    "beginner_task",
    "visible_result",
    "first_action",
    "time_saving_claim",
]

GENERIC_TOPIC_PATTERNS = [
    "AI 工具推荐",
    "ChatGPT 教程",
    "ChatGPT 很强",
    "AI 视频来了",
    "Codex 怎么用",
    "这个工具很好用",
    "AI 很厉害",
]

PROOF_TERMS = ["截图", "录屏", "真实", "UI", "输出", "命令", "文件", "官方", "文档", "结果", "对比"]
ABSTRACT_VISUAL_TERMS = ["赛博", "机器人", "光效", "科技背景", "抽象", "未来感", "粒子"]
WORKED_TERMS = ["真实", "截图", "对比", "模板", "清单", "错误纠正", "证明", "保存"]
FIX_TERMS = ["空话", "太静", "太暗", "字幕挡", "低清晰度", "抽象背景", "单图"]
TOPIC_OBJECT_TERMS = [
    "AI",
    "ChatGPT",
    "Codex",
    "Gemini",
    "OpenAI",
    "Google",
    "Claude",
    "Anthropic",
    "Grok",
    "xAI",
    "Veo",
    "Sora",
    "Agent",
    "插件",
    "模型",
    "网站",
    "工具",
    "软件",
    "应用",
    "平台",
]
TOPIC_EVENT_TERMS = [
    "新增",
    "更新",
    "发布",
    "上线",
    "推出",
    "开放",
    "加入",
    "支持",
    "升级",
    "改版",
    "变化",
    "新闻",
    "消息",
    "报告",
    "测试",
    "对比",
    "官方",
    "文档",
    "指南",
    "功能",
    "Release",
    "release",
    "changelog",
]
METHOD_ONLY_TITLE_PATTERNS = [
    "前先写",
    "三步",
    "技巧",
    "方法",
    "工作流",
    "清单",
]


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


def learning_bank_signals(text: str) -> dict[str, list[str]]:
    return {
        "worked_terms": sorted({term for term in WORKED_TERMS if term in text}),
        "fix_terms": sorted({term for term in FIX_TERMS if term in text}),
    }


def learning_bank_adjustment(candidate: dict[str, Any], signals: dict[str, list[str]]) -> tuple[float, list[str]]:
    blob = json.dumps(candidate, ensure_ascii=False)
    delta = 0.0
    reasons: list[str] = []
    if any(term in blob for term in signals.get("worked_terms", [])):
        delta += 0.2
        reasons.append("matches learning-bank worked terms")
    if "真实" in signals.get("worked_terms", []) and any(term in blob for term in ["截图", "录屏", "输出", "文件", "UI"]):
        delta += 0.2
        reasons.append("uses evidence assets favored by learning bank")
    if "抽象背景" in signals.get("fix_terms", []) and any(term in blob for term in ABSTRACT_VISUAL_TERMS):
        delta -= 0.35
        reasons.append("matches weak abstract-visual pattern")
    if "空话" in signals.get("fix_terms", []) and any(term in blob for term in ["提升效率", "很强", "神器"]):
        delta -= 0.35
        reasons.append("matches repeated empty-talk failure")
    return round(max(-0.8, min(0.8, delta)), 2), reasons


def score_candidate(candidate: dict[str, Any], learning_signals: Optional[dict[str, list[str]]] = None) -> float:
    scores = candidate.setdefault("scores", {})
    weights = BEGINNER_WEIGHTS if all(key in scores for key in BEGINNER_WEIGHTS) else LEGACY_WEIGHTS
    total = 0.0
    for key, weight in weights.items():
        total += clamp_score(scores.get(key)) * weight
    validation = validate_candidate(candidate)
    penalty = validation["penalty"]
    learning_delta = 0.0
    learning_reasons: list[str] = []
    if learning_signals:
        learning_delta, learning_reasons = learning_bank_adjustment(candidate, learning_signals)
    scores["raw_total_score"] = round(total, 2)
    scores["score_model"] = "beginner_task_weighted" if weights is BEGINNER_WEIGHTS else "legacy_topic_weighted"
    scores["total_score"] = round(max(0.0, min(10.0, total - penalty + learning_delta)), 2)
    candidate["learning_bank_adjustment"] = {
        "score_delta": learning_delta,
        "reasons": learning_reasons,
    }
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
    has_topic_object = any(term in title for term in TOPIC_OBJECT_TERMS)
    has_topic_event = any(term in title for term in TOPIC_EVENT_TERMS)
    if not has_topic_object:
        issues.append("topic title must name a concrete AI object/source such as software, website, company, model, feature, release, or news source")
        penalty += 1.0
    if not has_topic_event:
        issues.append("topic title must name a concrete event/feature/news/official source before the practical takeaway")
        penalty += 1.0
    if any(pattern in title for pattern in METHOD_ONLY_TITLE_PATTERNS) and not has_topic_event:
        issues.append("method-only topic title is not allowed; lead with object/source + event/feature/news")
        penalty += 1.2

    for field in ["target_viewer", "viewer_pain", "why_now", "save_reason", "comment_trigger", "visual_potential"]:
        value = str(candidate.get(field, "")).strip()
        if len(value) < 8:
            issues.append(f"{field} is too generic")
            penalty += 0.5

    missing_beginner_fields = [field for field in BEGINNER_FIELDS if not str(candidate.get(field, "")).strip()]
    if missing_beginner_fields:
        warnings.append("beginner task fields missing: " + ", ".join(missing_beginner_fields))
        penalty += 0.3
    else:
        beginner_blob = " ".join(str(candidate.get(field, "")) for field in BEGINNER_FIELDS)
        if not any(term in beginner_blob for term in ["打开", "复制", "上传", "点击", "填", "输入", "检查", "导出"]):
            issues.append("first_action must describe a concrete beginner action")
            penalty += 0.8
        if not any(term in beginner_blob for term in ["省", "少", "减少", "不用", "分钟", "步骤"]):
            issues.append("time_saving_claim must name the saved step, minute, or repeated action")
            penalty += 0.8

    comment_trigger = str(candidate.get("comment_trigger", ""))
    if any(term in comment_trigger for term in ["评论区打", "点赞", "转发", "私信"]):
        issues.append("comment_trigger must be natural and not engagement-bait")
        penalty += 1.0

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
    visual_potential = str(candidate.get("visual_potential", ""))
    if not proof_assets:
        issues.append("proof_assets_needed must name concrete proof assets")
        penalty += 1.0
    elif not any(term in proof_blob for term in PROOF_TERMS):
        warnings.append("proof assets may be too abstract; name screenshots, recordings, outputs, files, or docs")
        penalty += 0.5
    if any(term in proof_blob + visual_potential for term in ABSTRACT_VISUAL_TERMS) and not any(term in proof_blob for term in PROOF_TERMS):
        issues.append("topic cannot rely only on abstract AI visuals")
        penalty += 1.0

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
    parser.add_argument("--learning-bank", help="Optional learning_bank.md path for score feedback.")
    args = parser.parse_args()

    path = Path(args.input)
    data = json.loads(path.read_text(encoding="utf-8"))
    candidates = candidates_from(data)
    learning_signals = None
    if args.learning_bank:
        bank_path = Path(args.learning_bank)
        learning_signals = learning_bank_signals(bank_path.read_text(encoding="utf-8") if bank_path.exists() else "")
    for candidate in candidates:
        score_candidate(candidate, learning_signals)
    eligible = [item for item in candidates if item.get("scores", {}).get("total_score", 0) >= args.min_score]
    result = data if isinstance(data, dict) else {"candidates": candidates}
    result["eligible_topic_ids"] = [item.get("topic_id") for item in eligible]
    if learning_signals:
        result["learning_bank_applied"] = learning_signals
    result["status"] = "passed" if eligible and all(not item.get("validation_issues") for item in eligible) else "failed"
    result["blocking_issues"] = [
        f"{item.get('topic_id', 'unknown')}: {issue}"
        for item in candidates
        for issue in item.get("validation_issues", [])
    ]

    out = Path(args.out) if args.out else path
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "eligible_topic_ids": result["eligible_topic_ids"]}, ensure_ascii=False))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
