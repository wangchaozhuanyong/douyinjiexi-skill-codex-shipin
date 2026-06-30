#!/usr/bin/env python3
"""Create a V3 visual-director storyboard from a copy package."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


QUALITY_SPEC = {
    "target_quality_level": "high_quality",
    "visual_system": "premium 16:9 AI workflow explainer with real proof, operation simulation, and collectible template moments",
    "motion_policy": "useful motion only; varied HyperFrames recipes tied to meaning, no same-page slide deck repetition",
    "still_image_policy": "generated visuals are topic-bound support plates; real screenshots and operation proofs carry evidence",
    "evidence_policy": "real UI, source crop, terminal/file proof, and result evidence first; generated visuals never pretend to be proof",
    "sfx_policy": "subtle UI click, proof tray, card settle, and soft whoosh cues below narration",
    "render_policy": "HyperFrames quality high plus high-bitrate H.264 pass when needed",
    "cover_policy": "standalone poster cover, not a random frame grab",
    "frame_review_policy": "review first 5 seconds, full contact sheet, native detail frames, screen text, and empty-frame risk",
    "provider_policy": "free_first_local_or_authorized_openai_only",
    "runtime_choice": "HyperFrames final timeline; Remotion component clips when needed; FFmpeg only for mechanical media",
    "caption_template_plan": "mix proof_callout, comparison_label, chapter_card, terminal_code_caption, word_highlight, and final_takeaway",
    "timeline_contract_ref": "internal/timeline_contract.md",
    "narration_continuity_policy": "single continuous root narration audio; visual transitions never restart, mute, fade, or gap voice; max planned transition audio gap 80ms",
}

TARGET = {
    "width": 1920,
    "height": 1080,
    "fps": 30,
    "tts_speed": 1.0,
    "voice_speed_policy": "normal",
    "provider_policy": "free_first_local_or_authorized_openai_only",
}

SHOT_PRESETS = [
    {
        "shot_type": "hook_conflict",
        "layout_family": "workspace_ui",
        "camera_scale": "macro_closeup",
        "camera_motion": "push_in",
        "visual_subject": "AI 工作区里出现一个模糊任务，右侧立刻弹出歧义和空话风险提示",
        "primary_action": "模糊任务被框选，风险标签和错误输出预览快速落位",
        "viewer_focus": "先看到错误问法为什么会失败",
        "operation_elements": ["task_brief_panel"],
        "evidence": {"type": "real_ui_capture", "asset_id": "A001", "must_be_readable": True, "min_visible_width_px": 1100},
        "primary_text": "错误问法",
        "secondary": ["歧义", "空话风险"],
    },
    {
        "shot_type": "source_evidence",
        "layout_family": "source_crop",
        "camera_scale": "closeup",
        "camera_motion": "zoom_in",
        "visual_subject": "真实来源或演示截图局部被放大，旁边是干净来源说明卡",
        "primary_action": "证据区域被遮罩揭示，来源、日期或信号点依次点亮",
        "viewer_focus": "确认这不是空口讲概念，而是有证据支撑",
        "operation_elements": ["source_citation"],
        "evidence": {
            "type": "real_source_crop",
            "asset_id": "A001",
            "source_title": "local source or workflow capture",
            "source_url": "local://assets/screenshots/s01.png",
            "must_be_readable": True,
            "min_visible_width_px": 1100,
        },
        "primary_text": "证据点",
        "secondary": ["来源", "信号", "结论"],
    },
    {
        "shot_type": "operation_simulation",
        "layout_family": "repo_file_tree",
        "camera_scale": "medium",
        "camera_motion": "tracking",
        "visual_subject": "左侧任务 brief 展开目标、约束和文件结构，右侧输出区同步更新",
        "primary_action": "目标和约束从 brief 面板滑入执行面板",
        "viewer_focus": "看到方法怎样进入真实操作流程",
        "operation_elements": ["task_brief_panel", "repo_or_file_tree"],
        "evidence": {"type": "real_ui_capture", "asset_id": "A002", "must_be_readable": True, "min_visible_width_px": 1000},
        "primary_text": "任务 brief",
        "secondary": ["目标", "约束", "文件"],
    },
    {
        "shot_type": "method_template",
        "layout_family": "template_card",
        "camera_scale": "medium",
        "camera_motion": "parallax",
        "visual_subject": "方法模板卡拆成目标、环境、检查点和验收标准四块",
        "primary_action": "四块模板卡按 0.12 秒错峰抬升并锁定阅读区",
        "viewer_focus": "把抽象建议变成可保存结构",
        "operation_elements": ["risk_list"],
        "evidence": {"type": "abstract_non_official_diagram"},
        "primary_text": "方法模板",
        "secondary": ["目标", "环境", "检查点", "验收"],
    },
    {
        "shot_type": "operation_simulation",
        "layout_family": "terminal_output",
        "camera_scale": "closeup",
        "camera_motion": "tracking",
        "visual_subject": "终端或结果面板逐行出现检查输出、风险列表和证据包",
        "primary_action": "测试通过、风险关闭、证据包生成三个状态依次勾选",
        "viewer_focus": "看到结果不是口号，而是可验收输出",
        "operation_elements": ["test_or_check_output", "evidence_result_card"],
        "evidence": {"type": "terminal_or_file_proof", "asset_id": "A002", "must_be_readable": True, "min_visible_width_px": 1000},
        "primary_text": "执行结果",
        "secondary": ["检查", "风险", "证据"],
    },
    {
        "shot_type": "final_template",
        "layout_family": "final_cta",
        "camera_scale": "wide",
        "camera_motion": "pull_out",
        "visual_subject": "最终可收藏公式卡居中，背景工作区收束成一张稳定模板",
        "primary_action": "公式卡稳定停留，收藏提示轻微出现",
        "viewer_focus": "获得可以保存和复用的一句话模板",
        "operation_elements": ["evidence_result_card"],
        "evidence": {"type": "none"},
        "primary_text": "收藏模板",
        "secondary": ["直接套用"],
    },
]

VISUAL_PRESETS = [
    {
        "scene_type": "screenshot_proof",
        "evidence_source": "real_ui_screenshot",
        "asset_path": "assets/screenshots/s01.png",
        "asset_source_type": "proof",
        "caption_template": "proof_callout",
        "design_layers": ["topic-bound dark background plate", "real UI proof crop", "risk callout frame", "subtitle safe rail"],
        "description": "真实界面或工作区截图承载开头冲突",
    },
    {
        "scene_type": "comparison",
        "evidence_source": "real_source_crop",
        "asset_path": "assets/screenshots/s02.png",
        "asset_source_type": "proof",
        "caption_template": "comparison_label",
        "design_layers": ["source crop stage", "before-after comparison panels", "citation rail", "subtitle safe rail"],
        "description": "来源局部或前后对比证明当前观点",
    },
    {
        "scene_type": "real_ui_demo",
        "evidence_source": "real_or_simulated_workflow_capture",
        "asset_path": "assets/screenshots/s03.png",
        "asset_source_type": "proof",
        "caption_template": "chapter_card",
        "design_layers": ["workspace background plate", "task brief panel", "file tree lane", "active cursor path"],
        "description": "任务 brief 和工作区操作感镜头",
    },
    {
        "scene_type": "text_card",
        "evidence_source": "designed_method_card",
        "asset_path": "assets/generated/s04.png",
        "asset_source_type": "support",
        "caption_template": "word_highlight",
        "design_layers": ["generated support plate", "method cards", "checklist rail", "caption safe band"],
        "description": "方法模板卡作为解释支撑，不冒充证据",
    },
    {
        "scene_type": "code_or_file_proof",
        "evidence_source": "terminal_or_file_output",
        "asset_path": "assets/screenshots/s05.png",
        "asset_source_type": "proof",
        "caption_template": "terminal_code_caption",
        "design_layers": ["terminal proof tray", "status check row", "evidence package card", "caption safe band"],
        "description": "终端、文件或输出结果证明方法可验收",
    },
    {
        "scene_type": "text_card",
        "evidence_source": "collectible_template_card",
        "asset_path": "assets/generated/s06.png",
        "asset_source_type": "support",
        "caption_template": "final_takeaway",
        "design_layers": ["stable final background plate", "large formula card", "save CTA chip", "quiet glow layer"],
        "description": "最终可收藏模板卡稳定收束",
    },
]

MOTION_RECIPES = [
    {
        "transition": "source_focus_lens_reveal: lens aperture opens through local blur, source panel refracts in, outer frame scan locks on sentence boundary",
        "background_motion": "slow 100% to 103% push-in with low-opacity parallax source wall",
        "foreground_motion": "macro task panel mask reveal followed by risk chips staggered slide-in",
        "callout_motion": "warning callout draws a restrained outline around the vague task",
        "purpose": "warn and reveal",
    },
    {
        "transition": "source_focus_lens_reveal: citation lens expands from the source corner, refracts the proof crop, then locks the frame edge",
        "background_motion": "slow 100% to 103% push-in while citation rail stays readable",
        "foreground_motion": "source crop enters through a soft lens mask and settles before caption",
        "callout_motion": "citation rail reveals source, date, and signal with 0.12s stagger",
        "purpose": "verify",
    },
    {
        "transition": "operation_node_relay: active node emits a data packet that pulls the next workspace layer forward",
        "background_motion": "slow 100% to 103% push-in with workspace parallax depth",
        "foreground_motion": "brief panel and file tree track horizontally like a real operated workspace",
        "callout_motion": "cursor packet travels from brief to output panel",
        "purpose": "connect",
    },
    {
        "transition": "template_lift_settle: foreground template lifts through a masked depth layer, settles with one lock pulse",
        "background_motion": "slow 100% to 103% push-in behind stable template cards",
        "foreground_motion": "method cards lift in one by one and hold for readability",
        "callout_motion": "active card receives a thin marker sweep tied to narration",
        "purpose": "summarize",
    },
    {
        "transition": "terminal_scan_proof_tray: terminal scan line travels down, proof tray lifts through a masked data-light wipe",
        "background_motion": "slow 100% to 103% push-in under terminal proof tray",
        "foreground_motion": "terminal lines scan in, then evidence tray slides up below the result",
        "callout_motion": "test pass and evidence package cues pop subtly under the spoken beat",
        "purpose": "verify",
    },
    {
        "transition": "final_controlled_zoom: checklist nodes converge into the final card, then a restrained 102% camera settle",
        "background_motion": "slow 100% to 103% push-in then settle for final readability",
        "foreground_motion": "final formula card lifts 20px and locks centered",
        "callout_motion": "save CTA fades in after the formula, no extra bounce",
        "purpose": "summarize",
    },
]

STACK_TRIGGER_TERMS = ["codex", "skill", "插件", "remotion", "hyperframes", "imagegen", "image gen", "heygen"]
PLUGIN_TRIGGER_TERMS = [
    "插件",
    "plugin",
    "plugins",
    "browser plugin",
    "浏览器插件",
    "github",
    "hugging face",
    "huggingface",
    "openai developers",
    "heygen",
]


def extract_section(text: str, header: str) -> str:
    pattern = re.compile(rf"(?ms)^##\s*{re.escape(header)}\s*\n(.+?)(?=^##\s+|\Z)")
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def sentences(text: str) -> list[str]:
    items = [item.strip(" \t\r\n“”\"") for item in re.split(r"[。！？!?;\n]+", text) if item.strip()]
    return [item for item in items if len(item) >= 4]


def split_voice(text: str) -> list[str]:
    first_five = sentences(extract_section(text, "First 5 Seconds"))
    body = sentences(extract_section(text, "口播正文"))
    save_value = sentences(extract_section(text, "保存价值"))
    all_lines = []
    if first_five:
        all_lines.append(first_five[0])
    all_lines.extend(body)
    if save_value:
        all_lines.append(save_value[0])
    fallback = [
        "先把问题讲具体，别让 AI 猜你的真实目标",
        "再给它可见证据，让结果能被检查",
        "最后把方法收成一张可以复用的模板",
    ]
    all_lines.extend(fallback)
    cleaned: list[str] = []
    for line in all_lines:
        if line not in cleaned:
            cleaned.append(line)
    return cleaned[:6]


def load_copy_json(copy_path: Path) -> dict[str, Any]:
    json_path = copy_path.with_suffix(".json")
    if not json_path.exists():
        return {}
    try:
        return json.loads(json_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def infer_title(copy_path: Path, text: str) -> str:
    data = load_copy_json(copy_path)
    title_options = data.get("title_options")
    if isinstance(title_options, list) and title_options and str(title_options[0]).strip():
        return str(title_options[0]).strip()
    first_line = sentences(extract_section(text, "First 5 Seconds"))
    if first_line:
        return first_line[0][:26]
    return "AI 工作流高级分镜"


def caption_for(line: str) -> str:
    return line[:18]


def approved_primary_text(index: int, line: str) -> str:
    preset_text = SHOT_PRESETS[index]["primary_text"]
    if index == 5 and any(term in line for term in ["收藏", "模板", "公式"]):
        return "收藏模板"
    return preset_text


def proof_chain_for(index: int) -> dict[str, str]:
    labels = ["开头冲突", "来源证据", "操作过程", "方法模板", "执行结果", "收藏模板"]
    label = labels[index]
    return {
        "entry_or_source": f"{label} 使用真实截图、来源卡或明确标注的演示素材作为入口",
        "operation_or_step": f"画面展示 {label} 对应的可见操作或结构拆解",
        "output_or_result": f"输出 {label} 的证据、结果或可保存模板",
        "viewer_value": "观众能判断这一步为什么有用，并知道下一步怎么照着做",
    }


def motion_for(index: int) -> dict[str, str]:
    recipe = MOTION_RECIPES[index]
    return {
        "background_motion": recipe["background_motion"],
        "foreground_motion": recipe["foreground_motion"],
        "callout_motion": recipe["callout_motion"],
        "transition": recipe["transition"],
        "purpose": recipe["purpose"],
        "entrance": "0.6s cinematic fade-up from y=20px opacity 0",
        "stagger": "0.12s-0.18s between title/cards",
        "keyword_motion": "subtle scale-pop max 1.08x for 0.25s",
        "camera_motion": "background push-in 100% to 103%, foreground stable",
        "layering": "background parallax + foreground stable + callout reveal",
        "caption_motion": "keyword highlight only, no every-word bouncing",
        "glow": "ambient glow opacity 8%-18%, no flicker",
        "audio_reactive": "text 3%-5%, background glow 10%-15%",
        "negative_motion": "no excessive bounce, no chaotic movement, no glitch spam",
    }


def sfx_cues_for(index: int) -> list[dict[str, Any]]:
    return []


def scene_for(index: int, voice: str, elapsed: float, duration: float) -> dict[str, Any]:
    shot = SHOT_PRESETS[index]
    visual = dict(VISUAL_PRESETS[index])
    visual["proof_chain"] = proof_chain_for(index)
    visual["quality_checks"] = {
        "source_resolution_ok": True,
        "text_safe": True,
        "not_template_like": True,
        "not_static_dump": True,
    }
    primary_text = approved_primary_text(index, voice)
    return {
        "scene_id": f"S{index + 1:02d}",
        "concept": [
            "错误问法冲突",
            "来源证据验证",
            "真实操作拆解",
            "方法模板沉淀",
            "执行结果验收",
            "最终收藏模板",
        ][index],
        "duration_target": duration,
        "voice": voice,
        "caption": caption_for(voice),
        "on_screen_text": [primary_text] + shot["secondary"][:2],
        "visual": visual,
        "motion": motion_for(index),
        "sfx_cues": sfx_cues_for(index),
        "sync": {
            "voice_start": round(elapsed, 3),
            "voice_end": round(elapsed + duration, 3),
            "caption_start": round(elapsed, 3),
            "caption_end": round(elapsed + duration, 3),
            "narration_track": "continuous_root_audio",
            "transition_audio_policy": "visual-only transition; narration continues with no restart or mute",
            "max_audio_gap_ms": 80,
            "audio_bridge": "continuous clean narration bed under visual-only transition; no background audio by default, no restart, no mute, no silence gap",
        },
        "safe_zone": {
            "top_reserved": True,
            "bottom_caption_reserved": True,
            "right_buttons_reserved": True,
            "top_margin_px": 240,
            "bottom_margin_px": 360,
            "left_margin_px": 72,
            "right_margin_px": 180,
            "critical_content_inside_safe_area": True,
        },
        "beat_map": [
            {
                "voice_fragment": voice[:18],
                "visual_action": shot["primary_action"],
                "caption": caption_for(voice),
                "proof_or_explanation": ["错误对比", "真实证明", "操作证明", "方法模板", "结果证明", "保存模板"][index],
                "motion_trigger": MOTION_RECIPES[index]["callout_motion"],
            }
        ],
        "qa_notes": ["generated by build_storyboard.py V3 visual-director builder; replace placeholder asset paths with real proof before final render"],
    }


def director_shot_for(index: int, duration: float) -> dict[str, Any]:
    shot = dict(SHOT_PRESETS[index])
    primary_text = str(shot.pop("primary_text"))
    secondary = list(shot.pop("secondary"))
    shot["shot_id"] = f"S{index + 1:02d}"
    shot["duration_sec"] = duration
    shot["on_screen_text"] = {
        "primary": primary_text,
        "secondary": secondary,
        "approved_primary_text": [primary_text],
    }
    shot["forbidden_risks"] = ["empty_frame", "tiny_unreadable_text", "same_layout_repetition", "crowded_layout"]
    return shot


def needs_stack(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in STACK_TRIGGER_TERMS)


def needs_plugin_plan(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in PLUGIN_TRIGGER_TERMS)


def production_stack(text: str) -> dict[str, Any]:
    lowered = text.lower()
    tool_map = {
        "codex": "Codex",
        "skill": "Skill",
        "hyperframes": "HyperFrames",
        "remotion": "Remotion",
        "imagegen": "ImageGen",
        "image gen": "ImageGen",
        "heygen": "HeyGen",
        "插件": "Codex 插件",
    }
    tools = []
    for marker, name in tool_map.items():
        if marker in lowered and name not in [tool["name"] for tool in tools]:
            tools.append(
                {
                    "name": name,
                    "role": f"{name} 在视频中必须有入口、操作、输出和观众价值证明",
                    "aliases": [name.lower()],
                    "evidence_chain": {
                        "entry_or_source": f"{name} 的真实入口、官方说明或本地可见界面",
                        "operation_or_step": f"展示 {name} 参与的可复现操作步骤",
                        "output_or_result": f"展示 {name} 产生的文件、画面、日志或结果",
                        "viewer_value": f"说明 {name} 对观众的实际价值，不做空泛介绍",
                    },
                }
            )
    if not tools:
        tools.append(
            {
                "name": "AI workflow",
                "role": "解释这条 AI 工作流的证据、操作和输出",
                "aliases": ["ai"],
                "evidence_chain": {
                    "entry_or_source": "真实来源、界面或演示素材",
                    "operation_or_step": "可复现操作步骤",
                    "output_or_result": "可见输出结果",
                    "viewer_value": "观众能直接复用",
                },
            }
        )
    return {
        "reference_learning_applied": True,
        "reference_pattern": "visual_director_script_before_hyperframes",
        "workflow_order": ["证据采集", "视觉导演分镜", "HyperFrames 合成", "QA 验收"],
        "primary_tools": tools,
    }


def codex_plugin_plan(text: str) -> dict[str, Any]:
    plugins = [
        {
            "name": "HyperFrames",
            "availability": "local_cli_or_skill",
            "role": "最终时间线、字幕、动效和渲染执行器",
            "allowed_by_default": True,
            "evidence_required": ["composition 文件", "preview/inspect 结果", "render 输出"],
            "cost_or_auth_boundary": "本地或已安装 skill 路径优先，不使用新付费服务",
            "fallback": "如果 HyperFrames 不可用，停止并标注 blocked，不用低配轮播冒充 final",
        }
    ]
    if "heygen" in text.lower():
        plugins.append(
            {
                "name": "HeyGen",
                "availability": "needs_user_approval",
                "role": "可选数字人视频生成，不是默认生产路径",
                "allowed_by_default": False,
                "evidence_required": ["用户明确授权", "账号/额度边界", "生成结果"],
                "cost_or_auth_boundary": "可能需要账号、登录或额度；未授权不得使用",
                "fallback": "使用本地/已授权 TTS 和 HyperFrames 视觉合成",
            }
        )
        approval_required_for = ["HeyGen"]
    else:
        approval_required_for = []
    return {
        "use_case": "AI 视频插件或工具工作流讲解",
        "plugins": plugins,
        "blocked_plugins": [],
        "approval_required_for": approval_required_for,
    }


def build_storyboard(copy_path: Path) -> dict[str, Any]:
    text = copy_path.read_text(encoding="utf-8")
    voices = split_voice(text)
    durations = [3.0, 3.0, 3.2, 3.2, 3.2, 2.8]
    scenes = []
    director_shots = []
    elapsed = 0.0
    for index, voice in enumerate(voices):
        duration = durations[index]
        scenes.append(scene_for(index, voice, elapsed, duration))
        director_shots.append(director_shot_for(index, duration))
        elapsed += duration
    result: dict[str, Any] = {
        "status": "draft_only",
        "production_ready": False,
        "builder_role": "starter_storyboard_only",
        "title": infer_title(copy_path, text),
        "quality_spec": QUALITY_SPEC,
        "target": TARGET,
        "director_shots": director_shots,
        "scenes": scenes,
    }
    trigger_surface = " ".join([str(result["title"])] + voices)
    if needs_stack(trigger_surface):
        result["production_stack"] = production_stack(trigger_surface)
    if needs_plugin_plan(trigger_surface):
        result["codex_plugin_plan"] = codex_plugin_plan(trigger_surface)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a V3 visual-director storyboard.")
    parser.add_argument("--copy", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build_storyboard(Path(args.copy)), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
