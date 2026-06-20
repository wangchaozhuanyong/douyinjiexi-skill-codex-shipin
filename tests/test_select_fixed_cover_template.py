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
        "version": 1,
        "qingdou_visible_result": "未检查到敏感词",
        "pools": {
            "horizontal_16x9": [
                {
                    "template_id": "H01",
                    "canonical_id": "COV_AI_06",
                    "name": "横版一",
                    "aspect": "16:9",
                    "file": str(assets / "h01.jpg"),
                    "visible_text": ["AI解码", "横壹"],
                },
                {
                    "template_id": "H02",
                    "canonical_id": "COV_AI_07",
                    "name": "横版二",
                    "aspect": "16:9",
                    "file": str(assets / "h02.jpg"),
                    "visible_text": ["AI解码", "横贰"],
                },
            ],
            "vertical_9x16": [
                {
                    "template_id": "V01",
                    "canonical_id": "COV_AI_01",
                    "name": "竖版一",
                    "aspect": "9:16",
                    "file": str(assets / "v01.jpg"),
                    "visible_text": ["AI解码", "竖壹"],
                }
            ],
        },
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

    assert first["template_id"] == "H01"
    assert second["template_id"] == "H02"
    assert first["selection_method"] == "sequential_by_size_pool"
    assert first["frame_grab_used"] is False
    assert first["checks"]["template_from_fixed_library"] is True
    assert first["checks"]["cover_text_written"] is True
    assert (project / "internal" / "cover.png").exists()
    assert (project / "internal" / "first_frame_cover.png").exists()
    assert (project / "internal" / "cover_publish_horizontal.png").exists()
    assert (project / "internal" / "cover_publish_vertical.png").exists()


def test_selects_vertical_pool_without_advancing_horizontal(tmp_path: Path) -> None:
    manifest = make_manifest(tmp_path)
    project = tmp_path / "outputs" / "demo"

    vertical = run_selector(tmp_path, project, manifest, "--video-width", "1080", "--video-height", "1920")
    horizontal = run_selector(tmp_path, project, manifest, "--video-width", "1920", "--video-height", "1080")

    assert vertical["template_id"] == "V01"
    assert vertical["template_aspect"] == "9:16"
    assert vertical["video_aspect"] == "9:16"
    assert horizontal["template_id"] == "H01"
    assert horizontal["template_aspect"] == "16:9"
