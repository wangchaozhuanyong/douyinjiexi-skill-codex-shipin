#!/usr/bin/env python3
"""Generate deterministic first-3-seconds hook variants for AI videos."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


TOOL_NAMES = ["Codex", "ChatGPT", "Gemini", "OpenAI", "Claude", "Agent", "AI"]


def load_json_text(path: Path | None) -> str:
    if not path or not path.exists():
        return ""
    try:
        return json.dumps(json.loads(path.read_text(encoding="utf-8")), ensure_ascii=False)
    except json.JSONDecodeError:
        return path.read_text(encoding="utf-8")


def infer_tool(text: str) -> str:
    lower = text.lower()
    for name in TOOL_NAMES:
        if name.lower() in lower:
            return name
    if "插件" in text or "skill" in lower:
        return "Codex Skill"
    return "AI 工具"


def infer_task(text: str) -> str:
    if "视频" in text:
        return "视频生产流程"
    if "代码" in text or "codex" in text.lower():
        return "代码任务"
    if "提示词" in text or "prompt" in text.lower():
        return "提示词流程"
    if "新闻" in text or "更新" in text:
        return "新功能判断"
    return "复杂任务"


def build_variants(topic: str) -> list[dict[str, Any]]:
    tool = infer_tool(topic)
    task = infer_task(topic)
    lines = [
        f"别再让{tool}只回答问题了，先让它锁住一个可验收结果。",
        f"同一个{task}，别人少返工，不是更会问，是先让{tool}读懂边界。",
        f"今天不讲概念，只看{tool}怎么把{task}跑成一条能检查的流程。",
        f"如果你用{tool}总是跑偏，先检查这三个输入，而不是继续重试。",
        f"{tool}真正拉开差距的地方，是先给它证据、规则和验收标准。",
        f"这不是普通教程，我只保留一个标准：最后有没有可验证输出。",
        f"先别急着生成，让{tool}先确认目标、限制和证据来源。",
        f"你缺的不是一句提示词，是让{tool}稳定执行的工作流。",
        f"30 秒看懂：{tool}到底能帮你省掉{task}里的哪一步。",
        f"下次用{tool}前，先把这张检查表跑一遍，结果会稳很多。",
    ]
    variants: list[dict[str, Any]] = []
    for index, line in enumerate(lines, start=1):
        variants.append(
            {
                "hook_id": f"H{index:02d}",
                "first_3_seconds_line": line,
                "viewer_pain": "反复重试、结果跑偏、输出不可验收",
                "visible_result": "得到可检查的流程、证据或结果卡",
                "proof_hint": "展示真实步骤、文件、来源或输出证明",
                "save_reason": "观众能复用为下一次 AI/Codex 任务的检查表",
                "risk_note": "避免绝对化承诺和夸张营销词",
            }
        )
    return variants


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate hook variants.")
    parser.add_argument("--topic", default="")
    parser.add_argument("--selected-topic", help="selected_topic.json path")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    topic = " ".join([args.topic, load_json_text(Path(args.selected_topic)) if args.selected_topic else ""]).strip()
    if not topic:
        topic = "AI knowledge video"
    variants = build_variants(topic)
    report = {
        "status": "passed",
        "topic": topic,
        "variant_count": len(variants),
        "variants": variants,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "variant_count": len(variants)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
