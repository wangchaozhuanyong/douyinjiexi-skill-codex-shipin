from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_registry_has_18_playable_analyzed_samples() -> None:
    script = ROOT / "research" / "validate_registry.py"
    relaxed = subprocess.run(
        [sys.executable, str(script), "--allow-incomplete"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert relaxed.returncode == 0, relaxed.stdout + relaxed.stderr
    strict = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert '"tool_explainer": 6' in strict.stdout
    assert '"news_explainer": 6' in strict.stdout
    assert '"list_video": 6' in strict.stdout
    assert '"blocking_issues": []' in strict.stdout
