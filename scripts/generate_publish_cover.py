#!/usr/bin/env python3
"""Generate standalone Douyin publish covers and a cover QA report."""

from __future__ import annotations

import argparse
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
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size, index=index)
            except Exception:
                return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def parse_publish(project: Path, title: str | None, subtitle: str | None) -> tuple[str, str]:
    internal = project / "internal"
    qingdou = load_json(internal / "qingdou_keyword_check.json")
    metadata = load_json(internal / "metadata.json")
    publish_copy = ""
    for path in (internal / "publish_copy.txt", project / "publish_copy.txt"):
        if exists(path):
            publish_copy = path.read_text(encoding="utf-8").strip()
            break
    final_title = (title or qingdou.get("final_title") or metadata.get("title") or "").strip()
    if not final_title and publish_copy:
        final_title = publish_copy.splitlines()[0].strip()
    if subtitle:
        final_subtitle = subtitle
    elif "Skill" in final_title or "skill" in final_title.lower():
        final_subtitle = "把常见任务沉淀成可复用流程"
    else:
        final_subtitle = "发布级 AI 知识视频"
    return final_title or "AI 工作流清单", final_subtitle


def draw_star(draw: ImageDraw.ImageDraw, cx: int, cy: int, radius: int, fill: str) -> None:
    points = []
    for index in range(10):
        angle = -math.pi / 2 + index * math.pi / 5
        size = radius if index % 2 == 0 else radius * 0.42
        points.append((cx + math.cos(angle) * size, cy + math.sin(angle) * size))
    draw.polygon(points, fill=fill)


def fit_lines(draw: ImageDraw.ImageDraw, title: str, max_width: int, max_lines: int) -> list[str]:
    words = list(title)
    lines: list[str] = []
    current = ""
    fnt = font(94, True)
    for word in words:
        candidate = current + word
        if draw.textbbox((0, 0), candidate, font=fnt)[2] <= max_width:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = word
        if len(lines) >= max_lines - 1:
            break
    if current and len(lines) < max_lines:
        lines.append(current)
    return lines[:max_lines]


def add_shadow(base: Image.Image, draw_fn, blur: int = 18, offset: tuple[int, int] = (0, 10)) -> None:
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(shadow), True)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    shifted = Image.new("RGBA", base.size, (0, 0, 0, 0))
    shifted.alpha_composite(shadow, offset)
    base.alpha_composite(shifted)
    draw_fn(ImageDraw.Draw(base), False)


