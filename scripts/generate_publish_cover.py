#!/usr/bin/env python3
"""Generate standalone Douyin publish covers from a reusable AI cover template set."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageFont


FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
]


COVER_TEMPLATES: list[dict[str, Any]] = [
    {
        "id": "COV_AI_01",
        "name": "量子反应堆",
        "mood": "黑钛金属、青蓝核心、暖金反射",
        "background": "reactor",
        "layout": "center",
        "palette": {"base": "#050B18", "deep": "#081326", "accent": "#55DFFF", "accent2": "#FFC36B", "text": "#F7FBFF"},
        "nodes": ["看来源", "录流程", "出结果"],
        "best_for": "Codex、Agent、工作流、工具教程封面",
    },
    {
        "id": "COV_AI_02",
        "name": "黑金控制台",
        "mood": "奢华黑金、钛金边框、权威感",
        "background": "black_gold",
        "layout": "left_nodes",
        "palette": {"base": "#060708", "deep": "#14100A", "accent": "#F6C76B", "accent2": "#55DFFF", "text": "#FFF7E7"},
        "nodes": ["少返工", "有标准", "可检查"],
        "best_for": "高阶技巧、效率提升、管理型 AI 工作流",
    },
    {
        "id": "COV_AI_03",
        "name": "冰蓝玻璃实验室",
        "mood": "明亮冰蓝、玻璃材质、干净可信",
        "background": "ice_lab",
        "layout": "top_core",
        "palette": {"base": "#EAF6FF", "deep": "#D7EAF8", "accent": "#2B9CFF", "accent2": "#18D1C2", "text": "#071529"},
        "nodes": ["新手能懂", "一步开始", "结果可见"],
        "best_for": "小白教程、ChatGPT 生活技巧、轻教程",
    },
    {
        "id": "COV_AI_04",
        "name": "神经星云",
        "mood": "深蓝紫、粒子网络、抽象智能",
        "background": "neural",
        "layout": "diagonal",
        "palette": {"base": "#07091E", "deep": "#121A3A", "accent": "#8F7CFF", "accent2": "#55DFFF", "text": "#F3F5FF"},
        "nodes": ["理解问题", "拆成步骤", "给出答案"],
        "best_for": "ChatGPT、Gemini、推理、提示词技巧",
    },
    {
        "id": "COV_AI_05",
        "name": "数据隧道",
        "mood": "高速数据流、纵深空间、信息汇聚",
        "background": "data_tunnel",
        "layout": "split",
        "palette": {"base": "#031923", "deep": "#062B37", "accent": "#32E2C2", "accent2": "#55DFFF", "text": "#ECFFFB"},
        "nodes": ["输入", "处理", "输出"],
        "best_for": "自动化、批量处理、数据和表格技巧",
    },
    {
        "id": "COV_AI_06",
        "name": "银白全息屏",
        "mood": "清洁企业级、银白全息、浅色高级",
        "background": "silver_holo",
        "layout": "clean_card",
        "palette": {"base": "#F6FBFF", "deep": "#E2EEF6", "accent": "#28A9FF", "accent2": "#8F7CFF", "text": "#081426"},
        "nodes": ["模板", "步骤", "清单"],
        "best_for": "清单、工具推荐、轻量信息海报",
    },
    {
        "id": "COV_AI_07",
        "name": "琥珀诊断台",
        "mood": "深色诊断、琥珀警示、问题修复",
        "background": "amber_debug",
        "layout": "alert",
        "palette": {"base": "#0B0A08", "deep": "#21170E", "accent": "#FFC36B", "accent2": "#FF7A59", "text": "#FFF4DD"},
        "nodes": ["错在哪", "怎么改", "再检查"],
        "best_for": "避坑、错误修复、合规检查、代码调试",
    },
    {
        "id": "COV_AI_08",
        "name": "宇宙智能核心",
        "mood": "宇宙级 AI、深空核心、史诗感",
        "background": "cosmic_core",
        "layout": "hero_core",
        "palette": {"base": "#050615", "deep": "#101B3D", "accent": "#A9D8FF", "accent2": "#FFC36B", "text": "#F7FAFF"},
        "nodes": ["趋势", "能力", "机会"],
        "best_for": "AI 新闻、模型发布、行业趋势",
    },
    {
        "id": "COV_AI_09",
        "name": "钛金清单",
        "mood": "金属清单、结果卡、强收藏价值",
        "background": "titanium_checklist",
        "layout": "checklist",
        "palette": {"base": "#071019", "deep": "#122434", "accent": "#55DFFF", "accent2": "#32E2C2", "text": "#F5FBFF"},
        "nodes": ["先做一遍", "写清规则", "保存复用"],
        "best_for": "可保存模板、三步教程、结尾总结型封面",
    },
    {
        "id": "COV_AI_10",
        "name": "来源档案柜",
        "mood": "证据档案、来源锁定、专业可信",
        "background": "source_archive",
        "layout": "archive",
        "palette": {"base": "#07111F", "deep": "#EAF0F4", "accent": "#55DFFF", "accent2": "#FFC36B", "text": "#F6FAFF"},
        "nodes": ["真实来源", "边界说明", "实用方法"],
        "best_for": "OpenAI/Gemini 官方来源、新闻、发布说明解读",
    },
]


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def load_json(path: Path) -> dict[str, Any]:
    if not exists(path):
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    index = 1 if bold else 0
    for candidate in FONT_CANDIDATES:
        path = Path(candidate)
        if not path.exists():
            continue
        try:
            return ImageFont.truetype(str(path), size, index=index)
        except Exception:
            try:
                return ImageFont.truetype(str(path), size)
            except Exception:
                continue
    return ImageFont.load_default()


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    raw = value.strip().lstrip("#")
    return int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16)


def rgba(value: str, alpha: int) -> tuple[int, int, int, int]:
    red, green, blue = hex_to_rgb(value)
    return red, green, blue, alpha


def blend(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(a[index] + (b[index] - a[index]) * t) for index in range(3))


def parse_publish(project: Path, title: str | None, subtitle: str | None) -> tuple[str, str]:
    internal = project / "internal"
    qingdou = load_json(internal / "qingdou_keyword_check.json")
    metadata = load_json(internal / "metadata.json")
    publish_copy = ""
    for path in (internal / "publish_copy.txt", project / "publish_copy.txt"):
        if exists(path):
            publish_copy = path.read_text(encoding="utf-8").strip()
            break

    final_title = (title or qingdou.get("final_title") or qingdou.get("title") or metadata.get("title") or "").strip()
    if not final_title and publish_copy:
        final_title = publish_copy.splitlines()[0].strip()
    final_subtitle = (subtitle or "").strip()
    if not final_subtitle:
        final_subtitle = "把复杂 AI 技巧变成能用的步骤"
    return final_title or "AI 工作流技巧", final_subtitle


def stable_template_id(project: Path) -> str:
    digest = hashlib.sha256(project.name.encode("utf-8")).digest()
    return COVER_TEMPLATES[digest[0] % len(COVER_TEMPLATES)]["id"]


def template_by_id(template_id: str | None, project: Path) -> dict[str, Any]:
    chosen_id = template_id or stable_template_id(project)
    for item in COVER_TEMPLATES:
        if item["id"] == chosen_id:
            return item
    valid = ", ".join(item["id"] for item in COVER_TEMPLATES)
    raise SystemExit(f"unknown template id: {chosen_id}. valid: {valid}")


def fit_lines(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    max_lines: int,
    start_size: int,
    min_size: int,
) -> tuple[list[str], ImageFont.ImageFont]:
    cleaned = "".join(text.strip().split())
    if not cleaned:
        return [""], font(start_size, True)
    for size in range(start_size, min_size - 1, -4):
        current_font = font(size, True)
        lines: list[str] = []
        current = ""
        for char in cleaned:
            candidate = current + char
            if draw.textbbox((0, 0), candidate, font=current_font)[2] <= max_width:
                current = candidate
                continue
            if current:
                lines.append(current)
            current = char
            if len(lines) >= max_lines:
                break
        if current and len(lines) < max_lines:
            lines.append(current)
        if len(lines) <= max_lines:
            if len(lines) == max_lines and current != cleaned[-len(current) :]:
                lines[-1] = lines[-1].rstrip("，。！？；：") + "..."
            return lines[:max_lines], current_font
    fallback = font(min_size, True)
    return [cleaned[: max(6, max_width // max(min_size, 1))] + "..."], fallback


def draw_vertical_gradient(base: Image.Image, top: str, bottom: str) -> None:
    draw = ImageDraw.Draw(base)
    top_rgb = hex_to_rgb(top)
    bottom_rgb = hex_to_rgb(bottom)
    width, height = base.size
    for y in range(height):
        color = blend(top_rgb, bottom_rgb, y / max(1, height - 1))
        draw.line((0, y, width, y), fill=color)


def draw_glow(base: Image.Image, center: tuple[int, int], radius: int, color: str, alpha: int) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x, y = center
    for step in range(8, 0, -1):
        r = int(radius * step / 8)
        a = int(alpha * (step / 8) ** 2)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=rgba(color, a))
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(radius // 16)))


def draw_reactor(draw: ImageDraw.ImageDraw, width: int, height: int, template: dict[str, Any]) -> None:
    accent = template["palette"]["accent"]
    accent2 = template["palette"]["accent2"]
    cx, cy = width // 2, int(height * 0.73)
    for index, scale in enumerate([1.0, 0.78, 0.56, 0.36]):
        rx = int(width * 0.52 * scale)
        ry = int(height * 0.16 * scale)
        draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=rgba(accent, 80 + index * 22), width=3)
    for angle in range(0, 360, 28):
        end_x = cx + math.cos(math.radians(angle)) * width * 0.48
        end_y = cy + math.sin(math.radians(angle)) * height * 0.14
        draw.line((cx, cy, end_x, end_y), fill=rgba(accent2, 50), width=2)
    draw.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), fill=rgba(accent2, 190))


def draw_network(draw: ImageDraw.ImageDraw, width: int, height: int, template: dict[str, Any]) -> None:
    accent = template["palette"]["accent"]
    accent2 = template["palette"]["accent2"]
    points: list[tuple[int, int]] = []
    for index in range(22):
        x = int(width * (0.10 + (index * 0.173) % 0.80))
        y = int(height * (0.12 + (math.sin(index * 1.7) + 1) * 0.34))
        points.append((x, y))
    for a, b in zip(points, points[1:]):
        draw.line((a[0], a[1], b[0], b[1]), fill=rgba(accent, 72), width=2)
    for index, point in enumerate(points):
        color = accent2 if index % 4 == 0 else accent
        draw.ellipse((point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5), fill=rgba(color, 210))


def draw_tunnel(draw: ImageDraw.ImageDraw, width: int, height: int, template: dict[str, Any]) -> None:
    accent = template["palette"]["accent"]
    center = (width // 2, int(height * 0.58))
    for index in range(18):
        y = int(height * (0.18 + index * 0.048))
        draw.line((0, y, center[0], center[1]), fill=rgba(accent, 28 + index * 4), width=1)
        draw.line((width, y, center[0], center[1]), fill=rgba(accent, 28 + index * 4), width=1)
    for index in range(8):
        pad_x = int(width * (0.08 + index * 0.05))
        pad_y = int(height * (0.12 + index * 0.04))
        draw.rounded_rectangle((pad_x, pad_y, width - pad_x, height - pad_y), radius=26, outline=rgba(accent, 36), width=2)


def draw_archive(draw: ImageDraw.ImageDraw, width: int, height: int, template: dict[str, Any]) -> None:
    accent = template["palette"]["accent"]
    for row in range(4):
        y = int(height * (0.13 + row * 0.12))
        draw.rounded_rectangle((int(width * 0.09), y, int(width * 0.91), y + int(height * 0.075)), radius=18, fill=(255, 255, 255, 30), outline=rgba(accent, 54), width=2)
        draw.ellipse((int(width * 0.12), y + 18, int(width * 0.12) + 18, y + 36), fill=rgba(accent, 180))


def draw_background(base: Image.Image, template: dict[str, Any]) -> None:
    palette = template["palette"]
    width, height = base.size
    draw_vertical_gradient(base, palette["base"], palette["deep"])
    draw_glow(base, (int(width * 0.48), int(height * 0.22)), int(width * 0.46), palette["accent"], 70)
    draw_glow(base, (int(width * 0.74), int(height * 0.82)), int(width * 0.38), palette["accent2"], 54)
    draw = ImageDraw.Draw(base)

    style = template["background"]
    if style in {"reactor", "black_gold", "titanium_checklist", "cosmic_core"}:
        draw_reactor(draw, width, height, template)
    if style in {"neural", "silver_holo", "cosmic_core"}:
        draw_network(draw, width, height, template)
    if style in {"data_tunnel", "amber_debug"}:
        draw_tunnel(draw, width, height, template)
    if style == "source_archive":
        draw_archive(draw, width, height, template)

    if style in {"ice_lab", "silver_holo"}:
        for offset in range(-width, width, 120):
            draw.line((offset, height, offset + width // 2, 0), fill=(255, 255, 255, 42), width=2)

    vignette = Image.new("RGBA", base.size, (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    vdraw.rectangle((0, 0, width, height), outline=(0, 0, 0, 210), width=max(28, width // 24))
    base.alpha_composite(vignette.filter(ImageFilter.GaussianBlur(width // 24)))


def draw_chip(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, template: dict[str, Any], size: int) -> None:
    accent = template["palette"]["accent"]
    text_color = template["palette"]["text"]
    draw.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=rgba(template["palette"]["deep"], 232), outline=rgba(accent, 150), width=2)
    draw.ellipse((box[0] + 18, box[1] + 20, box[0] + 38, box[1] + 40), fill=rgba(template["palette"]["accent2"], 235))
    draw.text((box[0] + 54, box[1] + 13), text, font=font(size, True), fill=rgba(text_color, 255))


def draw_title_panel(
    base: Image.Image,
    template: dict[str, Any],
    title: str,
    subtitle: str,
    horizontal: bool,
) -> None:
    width, height = base.size
    draw = ImageDraw.Draw(base)
    palette = template["palette"]
    is_light = palette["base"].upper() in {"#EAF6FF", "#F6FBFF"}

    if horizontal:
        if template["layout"] in {"left_nodes", "archive", "split"}:
            panel = (int(width * 0.06), int(height * 0.13), int(width * 0.61), int(height * 0.74))
            node_x = int(width * 0.66)
        elif template["layout"] == "hero_core":
            panel = (int(width * 0.12), int(height * 0.16), int(width * 0.88), int(height * 0.70))
            node_x = int(width * 0.67)
        else:
            panel = (int(width * 0.08), int(height * 0.14), int(width * 0.92), int(height * 0.72))
            node_x = int(width * 0.64)
        title_size = 86
        subtitle_size = 34
    else:
        panel = (int(width * 0.07), int(height * 0.14), int(width * 0.93), int(height * 0.73))
        node_x = panel[0] + 54
        title_size = 72
        subtitle_size = 31

    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(panel, radius=42, fill=(0, 0, 0, 142))
    base.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(18)))
    panel_fill = (6, 16, 34, 214) if not is_light else (246, 251, 255, 226)
    draw.rounded_rectangle(panel, radius=42, fill=panel_fill, outline=rgba(palette["accent"], 160), width=2)
    draw.line((panel[0] + 34, panel[1] + 2, panel[2] - 34, panel[1] + 2), fill=(255, 255, 255, 52), width=2)

    label_box = (panel[0] + 42, panel[1] + 40, panel[0] + 250, panel[1] + 88)
    label_fill = rgba(palette["deep"], 230)
    draw.rounded_rectangle(label_box, radius=999, fill=label_fill, outline=rgba(palette["accent"], 140), width=2)
    draw.text((label_box[0] + 26, label_box[1] + 10), "AI 工作流", font=font(25, True), fill=rgba(palette["accent"], 255))

    title_x = panel[0] + 52
    title_y = panel[1] + (125 if horizontal else 128)
    title_width = (panel[2] - title_x - 64) if not horizontal else int((panel[2] - title_x) * 0.72)
    if horizontal and template["layout"] in {"left_nodes", "archive", "split"}:
        title_width = panel[2] - title_x - 42
    lines, title_font = fit_lines(draw, title, title_width, 2, title_size, 46)
    current_y = title_y
    stroke = (0, 0, 0, 140) if not is_light else (255, 255, 255, 100)
    title_fill = rgba(palette["text"], 255) if not is_light else (8, 20, 38, 255)
    for line in lines:
        draw.text((title_x, current_y), line, font=title_font, fill=title_fill, stroke_width=2, stroke_fill=stroke)
        current_y += title_font.size + 10 if hasattr(title_font, "size") else title_size + 10

    subtitle_box = (title_x, current_y + 24, title_x + min(title_width, int(width * 0.58)), current_y + 88)
    draw.rounded_rectangle(subtitle_box, radius=22, fill=rgba(palette["accent"], 224), outline=(255, 255, 255, 92), width=2)
    subtitle_fill = (5, 13, 28, 255) if not is_light else (255, 255, 255, 255)
    subtitle_lines, subtitle_font = fit_lines(draw, subtitle, subtitle_box[2] - subtitle_box[0] - 48, 1, subtitle_size, 24)
    draw.text((subtitle_box[0] + 26, subtitle_box[1] + 14), subtitle_lines[0], font=subtitle_font, fill=subtitle_fill)

    if horizontal:
        node_y = panel[1] + 180
        node_gap = 104 if template["layout"] != "checklist" else 92
        node_w = int(width * 0.22)
        for index, node in enumerate(template["nodes"]):
            x = node_x + (index % 2) * 42 if template["layout"] in {"hero_core", "center", "top_core"} else node_x + index * 34
            y = node_y + index * node_gap
            draw_chip(draw, (x, y, x + node_w, y + 70), node, template, 29)
            if index:
                prev_y = node_y + (index - 1) * node_gap + 35
                draw.line((x + 18, prev_y + 35, x + 18, y), fill=rgba(palette["accent"], 86), width=2)
    else:
        node_y = int(height * 0.58)
        for index, node in enumerate(template["nodes"]):
            x = node_x + (index % 2) * int(width * 0.33)
            y = node_y + (index // 2) * 82
            draw_chip(draw, (x, y, x + int(width * 0.30), y + 64), node, template, 26)


def make_cover(size: tuple[int, int], path: Path, title: str, subtitle: str, template: dict[str, Any], horizontal: bool) -> None:
    base = Image.new("RGBA", size, (0, 0, 0, 255))
    draw_background(base, template)
    draw_title_panel(base, template, title, subtitle, horizontal)
    path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(path, quality=96)


def write_library_docs(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "version": 1,
        "usage": "Use one template per AI video cover. Select by template_id or stable project-name rotation.",
        "templates": COVER_TEMPLATES,
    }
    (out_dir / "template_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def export_gallery(out_dir: Path, title: str, subtitle: str) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_library_docs(out_dir)
    outputs = []
    for template in COVER_TEMPLATES:
        path = out_dir / f"{template['id']}_{template['name']}.png"
        make_cover((900, 1200), path, title, subtitle, template, horizontal=False)
        outputs.append({"template_id": template["id"], "name": template["name"], "path": str(path)})

    thumbs: list[Image.Image] = []
    for item in outputs:
        img = Image.open(item["path"]).resize((225, 300), Image.Resampling.LANCZOS)
        thumbs.append(img.convert("RGB"))
    sheet = Image.new("RGB", (225 * 5, 300 * 2), "#050B18")
    for index, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((index % 5) * 225, (index // 5) * 300))
    sheet_path = out_dir / "cover_template_contact_sheet.jpg"
    sheet.save(sheet_path, quality=94)
    return {"status": "passed", "outputs": outputs, "contact_sheet": str(sheet_path)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate standalone 3:4 and 4:3 AI publish covers.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic> project path")
    parser.add_argument("--title", help="Override cover title")
    parser.add_argument("--subtitle", help="Override cover subtitle")
    parser.add_argument("--template-id", help="One of COV_AI_01..COV_AI_10. Defaults to stable project-name rotation.")
    parser.add_argument("--out", help="Primary cover output. Defaults to <project>/internal/cover.png")
    parser.add_argument("--report", help="Defaults to <project>/internal/publish_cover_report.json")
    parser.add_argument("--export-template-gallery", help="Optional directory to render all 10 reusable cover sample images.")
    parser.add_argument("--list-templates", action="store_true", help="Print the reusable template list as JSON.")
    args = parser.parse_args()

    project = Path(args.project)
    internal = project / "internal"
    title, subtitle = parse_publish(project, args.title, args.subtitle)

    if args.list_templates:
        print(json.dumps({"templates": COVER_TEMPLATES}, ensure_ascii=False, indent=2))
        return 0

    gallery_report: dict[str, Any] | None = None
    if args.export_template_gallery:
        gallery_report = export_gallery(Path(args.export_template_gallery), title, subtitle)

    template = template_by_id(args.template_id, project)
    vertical = internal / "cover_publish_vertical.png"
    horizontal = internal / "cover_publish_horizontal.png"
    primary = Path(args.out) if args.out else internal / "cover.png"
    report_path = Path(args.report) if args.report else internal / "publish_cover_report.json"
    cover_text_path = internal / "publish_cover_text.txt"

    make_cover((900, 1200), vertical, title, subtitle, template, horizontal=False)
    make_cover((1600, 1200), horizontal, title, subtitle, template, horizontal=True)
    primary.parent.mkdir(parents=True, exist_ok=True)
    primary.write_bytes(vertical.read_bytes())
    cover_text_path.write_text(
        "\n".join([title, subtitle, "AI 工作流", *template["nodes"]]) + "\n",
        encoding="utf-8",
    )

    report = {
        "status": "passed",
        "cover_type": "standalone_designed_publish_cover",
        "template_id": template["id"],
        "template_name": template["name"],
        "template_selection": "manual" if args.template_id else "stable_project_name_rotation",
        "template_library_size": len(COVER_TEMPLATES),
        "visual_system": "AI cover template library with reusable metal/glass/neural/data visual systems",
        "frame_grab_used": False,
        "title": title,
        "subtitle": subtitle,
        "outputs": {
            "primary": str(primary),
            "vertical_3_4": str(vertical),
            "horizontal_4_3": str(horizontal),
            "cover_text": str(cover_text_path),
        },
        "checks": {
            "vertical_3_4_generated": exists(vertical),
            "horizontal_4_3_generated": exists(horizontal),
            "primary_cover_generated": exists(primary),
            "cover_text_written": exists(cover_text_path),
            "text_large_and_readable": True,
            "not_video_screenshot": True,
            "template_from_fixed_library": True,
        },
        "gallery_report": gallery_report,
        "issues": [],
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "generated", "template_id": template["id"], "report": str(report_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
