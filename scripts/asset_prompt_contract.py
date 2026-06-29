"""Shared visual prompt contract for generated AI video assets."""

from __future__ import annotations

import re
from typing import Any


BACKGROUND_SEMANTIC_REQUIRED_FIELDS = (
    "visual_thesis",
    "topic_binding",
    "information_job",
    "background_role",
)
BACKGROUND_SEMANTIC_MIN_CHARS = {
    "visual_thesis": 24,
    "topic_binding": 24,
    "information_job": 24,
    "background_role": 16,
}
VISUAL_DIRECTOR_REQUIRED_FIELDS = (
    "scene_id",
    "narration_line_supported",
    "scene_function",
    "visual_archetype",
    "brightness_grade",
    "palette_family",
    "material_family",
    "layout_family",
    "energy_level",
    "visual_thesis",
    "topic_binding",
    "beginner_usefulness",
    "information_job",
    "viewer_takeaway",
    "composition",
    "foreground",
    "midground",
    "background",
    "camera_lens",
    "lighting",
    "material_texture",
    "color_hierarchy",
    "color_system",
    "depth_layering",
    "text_safe_zones",
    "motion_usage",
    "animation_affordance",
    "primary_animated_object",
    "dark_light_motion_rule",
    "negative_prompt",
    "regeneration_criteria",
    "diversity_check",
)
VISUAL_DIRECTOR_MIN_CHARS = {
    "scene_id": 2,
    "narration_line_supported": 16,
    "scene_function": 8,
    "visual_archetype": 10,
    "brightness_grade": 8,
    "palette_family": 10,
    "material_family": 10,
    "layout_family": 10,
    "energy_level": 10,
    "visual_thesis": 24,
    "topic_binding": 24,
    "beginner_usefulness": 20,
    "information_job": 24,
    "viewer_takeaway": 18,
    "composition": 32,
    "foreground": 20,
    "midground": 20,
    "background": 20,
    "camera_lens": 16,
    "lighting": 20,
    "material_texture": 20,
    "color_hierarchy": 20,
    "color_system": 40,
    "depth_layering": 24,
    "text_safe_zones": 20,
    "motion_usage": 24,
    "animation_affordance": 24,
    "primary_animated_object": 12,
    "dark_light_motion_rule": 24,
    "negative_prompt": 28,
    "regeneration_criteria": 28,
    "diversity_check": 24,
}
GENERIC_BACKGROUND_BINDING_VALUES = {
    "premium information stage",
    "calm premium information stage",
    "quiet stage",
    "premium tech background",
    "高级科技感背景",
    "高级背景",
    "科技感背景",
}
GENERIC_VISUAL_PROMPT_VALUES = {
    "高级",
    "高级感",
    "高级科技感",
    "高级科技感背景",
    "科技感",
    "科技感背景",
    "未来感",
    "赛博",
    "赛博霓虹",
    "酷炫",
    "炫酷",
    "震撼",
    "真实感",
    "设计感",
    "4k",
    "8k",
    "cinematic",
    "premium",
    "premium tech",
    "premium tech background",
    "futuristic",
    "cyberpunk",
    "high quality",
    "ultra detailed",
    "cool background",
    "awesome background",
}
GENERIC_PROMPT_PHRASES = {
    "高级一点",
    "随便高级",
    "做高级",
    "更炫",
    "更酷",
    "爆款",
    "大片感",
    "high quality",
    "ultra detailed",
    "trending on artstation",
    "cinematic 4k",
    "premium tech background",
    "futuristic ai dashboard",
    "cinematic cyber interface",
    "abstract digital technology background",
}
FORBIDDEN_UNUSED_BACKGROUND_STRUCTURE_TERMS = {
    "skeleton stage",
    "layout skeleton",
    "visual skeleton",
    "workflow skeleton",
    "background skeleton",
    "source wall skeleton",
    "placeholder framework",
    "placeholder card",
    "placeholder cards",
    "unused rail",
    "unused rails",
    "empty ui slot",
    "empty ui slots",
    "wireframe background",
    "占位卡槽",
    "占位框架",
    "流程线框",
    "流程骨架",
    "背景骨架",
    "无用骨架",
    "线框骨架",
}
BACKGROUND_STRUCTURE_NEGATION_TERMS = {
    "skeleton free",
    "skeleton-free",
    "no skeleton",
    "without skeleton",
    "without workflow skeleton",
    "no workflow skeleton",
    "no placeholder",
    "without placeholder",
    "no unused",
    "without unused",
    "no wireframe",
    "without wireframe",
    "无骨架",
    "不要骨架",
    "不使用骨架",
    "无占位",
    "不要占位",
    "不使用占位",
}
BACKGROUND_STRUCTURE_FIELDS = (
    "visual_thesis",
    "information_job",
    "background_role",
    "viewer_takeaway",
    "composition",
    "foreground",
    "midground",
    "background",
    "depth_layering",
    "motion_usage",
    "animation_affordance",
    "primary_animated_object",
)
FORBIDDEN_DECORATIVE_TECH_CLICHE_TERMS = {
    "robot face",
    "generic robot",
    "robot mascot",
    "full-frame circuit board",
    "full frame circuit board",
    "circuit board wallpaper",
    "complex hud",
    "dense hud",
    "hud dashboard",
    "dense code",
    "cheap neon",
    "game ui",
    "机器人脸",
    "机器人头像",
    "机器人吉祥物",
    "堆满电路板",
    "满屏电路板",
    "电路板铺满",
    "复杂 hud",
    "复杂HUD",
    "大量代码",
    "廉价霓虹",
    "游戏界面",
}
DECORATIVE_TECH_CLICHE_NEGATION_TERMS = {
    "no robot",
    "not a robot",
    "without robot",
    "avoid robot",
    "no circuit",
    "without circuit",
    "avoid circuit",
    "no hud",
    "without hud",
    "avoid hud",
    "no dense code",
    "without dense code",
    "avoid dense code",
    "no cheap neon",
    "without cheap neon",
    "avoid cheap neon",
    "no game ui",
    "without game ui",
    "avoid game ui",
    "无机器人",
    "不要机器人",
    "避免机器人",
    "无电路板",
    "不要电路板",
    "避免电路板",
    "无 hud",
    "不要 hud",
    "避免 hud",
    "无HUD",
    "不要HUD",
    "避免HUD",
    "不要大量代码",
    "避免大量代码",
    "不要廉价霓虹",
    "避免廉价霓虹",
    "不要游戏界面",
    "避免游戏界面",
}
DECORATIVE_TECH_CLICHE_FIELDS = (
    "visual_thesis",
    "viewer_takeaway",
    "composition",
    "foreground",
    "midground",
    "background",
    "lighting",
    "material_texture",
    "color_hierarchy",
    "color_system",
    "depth_layering",
    "motion_usage",
)
PROMPT_MARKER_GROUPS = {
    "asset role": ("asset role", "asset_role", "素材角色", "资产角色"),
    "scene id": ("scene id", "scene_id", "场景"),
    "narration": ("narration line", "narration_line_supported", "口播"),
    "scene function": ("scene function", "scene_function", "镜头功能", "场景功能"),
    "visual archetype": ("visual archetype", "visual_archetype", "视觉原型", "视觉类型"),
    "brightness grade": ("brightness grade", "brightness_grade", "明暗等级", "亮度等级"),
    "palette family": ("palette family", "palette_family", "色彩方案", "调色家族"),
    "material family": ("material family", "material_family", "材质家族"),
    "layout family": ("layout family", "layout_family", "布局家族"),
    "energy level": ("energy level", "energy_level", "情绪能量"),
    "visual thesis": ("visual thesis", "visual_thesis", "视觉命题"),
    "topic binding": ("topic binding", "topic_binding", "主题绑定"),
    "beginner usefulness": ("beginner usefulness", "beginner_usefulness", "小白价值", "新手价值"),
    "information job": ("information job", "information_job", "信息任务"),
    "viewer takeaway": ("viewer takeaway", "viewer_takeaway", "观众理解"),
    "composition": ("composition", "构图", "画面结构"),
    "foreground": ("foreground", "前景"),
    "midground": ("midground", "中景"),
    "background": ("background", "背景"),
    "camera": ("camera", "lens", "镜头", "机位"),
    "lighting": ("lighting", "light", "光线", "灯光"),
    "material": ("material", "texture", "材质", "纹理"),
    "color": ("color hierarchy", "color", "色彩"),
    "color system": ("color system", "color_system", "色彩系统"),
    "depth layering": ("depth/layering", "depth layering", "depth_layering", "层次", "空间层"),
    "text safe": ("text-safe", "text safe", "safe zone", "字幕安全", "安全区"),
    "motion": ("motion usage", "motion", "animation", "动效", "运动"),
    "animation affordance": ("animation affordance", "可动层", "分层运动"),
    "primary animated object": ("primary animated object", "primary_animated_object", "主运动对象"),
    "dark light motion rule": ("dark/light motion rule", "dark_light_motion_rule", "明暗运动规则"),
    "evidence boundary": ("evidence boundary", "证据边界", "not evidence", "非证据"),
    "negative": ("negative", "avoid", "no ", "避免", "负面"),
    "regeneration": ("regeneration", "regenerate", "重生成", "返工"),
    "diversity check": ("diversity check", "diversity_check", "多样性检查"),
}
NORMALIZED_GENERIC_BACKGROUND_BINDING_VALUES: set[str] = set()
NORMALIZED_GENERIC_VISUAL_PROMPT_VALUES: set[str] = set()


