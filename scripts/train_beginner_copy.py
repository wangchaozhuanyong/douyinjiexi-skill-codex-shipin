#!/usr/bin/env python3
"""Run deterministic beginner-copy rewrite drills."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

import validate_beginner_copy


def initial_state() -> dict[str, Any]:
    return {
        "title_options": ["ChatGPT 新功能太强了"],
        "target_viewer": "",
        "task": "",
        "visible_result": "",
        "why_watch_now": "",
        "first_action": "",
        "first_5": "今天给大家分享一个 AI 技巧。这个功能很强，可以提升效率，适合大家学习。",
        "voice_lines": [
            "现在 AI 工具越来越多，大家一定要重视。",
            "它可以帮助你优化工作流，提升内容生产效率。",
            "我们要学会使用提示词，让输出更好。",
        ],
        "proof_visual_plan": [],
        "problem_examples": [],
        "terminology": [],
        "save_value": "",
        "time_saving_claim": "",
        "retention_beats": [],
    }


def copy_json(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "beginner_task_card": {
            "target_viewer": state["target_viewer"],
            "task": state["task"],
            "visible_result": state["visible_result"],
            "why_watch_now": state["why_watch_now"],
            "first_action": state["first_action"],
            "time_saving_claim": state["time_saving_claim"],
        },
        "title_options": state["title_options"],
        "first_5_seconds_hook": {
            "line": state["first_5"],
            "visual_changes": [
                "先展示改前改后结果",
                "再切到三步操作",
            ],
        },
        "full_voiceover": {
            "target_duration": 65,
            "speed": "正常语速",
            "text": "\n".join(state["voice_lines"]),
        },
        "retention_beats": state["retention_beats"],
        "problem_examples": state["problem_examples"],
        "save_value": {
            "reason": state["save_value"],
            "reusable_asset": "对象 + 场景 + 输出格式 + 禁区 + 证据素材",
        },
        "before_after_plan": {
            "before": "只写一句泛需求，输出像套话。",
            "after": "补上对象、场景、格式、禁区和证据素材，输出能直接检查。",
            "visual_comparison": "左边是空话输出，右边圈出能直接发的标题、口播和检查项。",
        },
        "terminology_explained": state["terminology"],
        "proof_visual_plan": state["proof_visual_plan"],
    }


def render_markdown(state: dict[str, Any]) -> str:
    titles = "\n".join(f"{idx}. {title}" for idx, title in enumerate(state["title_options"], start=1))
    proof_rows = "\n".join(
        f"| {item['claim']} | {item['proof_visual']} | {item['asset_needed']} |"
        for item in state["proof_visual_plan"]
    )
    example_rows = "\n".join(
        f"| {item['problem']} | {item['example']} | {item['why_it_fails']} | {item['corrected_action']} |"
        for item in state["problem_examples"]
    )
    term_rows = "\n".join(
        f"| {item['term']} | {item['plain_explanation']} |"
        for item in state["terminology"]
    )
    beat_rows = "\n".join(
        f"| {item['time_range']} | {item['type']} | {item['line']} | {item['visual']} |"
        for item in state["retention_beats"]
    )
    return f"""# Copy Package

## First 5 Seconds

{state["first_5"]}

## Title Options

{titles}

## Beginner Task Card

- 目标观众：{state["target_viewer"]}
- 任务：{state["task"]}
- 可见结果：{state["visible_result"]}
- 为什么现在要看：{state["why_watch_now"]}
- 第一动作：{state["first_action"]}
- 省时说明：{state["time_saving_claim"]}


## Voiceover

{chr(10).join(state["voice_lines"])}

## Problem Examples

| Problem | Example | Why It Fails | Corrected Action |
|---|---|---|---|
{example_rows}

## Retention Beats

| Time Range | Type | Line | Visual |
|---|---|---|---|
{beat_rows}

## Proof Visual Plan

| Claim | Proof Visual | Asset Needed |
|---|---|---|
{proof_rows}

## Terminology Explained

| Term | Plain Explanation |
|---|---|
{term_rows}

