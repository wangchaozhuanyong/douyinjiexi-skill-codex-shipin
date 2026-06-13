#!/usr/bin/env python3
"""Create structured AI-circle topic candidates for the V3 workflow."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any


TOPIC_BLUEPRINTS = [
    {
        "topic_id": "T001",
        "title_direction": "普通人用 ChatGPT 写文案为什么总是空话",
        "core_angle": "少给目标对象、使用场景和输出格式，会让结果泛化",
        "content_format": "mistake_correction",
        "format_reason": "先展示错误问法和空泛输出，再给可复制限制条件。",
        "target_viewer": "想用 AI 写短视频文案的新手创作者",
        "viewer_pain": "写出来像套话，不能直接发，也不知道哪里问错了",
        "why_now": "AI 写作普及后，提示词质量开始决定输出能不能直接用",
        "curiosity_gap": "为什么别人同样用 ChatGPT，输出更具体",
        "save_reason": "给出对象、场景、格式三段模板",
        "comment_trigger": "观众会问自己的行业怎么填这三个限制",
        "visual_potential": "错误提示词和改良提示词的左右对比",
        "proof_assets_needed": ["真实 ChatGPT 输入截图", "真实输出对比截图"],
        "main_claims": ["更具体的任务约束通常能让输出更可控"],
        "sources": [
            {
                "title": "OpenAI prompting guidance",
                "url_or_note": "official docs or locally captured doc screenshot",
                "claim_supported": "明确任务和约束有助于输出控制",
            }
        ],
        "scores": {
            "pain_score": 9,
            "novelty_score": 8,
            "save_score": 9,
            "comment_score": 8,
            "visual_score": 9,
            "compliance_safety_score": 9,
        },
    },
    {
        "topic_id": "T002",
        "title_direction": "别直接让 AI 生成视频，先让它写镜头表",
        "core_angle": "镜头表先锁定口播、画面和证据，成片更稳定",
        "content_format": "three_step_tutorial",
        "format_reason": "拆成选题、镜头表、证据素材三步，适合收藏复用。",
        "target_viewer": "用 AI 做短视频但经常跑偏的创作者",
        "viewer_pain": "画面、字幕和口播互相不对应，返工很多",
        "why_now": "AI 视频工具更容易生成画面，但流程调度仍要人工设计",
        "curiosity_gap": "为什么先写镜头表比直接生成视频更稳",
        "save_reason": "给出镜头表字段模板",
        "comment_trigger": "观众会问不同选题怎么拆镜头",
        "visual_potential": "无镜头表草稿 vs 有镜头表分镜的对比",
        "proof_assets_needed": ["真实镜头表文件截图", "分镜 JSON 片段", "成片关键帧"],
        "main_claims": ["镜头表能减少口播和画面不同步"],
        "sources": [
            {
                "title": "Local visual sync rules",
                "url_or_note": "references/visual_sync_rules.md",
                "claim_supported": "当前画面必须解释当前口播",
            }
        ],
        "scores": {
            "pain_score": 8,
            "novelty_score": 8,
            "save_score": 9,
            "comment_score": 8,
            "visual_score": 9,
            "compliance_safety_score": 9,
        },
    },
    {
        "topic_id": "T003",
        "title_direction": "AI 教程视频差，不是因为画面不够炫",
        "core_angle": "缺少真实证据镜头会让教程失去可信度",
        "content_format": "myth_busting",
        "format_reason": "破除“多加特效就高级”的误区，转向证据画面。",
        "target_viewer": "正在做 AI 工具教程的短视频创作者",
        "viewer_pain": "画面很花，但观众不信，也不知道怎么照做",
        "why_now": "AI 教程内容越来越多，真实演示会拉开信任差距",
        "curiosity_gap": "为什么真实 UI 比抽象科技背景更有效",
        "save_reason": "给出证据镜头清单",
        "comment_trigger": "观众会问哪些画面算证据",
        "visual_potential": "抽象背景讲解 vs 真实输入输出证明",
        "proof_assets_needed": ["真实 UI 截图", "终端命令结果", "输出文件预览"],
        "main_claims": ["知识类视频需要证据画面支撑口播"],
        "sources": [
            {
                "title": "Local AI circle content rules",
                "url_or_note": "references/ai_circle_content_rules.md",
                "claim_supported": "优先使用真实 UI、真实截图和真实输出证明",
            }
        ],
        "scores": {
            "pain_score": 9,
            "novelty_score": 8,
            "save_score": 9,
            "comment_score": 8,
            "visual_score": 9,
            "compliance_safety_score": 9,
        },
    },
    {
        "topic_id": "T004",
        "title_direction": "Codex Skill 真正有用的是把流程变成工厂",
        "core_angle": "把重复检查写进 skill，能减少漏步骤和假完成",
        "content_format": "case_breakdown",
        "format_reason": "用一次视频生产流水线拆解 skill 的价值。",
        "target_viewer": "每天重复做内容、代码或自动化任务的人",
        "viewer_pain": "每次都靠记忆跑流程，容易漏 QA、漏证据、漏交付文件",
        "why_now": "Agent 工作流开始从单次回答转向可复用流程",
        "curiosity_gap": "为什么同样用 Codex，有人更稳定",
        "save_reason": "给出一条 skill 化流程清单",
        "comment_trigger": "观众会问自己的流程能不能做成 skill",
        "visual_potential": "skill 文件、命令输出、QA 报告和 final 目录联动展示",
        "proof_assets_needed": ["SKILL.md 截图", "doctor.py 输出", "qa_report.json 截图"],
        "main_claims": ["重复流程适合沉淀成 skill"],
        "sources": [
            {
                "title": "Codex skill docs",
                "url_or_note": "official docs or local docs screenshot",
                "claim_supported": "skills package repeatable workflows",
            }
        ],
        "scores": {
            "pain_score": 8,
            "novelty_score": 8,
            "save_score": 9,
            "comment_score": 8,
            "visual_score": 8,
            "compliance_safety_score": 9,
        },
    },
    {
        "topic_id": "T005",
        "title_direction": "做 AI 视频前，先问哪一帧能证明这句话是真的",
        "core_angle": "每个关键口播都要绑定一个证明画面",
        "content_format": "before_after",
        "format_reason": "对比空讲版和证据版，能直观看出差异。",
        "target_viewer": "想提升 AI 知识视频质感的创作者",
        "viewer_pain": "视频看起来像 PPT，观众听完也不知道怎么做",
        "why_now": "平台和观众都更容易识别低信息价值内容",
        "curiosity_gap": "为什么加证据画面比加动效更重要",
        "save_reason": "给出口播到证据的检查表",
        "comment_trigger": "观众会拿自己的视频来对照检查",
        "visual_potential": "一条口播对应一帧证据，逐句打勾",
        "proof_assets_needed": ["口播稿截图", "证据帧 contact sheet", "审片报告"],
        "main_claims": ["证据帧能提高教程视频的可理解性和可信度"],
        "sources": [
            {
                "title": "Local video quality contract",
                "url_or_note": "references/video_quality_contract.md",
                "claim_supported": "高质量视频需要真实证明和同步画面",
            }
        ],
        "scores": {
            "pain_score": 9,
            "novelty_score": 8,
            "save_score": 9,
            "comment_score": 8,
            "visual_score": 9,
            "compliance_safety_score": 9,
        },
    },
]


def weighted_total(scores: dict[str, Any]) -> float:
    weights = {
        "pain_score": 0.25,
        "novelty_score": 0.15,
        "save_score": 0.25,
        "comment_score": 0.10,
        "visual_score": 0.15,
        "compliance_safety_score": 0.10,
    }
    return round(sum(float(scores.get(key, 0)) * weight for key, weight in weights.items()), 2)


def build_candidates(theme: str, source_date: str) -> dict[str, Any]:
    candidates = []
    for item in TOPIC_BLUEPRINTS:
        candidate = json.loads(json.dumps(item, ensure_ascii=False))
        candidate["research_theme"] = theme
        candidate["risk_flags"] = []
        for source in candidate["sources"]:
            source["date"] = source_date
        candidate["scores"]["total_score"] = weighted_total(candidate["scores"])
        candidates.append(candidate)
    return {
        "research_theme": theme,
        "generated_at": source_date,
        "candidates": candidates,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate structured AI-circle topic candidates.")
    parser.add_argument("--theme", default="AI 圈知识类抖音视频")
    parser.add_argument("--out", required=True, help="topic_candidates.json path")
    parser.add_argument("--date", default=date.today().isoformat())
    args = parser.parse_args()

    result = build_candidates(args.theme, args.date)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "candidate_count": len(result["candidates"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