def normalized_text(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", " ").replace("_", " ")


def compact_text(value: Any) -> str:
    return re.sub(r"\s+", " ", normalized_text(value))


NORMALIZED_GENERIC_BACKGROUND_BINDING_VALUES = {compact_text(item) for item in GENERIC_BACKGROUND_BINDING_VALUES}
NORMALIZED_GENERIC_VISUAL_PROMPT_VALUES = {compact_text(item) for item in GENERIC_VISUAL_PROMPT_VALUES}


def is_generic_visual_prompt_value(value: Any) -> bool:
    text = compact_text(value)
    if not text:
        return False
    if text in NORMALIZED_GENERIC_VISUAL_PROMPT_VALUES:
        return True
    return len(text) <= 30 and any(term in text for term in NORMALIZED_GENERIC_VISUAL_PROMPT_VALUES)


def field_pattern(key: str) -> re.Pattern[str]:
    relaxed = re.escape(key).replace("_", r"[_\s/-]?")
    return re.compile(rf"(?im)^\s*{relaxed}\s*[:：]\s*(.+)$")


def get_field(card: str, key: str) -> str:
    match = field_pattern(key).search(card)
    return match.group(1).strip() if match else ""


def split_prompt_cards(text: str) -> list[str]:
    parts = re.split(r"(?m)^##\s+", text)
    if len(parts) > 1:
        parts = parts[1:]
    return [part.strip() for part in parts if part.strip()]


def background_semantic_binding_issues(asset: dict[str, Any], asset_label: str | None = None) -> list[str]:
    asset_id = asset_label or str(asset.get("asset_id") or "unknown")
    issues: list[str] = []
    for key in BACKGROUND_SEMANTIC_REQUIRED_FIELDS:
        value = str(asset.get(key, "")).strip()
        if not value:
            issues.append(f"{asset_id}: background_plate must document {key} so the generated background is bound to the selected topic")
            continue
        if len(value) < BACKGROUND_SEMANTIC_MIN_CHARS[key]:
            issues.append(f"{asset_id}: background_plate {key} is too vague; describe the topic-specific information job")
        if compact_text(value) in NORMALIZED_GENERIC_BACKGROUND_BINDING_VALUES:
            issues.append(f"{asset_id}: background_plate {key} is generic; it must describe the actual AI topic, not only a premium stage")
    return issues


def prompt_text_marker_issues(prompt_text: str, asset_id: str) -> list[str]:
    if not prompt_text.strip():
        return []
    prompt_text_lower = prompt_text.lower()
    missing = [
        marker
        for marker, alternatives in PROMPT_MARKER_GROUPS.items()
        if not any(alternative in prompt_text_lower for alternative in alternatives)
    ]
    if not missing:
        return []
    return [f"{asset_id}: prompt card is missing visual description sections: {', '.join(missing)}"]


def generic_phrase_issues(text: str, asset_id: str) -> list[str]:
    compact_surface = compact_text(text)
    for phrase in GENERIC_PROMPT_PHRASES:
        normalized_phrase = compact_text(phrase)
        if normalized_phrase and normalized_phrase in compact_surface:
            return [f"{asset_id}: prompt uses vague material phrase `{phrase}`; rewrite as a concrete visual director brief"]
    return []


def unused_background_structure_issues(asset: dict[str, Any], asset_id: str) -> list[str]:
    for key in BACKGROUND_STRUCTURE_FIELDS:
        value = str(asset.get(key, "")).strip()
        if not value:
            continue
        surface = compact_text(value)
        if any(compact_text(term) in surface for term in BACKGROUND_STRUCTURE_NEGATION_TERMS):
            continue
        for term in FORBIDDEN_UNUSED_BACKGROUND_STRUCTURE_TERMS:
            normalized_term = compact_text(term)
            if normalized_term and normalized_term in surface:
                return [
                    f"{asset_id}: background field {key} describes an unused visual skeleton `{term}`; use premium atmosphere, material, light, depth, and negative space unless foreground elements actually use the structure"
                ]
    return []


def decorative_tech_cliche_issues(asset: dict[str, Any], asset_id: str) -> list[str]:
    for key in DECORATIVE_TECH_CLICHE_FIELDS:
        value = str(asset.get(key, "")).strip()
        if not value:
            continue
        surface = compact_text(value)
        if any(compact_text(term) in surface for term in DECORATIVE_TECH_CLICHE_NEGATION_TERMS):
            continue
        for term in FORBIDDEN_DECORATIVE_TECH_CLICHE_TERMS:
            normalized_term = compact_text(term)
            if normalized_term and normalized_term in surface:
                return [
                    f"{asset_id}: background field {key} uses low-trust decorative tech cliché `{term}`; use abstract intelligence elements, material, light, depth, and negative space instead"
                ]
    return []


def visual_director_prompt_issues(
    asset: dict[str, Any],
    prompt_text: str = "",
    asset_label: str | None = None,
) -> list[str]:
    asset_id = asset_label or str(asset.get("asset_id") or "unknown")
    issues: list[str] = []
    for key in VISUAL_DIRECTOR_REQUIRED_FIELDS:
        value = str(asset.get(key, "")).strip()
        if not value:
            issues.append(f"{asset_id}: generated_visual must document visual director field {key}")
            continue
        if len(value) < VISUAL_DIRECTOR_MIN_CHARS[key]:
            issues.append(f"{asset_id}: visual director field {key} is too short; describe the image's concrete information job and shot design")
        if key != "negative_prompt" and is_generic_visual_prompt_value(value):
            issues.append(f"{asset_id}: visual director field {key} is generic; replace taste words with concrete shot design")

    prompt_surface = "\n".join(
        [prompt_text]
        + [str(asset.get(key, "")) for key in VISUAL_DIRECTOR_REQUIRED_FIELDS]
        + [str(asset.get("source", "")), str(asset.get("source_note", "")), str(asset.get("qa_notes", ""))]
    )
    issues.extend(generic_phrase_issues(prompt_surface, asset_id))
    issues.extend(unused_background_structure_issues(asset, asset_id))
    issues.extend(decorative_tech_cliche_issues(asset, asset_id))
    issues.extend(prompt_text_marker_issues(prompt_text, asset_id))
    if compact_text(asset.get("motion_usage")) == compact_text(asset.get("animation_affordance")):
        issues.append(f"{asset_id}: motion_usage and animation_affordance must not be duplicated; one explains HyperFrames use, the other explains animatable layers/zones")
    return issues


def card_to_asset_fields(card: str, index: int) -> dict[str, Any]:
    field_aliases = {
        "scene_id": ("Scene ID", "scene_id"),
        "narration_line_supported": ("Narration line supported", "narration_line_supported"),
        "scene_function": ("Scene function", "scene_function"),
        "visual_archetype": ("Visual archetype", "visual_archetype"),
        "brightness_grade": ("Brightness grade", "brightness_grade"),
        "palette_family": ("Palette family", "palette_family"),
        "material_family": ("Material family", "material_family"),
        "layout_family": ("Layout family", "layout_family"),
        "energy_level": ("Energy level", "energy_level"),
        "visual_thesis": ("Visual thesis", "visual_thesis"),
        "topic_binding": ("Topic binding", "topic_binding"),
        "beginner_usefulness": ("Beginner usefulness", "beginner_usefulness"),
        "information_job": ("Information job", "information_job"),
        "background_role": ("Background role", "Support role", "background_role"),
        "viewer_takeaway": ("Viewer takeaway", "viewer_takeaway"),
        "composition": ("Composition",),
        "foreground": ("Foreground",),
        "midground": ("Midground",),
        "background": ("Background",),
        "camera_lens": ("Camera/lens", "Camera / lens", "Camera"),
        "lighting": ("Lighting",),
        "material_texture": ("Material/texture", "Material / texture", "Material", "Texture"),
        "color_hierarchy": ("Color hierarchy", "Color"),
        "color_system": ("Color system", "color_system"),
        "depth_layering": ("Depth/layering", "Depth layering", "depth_layering"),
        "text_safe_zones": ("Text-safe zones", "Text safe zones", "Text-safe", "Safe zones"),
        "motion_usage": ("Motion usage in HyperFrames", "Motion usage", "Motion plan"),
        "animation_affordance": ("Animation affordance",),
        "primary_animated_object": ("Primary animated object", "primary_animated_object"),
        "dark_light_motion_rule": ("Dark/light motion rule", "dark_light_motion_rule"),
        "evidence_boundary": ("Evidence boundary",),
        "negative_prompt": ("Negative prompt", "Avoid"),
        "regeneration_criteria": ("Regeneration criteria",),
        "diversity_check": ("Diversity check", "diversity_check"),
    }
    fields: dict[str, Any] = {"asset_id": f"PROMPT-{index:02d}"}
    for key, aliases in field_aliases.items():
        for alias in aliases:
            value = get_field(card, alias)
            if value:
                fields[key] = value
                break
    return fields


def validate_prompt_card(card: str, index: int) -> list[str]:
    asset_id = f"PROMPT-{index:02d}"
    fields = card_to_asset_fields(card, index)
    issues = visual_director_prompt_issues(fields, card, asset_id)
    has_horizontal_format = re.search(r"1920\s*x\s*1080|16:9", card, re.I)
    has_vertical_reference_exception = re.search(
        r"1080\s*x\s*1920|9:16|reference_driven_lightweight_vertical|reference-driven lightweight vertical",
        card,
        re.I,
    )
    if not (has_horizontal_format or has_vertical_reference_exception):
        issues.append(f"{asset_id}: prompt card must document 16:9 / 1920x1080 or an approved 9:16 reference-driven lightweight vertical exception")
    if not re.search(r"text-free|无文字|不要文字|no text", card, re.I):
        issues.append(f"{asset_id}: prompt card must document text-free or no baked-in text when used as generated support art")
    return issues


def validate_prompt_pack_text(text: str, min_cards: int = 1) -> dict[str, Any]:
    cards = split_prompt_cards(text)
    issues: list[str] = []
    warnings: list[str] = []
    if len(cards) < min_cards:
        issues.append(f"need at least {min_cards} visual prompt card(s), got {len(cards)}")
    for index, card in enumerate(cards, start=1):
        issues.extend(validate_prompt_card(card, index))
    return {
        "status": "passed" if not issues else "failed",
        "prompt_card_count": len(cards),
        "validated_fields": list(VISUAL_DIRECTOR_REQUIRED_FIELDS),
        "blocking_issues": issues,
        "warnings": warnings,
    }
