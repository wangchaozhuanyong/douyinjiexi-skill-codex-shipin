#!/usr/bin/env python3
"""Generate the Ant AI Scheme 7 cinematic deep-space nebula background and preview."""

from __future__ import annotations

import argparse
import math
import random
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "ai_background_templates_dynamic"
PREVIEW_DIR = ROOT / "reference_downloads" / "ai_research_top5_20260518"
SOURCE_COSMIC_IMAGE = ROOT / "assets" / "source_cosmic_backgrounds" / "heic0506a_m51_mobile_fhd.jpg"
SOURCE_CARINA_IMAGE = ROOT / "assets" / "source_cosmic_backgrounds" / "weic2205a_carina_cosmic_cliffs_publication.jpg"
SOURCE_NGC1514_IMAGE = ROOT / "assets" / "source_cosmic_backgrounds" / "weic2508a_ngc1514_miri_large.jpg"


def ffmpeg_bin() -> str:
    return shutil.which("ffmpeg") or "ffmpeg"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def clamp(value: int, low: int = 0, high: int = 255) -> int:
    return max(low, min(high, value))


def smooth_mask(width: int, height: int, seed: int, blur: float, contrast: float = 1.0) -> Image.Image:
    rng = random.Random(seed)
    small_width = max(80, width // 4)
    small_height = max(120, height // 4)
    data = bytes(rng.randrange(256) for _ in range(small_width * small_height))
    noise = Image.frombytes("L", (small_width, small_height), data)
    noise = noise.resize((width, height), Image.Resampling.BICUBIC)
    noise = noise.filter(ImageFilter.GaussianBlur(blur))
    if contrast != 1.0:
        noise = ImageEnhance.Contrast(noise).enhance(contrast)
    return noise


def screen(base: Image.Image, layer: Image.Image) -> Image.Image:
    return ImageChops.screen(base.convert("RGB"), layer.convert("RGB")).convert("RGBA")


def set_opacity(layer: Image.Image, opacity: float) -> Image.Image:
    out = layer.convert("RGBA").copy()
    alpha = out.getchannel("A").point(lambda p: int(p * opacity))
    out.putalpha(alpha)
    return out


def radial_mask(
    width: int,
    height: int,
    cxn: float,
    cyn: float,
    rxn: float,
    ryn: float,
    max_alpha: int,
    inner: float = 0.0,
) -> Image.Image:
    mask = Image.new("L", (width, height), 0)
    pix = mask.load()
    cx = width * cxn
    cy = height * cyn
    rx = width * rxn
    ry = height * ryn
    for y in range(height):
        for x in range(width):
            d = math.hypot((x - cx) / max(1, rx), (y - cy) / max(1, ry))
            if d <= inner:
                value = max_alpha
            elif d >= 1:
                value = 0
            else:
                t = (d - inner) / max(0.001, 1 - inner)
                value = int(max_alpha * (1 - t) ** 1.8)
            pix[x, y] = value
    return mask.filter(ImageFilter.GaussianBlur(18))


def build_deep_space(width: int, height: int) -> Image.Image:
    image = Image.new("RGB", (width, height), (2, 5, 14))
    pix = image.load()
    for y in range(height):
        ny = y / max(1, height - 1)
        for x in range(width):
            nx = x / max(1, width - 1)
            upper_depth = max(0.0, 1.0 - math.hypot((nx - 0.50) * 1.0, (ny - 0.20) * 1.65))
            center_vortex = max(0.0, 1.0 - math.hypot((nx - 0.56) * 1.15, (ny - 0.43) * 1.28))
            lower_clouds = max(0.0, 1.0 - math.hypot((nx - 0.48) * 1.35, (ny - 0.78) * 2.2))
            r = int(1 + 8 * (1 - ny) + 20 * upper_depth + 20 * center_vortex + 8 * lower_clouds)
            g = int(5 + 18 * (1 - ny) + 42 * upper_depth + 22 * center_vortex + 20 * lower_clouds)
            b = int(18 + 62 * (1 - ny) + 108 * upper_depth + 45 * center_vortex + 38 * lower_clouds)
            pix[x, y] = (clamp(r), clamp(g), clamp(b))
    return image.convert("RGBA")


def add_faint_real_space_texture(base: Image.Image) -> None:
    """Use the archived Hubble image only as low-opacity organic grain, not as the visible composition."""
    if not SOURCE_COSMIC_IMAGE.exists():
        return
    width, height = base.size
    source = Image.open(SOURCE_COSMIC_IMAGE).convert("RGB")
    source = ImageOps.fit(source, (width, height), method=Image.Resampling.LANCZOS, centering=(0.53, 0.45))
    source = source.filter(ImageFilter.GaussianBlur(4.2))
    source = ImageEnhance.Color(source).enhance(0.72)
    source = ImageEnhance.Contrast(source).enhance(0.82)
    source = ImageEnhance.Brightness(source).enhance(0.36).convert("RGBA")
    blue_wash = Image.new("RGBA", (width, height), (12, 35, 82, 130))
    source = screen(source, blue_wash)
    base.alpha_composite(set_opacity(source, 0.16))


def add_nebula_clouds(base: Image.Image, seed: int) -> None:
    width, height = base.size
    colors = [
        (62, 156, 255, 86),
        (98, 82, 246, 72),
        (244, 92, 202, 56),
        (126, 229, 255, 48),
        (32, 72, 142, 88),
    ]
    specs = [
        (0.57, 0.25, 1.08, 0.25, -18, 114),
        (0.53, 0.42, 1.22, 0.34, -19, 118),
        (0.56, 0.55, 1.08, 0.29, -17, 122),
        (0.43, 0.70, 1.18, 0.31, -12, 126),
        (0.55, 0.83, 1.22, 0.24, -8, 116),
    ]
    for index, (cxn, cyn, sx, sy, angle, threshold) in enumerate(specs):
        mask = smooth_mask(width, height, seed + index * 37, blur=24 + index * 4, contrast=1.55)
        mask = ImageOps.autocontrast(mask)
        mask = mask.point(lambda p, t=threshold: 0 if p < t else int((p - t) * 1.55))
        layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        cloud = Image.new("RGBA", (width, height), colors[index])
        cloud.putalpha(mask)
        cloud = cloud.resize((int(width * sx), int(height * sy)), Image.Resampling.BICUBIC).rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
        x = int(width * cxn - cloud.width / 2)
        y = int(height * cyn - cloud.height / 2)
        layer.alpha_composite(cloud, (x, y))
        layer = layer.filter(ImageFilter.GaussianBlur(12))
        base.alpha_composite(layer)


def add_top_depth_lights(base: Image.Image) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    rng = random.Random(2026063019)
    for _ in range(16):
        x = rng.uniform(width * 0.05, width * 0.95)
        y0 = rng.uniform(-height * 0.05, height * 0.18)
        length = rng.uniform(height * 0.10, height * 0.28)
        alpha = rng.randint(20, 48)
        color = (96, 210, 255, alpha) if rng.random() < 0.7 else (242, 94, 204, alpha)
        draw.line([(x, y0), (x + rng.uniform(-35, 35), y0 + length)], fill=color, width=rng.randint(4, 10))
    layer = layer.filter(ImageFilter.GaussianBlur(14))
    base.alpha_composite(layer)


def add_reference_top_wisps(base: Image.Image) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    rng = random.Random(2026063057)
    for index in range(12):
        x = rng.uniform(width * 0.12, width * 0.90)
        y = rng.uniform(-height * 0.04, height * 0.18)
        points: list[tuple[float, float]] = []
        for step in range(8):
            points.append(
                (
                    x + math.sin(step * 0.75 + index) * rng.uniform(8, 32),
                    y + step * rng.uniform(22, 42),
                )
            )
        draw.line(points, fill=(86, 196, 255, rng.randint(24, 52)), width=rng.randint(5, 11), joint="curve")
    layer = layer.filter(ImageFilter.GaussianBlur(13))
    base.alpha_composite(layer)


def add_reference_hotlist_vortex(base: Image.Image) -> None:
    width, height = base.size
    cx = width * 0.54
    cy = height * 0.46
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    rng = random.Random(2026063061)

    for arm in range(5):
        arm_shift = arm * math.tau / 5 + 0.42
        for i in range(900):
            t = i / 899
            angle = arm_shift + t * math.tau * 1.45 + 0.18 * math.sin(t * math.tau * 2.3)
            radius = 28 + t * width * 0.56
            x = cx + math.cos(angle) * radius * 1.04 + rng.uniform(-10, 10) * (1 - t * 0.35)
            y = cy + math.sin(angle) * radius * 0.48 + rng.uniform(-5, 5)
            thickness = 26 * (1 - t) + 4.5
            alpha = int(92 * (1 - t) + 18)
            if arm in (1, 4):
                color = (235, 86, 198, int(alpha * 0.82))
            else:
                color = (92, 178, 255, alpha)
            draw.ellipse([x - thickness, y - thickness * 0.58, x + thickness, y + thickness * 0.58], fill=color)

    cloud_mask = smooth_mask(width, height, 2026063067, blur=18, contrast=1.25)
    cloud_mask = cloud_mask.point(lambda p: 0 if p < 104 else int((p - 104) * 1.22))
    cloud = Image.new("RGBA", base.size, (96, 166, 255, 42))
    cloud.putalpha(cloud_mask)
    cloud = cloud.rotate(-17, resample=Image.Resampling.BICUBIC, center=(cx, cy))
    cloud.putalpha(radial_mask(width, height, 0.54, 0.46, 0.64, 0.36, 118, inner=0.08))
    layer.alpha_composite(cloud)

    core = Image.new("RGBA", base.size, (0, 0, 0, 0))
    core_draw = ImageDraw.Draw(core, "RGBA")
    core_draw.ellipse([cx - 220, cy - 118, cx + 220, cy + 118], fill=(76, 128, 225, 38))
    core_draw.ellipse([cx - 150, cy - 76, cx + 150, cy + 76], fill=(222, 86, 202, 30))
    core_draw.ellipse([cx - 92, cy - 46, cx + 92, cy + 46], fill=(8, 12, 28, 44))
    for arc_index, (start, end, color, width_px) in enumerate(
        [
            (12, 318, (178, 126, 240, 104), 8),
            (196, 358, (80, 190, 255, 92), 7),
            (36, 210, (232, 82, 198, 64), 5),
        ]
    ):
        pad_x = 188 + arc_index * 34
        pad_y = 102 + arc_index * 18
        core_draw.arc([cx - pad_x, cy - pad_y, cx + pad_x, cy + pad_y], start, end, fill=color, width=width_px)

    layer = layer.rotate(-6, resample=Image.Resampling.BICUBIC, center=(cx, cy)).filter(ImageFilter.GaussianBlur(5))
    core = core.rotate(-8, resample=Image.Resampling.BICUBIC, center=(cx, cy)).filter(ImageFilter.GaussianBlur(3))
    base.alpha_composite(layer)
    base.alpha_composite(core)


def add_reference_bottom_cloud_ocean(base: Image.Image) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    rng = random.Random(2026063071)
    for band in range(10):
        y_base = height * (0.63 + band * 0.030)
        points: list[tuple[float, float]] = []
        for i in range(70):
            x = width * i / 69
            y = y_base + math.sin(i * 0.27 + band * 0.55) * (22 + band * 2.2) + rng.uniform(-8, 8)
            points.append((x, y))
        fill = (3, 8, 24, 80 + band * 13)
        draw.polygon([(0, height)] + points + [(width, height)], fill=fill)
        rim_color = (92, 154, 255, 30) if band % 2 == 0 else (226, 80, 194, 24)
        draw.line(points, fill=rim_color, width=10 + band, joint="curve")
    layer = layer.filter(ImageFilter.GaussianBlur(11))
    base.alpha_composite(layer)


def add_reference_star_accents(base: Image.Image) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    rng = random.Random(2026063077)
    for _ in range(72):
        x = rng.uniform(0, width)
        y = rng.uniform(0, height)
        if width * 0.12 < x < width * 0.90 and height * 0.30 < y < height * 0.72 and rng.random() < 0.82:
            continue
        r = rng.uniform(0.55, 1.4)
        color = (228, 246, 255, rng.randint(55, 150))
        if rng.random() < 0.18:
            color = (255, 102, 205, rng.randint(65, 160))
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
    for x, y, color in [
        (width * 0.10, height * 0.08, (105, 214, 255, 70)),
        (width * 0.87, height * 0.12, (250, 82, 205, 66)),
        (width * 0.19, height * 0.76, (82, 204, 255, 58)),
    ]:
        draw.ellipse([x - 8, y - 8, x + 8, y + 8], fill=color)
        draw.ellipse([x - 30, y - 30, x + 30, y + 30], fill=(color[0], color[1], color[2], 18))
    layer = layer.filter(ImageFilter.GaussianBlur(0.5))
    base.alpha_composite(layer)


def add_deep_space_void(base: Image.Image) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    pix = layer.load()
    for y in range(height):
        ny = y / max(1, height - 1)
        for x in range(width):
            nx = x / max(1, width - 1)
            edge_depth = min(1.0, math.hypot((nx - 0.50) * 1.28, (ny - 0.44) * 1.18))
            top_void = max(0.0, 1.0 - ny / 0.28)
            bottom_void = max(0.0, (ny - 0.64) / 0.36)
            galaxy_keep = max(0.0, 1.0 - math.hypot((nx - 0.52) * 1.16, (ny - 0.31) * 2.25))
            center_card_keep = max(0.0, 1.0 - math.hypot((nx - 0.50) * 1.75, (ny - 0.53) * 2.95))
            alpha = int(24 + 112 * edge_depth**1.55 + 60 * top_void + 92 * bottom_void - 48 * galaxy_keep - 24 * center_card_keep)
            pix[x, y] = (0, 2, 10, clamp(alpha, 0, 202))
    layer = layer.filter(ImageFilter.GaussianBlur(20))
    base.alpha_composite(layer)


def add_real_nebula_accent(base: Image.Image) -> None:
    source_path = SOURCE_NGC1514_IMAGE if SOURCE_NGC1514_IMAGE.exists() else SOURCE_CARINA_IMAGE
    if not source_path.exists():
        return
    width, height = base.size
    source = Image.open(source_path).convert("RGB")
    accent_w = int(width * 1.48)
    accent_h = int(height * 0.58)
    accent = ImageOps.fit(source, (accent_w, accent_h), method=Image.Resampling.LANCZOS, centering=(0.50, 0.46))
    accent = accent.filter(ImageFilter.GaussianBlur(0.7))
    accent = ImageEnhance.Brightness(accent).enhance(0.74)
    accent = ImageEnhance.Contrast(accent).enhance(1.28)
    accent = ImageEnhance.Color(accent).enhance(1.10).convert("RGBA")
    cool_lift = Image.new("RGBA", accent.size, (20, 54, 108, 38))
    accent = screen(accent, cool_lift)
    accent_mask = radial_mask(accent.width, accent.height, 0.55, 0.50, 0.50, 0.45, 142, inner=0.12)
    accent.putalpha(ImageChops.multiply(accent.getchannel("A"), accent_mask))
    accent = accent.rotate(-12, resample=Image.Resampling.BICUBIC, expand=True)

    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    composite_centered(layer, accent, int(width * 0.62), int(height * 0.20))
    layer = layer.filter(ImageFilter.GaussianBlur(1.4))
    base.alpha_composite(layer)


def add_cosmic_dust_lanes(base: Image.Image) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    rng = random.Random(2026070105)
    for band in range(13):
        y_base = height * (0.12 + band * 0.036)
        points: list[tuple[float, float]] = []
        wave = rng.uniform(0.26, 0.46)
        phase = rng.uniform(0, math.tau)
        for i in range(72):
            t = i / 71
            x = width * (-0.10 + t * 1.20)
            y = y_base + math.sin(t * math.tau * wave + phase) * (22 + band * 1.7) + (t - 0.5) * height * 0.07
            points.append((x, y))
        draw.line(points, fill=(0, 3, 13, 20 + band), width=14 + band * 2, joint="curve")
    layer = layer.rotate(-8, resample=Image.Resampling.BICUBIC, center=(width * 0.52, height * 0.30))
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), upper_galaxy_mask(width, height, 0.70)))
    layer = layer.filter(ImageFilter.GaussianBlur(8))
    base.alpha_composite(layer)


