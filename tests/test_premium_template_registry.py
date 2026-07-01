from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_premium_template_registry.py"
ANT_AI_GALAXY_CHECKER = ROOT / "scripts" / "check_ant_ai_galaxy_template.py"


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
    assert report["signals"]["top5_template"] == "templates/ai_hot_rank_top5.template.json"
    assert report["signals"]["ant_ai_galaxy_template"] == "templates/ant_ai_hotlist_galaxy/renderer_config.json"
    top5_template = json.loads((ROOT / "templates" / "ai_hot_rank_top5.template.json").read_text(encoding="utf-8"))
    assert top5_template["audio_policy"]["generated_bgm_allowed"] is False
    assert top5_template["audio_policy"]["replacement_requires_explicit_user_approval"] is True
    ant_ai = top5_template["extended_profiles"]["ant_ai_hotlist_extended"]
    assert ant_ai["fixed_cta"] == "关注 蚂蚁AI"
    assert ant_ai["background_template_id"] == "BG_FIXED_11_ANT_AI_HOTLIST_NEBULA_9X16"
    assert ant_ai["bgm_source_id"] == "ant_ai_scheme7_top5_reference_bgm_7654135072895400421"
    assert ant_ai["preview_template"] == "templates/ant_ai_hotlist_galaxy/preview.html"
    assert ant_ai["galaxy_motion_contract"]["motion_mode"] == "local_internal_rotation"
    assert ant_ai["glass_card_contract"]["maxBackgroundAlpha"] == 0.34


def test_ant_ai_galaxy_template_contract_passes(tmp_path: Path) -> None:
    report_path = tmp_path / "ant_ai_galaxy_template_check.json"
    result = subprocess.run(
        [sys.executable, str(ANT_AI_GALAXY_CHECKER), "--out", str(report_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["status"] == "passed"
    assert report["signals"]["preview_template"] == "templates/ant_ai_hotlist_galaxy/preview.html"
    assert report["signals"]["galaxy_rotation_duration_sec"] == 42
    assert report["signals"]["glass_card_alpha_default"] == 0.26
    assert report["signals"]["sample_rank_items"] == 5


def test_motion_runtime_has_no_soft_fallback_language() -> None:
    runtime = (ROOT / "assets" / "hyperframes_components" / "advanced_motion_templates.js").read_text(encoding="utf-8")
    assert "No premium" in runtime
    assert "fallback" not in runtime.lower()
    assert "plain fade" not in runtime.lower()
    assert "simple slide" not in runtime.lower()


def test_hyperframes_module_css_keeps_dynamic_background_visible() -> None:
    component_dir = ROOT / "assets" / "hyperframes_components"
    css_paths = [
        component_dir / "foreground_modules.css",
        component_dir / "premium_foreground_modules.css",
        component_dir / "tokens.css",
        component_dir / "components.css",
    ]
    for path in css_paths:
        css = path.read_text(encoding="utf-8")
        assert "backdrop-filter" in css
        for line_no, line in enumerate(css.splitlines(), start=1):
            if "background" not in line or "rgba(" not in line:
                continue
            alphas = [float(value) for value in re.findall(r"rgba\([^)]*,\s*([0-9]*\.?[0-9]+)\s*\)", line)]
            assert not alphas or max(alphas) <= 0.34, f"{path}:{line_no} uses opaque background fill: {line.strip()}"
