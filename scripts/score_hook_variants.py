#!/usr/bin/env python3
"""Score hook variants and select the strongest one."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


AI_OBJECT_TERMS = ["codex", "chatgpt", "gemini", "openai", "claude", "agent", "ai", "工具", "插件", "skill"]
PAIN_TERMS = ["别再", "跑偏", "重试", "返工", "缺", "不是", "检查"]
RESULT_TERMS = ["结果", "输出", "流程", "检查表", "验收", "证明", "省掉", "稳定"]
PROOF_TERMS = ["证据", "证明", "检查", "验收", "来源", "文件", "步骤"]
HYPE_TERMS = ["神级", "逆天", "秒杀", "全网", "必看", "炸裂", "保姆级"]


def has_any(text: str, terms: list[str]) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def spoken_rhythm_score(line: str) -> float:
    length = len(line)
    if 18 <= length <= 42:
        return 1.0
    if 12 <= length <= 52:
        return 0.7
    return 0.3


def score_variant(variant: dict[str, Any]) -> dict[str, Any]:
    line = str(variant.get("first_3_seconds_line", ""))
    score = 0.0
    details: dict[str, float] = {}
    details["concrete_ai_object"] = 1.5 if has_any(line, AI_OBJECT_TERMS) else 0.0
    details["viewer_pain"] = 1.5 if has_any(line + str(variant.get("viewer_pain", "")), PAIN_TERMS) else 0.0
    details["visible_result"] = 1.5 if has_any(line + str(variant.get("visible_result", "")), RESULT_TERMS) else 0.0
    details["proof_hint"] = 1.2 if has_any(line + str(variant.get("proof_hint", "")), PROOF_TERMS) else 0.0
    details["save_value"] = 1.0 if str(variant.get("save_reason", "")).strip() else 0.0
    details["spoken_rhythm"] = spoken_rhythm_score(line)
    details["low_hype"] = 0.0 if has_any(line, HYPE_TERMS) else 1.3
    score = round(sum(details.values()), 2)
    return {
        "hook_id": variant.get("hook_id"),
        "score": score,
        "line": line,
        "details": details,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score hook variants.")
    parser.add_argument("--hooks", required=True, help="hook_variants.json")
    parser.add_argument("--out", required=True, help="hook_score_report.json")
    args = parser.parse_args()

    data = json.loads(Path(args.hooks).read_text(encoding="utf-8"))
    variants = data.get("variants", [])
    scores = [score_variant(variant) for variant in variants if isinstance(variant, dict)]
    scores.sort(key=lambda item: (-float(item["score"]), str(item["hook_id"])))
    selected = scores[0] if scores else {}
    issues: list[str] = []
    if len(scores) < 10:
        issues.append("hook_variants.json must include at least 10 variants")
    if float(selected.get("score", 0.0)) < 8.5:
        issues.append("selected hook score must be >= 8.5")
    report = {
        "status": "passed" if not issues else "failed",
        "variant_count": len(scores),
        "top_score": selected.get("score", 0.0),
        "selected_hook": selected,
        "scores": scores,
        "blocking_issues": issues,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "top_score": report["top_score"]}, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
