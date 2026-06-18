#!/usr/bin/env python3
"""Review copy from a beginner viewer's point of view."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Optional


TARGET_TERMS = ["小白", "新手", "普通人", "创作者", "运营", "老板", "店主", "学生", "上班族", "你"]
TASK_TERMS = [
    "写文案",
    "写周报",
    "整理资料",
    "做视频",
    "做封面",
    "做 PPT",
    "做表格",
    "写标题",
    "客服回复",
    "简历",
    "报告",
    "口播",
    "提示词",
]
ACTION_TERMS = ["打开", "复制", "粘贴", "上传", "选择", "点击", "填", "输入", "检查", "导出", "保存", "发"]
RESULT_TERMS = ["结果", "可见", "前后对比", "左边", "右边", "改前", "改后", "能发", "直接用", "变成", "输出"]
PAIN_TERMS = ["不会", "卡", "空话", "套话", "乱", "浪费", "反复改", "手动", "错误", "别再", "不知道"]
PROOF_TERMS = ["截图", "录屏", "真实", "UI", "输出", "文件", "命令", "对比", "演示", "证据"]
SAVE_TERMS = ["模板", "清单", "公式", "步骤", "判断标准", "直接套", "收藏", "流程"]
TIME_SAVING_TERMS = ["省", "少", "减少", "压到", "不用", "不再", "少复制", "少改", "重复步骤", "分钟"]
EXAMPLE_TERMS = ["比如", "例如", "举例", "像", "假设", "场景", "同一句", "这段", "一段", "产品介绍", "周报", "标题"]
JARGON_TERMS = ["Agent", "RAG", "API", "workflow", "embedding", "token", "MCP", "function calling", "多模态", "长上下文"]
EXPLAIN_TERMS = ["也就是", "简单说", "意思是", "你可以理解为", "换句话说", "翻译成"]


def load_json(path: Optional[Path]) -> dict[str, Any]:
    if not path or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def section_value(copy_json: dict[str, Any], key: str) -> str:
    value = copy_json.get(key)
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def list_strings(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def title_blob(text: str, copy_json: dict[str, Any]) -> str:
    titles = list_strings(copy_json.get("title_options"))
    if titles:
        return "\n".join(titles)
    lines = []
    in_title = False
    for raw in text.splitlines():
        line = raw.strip()
        if re.search(r"title|标题", line, flags=re.IGNORECASE):
            in_title = True
            continue
        if in_title and line.startswith("#"):
            break
        if in_title and line:
            lines.append(line)
    return "\n".join(lines) if lines else text[:260]


def first_5_blob(text: str, copy_json: dict[str, Any]) -> str:
    first_5 = copy_json.get("first_5_seconds_hook")
    if isinstance(first_5, dict):
        return section_value(first_5, "line") + section_value(first_5, "visual_changes")
    hooks = copy_json.get("first_5_seconds_hooks")
    if isinstance(hooks, list):
        return json.dumps(hooks, ensure_ascii=False)
    first_160 = compact(text)[:180]
    return first_160


def has_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def count_terms(text: str, terms: list[str]) -> int:
    return sum(text.count(term) for term in terms)


def score_from_hits(base: float, hits: int, step: float = 0.8, cap: float = 9.6) -> float:
    return round(min(cap, base + hits * step), 2)


def score_title(text: str, copy_json: dict[str, Any]) -> float:
    blob = title_blob(text, copy_json)
    hits = int(has_any(blob, TARGET_TERMS)) + int(has_any(blob, TASK_TERMS + ACTION_TERMS)) + int(has_any(blob, RESULT_TERMS))
    if hits == 3:
        return 9.4
    if hits == 2:
        return 8.4
    if hits == 1:
        return 7.2
    return 6.4


def score_first_5(text: str, copy_json: dict[str, Any]) -> float:
    blob = first_5_blob(text, copy_json)
    hits = int(has_any(blob, PAIN_TERMS)) + int(has_any(blob, RESULT_TERMS)) + int(has_any(blob, ["步骤", "三步", "演示", "我给你看"] + ACTION_TERMS))
    if hits == 3:
        return 9.5
    if hits == 2:
        return 8.4
    if hits == 1:
        return 7.0
    return 6.2


def score_task_fit(text: str, copy_json: dict[str, Any]) -> float:
    card = copy_json.get("beginner_task_card")
    filled = 0
    if isinstance(card, dict):
        for key in ["target_viewer", "task", "visible_result", "why_watch_now", "first_action"]:
            filled += int(bool(str(card.get(key, "")).strip()))
    blob = json.dumps(card, ensure_ascii=False) if isinstance(card, dict) else text
    hits = int(has_any(blob, TARGET_TERMS)) + int(has_any(blob, TASK_TERMS)) + int(has_any(blob, PAIN_TERMS + RESULT_TERMS))
    if filled >= 5:
        return 9.5
    if filled >= 3 or hits == 3:
        return 8.8
    if hits >= 2:
        return 7.8
    return 6.5


def score_visible_result(text: str, copy_json: dict[str, Any]) -> float:
    blob = text + section_value(copy_json, "proof_visual_plan") + section_value(copy_json, "before_after_plan")
    hits = int(has_any(blob, RESULT_TERMS)) + int(has_any(blob, PROOF_TERMS)) + int(has_any(blob, ["先展示", "先看", "第一屏"]))
    if hits >= 3:
        return 9.3
    if hits == 2:
        return 8.6
    if hits == 1:
        return 7.0
    return 6.2


def score_steps(text: str, copy_json: dict[str, Any]) -> float:
    blob = text + section_value(copy_json, "full_voiceover")
    step_hits = count_terms(blob, ["第一步", "第二步", "第三步", "步骤", "先", "再", "最后"])
    action_hits = count_terms(blob, ACTION_TERMS)
    if step_hits >= 3 and action_hits >= 4:
        return 9.4
    if step_hits >= 2 and action_hits >= 2:
        return 8.6
    if step_hits >= 1 or action_hits >= 2:
        return 7.2
    return 6.0


def score_time_saving(text: str, copy_json: dict[str, Any]) -> float:
    blob = text + section_value(copy_json, "beginner_task_card")
    hits = count_terms(blob, TIME_SAVING_TERMS)
    if hits >= 3 and re.search(r"\d+\s*(分钟|次|步)", blob):
        return 9.2
    if hits >= 2:
        return 8.5
    if hits == 1:
        return 7.2
    return 6.0


def score_problem_examples(text: str, copy_json: dict[str, Any]) -> float:
    blob = text + section_value(copy_json, "problem_examples") + section_value(copy_json, "beginner_task_card")
    pain_hits = count_terms(blob, PAIN_TERMS)
    example_hits = count_terms(blob, EXAMPLE_TERMS)
    before_after_example = has_any(blob, ["左边", "右边", "改前", "改后", "同一句"])
    if pain_hits == 0:
        return 9.0
    if example_hits >= 3 and before_after_example:
        return 9.4
    if example_hits >= 2:
        return 8.8
    if example_hits == 1:
        return 7.2
    return 6.0


def score_jargon(text: str, copy_json: dict[str, Any]) -> float:
    blob = text + section_value(copy_json, "terminology_explained")
    used = [term for term in JARGON_TERMS if term in blob]
    if not used:
        return 9.2
    explained = [term for term in used if has_any(blob, EXPLAIN_TERMS) or term in section_value(copy_json, "terminology_explained")]
    if len(explained) == len(used):
        return 9.1
    return 6.8


def score_save_asset(text: str, copy_json: dict[str, Any]) -> float:
    blob = text + section_value(copy_json, "save_value")
    hits = count_terms(blob, SAVE_TERMS)
    return score_from_hits(6.4, hits, step=0.7, cap=9.4)


def review(text: str, copy_json: dict[str, Any]) -> dict[str, Any]:
    scores = {
        "title_clarity": score_title(text, copy_json),
        "first_5_seconds_pull": score_first_5(text, copy_json),
        "beginner_task_fit": score_task_fit(text, copy_json),
        "visible_result": score_visible_result(text, copy_json),
        "step_by_step_value": score_steps(text, copy_json),
        "time_saving_claim": score_time_saving(text, copy_json),
        "problem_example_score": score_problem_examples(text, copy_json),
        "jargon_translation": score_jargon(text, copy_json),
        "save_asset": score_save_asset(text, copy_json),
    }
    total = round(sum(scores.values()) / len(scores), 2)
    rewrite_required: list[str] = []
    thresholds = {
        "title_clarity": 9.0,
        "first_5_seconds_pull": 9.0,
        "visible_result": 8.5,
        "step_by_step_value": 8.5,
        "problem_example_score": 8.5,
    }
    for key, minimum in thresholds.items():
        if scores[key] < minimum:
            rewrite_required.append(f"{key} must be >= {minimum}")
    if total < 8.8:
        rewrite_required.append("overall beginner value score must be >= 8.8")
    status = "passed" if not rewrite_required else "failed"
    return {
        "status": status,
        "final_decision": "pass" if status == "passed" else "fail",
        "total_score": total,
        "scores": scores,
        "rewrite_required": rewrite_required,
        "questions": {
            "title_clarity": "小白只看标题，是否知道这条视频教什么？",
            "first_5_seconds_pull": "前 5 秒是否出现痛点、结果或前后对比？",
            "beginner_task_fit": "这条视频是否绑定一个真实任务，而不是泛讲 AI？",
            "visible_result": "视频是否先展示一个可见结果？",
            "step_by_step_value": "小白是否能照着做？",
            "time_saving_claim": "是否具体说明省掉哪一步，而不是空说提升效率？",
            "problem_example_score": "提到问题时，是否给了小白能代入的具体例子？",
            "jargon_translation": "所有术语是否翻译成人话？",
            "save_asset": "是否有模板、清单、流程或判断标准？",
        },
        "signals": {
            "target_terms": count_terms(text, TARGET_TERMS),
            "task_terms": count_terms(text, TASK_TERMS),
            "action_terms": count_terms(text, ACTION_TERMS),
            "proof_terms": count_terms(text, PROOF_TERMS),
            "save_terms": count_terms(text, SAVE_TERMS),
            "time_saving_terms": count_terms(text, TIME_SAVING_TERMS),
            "example_terms": count_terms(text, EXAMPLE_TERMS),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Review a copy package for beginner viewer value.")
    parser.add_argument("--copy", required=True, help="copy_package.md path")
    parser.add_argument("--copy-json", help="Optional copy_package.json path")
    parser.add_argument("--out", help="beginner_value_review.json path")
    args = parser.parse_args()

    copy_path = Path(args.copy)
    copy_json_path = Path(args.copy_json) if args.copy_json else None
    result = review(copy_path.read_text(encoding="utf-8"), load_json(copy_json_path))
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