def add_distant_galaxy_specks(base: Image.Image) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    rng = random.Random(2026070109)
    for _ in range(430):
        x = rng.uniform(0, width)
        y = rng.uniform(0, height)
        if width * 0.10 < x < width * 0.90 and height * 0.30 < y < height * 0.72 and rng.random() < 0.64:
            continue
        r = rng.uniform(0.28, 1.20)
        alpha = rng.randint(34, 126)
        color = (226, 244, 255, alpha)
        roll = rng.random()
        if roll < 0.10:
            color = (116, 214, 255, alpha)
        elif roll < 0.16:
            color = (255, 132, 208, int(alpha * 0.86))
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)

    for _ in range(30):
        cluster = Image.new("RGBA", (84, 44), (0, 0, 0, 0))
        cluster_draw = ImageDraw.Draw(cluster, "RGBA")
        tint = (116, 205, 255) if rng.random() < 0.7 else (248, 118, 208)
        cluster_draw.ellipse([14, 15, 70, 29], fill=(*tint, rng.randint(3, 8)))
        for _dot in range(18):
            dx = rng.gauss(42, 15)
            dy = rng.gauss(22, 6)
            rr = rng.uniform(0.25, 0.62)
            aa = rng.randint(26, 78)
            cluster_draw.ellipse([dx - rr, dy - rr, dx + rr, dy + rr], fill=(232, 246, 255, aa))
        cluster = cluster.filter(ImageFilter.GaussianBlur(0.35)).rotate(rng.uniform(-32, 32), resample=Image.Resampling.BICUBIC, expand=True)
        x = int(rng.uniform(width * 0.02, width * 0.98))
        y = int(rng.choice((rng.uniform(height * 0.03, height * 0.46), rng.uniform(height * 0.78, height * 0.94))))
        if width * 0.18 < x < width * 0.82 and height * 0.34 < y < height * 0.68 and rng.random() < 0.82:
            continue
        composite_centered(layer, cluster, x, y)

    for x, y, color in [
        (width * 0.13, height * 0.10, (156, 226, 255, 128)),
        (width * 0.82, height * 0.17, (252, 156, 220, 116)),
        (width * 0.72, height * 0.77, (146, 218, 255, 94)),
        (width * 0.22, height * 0.84, (232, 246, 255, 92)),
    ]:
        draw.line([(x - 18, y), (x + 18, y)], fill=color, width=2)
        draw.line([(x, y - 18), (x, y + 18)], fill=color, width=2)
        draw.ellipse([x - 3.2, y - 3.2, x + 3.2, y + 3.2], fill=(255, 255, 255, min(210, color[3] + 55)))
    layer = layer.filter(ImageFilter.GaussianBlur(0.18))
    base.alpha_composite(layer)