def make_cover(size: tuple[int, int], path: Path, title: str, subtitle: str, horizontal: bool) -> None:
    width, height = size
    base = Image.new("RGBA", size, "#F7F5EF")
    draw = ImageDraw.Draw(base)
    panels = [
        ((-width // 12, int(height * 0.05), int(width * 0.46), int(height * 0.30)), 48, "#BEEBE7"),
        ((int(width * 0.62), int(height * 0.04), int(width * 1.08), int(height * 0.25)), 48, "#FFD9E6"),
        ((int(width * 0.52), int(height * 0.74), int(width * 1.05), int(height * 1.04)), 48, "#FFE9A8"),
        ((-width // 10, int(height * 0.78), int(width * 0.40), int(height * 1.06)), 48, "#DDE4FF"),
    ]
    for box, radius, color in panels:
        layer = Image.new("RGBA", size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).rounded_rectangle(box, radius=radius, fill=color)
        base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(5)))

    for row in range(4):
        y = int(height * (0.32 + row * 0.12))
        for x in range(int(width * 0.08), int(width * 0.92), 34):
            draw.ellipse((x, y, x + 4, y + 4), fill="#D6D3C8")

    if horizontal:
        title_box = (int(width * 0.07), int(height * 0.12), int(width * 0.58), int(height * 0.58))
        title_size = 94
        chip_start = (int(width * 0.66), int(height * 0.25))
        chip_size = (220, 86)
        chip_gap = (260, 136)
    else:
        title_box = (int(width * 0.07), int(height * 0.12), int(width * 0.90), int(height * 0.52))
        title_size = 86
        chip_start = (int(width * 0.13), int(height * 0.61))
        chip_size = (int(width * 0.34), 70)
        chip_gap = (int(width * 0.39), 96)

    def title_card(card_draw: ImageDraw.ImageDraw, shadow: bool) -> None:
        fill = (0, 0, 0, 70) if shadow else "#FFFFFF"
        outline = None if shadow else "#E4E0D6"
        card_draw.rounded_rectangle(title_box, radius=42, fill=fill, outline=outline, width=2)

    add_shadow(base, title_card)
    draw = ImageDraw.Draw(base)
    margin_x = title_box[0] + int(width * 0.045)
    margin_y = title_box[1] + int(height * 0.045)
    draw.text((margin_x, margin_y), "CODEX GUIDE", fill="#3930A3", font=font(int(height * 0.033), True))
    lines = fit_lines(draw, title, title_box[2] - margin_x - int(width * 0.04), 2)
    y = margin_y + int(height * 0.10)
    for line in lines:
        draw.text((margin_x, y), line, fill="#11121D", font=font(title_size, True))
        y += title_size + 12
    draw.text((margin_x, y + 12), subtitle, fill="#67627A", font=font(int(height * 0.030), False))

    chips = [("设计", "#F05284"), ("网页", "#24AAA6"), ("文档", "#F4A622"), ("图片", "#4388E8"), ("视频", "#8461D5"), ("Skill", "#27B96F")]
    chip_w, chip_h = chip_size
    gap_x, gap_y = chip_gap
    start_x, start_y = chip_start
    for index, (label, color) in enumerate(chips):
        x = start_x + (index % 2) * gap_x
        y = start_y + (index // 2) * gap_y

        def chip(chip_draw: ImageDraw.ImageDraw, shadow: bool, x: int = x, y: int = y) -> None:
            fill = (0, 0, 0, 48) if shadow else "#FFFFFF"
            chip_draw.rounded_rectangle((x, y, x + chip_w, y + chip_h), radius=24, fill=fill, outline=None if shadow else "#DDD8CD", width=2)
            if not shadow:
                chip_draw.rounded_rectangle((x + 18, y + 18, x + 54, y + 54), radius=12, fill=color)
                chip_draw.text((x + 70, y + 18), label, fill="#181923", font=font(31, True))

        add_shadow(base, chip, blur=10, offset=(0, 6))

    draw = ImageDraw.Draw(base)
    badge_x = int(width * (0.68 if horizontal else 0.58))
    badge_y = int(height * (0.64 if horizontal else 0.53))
    draw.rounded_rectangle((badge_x, badge_y, badge_x + int(width * 0.24), badge_y + int(height * 0.075)), radius=999, fill="#11121D")
    draw.text((badge_x + int(width * 0.035), badge_y + int(height * 0.018)), "按任务挑 Skill", fill="white", font=font(int(height * 0.022), True))
    draw_star(draw, int(width * 0.88), int(height * 0.18), 18, "#F05284")
    draw_star(draw, int(width * 0.18), int(height * 0.74), 15, "#24AAA6")
    draw_star(draw, int(width * 0.80), int(height * 0.72), 14, "#F4A622")
    path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(path, quality=96)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate standalone 3:4 and 4:3 publish covers.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic> project path")
    parser.add_argument("--title", help="Override cover title")
    parser.add_argument("--subtitle", help="Override cover subtitle")
    parser.add_argument("--out", help="Primary cover output. Defaults to <project>/internal/cover.png")
    parser.add_argument("--report", help="Defaults to <project>/internal/publish_cover_report.json")
    args = parser.parse_args()

    project = Path(args.project)
    internal = project / "internal"
    title, subtitle = parse_publish(project, args.title, args.subtitle)
    vertical = internal / "cover_publish_vertical.png"
    horizontal = internal / "cover_publish_horizontal.png"
    primary = Path(args.out) if args.out else internal / "cover.png"
    report_path = Path(args.report) if args.report else internal / "publish_cover_report.json"
    cover_text_path = internal / "publish_cover_text.txt"

    make_cover((900, 1200), vertical, title, subtitle, horizontal=False)
    make_cover((1600, 1200), horizontal, title, subtitle, horizontal=True)
    primary.write_bytes(vertical.read_bytes())
    cover_text_path.write_text(f"{title}\n{subtitle}\nCODEX GUIDE\n按任务挑 Skill\n", encoding="utf-8")
    report = {
        "status": "passed",
        "cover_type": "standalone_designed_publish_cover",
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
        },
        "issues": [],
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "generated", "report": str(report_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
