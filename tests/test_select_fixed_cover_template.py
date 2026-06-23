from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SELECTOR = ROOT / "scripts" / "select_fixed_cover_template.py"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_image(path: Path, size: tuple[int, int], color: tuple[int, int, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", size, color).save(path)


def make_manifest(tmp_path: Path) -> Path:
    assets = tmp_path / "assets"
    make_image(assets / "h01.jpg", (1920, 1080), (10, 20, 30))
    make_image(assets / "h02.jpg", (1920, 1080), (20, 30, 40))
    make_image(assets / "v01.jpg", (1080, 1920), (30, 40, 50))
    manifest = {
        "version": "2.0-test",
        "templates": [
            {
                "id": "T01",
                "name": "横版一",
                "ratio": "16x9",
                "file": str(assets / "h01.jpg"),
                "accent_rgb": [66, 211, 255],
                "recommended_text_safe_rect_px": [690, 150, 1230, 820],
                "douyin_center_crop_rect_px": [656, 0, 1264, 1080],
                "douyin_center_text_safe_rect_px": [690, 150, 1230, 820],
                "runtime_text_backdrop": {"recommended": True, "overlay_rgba": "rgba(2,7,18,0.18)", "feather_px": 48},
                "background_contains_text": False,
            },
            {
                "id": "T02",
                "name": "横版二",
                "ratio": "16x9",
                "file": str(assets / "h02.jpg"),
                "accent_rgb": [48, 224, 192],
                "recommended_text_safe_rect_px": [690, 150, 1230, 820],
                "douyin_center_crop_rect_px": [656, 0, 1264, 1080],
                "douyin_center_text_safe_rect_px": [690, 150, 1230, 820],
                "runtime_text_backdrop": {"recommended": True, "overlay_rgba": "rgba(2,7,18,0.18)", "feather_px": 48},
                "background_contains_text": False,
            },
            {
                "id": "T01",
                "name": "竖版一",
                "ratio": "9x16",
                "file": str(assets / "v01.jpg"),
                "accent_rgb": [66, 211, 255],
                "recommended_text_safe_rect_px": [55, 100, 1025, 675],
                "douyin_center_crop_rect_px": [0, 0, 1080, 1920],
                "douyin_center_text_safe_rect_px": [55, 100, 1025, 675],
                "runtime_text_backdrop": {"recommended": True, "overlay_rgba": "rgba(2,7,18,0.18)", "feather_px": 48},
                "background_contains_text": False,
            },
        ],
    }
    path = tmp_path / "manifest.json"
    write_json(path, manifest)
    return path


def run_selector(tmp_path: Path, project: Path, manifest: Path, *extra: str) -> dict:
    state = tmp_path / "state.json"
    result = subprocess.run(
        [
            sys.executable,
            str(SELECTOR),
            "--project",
            str(project),
            "--manifest",
            str(manifest),
            "--state-file",
            str(state),
            "--cover-text",
            "测试封面标题|封面副标题",
            *extra,
        ],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    return json.loads((project / "internal" / "publish_cover_report.json").read_text(encoding="utf-8"))


def test_selects_horizontal_templates_sequentially(tmp_path: Path) -> None:
    manifest = make_manifest(tmp_path)
    project = tmp_path / "outputs" / "demo"

    first = run_selector(tmp_path, project, manifest, "--video-width", "1920", "--video-height", "1080")
    second = run_selector(tmp_path, project, manifest, "--video-width", "1920", "--video-height", "1080")

    assert first["template_id"] == "T01"
    assert second["template_id"] == "T02"
    assert first["cover_type"] == "fixed_pure_background_runtime_text_first_frame"
    assert first["selection_method"] == "sequential_by_size_pool"
    assert first["frame_grab_used"] is False
    assert first["checks"]["template_from_fixed_library"] is True
    assert first["checks"]["fixed_pure_background_asset"] is True
    assert first["checks"]["dynamic_text_overlay_used"] is True
    assert first["checks"]["uses_old_cover_template_asset"] is False
    assert first["checks"]["cover_text_fit_safe_rect"] is True
    assert first["checks"]["primary_text_inside_douyin_center_crop"] is True
    assert first["checks"]["douyin_center_crop_preview_generated"] is True
    assert first["checks"]["compact_cover_text_used"] is True
    assert first["cover_layout"]["text_bbox_inside_douyin_center_crop"] is True
    assert first["checks"]["cover_text_written"] is True
    assert (project / "internal" / "cover.png").exists()
    assert (project / "internal" / "first_frame_cover.png").exists()
    assert (project / "internal" / "cover_publish_horizontal.png").exists()
    assert (project / "internal" / "cover_publish_vertical.png").exists()
    assert (project / "internal" / "cover_publish_douyin_center_crop.png").exists()


def test_selects_vertical_pool_without_advancing_horizontal(tmp_path: Path) -> None:
    manifest = make_manifest(tmp_path)
    project = tmp_path / "outputs" / "demo"

    vertical = run_selector(tmp_path, project, manifest, "--video-width", "1080", "--video-height", "1920")
    horizontal = run_selector(tmp_path, project, manifest, "--video-width", "1920", "--video-height", "1080")

    assert vertical["template_id"] == "T01"
    assert vertical["template_aspect"] == "9:16"
    assert vertical["video_aspect"] == "9:16"
    assert horizontal["template_id"] == "T01"
    assert horizontal["template_aspect"] == "16:9"


def test_requires_checked_cover_text_with_project_relative_path(tmp_path: Path) -> None:
    manifest = make_manifest(tmp_path)
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    internal.mkdir(parents=True)
    (internal / "publish_cover_text.txt").write_text("测试封面标题\n封面副标题\n", encoding="utf-8")
    write_json(
        internal / "on_screen_and_publish_text_compliance_report.json",
        {
            "status": "passed",
            "checked_files": ["internal/publish_cover_text.txt"],
            "risk_items": [],
            "summary": {"error_count": 0, "warning_count": 0},
        },
    )

    report = run_selector(
        tmp_path,
        project,
        manifest,
        "--video-width",
        "1920",
        "--video-height",
        "1080",
        "--require-checked-cover-text",
    )

    assert report["text_policy"]["checked_before_render"] is True
    assert report["text_policy"]["checked_cover_text_report"].endswith("on_screen_and_publish_text_compliance_report.json")
