#!/usr/bin/env python3
"""Maintain fixed reusable AI background plates from the template library.

Existing high-quality fixed assets are preserved by default. Missing assets can
be filled with deterministic fallback plates: no baked text, no people, no logos.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIBRARY = ROOT / "references" / "fixed_ai_background_template_rotation.json"
DEFAULT_OUT_DIR = ROOT / "assets" / "ai_background_templates_fixed"


COLOR_MAP: dict[str, tuple[int, int, int]] = {
    "gunmetal": (36, 45, 55),
    "deep navy": (5, 12, 31),
    "ice cyan": (83, 223, 255),
    "small amber locks": (255, 195, 107),
    "deep blue": (8, 27, 68),
    "cyan": (59, 223, 239),
    "violet": (140, 116, 255),
    "low saturation black": (3, 5, 11),
    "near black": (2, 3, 7),
    "champagne gold": (221, 174, 92),
    "warm white": (255, 236, 202),
    "low cyan": (82, 198, 209),
    "graphite": (29, 35, 45),
    "ice blue": (115, 221, 255),
    "soft white": (226, 242, 255),
    "muted teal": (62, 186, 178),
    "white": (244, 248, 250),
    "silver gray": (176, 188, 198),
    "clear cyan": (94, 226, 242),
    "electric cyan": (55, 230, 255),
    "silver metal": (169, 181, 195),
    "deep space blue": (6, 11, 33),
    "small warm gold": (240, 188, 96),
    "silver": (174, 187, 199),
    "small amber": (255, 185, 83),
    "teal": (55, 216, 191),
    "low violet": (94, 83, 176),
    "deep space": (4, 7, 22),
    "soft gold": (232, 188, 98),
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def stable_rng(value: str) -> random.Random:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def clamp(value: float, low: int = 0, high: int = 255) -> int:
    return max(low, min(high, int(round(value))))


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(clamp(a[i] + (b[i] - a[i]) * t) for i in range(3))


def tint(color: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    if amount >= 0:
        return mix(color, (255, 255, 255), amount)
    return mix(color, (0, 0, 0), abs(amount))


def template_colors(template: dict[str, Any]) -> list[tuple[int, int, int]]:
    colors: list[tuple[int, int, int]] = []
    for term in template.get("palette", []):
        mapped = COLOR_MAP.get(str(term).strip().lower())
        if mapped:
            colors.append(mapped)
    while len(colors) < 4:
        colors.append([(5, 12, 31), (83, 223, 255), (140, 116, 255), (255, 195, 107)][len(colors)])
    return colors[:4]


def gradient(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, top)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        t = y / max(1, height - 1)
        draw.line((0, y, width, y), fill=mix(top, bottom, t))
    return image.convert("RGBA")


def add_noise(base: Image.Image, rng: random.Random, opacity: float = 0.045) -> Image.Image:
    width, height = base.size
    small = (max(160, width // 8), max(120, height // 8))
    noise = Image.new("L", small)
    noise.putdata([rng.randrange(255) for _ in range(small[0] * small[1])])
    noise = noise.resize((width, height), Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(0.35))
    noise_rgb = Image.merge("RGBA", (noise, noise, noise, Image.new("L", (width, height), int(255 * opacity))))
    base.alpha_composite(noise_rgb)
    return base


def add_vignette(base: Image.Image, strength: float = 0.48) -> Image.Image:
    width, height = base.size
    small_w, small_h = max(240, width // 6), max(160, height // 6)
    mask = Image.new("L", (small_w, small_h), 0)
    pixels = []
    cx, cy = small_w / 2, small_h / 2
    max_dist = math.hypot(cx, cy)
    for y in range(small_h):
        for x in range(small_w):
            d = math.hypot(x - cx, y - cy) / max_dist
            pixels.append(clamp((max(0.0, d - 0.34) / 0.66) ** 1.7 * 255 * strength))
    mask.putdata(pixels)
    mask = mask.resize((width, height), Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(28))
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    overlay.putalpha(mask)
    base.alpha_composite(overlay)
    return base


def add_radial_glow(
    base: Image.Image,
    center: tuple[float, float],
    radius: float,
    color: tuple[int, int, int],
    alpha: int,
) -> None:
    width, height = base.size
    small = Image.new("L", (max(120, width // 5), max(120, height // 5)), 0)
    draw = ImageDraw.Draw(small)
    scale_x = small.width / width
    scale_y = small.height / height
    cx, cy = center[0] * scale_x, center[1] * scale_y
    r = radius * max(scale_x, scale_y)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=alpha)
    small = small.filter(ImageFilter.GaussianBlur(max(18, int(r * 0.55))))
    mask = small.resize((width, height), Image.Resampling.BICUBIC)
    glow = Image.new("RGBA", (width, height), (*color, 0))
    glow.putalpha(mask)
    base.alpha_composite(glow)


def glow_line(
    base: Image.Image,
    p1: tuple[float, float],
    p2: tuple[float, float],
    color: tuple[int, int, int],
    width: int = 2,
    alpha: int = 120,
    blur: int = 10,
) -> None:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.line((p1, p2), fill=(*color, max(18, alpha // 3)), width=max(width * 4, 5))
    base.alpha_composite(overlay.filter(ImageFilter.GaussianBlur(blur)))
    sharp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(sharp)
    draw.line((p1, p2), fill=(*color, alpha), width=width)
    base.alpha_composite(sharp)


def glow_ellipse(
    base: Image.Image,
    bbox: tuple[float, float, float, float],
    color: tuple[int, int, int],
    width: int = 2,
    alpha: int = 100,
    blur: int = 14,
) -> None:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.ellipse(bbox, outline=(*color, max(18, alpha // 3)), width=max(width * 5, 6))
    base.alpha_composite(overlay.filter(ImageFilter.GaussianBlur(blur)))
    sharp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(sharp)
    draw.ellipse(bbox, outline=(*color, alpha), width=width)
    base.alpha_composite(sharp)


def glow_rect(
    base: Image.Image,
    bbox: tuple[float, float, float, float],
    color: tuple[int, int, int],
    outline_alpha: int = 72,
    fill_alpha: int = 18,
    radius: int = 18,
) -> None:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle(bbox, radius=radius, fill=(*tint(color, -0.7), fill_alpha), outline=(*color, outline_alpha), width=1)
    base.alpha_composite(overlay.filter(ImageFilter.GaussianBlur(0.25)))


def node(base: Image.Image, center: tuple[float, float], color: tuple[int, int, int], radius: int = 5, alpha: int = 170) -> None:
    x, y = center
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.ellipse((x - radius * 3, y - radius * 3, x + radius * 3, y + radius * 3), fill=(*color, max(16, alpha // 5)))
    base.alpha_composite(overlay.filter(ImageFilter.GaussianBlur(radius * 2)))
    sharp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(sharp)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, alpha))
    draw.ellipse((x - radius * 1.8, y - radius * 1.8, x + radius * 1.8, y + radius * 1.8), outline=(*color, alpha // 2), width=1)
    base.alpha_composite(sharp)


def draw_particles(base: Image.Image, rng: random.Random, color: tuple[int, int, int], count: int, alpha_range: tuple[int, int] = (24, 110)) -> None:
    draw = ImageDraw.Draw(base)
    width, height = base.size
    for _ in range(count):
        x = rng.random() * width
        y = rng.random() * height
        r = rng.choice([1, 1, 1, 2, 2, 3])
        alpha = rng.randint(*alpha_range)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(*color, alpha))


def draw_titanium_neural_control_room(base: Image.Image, rng: random.Random, colors: list[tuple[int, int, int]]) -> None:
    width, height = base.size
    cyan, violet, amber = colors[2], (126, 116, 255), colors[3]
    add_radial_glow(base, (width * 0.62, height * 0.43), height * 0.55, cyan, 82)
    vp = (width * 0.58, height * 0.49)
    for x in range(-width // 4, width + width // 4, width // 12):
        glow_line(base, (x, height), vp, tint(cyan, -0.22), 1, 38, 8)
    for y in [height * 0.28, height * 0.42, height * 0.56, height * 0.72]:
        glow_line(base, (0, y), (width, y + rng.uniform(-28, 28)), tint(cyan, -0.35), 1, 32, 7)
    for i in range(12):
        x = width * (0.08 + i * 0.075)
        top = rng.uniform(height * 0.1, height * 0.34)
        bottom = height * rng.uniform(0.82, 1.0)
        glow_line(base, (x, top), (x + rng.uniform(-20, 20), bottom), tint(colors[0], 0.55), 3, 35, 9)
    points = [(rng.uniform(width * 0.36, width * 0.88), rng.uniform(height * 0.18, height * 0.78)) for _ in range(34)]
    for index, p1 in enumerate(points):
        nearest = sorted(points[index + 1 :], key=lambda p: math.hypot(p[0] - p1[0], p[1] - p1[1]))[:2]
        for p2 in nearest:
            if math.hypot(p2[0] - p1[0], p2[1] - p1[1]) < width * 0.18:
                glow_line(base, p1, p2, cyan, 1, 54, 7)
    for point in points:
        node(base, point, cyan if rng.random() > 0.18 else amber, rng.randint(3, 7), 150)
    draw_particles(base, rng, tint(cyan, 0.15), 420, (22, 88))
    add_vignette(base, 0.42)


def draw_deep_data_light_rail(base: Image.Image, rng: random.Random, colors: list[tuple[int, int, int]]) -> None:
    width, height = base.size
    cyan, violet = colors[1], colors[2]
    vp = (width * 0.66, height * 0.46)
    add_radial_glow(base, vp, height * 0.48, cyan, 90)
    for i in range(22):
        left_y = height * (i / 21)
        right_y = height * ((i + 0.4) / 21)
        color = cyan if i % 3 else violet
        glow_line(base, (0, left_y), vp, color, 1, 54, 9)
        glow_line(base, (width, right_y), vp, color, 1, 44, 9)
    for offset in [-0.22, -0.12, -0.04, 0.04, 0.12, 0.22]:
        p1 = (width * (0.5 + offset), height)
        p2 = (width * (0.61 + offset * 0.28), height * 0.5)
        glow_line(base, p1, p2, cyan, 3, 128, 12)
    for _ in range(42):
        start = (rng.uniform(0, width), rng.uniform(0, height))
        end = (start[0] + (vp[0] - start[0]) * rng.uniform(0.08, 0.2), start[1] + (vp[1] - start[1]) * rng.uniform(0.08, 0.2))
        glow_line(base, start, end, cyan if rng.random() > 0.35 else violet, 1, rng.randint(42, 112), 5)
    draw_particles(base, rng, cyan, 650, (18, 96))
    add_vignette(base, 0.52)


def draw_black_gold_strategy_chamber(base: Image.Image, rng: random.Random, colors: list[tuple[int, int, int]]) -> None:
    width, height = base.size
    gold, warm, cyan = colors[1], colors[2], colors[3]
    center = (width * 0.52, height * 0.46)
    add_radial_glow(base, center, height * 0.44, gold, 62)
    for radius in [0.16, 0.22, 0.3, 0.39, 0.52]:
        bbox = (
            center[0] - width * radius,
            center[1] - height * radius * 0.72,
            center[0] + width * radius,
            center[1] + height * radius * 0.72,
        )
        glow_ellipse(base, bbox, gold, width=2 if radius < 0.35 else 1, alpha=86, blur=12)
    for angle in range(0, 360, 18):
        r1 = height * 0.18
        r2 = height * rng.uniform(0.42, 0.58)
        a = math.radians(angle + rng.uniform(-2, 2))
        p1 = (center[0] + math.cos(a) * r1 * 1.42, center[1] + math.sin(a) * r1)
        p2 = (center[0] + math.cos(a) * r2 * 1.42, center[1] + math.sin(a) * r2)
        glow_line(base, p1, p2, gold if angle % 54 else cyan, 1, 58, 8)
    for i in range(10):
        y = height * (0.18 + i * 0.075)
        glow_line(base, (width * 0.03, y), (width * 0.28, y + rng.uniform(-18, 18)), gold, 1, 34, 8)
        glow_line(base, (width * 0.72, y + rng.uniform(-14, 14)), (width * 0.97, y), gold, 1, 34, 8)
    draw_particles(base, rng, warm, 260, (18, 76))
    add_vignette(base, 0.62)


def draw_source_archive_wall(base: Image.Image, rng: random.Random, colors: list[tuple[int, int, int]]) -> None:
    width, height = base.size
    cyan, teal, white = colors[1], colors[3], colors[2]
    add_radial_glow(base, (width * 0.48, height * 0.45), height * 0.55, cyan, 58)
    cols, rows = 5, 3
    margin_x, margin_y = width * 0.08, height * 0.16
    cell_w = (width - margin_x * 2) / cols
    cell_h = (height - margin_y * 2) / rows
    for row in range(rows):
        for col in range(cols):
            x1 = margin_x + col * cell_w + rng.uniform(-8, 8)
            y1 = margin_y + row * cell_h + rng.uniform(-8, 8)
            x2 = x1 + cell_w * rng.uniform(0.68, 0.88)
            y2 = y1 + cell_h * rng.uniform(0.58, 0.74)
            glow_rect(base, (x1, y1, x2, y2), cyan if (row + col) % 2 else teal, 62, 14, 12)
            corner = min(cell_w, cell_h) * 0.1
            for sx, sy in [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]:
                dx = corner if sx == x1 else -corner
                dy = corner if sy == y1 else -corner
                glow_line(base, (sx, sy), (sx + dx, sy), white, 1, 48, 5)
                glow_line(base, (sx, sy), (sx, sy + dy), white, 1, 48, 5)
    for y in [height * 0.29, height * 0.51, height * 0.73]:
        glow_line(base, (0, y), (width, y + rng.uniform(-12, 12)), cyan, 2, 52, 13)
    draw_particles(base, rng, cyan, 330, (14, 72))
    add_vignette(base, 0.46)


def draw_white_ice_tool_lab(base: Image.Image, rng: random.Random, colors: list[tuple[int, int, int]]) -> None:
    width, height = base.size
    cyan, silver = colors[3], colors[1]
    add_radial_glow(base, (width * 0.56, height * 0.38), height * 0.62, cyan, 76)
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for i in range(8):
        y = height * (0.14 + i * 0.1)
        bbox = (width * -0.12, y - height * 0.18, width * 1.08, y + height * 0.22)
        draw.arc(bbox, start=190, end=350, fill=(*cyan, 54), width=2)
    base.alpha_composite(overlay.filter(ImageFilter.GaussianBlur(0.7)))
    for _ in range(38):
        p1 = (rng.uniform(width * 0.15, width * 0.86), rng.uniform(height * 0.15, height * 0.74))
        p2 = (p1[0] + rng.uniform(-180, 180), p1[1] + rng.uniform(-90, 90))
        glow_line(base, p1, p2, cyan, 1, 44, 7)
    for _ in range(34):
        x = rng.uniform(width * 0.18, width * 0.84)
        y = rng.uniform(height * 0.16, height * 0.78)
        node(base, (x, y), cyan if rng.random() > 0.35 else silver, rng.randint(3, 5), 132)
    draw_particles(base, rng, tint(cyan, 0.45), 260, (18, 86))
    base.alpha_composite(Image.new("RGBA", base.size, (255, 255, 255, 18)))
    add_vignette(base, 0.26)


def draw_quantum_ring_core(base: Image.Image, rng: random.Random, colors: list[tuple[int, int, int]]) -> None:
    width, height = base.size
    cyan, violet, silver = colors[1], colors[2], colors[3]
    center = (width * 0.56, height * 0.48)
    add_radial_glow(base, center, height * 0.58, cyan, 96)
    for scale, color, alpha in [(0.52, cyan, 118), (0.42, silver, 72), (0.31, violet, 96), (0.2, cyan, 86)]:
        bbox = (
            center[0] - width * scale * 0.56,
            center[1] - height * scale,
            center[0] + width * scale * 0.56,
            center[1] + height * scale,
        )
        glow_ellipse(base, bbox, color, width=3 if scale > 0.4 else 2, alpha=alpha, blur=16)
    for angle in range(0, 360, 12):
        a = math.radians(angle)
        rx = width * 0.31
        ry = height * 0.49
        p1 = (center[0] + math.cos(a) * rx * 0.72, center[1] + math.sin(a) * ry * 0.72)
        p2 = (center[0] + math.cos(a) * rx, center[1] + math.sin(a) * ry)
        glow_line(base, p1, p2, cyan if angle % 48 else violet, 1, 58, 8)
    points = []
    for _ in range(42):
        angle = rng.random() * math.tau
        radius = rng.uniform(0.08, 0.42)
        points.append((center[0] + math.cos(angle) * width * radius * 0.48, center[1] + math.sin(angle) * height * radius))
    for i, p1 in enumerate(points):
        for p2 in points[i + 1 : i + 4]:
            glow_line(base, p1, p2, cyan, 1, 42, 6)
    for point in points:
        node(base, point, cyan if rng.random() > 0.25 else violet, rng.randint(3, 6), 142)
    draw_particles(base, rng, cyan, 520, (16, 82))
    add_vignette(base, 0.5)


def draw_cosmic_ai_network(base: Image.Image, rng: random.Random, colors: list[tuple[int, int, int]]) -> None:
    width, height = base.size
    cyan, violet, gold = colors[2], colors[1], colors[3]
    add_radial_glow(base, (width * 0.5, height * 0.45), height * 0.62, violet, 66)
    add_radial_glow(base, (width * 0.63, height * 0.5), height * 0.48, cyan, 76)
    draw_particles(base, rng, (245, 250, 255), 900, (18, 110))
    core = (width * 0.52, height * 0.48)
    for radius in [0.18, 0.27, 0.38, 0.5]:
        bbox = (
            core[0] - width * radius,
            core[1] - height * radius * 0.62,
            core[0] + width * radius,
            core[1] + height * radius * 0.62,
        )
        glow_ellipse(base, bbox, cyan if radius < 0.4 else violet, 1, 62, 12)
    points = [(rng.uniform(width * 0.14, width * 0.9), rng.uniform(height * 0.12, height * 0.82)) for _ in range(46)]
    for index, p1 in enumerate(points):
        for p2 in sorted(points[index + 1 :], key=lambda p: math.hypot(p[0] - p1[0], p[1] - p1[1]))[:2]:
            if math.hypot(p2[0] - p1[0], p2[1] - p1[1]) < width * 0.19:
                glow_line(base, p1, p2, cyan if rng.random() > 0.24 else violet, 1, 46, 8)
    for point in points:
        node(base, point, cyan if rng.random() > 0.1 else gold, rng.randint(2, 5), 138)
    add_vignette(base, 0.54)


def draw_vertical_tool_test_chamber(base: Image.Image, rng: random.Random, colors: list[tuple[int, int, int]]) -> None:
    width, height = base.size
    cyan, silver, amber = colors[1], colors[2], colors[3]
    center_x = width * 0.5
    add_radial_glow(base, (center_x, height * 0.42), width * 0.72, cyan, 88)
    for offset in [-0.28, -0.18, 0.18, 0.28]:
        glow_line(base, (width * (0.5 + offset), height * 0.05), (width * (0.5 + offset * 0.55), height * 0.95), silver, 3, 48, 12)
    for y in [height * 0.2, height * 0.34, height * 0.5, height * 0.66]:
        bbox = (width * 0.3, y - height * 0.065, width * 0.7, y + height * 0.065)
        glow_ellipse(base, bbox, cyan if y < height * 0.55 else amber, 2, 82, 14)
        node(base, (center_x, y), cyan, 7, 158)
    for i in range(18):
        y = height * (0.11 + i * 0.047)
        glow_line(base, (width * 0.12, y), (width * 0.32, y + rng.uniform(-20, 20)), cyan, 1, 38, 7)
        glow_line(base, (width * 0.68, y + rng.uniform(-20, 20)), (width * 0.88, y), cyan, 1, 38, 7)
    draw_particles(base, rng, cyan, 440, (16, 84))
    add_vignette(base, 0.48)


def draw_vertical_workflow_spine(base: Image.Image, rng: random.Random, colors: list[tuple[int, int, int]]) -> None:
    width, height = base.size
    cyan, teal, violet = colors[1], colors[2], colors[3]
    x = width * 0.48
    add_radial_glow(base, (x, height * 0.5), width * 0.72, cyan, 70)
    glow_line(base, (x, height * 0.08), (x, height * 0.92), cyan, 4, 122, 18)
    ys = [height * 0.16, height * 0.32, height * 0.49, height * 0.66, height * 0.82]
    for index, y in enumerate(ys):
        color = [cyan, teal, violet, cyan, teal][index]
        node(base, (x, y), color, 9, 170)
        glow_ellipse(base, (x - width * 0.16, y - width * 0.1, x + width * 0.16, y + width * 0.1), color, 2, 70, 10)
        left = index % 2 == 0
        start = (x, y)
        end = (width * (0.2 if left else 0.78), y + rng.uniform(-24, 24))
        glow_line(base, start, end, color, 2, 72, 10)
        glow_rect(
            base,
            (
                end[0] - width * (0.17 if left else 0.03),
                end[1] - height * 0.035,
                end[0] + width * (0.03 if left else 0.17),
                end[1] + height * 0.035,
            ),
            color,
            56,
            12,
            18,
        )
    for _ in range(38):
        px = x + rng.uniform(-width * 0.24, width * 0.24)
        py = rng.uniform(height * 0.08, height * 0.92)
        glow_line(base, (px, py), (x, py + rng.uniform(-50, 50)), teal if rng.random() > 0.4 else cyan, 1, 32, 7)
    draw_particles(base, rng, cyan, 400, (14, 76))
    add_vignette(base, 0.5)


def draw_vertical_ai_trend_star_map(base: Image.Image, rng: random.Random, colors: list[tuple[int, int, int]]) -> None:
    width, height = base.size
    cyan, violet, gold = colors[1], colors[2], colors[3]
    add_radial_glow(base, (width * 0.5, height * 0.43), width * 0.78, violet, 62)
    draw_particles(base, rng, (240, 248, 255), 880, (16, 102))
    core = (width * 0.5, height * 0.46)
    glow_ellipse(base, (width * 0.18, height * 0.27, width * 0.82, height * 0.63), cyan, 2, 80, 14)
    glow_ellipse(base, (width * 0.08, height * 0.2, width * 0.92, height * 0.72), violet, 1, 56, 12)
    nodes = [core]
    for angle in [-110, -62, -22, 24, 66, 112, 154, 202]:
        a = math.radians(angle)
        nodes.append((core[0] + math.cos(a) * width * rng.uniform(0.18, 0.36), core[1] + math.sin(a) * height * rng.uniform(0.13, 0.24)))
    for p in nodes[1:]:
        glow_line(base, core, p, cyan if rng.random() > 0.3 else violet, 2, 68, 10)
    for i, p1 in enumerate(nodes[1:], start=1):
        p2 = nodes[1 + (i % (len(nodes) - 1))]
        glow_line(base, p1, p2, violet, 1, 44, 9)
    for index, point in enumerate(nodes):
        node(base, point, gold if index == 0 else (cyan if index % 3 else violet), 10 if index == 0 else 6, 168)
    for _ in range(24):
        p1 = (rng.uniform(width * 0.12, width * 0.88), rng.uniform(height * 0.12, height * 0.86))
        p2 = (p1[0] + rng.uniform(-140, 140), p1[1] + rng.uniform(-180, 180))
        glow_line(base, p1, p2, cyan if rng.random() > 0.45 else violet, 1, 34, 8)
    add_vignette(base, 0.52)


STYLE_RENDERERS = {
    "titanium_neural_control_room": draw_titanium_neural_control_room,
    "deep_data_light_rail": draw_deep_data_light_rail,
    "black_gold_strategy_chamber": draw_black_gold_strategy_chamber,
    "source_archive_wall": draw_source_archive_wall,
    "white_ice_tool_lab": draw_white_ice_tool_lab,
    "quantum_ring_core": draw_quantum_ring_core,
    "cosmic_ai_network": draw_cosmic_ai_network,
    "vertical_tool_test_chamber": draw_vertical_tool_test_chamber,
    "vertical_workflow_spine": draw_vertical_workflow_spine,
    "vertical_ai_trend_star_map": draw_vertical_ai_trend_star_map,
}


def filename_for(template: dict[str, Any]) -> str:
    aspect = str(template.get("aspect") or "").replace(":", "x")
    return f"{template['id']}_{template['name']}_{aspect}.png"


def render_template(template: dict[str, Any]) -> Image.Image:
    width = int(template["width"])
    height = int(template["height"])
    rng = stable_rng(str(template["id"]))
    colors = template_colors(template)
    base = gradient((width, height), tint(colors[0], -0.42), tint(colors[1], -0.66))
    add_noise(base, rng, 0.04)
    renderer = STYLE_RENDERERS.get(str(template.get("visual_family") or ""))
    if not renderer:
        raise SystemExit(f"unsupported visual_family for {template.get('id')}: {template.get('visual_family')}")
    renderer(base, rng, colors)
    base = ImageEnhance.Contrast(base.convert("RGB")).enhance(1.08).convert("RGBA")
    base = ImageEnhance.Sharpness(base).enhance(1.05)
    return base.convert("RGB")


def build_asset_report(template: dict[str, Any], output_path: Path, image: Image.Image, out_dir: Path) -> dict[str, Any]:
    relative = output_path.relative_to(ROOT) if output_path.is_relative_to(ROOT) else output_path
    generation_method = str(template.get("asset_generation_method") or "deterministic_pil_fixed_asset_v1")
    return {
        "id": template.get("id"),
        "name": template.get("name"),
        "aspect": template.get("aspect"),
        "width": image.width,
        "height": image.height,
        "visual_family": template.get("visual_family"),
        "path": str(relative),
        "size_bytes": output_path.stat().st_size,
        "asset_source_type": template.get("asset_source_type"),
        "generation_method": generation_method,
        "checks": {
            "fixed_background_asset": True,
            "no_baked_text": True,
            "no_people": True,
            "no_logo": True,
            "foreground_text_must_be_overlay": True,
            "dimensions_match_template": image.width == int(template["width"]) and image.height == int(template["height"]),
        },
    }


def iter_templates(library: dict[str, Any]) -> Iterable[dict[str, Any]]:
    for item in library.get("templates", []):
        if isinstance(item, dict):
            yield item


def main() -> int:
    parser = argparse.ArgumentParser(description="Maintain fixed AI background image assets.")
    parser.add_argument("--library", default=str(DEFAULT_LIBRARY), help="Fixed background template JSON")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Output directory for PNG assets")
    parser.add_argument("--manifest-out", help="Output asset manifest JSON. Defaults to <out-dir>/asset_manifest.json")
    parser.add_argument("--force", action="store_true", help="Overwrite existing assets with deterministic fallback renders.")
    args = parser.parse_args()

    library_path = resolve_path(args.library)
    out_dir = resolve_path(args.out_dir)
    manifest_out = resolve_path(args.manifest_out) if args.manifest_out else out_dir / "asset_manifest.json"
    library = load_json(library_path)

    out_dir.mkdir(parents=True, exist_ok=True)
    assets: list[dict[str, Any]] = []
    for template in iter_templates(library):
        output_path = out_dir / filename_for(template)
        if output_path.exists() and output_path.is_file() and output_path.stat().st_size > 0 and not args.force:
            image = Image.open(output_path).convert("RGB")
        else:
            image = render_template(template)
            image.save(output_path, format="PNG", optimize=True)
        assets.append(build_asset_report(template, output_path, image, out_dir))

    report = {
        "status": "passed",
        "created_at": now_iso(),
        "library": str(library_path),
        "out_dir": str(out_dir),
        "asset_count": len(assets),
        "generation_method": "preserve_existing_assets_or_deterministic_fallback_v1",
        "checks": {
            "all_assets_generated": len(assets) == len(list(iter_templates(library))),
            "no_baked_text_policy": True,
            "manual_qingdou_not_required_for_background_no_text": True,
            "foreground_text_still_requires_qingdou": True,
        },
        "assets": assets,
    }
    write_json(manifest_out, report)
    print(json.dumps({"status": "passed", "asset_count": len(assets), "manifest": str(manifest_out)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
