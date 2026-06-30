#!/usr/bin/env python3
"""Select the AI video scheme, visual family, and component mix.

The selector is deterministic by topic text. It is not a generative model; it
creates an auditable director decision before copy/storyboard work.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STYLE_CARDS = ROOT / "references" / "reference_style_cards.json"
DEFAULT_COMPONENT_REGISTRY = ROOT / "references" / "component_motion_registry.json"


SCHEMES: dict[str, dict[str, str]] = {
    "scheme_1_skill_recommendation_no_voice": {
        "name": "方案1: Skill 推荐无人声",
        "format": "1080x1920",
        "content_job": "recommend Skills/tools and explain what each one does for a beginner",
    },
    "scheme_2_source_led_tool_tutorial": {
        "name": "方案2: Source-Led AI Tool Tutorial",
        "format": "1920x1080",
        "content_job": "teach one AI tool or Codex workflow with source/proof",
    },
    "scheme_3_ai_news_to_beginner_action": {
        "name": "方案3: AI News To Beginner Action",
        "format": "1920x1080",
        "content_job": "turn a recent AI update into one beginner action",
    },
    "scheme_4_multi_skill_stack_explainer": {
        "name": "方案4: Multi-Skill / Production Stack Explainer",
        "format": "1920x1080",
        "content_job": "show how several skills/plugins/tools cooperate",
    },
    "scheme_5_checklist_template_poster": {
        "name": "方案5: Checklist / Mistake / Template Poster",
        "format": "1920x1080",
        "content_job": "give a saveable checklist, mistake list, or prompt template",
    },
    "scheme_6_operation_proof_short": {
        "name": "方案6: Operation Proof / Test Result Short",
        "format": "1920x1080",
        "content_job": "prove an operation actually ran",
    },
    "scheme_7_ai_hot_rank_top5": {
        "name": "方案7: AI 热榜 TOP5 榜单",
        "format": "1080x1920",
        "content_job": "rank five current AI signals from real sources and explain why each matters",
    },
}

MUSIC_DECISIONS: dict[str, dict[str, Any]] = {
    "scheme_1_skill_recommendation_no_voice": {
        "music_policy": "required_bgm",
        "reason": "vertical no-voice recommendation videos need music to carry pacing and row reveals",
        "bgm_source_priority": ["douyin_reference", "authorized_local_library", "pixabay", "mixkit"],
        "voice_policy": "no_voice",
        "voice_priority": False,
        "sfx_required": False,
        "generated_bgm_allowed": False,
        "generated_background_audio_allowed": False,
        "reference_bgm_policy": "when a user-provided Douyin reference has BGM, use the same reference music or block for user approval; do not generate or silently substitute BGM",
        "mix_note": "BGM is the rhythm bed and must be approved library/reference music; do not create SFX/noise beds.",
    },
    "scheme_2_source_led_tool_tutorial": {
        "music_policy": "voice_only_clean",
        "reason": "proof-heavy tool tutorials need clear narration and clean audio",
        "bgm_source_priority": [],
        "voice_policy": "required_narration",
        "voice_priority": True,
        "sfx_required": False,
        "generated_bgm_allowed": False,
        "generated_background_audio_allowed": False,
        "reference_bgm_policy": "if an approved Douyin reference explicitly requires BGM, use the same reference music or block for user approval",
        "mix_note": "Use clean narration only by default; do not add BGM or SFX/noise beds unless approved reference music is required.",
    },
    "scheme_3_ai_news_to_beginner_action": {
        "music_policy": "voice_only_clean",
        "reason": "news-to-action explainers default to clean narration; music is used only from approved library/reference tracks",
        "bgm_source_priority": ["authorized_local_library", "pixabay", "mixkit"],
        "voice_policy": "required_narration",
        "voice_priority": True,
        "sfx_required": False,
        "generated_bgm_allowed": False,
        "generated_background_audio_allowed": False,
        "reference_bgm_policy": "when a user-provided Douyin reference has BGM, use the same reference music or block for user approval; do not generate or silently substitute BGM",
        "mix_note": "Default voice_only_clean. If approved music is used, keep it roughly 18dB below narration and never mask source/date proof.",
    },
    "scheme_4_multi_skill_stack_explainer": {
        "music_policy": "voice_only_clean",
        "reason": "production-stack explainers default to clean narration; tool proof and narration stay primary",
        "bgm_source_priority": ["authorized_local_library", "pixabay", "mixkit"],
        "voice_policy": "required_narration",
        "voice_priority": True,
        "sfx_required": False,
        "generated_bgm_allowed": False,
        "generated_background_audio_allowed": False,
        "reference_bgm_policy": "when a user-provided Douyin reference has BGM, use the same reference music or block for user approval; do not generate or silently substitute BGM",
        "mix_note": "Default voice_only_clean. If approved music is used, keep it below speech; do not create noise/SFX beds.",
    },
    "scheme_5_checklist_template_poster": {
        "music_policy": "voice_only_clean",
        "reason": "checklist/template videos may be music-led when short, or narration-led when explanation is needed",
        "bgm_source_priority": ["douyin_reference", "authorized_local_library", "pixabay", "mixkit"],
        "voice_policy": "contextual",
        "voice_priority": True,
        "sfx_required": False,
        "generated_bgm_allowed": False,
        "generated_background_audio_allowed": False,
        "reference_bgm_policy": "when a user-provided Douyin reference has BGM, use the same reference music or block for user approval; do not generate or silently substitute BGM",
        "mix_note": "Short poster mode may use approved music; narrated mode defaults to clean voice only.",
    },
    "scheme_6_operation_proof_short": {
        "music_policy": "voice_only_clean",
        "reason": "operation proof shorts need terminal/browser/test evidence and clean narration/captions",
        "bgm_source_priority": [],
        "voice_policy": "optional_narration",
        "voice_priority": True,
        "sfx_required": False,
        "generated_bgm_allowed": False,
        "generated_background_audio_allowed": False,
        "reference_bgm_policy": "operation-proof shorts default to no BGM; if an approved Douyin reference requires BGM, use the same reference music or block",
        "mix_note": "Use clean narration/captions; avoid music over terminal/browser evidence and do not create SFX/noise beds.",
    },
    "scheme_7_ai_hot_rank_top5": {
        "music_policy": "required_bgm",
        "reason": "hot-rank countdown videos need BGM for ranking rhythm, row locks, and final number-one emphasis",
        "bgm_source_priority": ["douyin_reference", "authorized_local_library", "pixabay", "mixkit"],
        "voice_policy": "optional_short_narration",
        "voice_priority": False,
        "sfx_required": False,
        "generated_bgm_allowed": False,
        "generated_background_audio_allowed": False,
        "reference_bgm_policy": "when a user-provided Douyin reference has BGM, use the same reference music or block for user approval; do not generate or silently substitute BGM",
        "mix_note": "Approved BGM drives countdown energy; voice, if present, stays short and ducked above the music. Do not create SFX/noise beds.",
    },
}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists() or path.stat().st_size == 0:
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def compact_json_text(path: Path | None) -> str:
    if not path:
        return ""
    if not path.exists():
        return ""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return path.read_text(encoding="utf-8")
    return json.dumps(data, ensure_ascii=False)


def topic_blob(args: argparse.Namespace) -> str:
    parts = [
        args.topic or "",
        compact_json_text(Path(args.selected_topic)) if args.selected_topic else "",
        compact_json_text(Path(args.copy_json)) if args.copy_json else "",
        compact_json_text(Path(args.reference_analysis)) if args.reference_analysis else "",
    ]
    return " ".join(part for part in parts if part).lower()


def stable_rng(text: str, seed: str | None) -> random.Random:
    raw = seed or hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    return random.Random(raw)


def has_any(text: str, terms: list[str]) -> bool:
    return any(term.lower() in text for term in terms)


def choose_scheme(text: str) -> str:
    if has_any(text, ["三个", "3个", "multi", "stack", "生产栈", "插件", "skills", "skill"]) and has_any(
        text, ["协作", "组合", "组成", "推荐", "工具", "生产栈", "拉开", "段位", "workflow", "工作流"]
    ):
        return "scheme_4_multi_skill_stack_explainer"
    skill_terms = ["skill", "skills", "插件", "工具"]
    skill_list_terms = [
        "top5",
        "top 5",
        "top five",
        "五个",
        "5个",
        "8个",
        "10个",
        "清单",
        "推荐",
        "先学",
        "先装",
        "必备",
        "用途",
        "功能介绍",
        "能达到什么目的",
    ]
    current_news_terms = ["热榜", "新闻", "热点", "更新", "发布", "新增", "release"]
    if has_any(text, skill_terms) and has_any(text, skill_list_terms) and not has_any(text, current_news_terms):
        return "scheme_1_skill_recommendation_no_voice"
    if has_any(text, ["无人声", "no voice", "9:16", "1080x1920", "竖屏"]) and has_any(
        text, ["skill", "skills", "工具", "插件", "清单", "推荐"]
    ):
        return "scheme_1_skill_recommendation_no_voice"
    if has_any(text, ["top5", "top 5", "top five", "热榜", "榜单", "排行", "排名", "五个", "5个"]) and has_any(
        text, ["ai", "人工智能", "openai", "chatgpt", "gemini", "codex", "模型", "工具"]
    ):
        return "scheme_7_ai_hot_rank_top5"
    if has_any(text, ["新闻", "发布", "新增", "更新", "release", "official", "官方", "gemini", "openai", "chatgpt"]):
        return "scheme_3_ai_news_to_beginner_action"
    if has_any(text, ["避坑", "错误", "别再", "不要", "对比", "模板", "清单", "checklist", "mistake"]):
        return "scheme_5_checklist_template_poster"
    if has_any(text, ["终端", "测试", "lint", "build", "文件", "memory", "agents.md", "点击", "操作", "proof"]):
        return "scheme_6_operation_proof_short"
    return "scheme_2_source_led_tool_tutorial"


def select_cards(cards: list[dict[str, Any]], scheme_id: str, text: str, rng: random.Random) -> list[dict[str, Any]]:
    scheme_cards = [card for card in cards if scheme_id in card.get("scheme_ids", [])]
    if not scheme_cards:
        scheme_cards = cards[:]

    weighted: list[tuple[int, dict[str, Any]]] = []
    for card in scheme_cards:
        score = 1
        for term in card.get("use_when", []):
            if str(term).lower() in text:
                score += 3
        if "金属" in text or "metal" in text or "科技" in text:
            if "titanium" in str(card.get("visual_family", "")).lower() or "metal" in str(card.get("material", "")).lower():
                score += 4
        if scheme_id == "scheme_7_ai_hot_rank_top5" and card.get("id") == "ai_hot_rank_top5_vertical":
            score += 8
        weighted.append((score, card))
    weighted.sort(key=lambda item: (-item[0], item[1].get("id", "")))

    selected = [weighted[0][1]]
    compatible = [item[1] for item in weighted[1:] if item[0] >= 2]
    if compatible:
        selected.append(rng.choice(compatible))
    if len(selected) == 1:
        universal = next((card for card in cards if card.get("id") == "enterprise_titanium_ai_control_console"), None)
        if universal and universal.get("id") != selected[0].get("id"):
            selected.append(universal)
    return selected[:2]


def select_components(registry: dict[str, Any], scheme_id: str, rng: random.Random) -> list[dict[str, Any]]:
    components = [item for item in registry.get("components", []) if scheme_id in item.get("schemes", [])]
    by_role: dict[str, list[dict[str, Any]]] = {}
    for component in components:
        by_role.setdefault(str(component.get("role", "misc")), []).append(component)

    role_order = ["hook", "ranking", "source", "operation", "proof", "tool_value", "system_map", "comparison", "checklist", "memory", "final"]
    selected: list[dict[str, Any]] = []
    for role in role_order:
        options = by_role.get(role, [])
        if not options:
            continue
        selected.append(rng.choice(options))
        if len(selected) >= 5:
            break

    if len(selected) < 4:
        for component in components:
            if component not in selected:
                selected.append(component)
            if len(selected) >= 4:
                break
    return selected


def why_not_other_schemes(selected_scheme: str) -> list[str]:
    reasons: list[str] = []
    for scheme_id, scheme in SCHEMES.items():
        if scheme_id == selected_scheme:
            continue
        reasons.append(f"{scheme['name']} not selected because the current content job is better served by {SCHEMES[selected_scheme]['name']}.")
    return reasons[:4]


def select_audio_music_decision(scheme_id: str, text: str) -> dict[str, Any]:
    decision = dict(MUSIC_DECISIONS[scheme_id])
    lowered = text.lower()
    if has_any(lowered, ["参考音乐", "同款音乐", "bgm", "music-led", "音乐驱动", "节奏感"]) and decision["music_policy"] != "no_bgm":
        decision["music_policy"] = "required_bgm"
        decision["reason"] += "; reference/topic text indicates music-led pacing"
    if has_any(lowered, ["不要音乐", "无音乐", "no bgm", "no music"]):
        decision["music_policy"] = "voice_only_clean"
        decision["bgm_source_priority"] = []
        decision["reason"] += "; explicit no-music request overrides the default"
    decision["decision_artifact"] = "audio_music_decision"
    return decision


def build_outputs(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    text = topic_blob(args)
    if not text.strip():
        text = "AI knowledge video"
    rng = stable_rng(text, args.seed)
    scheme_id = choose_scheme(text)
    cards_data = load_json(Path(args.style_cards), {"cards": []})
    registry = load_json(Path(args.component_registry), {"components": [], "motion_primitives": []})
    cards = select_cards(cards_data.get("cards", []), scheme_id, text, rng)
    components = select_components(registry, scheme_id, rng)
    primary_card = cards[0] if cards else {}
    motion_palette = list(dict.fromkeys(motion for item in components for motion in item.get("motion", [])))
    if len(motion_palette) < 3:
        motion_palette = [item.get("id") for item in registry.get("motion_primitives", [])][:5]

    scheme = SCHEMES[scheme_id]
    audio_music_decision = select_audio_music_decision(scheme_id, text)
    component_mix = [
        {
            "id": component.get("id"),
            "role": component.get("role"),
            "visual_shape": component.get("visual_shape"),
            "motion": component.get("motion", []),
            "caption_family": component.get("caption_family"),
        }
        for component in components
    ]
    forbidden = sorted(
        {
            "original frames",
            "original subtitles",
            "original wording",
            "original voice",
            "creator identity",
            "watermark",
            "full shot sequence",
            *(rule for card in cards for rule in card.get("do_not_copy", [])),
        }
    )
    selected_card_ids = [str(card.get("id")) for card in cards if card.get("id")]
    director = {
        "status": "passed",
        "selector": "scripts/select_video_style.py",
        "content_job_lock": scheme["content_job"],
        "scheme": {
            "id": scheme_id,
            "name": scheme["name"],
            "format": scheme["format"],
        },
        "reference_policy": {
            "selected_reference_cards": selected_card_ids,
            "reference_scope": "learn pacing, density, layout logic, component grammar, and audio relationship only",
            "forbidden_copying": forbidden,
            "latest_reference_is_not_default": True,
        },
        "visual_system": {
            "selected_card_id": primary_card.get("id", "enterprise_titanium_ai_control_console"),
            "visual_family": primary_card.get("visual_family", "enterprise_titanium_control_console"),
            "background_style_id": primary_card.get("background_style_id", "BG_STYLE_TITANIUM_NEURAL_CORE"),
            "palette": primary_card.get("palette", []),
            "material": primary_card.get("material", []),
            "single_video_style_lock": True,
            "inheritance_rule": "background, panels, captions, transitions, glow, and SFX inherit this one visual family for the full video",
        },
        "component_mix": component_mix,
        "motion_palette": motion_palette,
        "audio_music_decision": audio_music_decision,
        "cooldown_policy": {
            "style_repeat_limit": "do not reuse the same reference card as the only style on the next two videos",
            "component_repeat_limit": "avoid using the same lead component in three consecutive videos",
            "per_scene_random_backgrounds": "forbidden",
        },
        "why_selected": (
            f"Selected {scheme['name']} because the topic signals match the content job: {scheme['content_job']}. "
            "The selected visual card is a candidate style system, not a copied reference."
        ),
        "why_not_other_schemes": why_not_other_schemes(scheme_id),
        "required_next_artifacts": [
            "hook_variants.json",
            "hook_score_report.json",
            "reference_overfit_audit.json",
            "visual_style_decision.json",
            "visual_style_plan.json",
        ],
    }
    recipe = {
        "status": "passed",
        "selected_visual_family": director["visual_system"]["visual_family"],
        "background_style_id": director["visual_system"]["background_style_id"],
        "component_ids": [str(item.get("id")) for item in component_mix if item.get("id")],
        "motion_primitives": motion_palette,
        "caption_template_family": "metallic_glass_safe_zone_captions",
        "transition_language": "one restrained data-light rail transition, 10-14 frames, no flash and no narration interruption",
        "sfx_character": "soft panel settle, subtle digital tick, light scanner sweep, short clean lock click, low pulse below narration",
        "audio_music_decision": audio_music_decision,
        "cooldown": director["cooldown_policy"],
        "style_inheritance": director["visual_system"]["inheritance_rule"],
    }
    return director, recipe


def main() -> int:
    parser = argparse.ArgumentParser(description="Select AI video director style and component recipe.")
    parser.add_argument("--topic", default="", help="Plain topic text")
    parser.add_argument("--selected-topic", help="selected_topic.json path")
    parser.add_argument("--copy-json", help="copy_package.json path")
    parser.add_argument("--reference-analysis", help="reference analysis JSON path")
    parser.add_argument("--style-cards", default=str(DEFAULT_STYLE_CARDS))
    parser.add_argument("--component-registry", default=str(DEFAULT_COMPONENT_REGISTRY))
    parser.add_argument("--out", required=True, help="director_selection.json")
    parser.add_argument("--style-out", required=True, help="style_recipe.json")
    parser.add_argument("--seed", help="Optional deterministic seed")
    args = parser.parse_args()

    director, recipe = build_outputs(args)
    out = Path(args.out)
    style_out = Path(args.style_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    style_out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(director, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    style_out.write_text(json.dumps(recipe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "scheme": director["scheme"], "style": recipe["selected_visual_family"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
