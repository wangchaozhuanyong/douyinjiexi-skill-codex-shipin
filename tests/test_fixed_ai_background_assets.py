from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_fixed_ai_background_assets.py"


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