def add_spiral_vortex(base: Image.Image, phase: float = 0.0) -> None:
    width, height = base.size
    cx = width * 0.57
    cy = height * 0.42
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    rng = random.Random(2026063007)

    for arm in range(5):
        arm_shift = arm * math.tau / 5 + 0.52
        for i in range(760):
            t = i / 760
            angle = arm_shift + t * math.tau * 1.72 + 0.12 * math.sin(t * math.tau * 4)
            radius = 34 + t * width * 0.72
            thickness = max(1.2, 20 * (1 - t) + 2)
            wobble = rng.uniform(-1, 1) * 16 * (1 - t * 0.35)
            x = cx + math.cos(angle) * radius * (1.05 + 0.05 * math.sin(t * 7)) + wobble
            y = cy + math.sin(angle) * radius * 0.50 + wobble * 0.20
            alpha = int(42 * (1 - t) + 9)
            color = (126, 205, 255, alpha) if arm % 2 == 0 else (226, 98, 204, int(alpha * 0.86))
            draw.ellipse([x - thickness, y - thickness * 0.48, x + thickness, y + thickness * 0.48], fill=color)

    core = Image.new("RGBA", base.size, (0, 0, 0, 0))
    core_draw = ImageDraw.Draw(core, "RGBA")
    for r, a, color in [
        (190, 42, (128, 206, 255)),
        (142, 48, (238, 118, 214)),
        (92, 52, (90, 184, 255)),
    ]:
        core_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color, a))
    core_draw.ellipse([cx - 78, cy - 78, cx + 78, cy + 78], fill=(5, 15, 31, 205))
    core_draw.arc([cx - 88, cy - 88, cx + 88, cy + 88], 18, 300, fill=(160, 224, 255, 82), width=4)
    layer = layer.filter(ImageFilter.GaussianBlur(13))
    core = core.filter(ImageFilter.GaussianBlur(5))
    base.alpha_composite(layer)
    base.alpha_composite(core)


