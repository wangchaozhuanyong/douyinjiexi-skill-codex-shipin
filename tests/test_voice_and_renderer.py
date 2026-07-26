from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = (
    ROOT
    / "skills"
    / "douyin-video-production-core"
    / "scripts"
    / "preflight_providers.py"
)


def test_preflight_blocks_project_without_remotion(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text(
        json.dumps({"name": "missing-remotion", "private": True}),
        encoding="utf-8",
    )
    (tmp_path / "storyboard.json").write_text(
        json.dumps(
            {
                "render_plan": {
                    "canonical_renderer": "remotion",
                    "composition_id": "Test",
                    "optional_subrenderers": [],
                }
            }
        ),
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            str(PREFLIGHT),
            "--project",
            str(tmp_path),
            "--voice-provider",
            "existing",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "package.json missing Remotion packages" in result.stdout
    assert "Remotion is declared but not installed" in result.stdout


def test_preflight_never_prints_secret_values(tmp_path: Path, monkeypatch) -> None:
    secret = "never-print-this-secret"
    monkeypatch.setenv("ELEVENLABS_API_KEY", secret)
    monkeypatch.setenv("ELEVENLABS_VOICE_ID", "voice-id")
    (tmp_path / "package.json").write_text(
        json.dumps(
            {
                "dependencies": {
                    "remotion": "4.0.499",
                    "@remotion/cli": "4.0.499",
                    "@remotion/media": "4.0.499",
                }
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "storyboard.json").write_text(
        json.dumps(
            {
                "render_plan": {
                    "canonical_renderer": "remotion",
                    "composition_id": "Test",
                    "optional_subrenderers": [],
                }
            }
        ),
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            str(PREFLIGHT),
            "--project",
            str(tmp_path),
            "--voice-provider",
            "elevenlabs",
        ],
        capture_output=True,
        text=True,
    )
    assert secret not in result.stdout
    assert secret not in result.stderr
