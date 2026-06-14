#!/usr/bin/env python3
"""Heuristically score a Chinese Douyin copy package."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


BAD_OPENINGS = ["今天给大家介绍", "AI 时代来了", "你知道吗", "很多人不知道", "这个工具太强"]
FORBIDDEN = ["必火", "保证涨粉", "100%", "用了就能赚钱", "全网最强", "排名第一", "行业第一", "唯一方法", "评论区打 1"]
EMPTY_PHRASES = ["提升效率", "很方便", "很强", "赋能", "降本增效", "快速变现", "颠覆", "神器"]
PROOF_TERMS = ["截图", "演示", "证据", "真实", "对比", "录屏", "输出", "命令", "文件", "官方文档"]
SAVE_TERMS = ["收藏", "模板", "清单", "步骤", "判断标准", "直接套", "公式", "流程"]
HOOK_TERMS = ["不是", "别", "先看", "为什么", "少了", "错误", "结果", "对比", "空话"]
TARGET_TERMS = ["新手", "小白", "普通人", "创作者", "剪辑", "运营", "程序员", "老板", "店主", "你用", "你做"]
BEFORE_AFTER_TERMS = ["before_after", "前后对比", "before", "after", "左边", "右边", "改前", "改后", "错误做法", "正确做法"]
JARGON_TERMS = ["Agent", "RAG", "API", "workflow", "embedding", "token", "MCP", "function calling"]
EXPLAIN_TERMS = ["也就是", "简单说", "意思是", "你可以理解为", "换句话说"]
RETENTION_TERMS = ["retention", "beat", "前后对比", "结果揭示", "错误纠正", "证明墙", "真实界面", "模板"]


def count_sentences(text: str) -> list[str]:
    cleaned_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("|"):
            continue
        cleaned_lines.append(stripped)
    return [item.strip() for item in re.split(r"[。！？\n]", "\n".join(cleaned_lines)) if item.strip()]


def first_section(text: str, limit: int = 160) -> str:
    compact = re.sub(r"\s+", "", text)
    return compact[:limit]


def score(text: str) -> dict[str, object]:
    issues: list[str] = []
    warnings: list[str] = []
    has_hook = "First 5 Seconds" in text or "前 5" in text or "Hook" in text
    has_claim_ledger = "Claim Ledger" in text or "claim ledger" in text.lower()
    has_save = any(term in text for term in SAVE_TERMS)
    has_proof = any(term in text for term in PROOF_TERMS)
    has_before_after = any(term in text for term in BEFORE_AFTER_TERMS)
    has_bad_opening = any(term in text for term in BAD_OPENINGS)
    has_forbidden = any(term in text for term in FORBIDDEN)
    sentences = count_sentences(text)
    short_sentences = len(sentences) >= 8 and max([len(sentence) for sentence in sentences] or [0]) <= 55
    first_3 = first_section(text, 90)
    first_5_text = first_section(text, 160)
    first_3_strong = any(term in first_3 for term in HOOK_TERMS) and not has_bad_opening
    first_5_specific = any(term in first_5_text for term in ["ChatGPT", "Codex", "AI", "提示词", "视频", "文案", "工具", "镜头"])
    first_5_has_target = any(term in first_5_text for term in TARGET_TERMS)
    retention_count = sum(text.count(term) for term in RETENTION_TERMS)
    has_retention_beats = "retention_beats" in text or "Retention Beats" in text or "Retention Beats" in text or retention_count >= 2
    empty_talk_ratio = sum(text.count(term) for term in EMPTY_PHRASES) / max(1, len(sentences))
    unexplained_jargon = [
        term for term in JARGON_TERMS if term in text and not any(explain in text for explain in EXPLAIN_TERMS)
    ]
    terminology_explained = not unexplained_jargon
    suitable_for_voice = short_sentences
    has_proof_visual_plan = "proof_visual_plan" in text or "Proof Visual" in text or "证据画面" in text or has_proof

    first_3_score = 9.4 if first_3_strong else 6.4
    first_5 = 9.2 if has_hook and first_3_strong and first_5_specific and first_5_has_target else 6.5
    clarity = 8.5 if short_sentences else 7.0
    specificity = 8.6 if has_proof and first_5_specific else 7.0
    save_value = 8.6 if has_save else 6.8
    proof = 8.5 if has_proof else 6.5
    rhythm = 8.6 if short_sentences and has_retention_beats else 7.0
    compliance = 9.6 if not has_forbidden else 5.0
    if empty_talk_ratio > 0.18:
        specificity -= 1.2
        warnings.append("empty talk ratio is high; replace broad claims with proof")
    if unexplained_jargon:
        clarity -= 1.0
        warnings.append("jargon needs beginner explanation: " + ", ".join(unexplained_jargon))
    if not first_3_strong:
        issues.append("first 3 seconds need a clear pain, result, or counterintuitive claim")
    if not first_5_specific:
        issues.append("first 5 seconds need a concrete object, not generic AI talk")
    if not first_5_has_target:
        issues.append("first 5 seconds need a clear target viewer")
    if not has_retention_beats:
        issues.append("retention beats are missing or too weak")
    if not has_save:
        issues.append("save value needs a reusable template, checklist, workflow, or rule")
    if not has_before_after:
        issues.append("before/after plan is missing")
    if not has_proof:
        issues.append("script needs real proof visuals such as UI, output, command, file, or comparison")
    if not terminology_explained:
        issues.append("technical terminology must be explained for beginners")
    if not suitable_for_voice:
        issues.append("sentences are too long or too few for natural voiceover")
    if has_forbidden:
        issues.append("copy contains forbidden or overpromising language")

    script_score = round((first_3_score + first_5 + clarity + specificity + save_value + proof + rhythm + compliance) / 8, 2)

    return {
        "first_3_seconds_score": round(first_3_score, 2),
        "first_5_seconds_score": round(first_5, 2),
        "clarity_score": round(clarity, 2),
        "specificity_score": round(specificity, 2),
        "save_value_score": round(save_value, 2),
        "proof_score": round(proof, 2),
        "rhythm_score": round(rhythm, 2),
        "compliance_score": round(compliance, 2),
        "script_score": script_score,
        "claim_ledger_present": bool(has_claim_ledger),
        "retention_beats_present": bool(has_retention_beats),
        "before_after_present": bool(has_before_after),
        "terminology_explained": bool(terminology_explained),
        "proof_visual_plan_present": bool(has_proof_visual_plan),
        "suitable_for_voiceover": bool(suitable_for_voice),
        "empty_talk_ratio": round(empty_talk_ratio, 3),
        "issues": issues,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a copy package before storyboard.")
    parser.add_argument("--copy", required=True, help="copy_package.md")
    parser.add_argument("--out", help="Output JSON score report.")
    args = parser.parse_args()

    text = Path(args.copy).read_text(encoding="utf-8")
    result = score(text)
    passed = (
        result["first_3_seconds_score"] >= 9.2
        and result["script_score"] >= 8.5
        and result["first_5_seconds_score"] >= 9
        and result["save_value_score"] >= 8.5
        and result["proof_score"] >= 8.5
        and result["compliance_score"] >= 9.5
        and result["empty_talk_ratio"] <= 0.18
        and not result["issues"]
    )
    result["status"] = "passed" if passed else "failed"
    if args.out:
        Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