def add_bottom_nebula_ridge(base: Image.Image) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    rng = random.Random(2026063011)
    for band in range(7):
        y_base = height * (0.70 + band * 0.033)
        curve: list[tuple[float, float]] = []
        for i in range(64):
            x = width * (i / 63)
            y = y_base + math.sin(i * 0.32 + band * 0.7) * (26 + band * 4) + rng.uniform(-8, 8)
            curve.append((x, y))
        fill_points = [(0, height)] + curve + [(width, height)]
        draw.polygon(fill_points, fill=(2, 5, 17, 90 + band * 18))
    layer = layer.filter(ImageFilter.GaussianBlur(8))
    base.alpha_composite(layer)

    rim = Image.new("RGBA", base.size, (0, 0, 0, 0))
    rim_draw = ImageDraw.Draw(rim, "RGBA")
    for band in range(8):
        points: list[tuple[float, float]] = []
        y_base = height * (0.70 + band * 0.030)
        for i in range(42):
            x = width * (i / 41)
            y = y_base + math.sin(i * 0.50 + band) * 18 + rng.uniform(-9, 9)
            points.append((x, y))
        color = (76, 164, 255, 42) if band % 2 else (218, 84, 204, 34)
        rim_draw.line(points, fill=color, width=10 + band * 2, joint="curve")
    rim = rim.filter(ImageFilter.GaussianBlur(9))
    base.alpha_composite(rim)


