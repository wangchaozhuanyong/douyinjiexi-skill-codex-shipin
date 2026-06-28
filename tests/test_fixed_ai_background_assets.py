from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_fixed_ai_background_assets.py"
DYNAMIC_GENERATOR = ROOT / "scripts" / "generate_dynamic_ai_background_assets.py"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_generator(library: Path, out_dir: Path, manifest: Path, *extra: str) -> dict:
    result = subprocess.run(
        [
            sys.executable,
            str(GENERATOR),
            "--library",
            str(library),
            "--out-dir",
            str(out_dir),
            "--manifest-out",
            str(manifest),
            *extra,
        ],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(manifest.read_text(encoding="utf-8"))


def make_library(path: Path) -> Path:
    write_json(
        path,
        {
            "version": 1,
            "templates": [
                {
                    "id": "BG_TEST_01",
                    "name": "横版测试",
                    "aspect": "16:9",
                    "width": 320,
                    "height": 180,
                    "visual_family": "quantum_ring_core",
                    "palette": ["deep navy", "electric cyan", "violet", "silver metal"],
                    "asset_source_type": "fixed_generated_background_asset",
                    "asset_generation_method": "deterministic_pil_fixed_asset_v1",
                },
                {
                    "id": "BG_TEST_02",
                    "name": "竖版测试",
                    "aspect": "9:16",
                    "width": 180,
                    "height": 320,
                    "visual_family": "vertical_tool_test_chamber",
                    "palette": ["deep navy", "cyan", "silver", "small amber"],
                    "asset_source_type": "fixed_generated_background_asset",
                    "asset_generation_method": "deterministic_pil_fixed_asset_v1",
                },
            ],
        },
    )
    return path


def test_generates_fixed_background_assets_and_manifest(tmp_path: Path) -> None:
    library = make_library(tmp_path / "backgrounds.json")
    out_dir = tmp_path / "assets"
    manifest_path = tmp_path / "asset_manifest.json"

    manifest = run_generator(library, out_dir, manifest_path)

    assert manifest["status"] == "passed"
    assert manifest["asset_count"] == 2
    assert manifest["checks"]["no_baked_text_policy"] is True
    for asset in manifest["assets"]:
        path = ROOT / asset["path"] if not Path(asset["path"]).is_absolute() else Path(asset["path"])
        if not path.exists():
            path = out_dir / Path(asset["path"]).name
        assert path.exists()
        image = Image.open(path)
        assert image.size == (asset["width"], asset["height"])
        assert asset["checks"]["dimensions_match_template"] is True
        assert asset["checks"]["foreground_text_must_be_overlay"] is True


def test_preserves_existing_assets_without_force(tmp_path: Path) -> None:
    library = make_library(tmp_path / "backgrounds.json")
    out_dir = tmp_path / "assets"
    out_dir.mkdir(parents=True)
    existing = out_dir / "BG_TEST_01_横版测试_16x9.png"
    Image.new("RGB", (320, 180), (7, 8, 9)).save(existing)

    run_generator(library, out_dir, tmp_path / "asset_manifest.json")

    assert Image.open(existing).getpixel((0, 0)) == (7, 8, 9)


def test_generates_dynamic_background_assets_and_manifest(tmp_path: Path) -> None:
    source_dir = tmp_path / "fixed"
    source_dir.mkdir(parents=True)
    horizontal = source_dir / "BG_FIXED_01_钛金神经中枢_16x9.png"
    vertical = source_dir / "BG_FIXED_08_竖版工具测试舱_9x16.png"
    Image.new("RGB", (320, 180), (7, 18, 38)).save(horizontal)
    Image.new("RGB", (180, 320), (8, 14, 34)).save(vertical)
    fixed_manifest = tmp_path / "fixed_manifest.json"
    write_json(
        fixed_manifest,
        {
            "status": "passed",
            "assets": [
                {
                    "id": "BG_FIXED_01",
                    "name": "钛金神经中枢",
                    "aspect": "16:9",
                    "width": 320,
                    "height": 180,
                    "visual_family": "titanium_neural_control_room",
                    "path": str(horizontal),
                },
                {
                    "id": "BG_FIXED_08",
                    "name": "竖版工具测试舱",
                    "aspect": "9:16",
                    "width": 180,
                    "height": 320,
                    "visual_family": "vertical_tool_test_chamber",
                    "path": str(vertical),
                },
            ],
        },
    )
    out_dir = tmp_path / "dynamic"
    manifest_path = out_dir / "dynamic_asset_manifest.json"

    result = subprocess.run(
        [
            sys.executable,
            str(DYNAMIC_GENERATOR),
            "--fixed-manifest",
            str(fixed_manifest),
            "--out-dir",
            str(out_dir),
            "--manifest-out",
            str(manifest_path),
            "--duration",
            "0.5",
            "--fps",
            "4",
            "--crf",
            "28",
            "--force",
        ],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["status"] == "passed"
    assert manifest["asset_count"] == 2
    assert manifest["generation_method"] == "code_driven_procedural_motion_v2"
    assert manifest["checks"]["all_dynamic_assets_generated"] is True
    assert manifest["checks"]["code_driven_procedural_motion"] is True
    assert manifest["checks"]["static_source_pixels_not_used"] is True
    assert manifest["checks"]["static_background_fallback_removed"] is True
    assert manifest["checks"]["archived_source_assets_preserved"] is True
    for asset in manifest["assets"]:
        video_path = ROOT / asset["dynamic_asset_path"] if not Path(asset["dynamic_asset_path"]).is_absolute() else Path(asset["dynamic_asset_path"])
        poster_path = ROOT / asset["dynamic_poster_path"] if not Path(asset["dynamic_poster_path"]).is_absolute() else Path(asset["dynamic_poster_path"])
        if not video_path.exists():
            video_path = out_dir / Path(asset["dynamic_asset_path"]).name
        if not poster_path.exists():
            poster_path = out_dir / Path(asset["dynamic_poster_path"]).name
        assert video_path.exists()
        assert video_path.stat().st_size > 0
        assert poster_path.exists()
        assert Image.open(poster_path).size == (asset["width"], asset["height"])
        assert asset["generation_method"] == "code_driven_procedural_motion_v2"
        assert asset["code_driven_background"] is True
        assert asset["static_source_used_for_pixels"] is False
        assert len(asset["motion_layers"]) >= 5
        assert asset["checks"]["code_driven_procedural_motion"] is True
        assert asset["checks"]["static_source_pixels_not_used"] is True
        assert asset["checks"]["uses_existing_fixed_background_as_source"] is False
        assert asset["checks"]["no_baked_text"] is True