## Save Value

{state["save_value"]}

## Claim Ledger

| Claim | Type | Source | Risk | How to phrase safely |
|---|---|---|---|---|
| 更具体的任务说明更容易得到可检查输出 | advice | local demonstration | low | 用演示结果说话，不承诺任何平台数据 |
"""


def apply_iteration(state: dict[str, Any], iteration: int) -> str:
    if iteration == 1:
        state["title_options"] = [
            "用 ChatGPT 把一段废话改成能发的短视频文案",
            "小白写 AI 文案，先别只发一句需求",
            "3 步让 ChatGPT 输出一版能检查的口播稿",
        ]
        return "标题从泛 AI 夸法改成“人群/任务/结果”。"
    if iteration == 2:
        state["first_5"] = "别再让 ChatGPT 直接“帮我写文案”了。我给你看同一个需求，左边是空话，右边只加 3 步，就变成能发的口播。"
        return "前 5 秒补上痛点、结果预告和前后对比。"
    if iteration == 3:
        state["target_viewer"] = "第一次用 ChatGPT 写短视频文案的小白创作者"
        state["task"] = "把一段泛泛产品介绍改成 30 秒短视频口播"
        state["visible_result"] = "左边是套话输出，右边是能直接检查的标题、前 5 秒和口播"
        state["why_watch_now"] = "很多人已经会打开 AI，但还不会把需求说清楚"
        state["first_action"] = "打开 ChatGPT，先填目标观众"
        state["problem_examples"] = [
            {
                "problem": "只说帮我写文案",
                "example": "比如你只发一句：帮我写一条产品短视频文案",
                "why_it_fails": "AI 不知道发给谁、用在哪、要什么格式，只能写套话",
                "corrected_action": "先填目标观众、使用场景和输出格式",
            }
        ]
        return "锁定小白任务卡，避免继续泛讲 AI 能力。"
    if iteration == 4:
        state["voice_lines"] = [
            "第一步，打开 ChatGPT，不要先说“帮我写文案”。",
            "比如你只发一句：帮我写一条产品短视频文案，它大概率会写出“品质好、体验好”这种套话。",
            "先填目标观众：发给第一次了解这个产品的人。",
            "第二步，填使用场景：抖音 30 秒口播，开头先说痛点。",
            "第三步，填输出格式：标题、前 5 秒、完整口播、结尾提醒，分开写。",
            "最后加禁区：不要编造案例，不要承诺涨粉，不要写“高端品质”这种空话。",
        ]
        return "把解释概念改成打开、填写、检查这类动作。"
    if iteration == 5:
        state["proof_visual_plan"] = [
            {
                "claim": "一句泛需求会产出套话",
                "proof_visual": "真实 ChatGPT 输入和空泛输出截图",
                "asset_needed": "错误提示词截图",
            },
            {
                "claim": "补三步后输出更可检查",
                "proof_visual": "左右前后对比，圈出标题、前 5 秒和口播结构",
                "asset_needed": "改后输出截图",
            },
        ]
        return "补真实截图和左右对比，避免只靠口播说服。"
    if iteration == 6:
        state["time_saving_claim"] = "少来回改 3 次，先把对象、场景、格式填好，再让 AI 写。"
        state["voice_lines"].append("这样不是空说提升效率，而是少来回改 3 次，少复制粘贴重复需求。")
        return "把“提升效率”翻译成少改几次、少复制几步。"
    if iteration == 7:
        state["terminology"] = [
            {
                "term": "Prompt",
                "plain_explanation": "也就是你交给 AI 的任务说明，不是神秘指令。",
            }
        ]
        state["voice_lines"].append("Prompt 简单说就是任务说明，你不用背术语，只要把这几个格子填清楚。")
        return "把 Prompt 术语翻译成人话。"
    if iteration == 8:
        state["save_value"] = "保存这个模板：发给谁、用在哪、要什么格式、不要写什么、用哪张截图证明。"
        state["retention_beats"] = [
            {
                "time_range": "0-5s",
                "type": "before_after",
                "line": "左边空话，右边能发。",
                "visual": "左右输出对比",
            },
            {
                "time_range": "12-35s",
                "type": "step_build",
                "line": "目标观众、使用场景、输出格式逐步填入。",
                "visual": "提示词模板逐格高亮",
            },
            {
                "time_range": "55-65s",
                "type": "template_save",
                "line": "保存这 5 格，下次直接套。",
                "visual": "五格模板卡",
            },
        ]
        return "补收藏资产和留存节奏。"
    if iteration == 9:
        state["voice_lines"] = [
            line.replace("这样不是空说提升效率，而是", "")
            for line in state["voice_lines"]
            if "AI 工具越来越多" not in line and "优化工作流" not in line
        ]
        return "删掉抽象铺垫和空话，让口播更像人说话。"
    state["title_options"] = [
        "小白用 ChatGPT 写口播，先填这 5 格",
        "别只说帮我写文案，3 步让输出能直接检查",
        "把 AI 套话改成能发口播，就看这组前后对比",
        "不会写短视频文案？先让 ChatGPT 知道发给谁",
    ]
    state["first_5"] = "小白不会写口播，先别怪 ChatGPT。看左边，同一句“帮我写文案”全是套话；看右边，填 5 格后，标题、前 5 秒和口播都能直接检查。"
    return "最后收束成发布前可用的标题和前 5 秒。"


def weakest_dimension(review: dict[str, Any]) -> str:
    scores = review.get("scores", {})
    if not isinstance(scores, dict):
        return "unknown"
    return min(scores, key=lambda key: float(scores[key]))


def write_report(out_dir: Path, iterations: list[dict[str, Any]], final_md: str, final_json: dict[str, Any], final_review: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "final_copy_package.md").write_text(final_md, encoding="utf-8")
    (out_dir / "final_copy_package.json").write_text(json.dumps(final_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "beginner_value_review.json").write_text(json.dumps(final_review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "beginner_copy_training_report.json").write_text(
        json.dumps({"iterations": iterations, "final_review": final_review}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = ["# Beginner Copy Training Report", ""]
    for item in iterations:
        before = item["review_before"]
        after = item["review_after"]
        lines.extend(
            [
                f"## Iteration {item['iteration']}",
                "",
                f"- 小白视角最低分项：{item['weakest_before']}",
                f"- 本轮问题：{'; '.join(before.get('rewrite_required', [])) or '没有硬失败，继续打磨。'}",
                f"- 本轮编辑：{item['edit_applied']}",
                f"- 分数变化：{before['total_score']} -> {after['total_score']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Final",
            "",
            f"- status: {final_review['status']}",
            f"- total_score: {final_review['total_score']}",
            f"- rewrite_required: {', '.join(final_review['rewrite_required']) or 'none'}",
            "",
        ]
    )
    (out_dir / "beginner_copy_training_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run 10 beginner-copy rewrite iterations.")
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--out-dir", default=f"outputs/beginner-copy-training-{date.today().isoformat()}/internal")
    args = parser.parse_args()

    state = initial_state()
    records: list[dict[str, Any]] = []
    for iteration in range(1, args.iterations + 1):
        before_md = render_markdown(state)
        before_json = copy_json(state)
        before_review = validate_beginner_copy.review(before_md, before_json)
        edit = apply_iteration(state, iteration)
        after_md = render_markdown(state)
        after_json = copy_json(state)
        after_review = validate_beginner_copy.review(after_md, after_json)
        records.append(
            {
                "iteration": iteration,
                "weakest_before": weakest_dimension(before_review),
                "edit_applied": edit,
                "review_before": before_review,
                "review_after": after_review,
            }
        )

    final_md = render_markdown(state)
    final_json = copy_json(state)
    final_review = validate_beginner_copy.review(final_md, final_json)
    write_report(Path(args.out_dir), records, final_md, final_json, final_review)
    print(json.dumps({"status": final_review["status"], "total_score": final_review["total_score"], "out_dir": args.out_dir}, ensure_ascii=False))
    return 0 if final_review["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
