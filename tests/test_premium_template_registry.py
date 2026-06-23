from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_premium_template_registry.py"


def test_premium_template_registry_passes(tmp_path: Path) -> None:
    report_path = tmp_path / "premium_template_registry_report.json"
    result = subprocess.run(
        [sys.executable, str(CHECKER), "--out", str(report_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["status"] == "passed"
    assert report["signals"]["transition_template_count"] == 10
    assert report["signals"]["entrance_template_count"] == 10
    assert report["signals"]["foreground_module_count"] == 8


def test_motion_runtime_has_no_soft_fallback_language() -> None:
    runtime = (ROOT / "assets" / "hyperframes_components" / "advanced_motion_templates.js").read_text(encoding="utf-8")
    assert "No premium" in runtime
    assert "fallback" not in runtime.lower()
    assert "plain fade" not in runtime.lower()
    assert "simple slide" not in runtime.lower()
