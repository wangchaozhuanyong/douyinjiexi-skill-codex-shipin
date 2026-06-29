#!/usr/bin/env python3
"""Semantic review for Douyin copy packages.

This is intentionally deterministic: it judges whether a copy package has a
real conflict, usable information, proof grounding, and a human spoken rhythm
before the expensive video steps begin.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Optional

from check_content_alignment import review_copy_package_alignment


BAD_OPENINGS = ["今天给大家介绍", "AI 时代来了", "你知道吗", "很多人不知道", "这个工具太强"]
FORBIDDEN = ["必火", "保证涨粉", "用了就能赚钱", "全网最强", "排名第一", "行业第一", "唯一方法"]
CONFLICT_TERMS = ["别", "不是", "问题", "错误", "误区", "少了", "对比", "为什么", "结果"]
TARGET_TERMS = ["创作者", "运营", "老板", "新手", "小白", "店主", "程序员", "剪辑", "普通人", "你"]
SCENARIO_TERMS = ["投流", "汇报", "写文案", "做视频", "教程", "发布前", "测试", "演示", "使用场景"]
PROOF_TERMS = ["截图", "录屏", "真实", "输出", "文件", "命令", "官方文档", "对比", "证据", "UI"]
REUSE_TERMS = ["模板", "清单", "公式", "步骤", "流程", "判断标准", "直接套", "复用"]
REPORTY_TERMS = ["综上所述", "本文", "我们可以发现", "本期内容主要", "赋能", "降本增效"]


def load_json(path: Optional[Path]) -> dict[str, Any]:
    if not path or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def sentences(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("|"):
            continue
        lines.append(stripped)
    return [part.strip() for part in re.split(r"[。！？\n]", "\n".join(lines)) if part.strip()]


def count_terms(text: str, terms: list[str]) -> int:
    return sum(text.count(term) for term in terms)


def section_value(copy_json: dict[str, Any], key: str) -> str:
    value = copy_json.get(key)
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False) if value is not None else ""


def score_copy(text: str, copy_json: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    suggestions: list[str] = []
    sent = sentences(text)
    first_160 = re.sub(r"\s+", "", text)[:160]

    has_conflict = count_terms(first_160, CONFLICT_TERMS) >= 2 and not any(term in first_160 for term in BAD_OPENINGS)
    has_target = count_terms(text, TARGET_TERMS) >= 1
    has_scenario = count_terms(text, SCENARIO_TERMS) >= 1
    has_proof = count_terms(text + section_value(copy_json, "proof_visual_plan"), PROOF_TERMS) >= 2
    has_reuse = count_terms(text + section_value(copy_json, "before_after_plan"), REUSE_TERMS) >= 2
    has_before_after = "前后对比" in text or "before_after" in text or copy_json.get("before_after_plan")
    retention_beats = copy_json.get("retention_beats") if isinstance(copy_json.get("retention_beats"), list) else []
    avg_len = sum(len(item) for item in sent) / max(1, len(sent))
    long_sentences = [item for item in sent if len(item) > 58]
    reporty_count = count_terms(text, REPORTY_TERMS)
    forbidden_count = count_terms(text, FORBIDDEN)

    hook_conflict_score = 9.4 if has_conflict else 6.6
    specificity_score = 8.8 if has_target and has_scenario else 7.0
    reuse_value_score = 8.8 if has_reuse and retention_beats else 7.0
    human_voice_score = 8.8 if sent and avg_len <= 38 and len(long_sentences) <= 1 and reporty_count == 0 else 7.1
    information_gain_score = 8.7 if has_before_after and has_target and has_scenario and has_reuse else 7.2
    proof_grounding_score = 8.8 if has_proof else 6.8
    compliance_safety_score = 9.6 if forbidden_count == 0 else 5.0
    alignment_review = review_copy_package_alignment(text, copy_json)
    alignment_issues = alignment_review.get("blocking_issues", [])
    alignment_warnings = alignment_review.get("warnings", [])
    content_alignment_score = 8.9 if not alignment_issues else 6.2

    if not has_conflict:
        issues.append("opening lacks a real conflict, correction, or result contrast")
        suggestions.append("Rewrite the first 3 seconds around a concrete wrong method and visible result.")
    if not has_target:
        issues.append("target viewer is not concrete enough")
        suggestions.append("Name the exact viewer, such as creators, operators, founders, or beginner users.")
    if not has_scenario:
        issues.append("usage scenario is not concrete enough")
        suggestions.append("Tie the method to a specific production moment, such as pre-publish QA or prompt testing.")
    if not has_proof:
        issues.append("copy is not grounded in enough proof visuals")
        suggestions.append("Add real UI, output, file, command, official-doc, or before/after proof.")
    if not has_reuse:
        issues.append("save value is weak")
        suggestions.append("Add a reusable formula, checklist, workflow, or decision rule.")
    if not retention_beats:
        issues.append("retention beats are missing from copy_package.json")
        suggestions.append("Add timed retention beats with line and visual fields.")
    if long_sentences:
        suggestions.append("Split long voiceover sentences so each line can be spoken naturally.")
    if reporty_count:
        suggestions.append("Replace report-style language with spoken, visual, action-oriented sentences.")
    if forbidden_count:
        issues.append("copy contains forbidden overpromising or absolute wording")
    if alignment_issues:
        issues.extend(alignment_issues)
        suggestions.append("Rewrite copy with a source-backed content_alignment_map and one new information job per scene.")
    if alignment_warnings:
        suggestions.extend(alignment_warnings)

    scores = {
        "hook_conflict_score": round(hook_conflict_score, 2),
        "specificity_score": round(specificity_score, 2),
        "reuse_value_score": round(reuse_value_score, 2),
        "human_voice_score": round(human_voice_score, 2),
        "information_gain_score": round(information_gain_score, 2),
        "proof_grounding_score": round(proof_grounding_score, 2),
        "compliance_safety_score": round(compliance_safety_score, 2),
        "content_alignment_score": round(content_alignment_score, 2),
    }
    composite = round(sum(scores.values()) / len(scores), 2)
    hard_fail_reasons = issues if composite < 8.5 or forbidden_count or alignment_issues else []
    return {
        "status": "passed" if not hard_fail_reasons else "failed",
        "composite_score": composite,
        "scores": scores,
        "hard_fail_reasons": hard_fail_reasons,
        "revision_suggestions": suggestions,
        "signals": {
            "sentence_count": len(sent),
            "average_sentence_length": round(avg_len, 1),
            "retention_beat_count": len(retention_beats),
            "has_before_after": bool(has_before_after),
            "has_proof_visual_plan": bool(has_proof),
            "has_reusable_takeaway": bool(has_reuse),
            "content_alignment": alignment_review.get("signals", {}),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic semantic review for copy packages.")
    parser.add_argument("--copy", required=True, help="copy_package.md path")
    parser.add_argument("--copy-json", help="Optional copy_package.json path")
    parser.add_argument("--out", help="semantic_review.json path")
    args = parser.parse_args()

    copy_path = Path(args.copy)
    copy_json_path = Path(args.copy_json) if args.copy_json else None
    result = score_copy(copy_path.read_text(encoding="utf-8"), load_json(copy_json_path))
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