def add_static_star_depth(base: Image.Image) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    rng = random.Random(2026063023)
    for _ in range(190):
        x = rng.uniform(0, width)
        y = rng.uniform(0, height)
        if width * 0.18 < x < width * 0.86 and height * 0.31 < y < height * 0.70 and rng.random() < 0.72:
            continue
        r = rng.uniform(0.45, 1.45)
        alpha = rng.randint(60, 165)
        color = (226, 246, 255, alpha)
        if rng.random() < 0.10:
            color = (255, 120, 210, alpha)
        elif rng.random() < 0.18:
            color = (116, 215, 255, alpha)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
    layer = layer.filter(ImageFilter.GaussianBlur(0.2))
    base.alpha_composite(layer)


def add_starfield(base: Image.Image, stars: list[tuple[float, float, float, float, float]], phase: float) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    for sx, sy, size, hue, offset in stars:
        depth = 0.65 + size * 0.9
        zoom = 1.0 + 0.025 * math.sin(phase * math.tau + offset * math.tau)
        x = width * (0.5 + (sx - 0.5) * zoom)
        y = height * (0.5 + (sy - 0.5) * zoom)
        pulse = 0.55 + 0.45 * math.sin((phase * 0.85 + offset) * math.tau)
        alpha = int((18 + 52 * pulse) * min(1.0, depth))
        if hue < 0.72:
            color = (224, 246, 255, alpha)
        elif hue < 0.9:
            color = (120, 211, 255, alpha)
        else:
            color = (255, 124, 207, int(alpha * 0.82))
        r = max(0.55, size * 1.2)
        if size > 1.05:
            draw.ellipse([x - r * 3, y - r * 3, x + r * 3, y + r * 3], fill=(90, 190, 255, alpha // 20))
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
    layer = layer.filter(ImageFilter.GaussianBlur(0.15))
    base.alpha_composite(layer)


def add_vignette(base: Image.Image) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    pix = layer.load()
    for y in range(height):
        ny = (y / height - 0.5) * 2
        for x in range(width):
            nx = (x / width - 0.5) * 2
            d = min(1.0, math.hypot(nx * 0.9, ny * 0.78))
            alpha = int(max(0, d - 0.38) / 0.62 * 175)
            pix[x, y] = (0, 0, 10, alpha)
    base.alpha_composite(layer)


def add_readability_well(base: Image.Image) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    draw.rounded_rectangle(
        [width * 0.06, height * 0.28, width * 0.94, height * 0.73],
        radius=int(width * 0.06),
        fill=(0, 3, 14, 18),
    )
    layer = layer.filter(ImageFilter.GaussianBlur(34))
    base.alpha_composite(layer)


def make_base_plate(width: int, height: int) -> Image.Image:
    if SOURCE_COSMIC_IMAGE.exists() or SOURCE_CARINA_IMAGE.exists():
        return make_reference_like_space_plate(width, height)

    base = build_deep_space(width, height)
    add_faint_real_space_texture(base)
    add_top_depth_lights(base)
    add_nebula_clouds(base, 20260630)
    add_spiral_vortex(base)
    add_bottom_nebula_ridge(base)
    add_static_star_depth(base)
    add_readability_well(base)
    add_vignette(base)
    return base.convert("RGB")


def make_reference_like_space_plate(width: int, height: int) -> Image.Image:
    if SOURCE_COSMIC_IMAGE.exists():
        source = Image.open(SOURCE_COSMIC_IMAGE).convert("RGB")
        source = ImageOps.fit(source, (width, height), method=Image.Resampling.LANCZOS, centering=(0.50, 0.50))
        source = source.filter(ImageFilter.GaussianBlur(0.28))
        source = ImageEnhance.Brightness(source).enhance(0.68)
        source = ImageEnhance.Contrast(source).enhance(1.42)
        source = ImageEnhance.Color(source).enhance(0.98)
        luma = ImageOps.grayscale(source)
        blue_violet = ImageOps.colorize(luma, black="#010513", white="#8bd9ff").convert("RGBA")
        plate = Image.blend(source.convert("RGBA"), blue_violet, 0.28)
        plate = screen(plate, Image.new("RGBA", (width, height), (3, 20, 74, 32)))
        plate.alpha_composite(Image.new("RGBA", (width, height), (32, 8, 84, 8)))
        add_real_nebula_accent(plate)
        add_deep_space_void(plate)
        add_cosmic_dust_lanes(plate)

        card_dim = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        card_draw = ImageDraw.Draw(card_dim, "RGBA")
        card_draw.rounded_rectangle(
            [width * 0.07, height * 0.29, width * 0.93, height * 0.72],
            radius=int(width * 0.055),
            fill=(0, 3, 14, 22),
        )
        card_draw.rectangle([0, int(height * 0.73), width, height], fill=(0, 3, 14, 52))
        card_draw.rectangle([0, 0, width, int(height * 0.08)], fill=(0, 3, 14, 28))
        card_dim = card_dim.filter(ImageFilter.GaussianBlur(34))
        plate.alpha_composite(card_dim)

        add_reference_top_wisps(plate)
        lower_depth = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        lower_draw = ImageDraw.Draw(lower_depth, "RGBA")
        lower_draw.rectangle([0, int(height * 0.70), width, height], fill=(0, 3, 14, 56))
        lower_depth = lower_depth.filter(ImageFilter.GaussianBlur(40))
        plate.alpha_composite(lower_depth)
        add_distant_galaxy_specks(plate)
        add_reference_star_accents(plate)
        add_readability_well(plate)
        add_vignette(plate)
        return plate.convert("RGB")

    plate = build_deep_space(width, height)
    add_reference_top_wisps(plate)
    add_reference_hotlist_vortex(plate)
    add_reference_bottom_cloud_ocean(plate)
    dark = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    dark_draw = ImageDraw.Draw(dark, "RGBA")
    dark_draw.rectangle([0, 0, width, int(height * 0.06)], fill=(0, 3, 14, 46))
    dark_draw.rectangle([0, int(height * 0.74), width, height], fill=(0, 3, 14, 88))
    dark_draw.rounded_rectangle(
        [width * 0.08, height * 0.31, width * 0.92, height * 0.70],
        radius=int(width * 0.055),
        fill=(0, 3, 14, 34),
    )
    dark = dark.filter(ImageFilter.GaussianBlur(30))
    plate.alpha_composite(dark)

    add_reference_star_accents(plate)
    add_readability_well(plate)
    add_vignette(plate)
    return plate.convert("RGB")


def prepare_galaxy_sprite(width: int) -> Image.Image | None:
    if not SOURCE_COSMIC_IMAGE.exists():
        return None
    source = Image.open(SOURCE_COSMIC_IMAGE).convert("RGB")
    size = int(width * 2.45)
    sprite = ImageOps.fit(source, (size, size), method=Image.Resampling.LANCZOS, centering=(0.44, 0.47))
    sprite = sprite.filter(ImageFilter.GaussianBlur(0.25))
    sprite = ImageEnhance.Brightness(sprite).enhance(0.66)
    sprite = ImageEnhance.Contrast(sprite).enhance(1.34)
    sprite = ImageEnhance.Color(sprite).enhance(1.02)
    luma = ImageOps.grayscale(sprite)
    cool = ImageOps.colorize(luma, black="#01030d", white="#9be6ff").convert("RGBA")
    sprite = Image.blend(sprite.convert("RGBA"), cool, 0.30)
    sprite = screen(sprite, Image.new("RGBA", sprite.size, (28, 16, 98, 26)))
    return sprite.convert("RGBA")


def add_reference_style_fog(base: Image.Image, phase: float) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    shift_x = math.sin(phase * math.tau * 0.74) * width * 0.020
    shift_y = math.cos(phase * math.tau * 0.58) * height * 0.014
    draw.ellipse(
        [
            width * 0.03 + shift_x,
            height * 0.08 + shift_y,
            width * 1.05 + shift_x,
            height * 0.58 + shift_y,
        ],
        fill=(70, 184, 255, 14),
    )
    draw.ellipse(
        [
            width * 0.06 - shift_x * 0.8,
            height * 0.40 - shift_y,
            width * 1.00 - shift_x * 0.8,
            height * 0.91 - shift_y,
        ],
        fill=(228, 78, 202, 9),
    )
    layer = layer.filter(ImageFilter.GaussianBlur(54))
    base.alpha_composite(layer)


def composite_centered(canvas: Image.Image, layer: Image.Image, center_x: int, center_y: int) -> None:
    left = int(center_x - layer.width / 2)
    top = int(center_y - layer.height / 2)
    src_left = max(0, -left)
    src_top = max(0, -top)
    dst_left = max(0, left)
    dst_top = max(0, top)
    paste_width = min(layer.width - src_left, canvas.width - dst_left)
    paste_height = min(layer.height - src_top, canvas.height - dst_top)
    if paste_width <= 0 or paste_height <= 0:
        return
    crop = layer.crop((src_left, src_top, src_left + paste_width, src_top + paste_height))
    canvas.alpha_composite(crop, (dst_left, dst_top))


@lru_cache(maxsize=16)
def upper_galaxy_mask(width: int, height: int, opacity: float) -> Image.Image:
    mask = Image.new("L", (width, height), 0)
    pix = mask.load()
    max_alpha = int(255 * opacity)
    fade_start = int(height * 0.58)
    fade_end = int(height * 0.82)
    for y in range(height):
        if y < fade_start:
            alpha = max_alpha
        elif y < fade_end:
            t = (y - fade_start) / max(1, fade_end - fade_start)
            alpha = int(max_alpha * (1 - t) ** 1.7)
        else:
            alpha = 0
        for x in range(width):
            pix[x, y] = alpha
    return mask.filter(ImageFilter.GaussianBlur(22))


def add_rotating_galaxy_overlay(base: Image.Image, galaxy_sprite: Image.Image | None, phase: float) -> None:
    if galaxy_sprite is None:
        add_animated_nebula_breath(base, phase)
        return
    width, height = base.size
    cx = int(width * 0.50)
    cy = int(height * 0.30)
    work_size = int(width * 2.45)
    work_center = work_size // 2

    combined = Image.new("RGBA", base.size, (0, 0, 0, 0))
    for turn, opacity, scale, extra_phase in ((1, 0.40, 1.10, 0.00), (-1, 0.14, 1.22, 0.31)):
        angle = -10 + turn * (phase * 360 * 0.11 + extra_phase * 18)
        sprite_size = int(work_size * scale)
        sprite = galaxy_sprite.resize((sprite_size, sprite_size), Image.Resampling.BICUBIC)
        work = Image.new("RGBA", (work_size, work_size), (0, 0, 0, 0))
        work.alpha_composite(sprite, ((work_size - sprite_size) // 2, (work_size - sprite_size) // 2))
        rotated = work.rotate(angle, resample=Image.Resampling.BICUBIC, center=(work_center, work_center))
        layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        composite_centered(layer, rotated, cx, cy)
        mask = upper_galaxy_mask(width, height, opacity)
        layer.putalpha(ImageChops.multiply(layer.getchannel("A"), mask))
        combined.alpha_composite(layer)

    core = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(core, "RGBA")
    pulse = 0.78 + 0.22 * math.sin(phase * math.tau * 1.8)
    draw.ellipse(
        [cx - width * 0.38, cy - width * 0.16, cx + width * 0.38, cy + width * 0.16],
        fill=(92, 190, 255, int(14 * pulse)),
    )
    draw.ellipse(
        [cx - width * 0.24, cy - width * 0.10, cx + width * 0.24, cy + width * 0.10],
        fill=(255, 112, 204, int(7 * pulse)),
    )
    core.putalpha(ImageChops.multiply(core.getchannel("A"), upper_galaxy_mask(width, height, 0.38)))
    core = core.filter(ImageFilter.GaussianBlur(24))
    combined.alpha_composite(core)
    base.alpha_composite(combined)


def add_animated_nebula_breath(base: Image.Image, phase: float) -> None:
    width, height = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    shift_x = math.sin(phase * math.tau) * width * 0.018
    shift_y = math.cos(phase * math.tau) * height * 0.012
    draw.ellipse(
        [
            width * 0.15 + shift_x,
            height * 0.20 + shift_y,
            width * 1.05 + shift_x,
            height * 0.72 + shift_y,
        ],
        fill=(80, 170, 255, 24),
    )
    draw.ellipse(
        [
            width * 0.20 - shift_x * 0.7,
            height * 0.36 - shift_y,
            width * 0.95 - shift_x * 0.7,
            height * 0.83 - shift_y,
        ],
        fill=(236, 86, 205, 18),
    )
    layer = layer.rotate(-12 + 1.2 * math.sin(phase * math.tau), resample=Image.Resampling.BICUBIC, center=(width * 0.55, height * 0.50))
    layer = layer.filter(ImageFilter.GaussianBlur(42))
    base.alpha_composite(layer)


def animated_background_frame(
    base_plate: Image.Image,
    frame: int,
    total: int,
    stars: list[tuple[float, float, float, float, float]],
    width: int,
    height: int,
    galaxy_sprite: Image.Image | None,
) -> Image.Image:
    phase = frame / total
    frame_img = base_plate.convert("RGBA").copy()
    add_reference_style_fog(frame_img, phase)
    add_rotating_galaxy_overlay(frame_img, galaxy_sprite, phase)
    add_starfield(frame_img, stars, phase)
    return frame_img.convert("RGB")


def rounded_rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: tuple[int, int, int, int], outline: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)


def draw_centered(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt: ImageFont.ImageFont, fill: tuple[int, int, int, int]) -> None:
    bbox = draw.textbbox((0, 0), text, font=fnt)
    draw.text((xy[0] - (bbox[2] - bbox[0]) / 2, xy[1] - (bbox[3] - bbox[1]) / 2), text, font=fnt, fill=fill)


def draw_centered_shadow(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt: ImageFont.ImageFont, fill: tuple[int, int, int, int]) -> None:
    for dx, dy in ((0, 4), (2, 2), (-2, 2)):
        draw_centered(draw, (xy[0] + dx, xy[1] + dy), text, fnt, (0, 4, 14, 205))
    draw_centered(draw, xy, text, fnt, fill)


def preview_frame(background: Image.Image) -> Image.Image:
    image = background.convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    w, h = image.size
    card = (80, 585, w - 80, 1325)
    rounded_rect(draw, card, 34, (2, 7, 24, 82), (255, 255, 255, 76))
    draw_centered_shadow(draw, (w // 2, 715), "🔥", font(84, True), (255, 180, 60, 255))
    draw.rounded_rectangle((155, 770, w - 155, 890), radius=30, fill=(2, 8, 24, 52), outline=(255, 255, 255, 44), width=1)
    draw_centered_shadow(draw, (w // 2, 830), "蚂蚁AI 热榜 TOP5", font(78, True), (232, 248, 255, 255))
    draw.rounded_rectangle((390, 900, 690, 958), radius=29, fill=(8, 18, 42, 76), outline=(255, 255, 255, 54), width=1)
    draw_centered_shadow(draw, (w // 2, 930), "AI HOTLIST", font(32, True), (235, 245, 255, 245))
    y = 1050
    samples = [
        ("TOP1", "真实来源 + 日期 + 分数"),
        ("TOP2", "一句趋势理由"),
        ("TOP3", "一个用户行动"),
    ]
    for idx, (rank, line) in enumerate(samples):
        yy = y + idx * 72
        draw.rounded_rectangle((215, yy - 28, 865, yy + 32), radius=18, fill=(9, 25, 54, 78), outline=(255, 255, 255, 28), width=1)
        draw.text((252, yy - 16), rank, font=font(32, True), fill=(0, 4, 14, 165))
        draw.text((250, yy - 18), rank, font=font(32, True), fill=(238, 246, 255, 255))
        draw.text((374, yy - 16), line, font=font(30, True), fill=(0, 4, 14, 155))
        draw.text((372, yy - 18), line, font=font(30, True), fill=(226, 238, 250, 245))
    draw.line((325, 1268, 755, 1268), fill=(82, 185, 255, 255), width=4)
    draw.line((540, 1268, 755, 1268), fill=(255, 90, 155, 255), width=4)
    image.alpha_composite(overlay)
    return image.convert("RGB")


def encode_video(frame_dir: Path, pattern: str, out: Path, fps: int) -> None:
    subprocess.run(
        [
            ffmpeg_bin(),
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-framerate",
            str(fps),
            "-i",
            str(frame_dir / pattern),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(out),
        ],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--duration", type=float, default=8.0)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    args = parser.parse_args()

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    frames_dir = PREVIEW_DIR / "_ant_ai_bg_frames"
    preview_frames_dir = PREVIEW_DIR / "_ant_ai_preview_frames"
    shutil.rmtree(frames_dir, ignore_errors=True)
    shutil.rmtree(preview_frames_dir, ignore_errors=True)
    frames_dir.mkdir(parents=True)
    preview_frames_dir.mkdir(parents=True)

    rng = random.Random(20260630)
    base_plate = make_base_plate(args.width, args.height)
    galaxy_sprite = prepare_galaxy_sprite(args.width)
    stars = [(rng.random(), rng.random(), rng.uniform(0.20, 1.04), rng.random(), rng.random()) for _ in range(260)]
    total = int(args.fps * args.duration)
    poster: Image.Image | None = None
    for frame in range(total):
        bg = animated_background_frame(base_plate, frame, total, stars, args.width, args.height, galaxy_sprite)
        if frame == 0:
            poster = bg.copy()
        bg.save(frames_dir / f"frame_{frame:04d}.png")
        if frame < min(total, args.fps * 5):
            preview_frame(bg).save(preview_frames_dir / f"frame_{frame:04d}.png")

    asset_mp4 = ASSET_DIR / "BG_DYNAMIC_11_蚂蚁AI热榜星云_9x16.mp4"
    poster_png = ASSET_DIR / "BG_DYNAMIC_11_蚂蚁AI热榜星云_9x16.poster.png"
    preview_mp4 = PREVIEW_DIR / "ant_ai_hotlist_template_preview.mp4"
    preview_png = PREVIEW_DIR / "ant_ai_hotlist_template_preview.png"
    if poster is None:
        raise RuntimeError("poster frame not generated")
    poster.save(poster_png)
    preview_frame(poster).save(preview_png)
    encode_video(frames_dir, "frame_%04d.png", asset_mp4, args.fps)
    encode_video(preview_frames_dir, "frame_%04d.png", preview_mp4, args.fps)
    subprocess.run(
        [
            ffmpeg_bin(),
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(asset_mp4),
            "-vf",
            "fps=1,scale=270:-1,tile=5x1",
            "-frames:v",
            "1",
            str(PREVIEW_DIR / "ant_ai_hotlist_background_contact_sheet.jpg"),
        ],
        check=True,
    )
    subprocess.run(
        [
            ffmpeg_bin(),
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(preview_mp4),
            "-vf",
            "fps=1,scale=270:-1,tile=5x1",
            "-frames:v",
            "1",
            str(PREVIEW_DIR / "ant_ai_hotlist_template_preview_contact_sheet.jpg"),
        ],
        check=True,
    )
    shutil.rmtree(frames_dir, ignore_errors=True)
    shutil.rmtree(preview_frames_dir, ignore_errors=True)
    print(asset_mp4)
    print(preview_png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
