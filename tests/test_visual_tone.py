import json
import subprocess
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def test_visual_tone_passes_bright_l4_image(tmp_path):
    image = tmp_path / "bright.png"
    Image.new("RGB", (320, 180), (238, 232, 216)).save(image)
    out = tmp_path / "tone.json"

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_visual_tone.py"),
            "--image",
            str(image),
            "--brightness-grade",
            "L4",
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )

    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["status"] == "passed"
    assert data["results"][0]["metrics"]["avg_luma"] >= 135


def test_visual_tone_rejects_dark_l4_image(tmp_path):
    image = tmp_path / "dark.png"
    Image.new("RGB", (320, 180), (18, 22, 28)).save(image)
    out = tmp_path / "tone.json"

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_visual_tone.py"),
            "--image",
            str(image),
            "--brightness-grade",
            "L4",
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )

    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert any("too dark" in issue for issue in data["blocking_issues"])
