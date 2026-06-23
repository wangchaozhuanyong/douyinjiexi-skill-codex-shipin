from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELECTOR = ROOT / "scripts" / "select_fixed_ai_templates.py"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_selector(project: Path, state: Path, *extra: str) -> dict:
    result = subprocess.run(
        [
            sys.executable,
            str(SELECTOR),
            "--project",
            str(project),
            "--state-file",
            str(state),
            *extra,
        ],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    return json.loads((project / "internal" / "fixed_template_selection.json").read_text(encoding="utf-8"))


def test_selects_fixed_templates_from_director_scheme(tmp_path: Path) -> None:
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    state = tmp_path / "state.json"
    write_json(
        internal / "director_selection.json",
        {
            "scheme": {"id": "scheme_3_ai_news_to_beginner_action"},
            "visual_system": {"visual_family": "source_archive_wall", "background_style_id": "BG_STYLE_SOURCE_ARCHIVE"},
        },
    )
    write_json(
        internal / "style_recipe.json",
        {"selected_visual_family": "source_archive_wall", "background_style_id": "BG_STYLE_SOURCE_ARCHIVE"},
    )

    selection = run_selector(
        project,
        state,
        "--director-selection",
        str(internal / "director_selection.json"),
        "--style-recipe",
        str(internal / "style_recipe.json"),
        "--video-width",
        "1920",
        "--video-height",
        "1080",
    )

    assert selection["status"] == "passed"
    assert selection["content"]["scheme_id"] == "scheme_3_ai_news_to_beginner_action"
    assert selection["background_template"]["aspect"] == "16:9"
    assert selection["background_template"]["asset_source_type"] == "fixed_imagegen_background_asset"
    assert selection["background_template"]["fixed_asset_exists"] is True
    assert Path(selection["background_template"]["fixed_asset_path"]).exists()
    assert selection["transition_sfx_pack"]["id"]
    assert selection["transition_sfx_pack"]["quality_tier"] == "premium_only"
    assert selection["component_pack"]["id"]
    assert selection["voice_mix_profile"]["id"] == "VOICE_MALE_THICK_YUNYANG_V1"
    assert selection["scene_motion_templates"]["main_project_template"]["id"] == "AI_PREMIUM_MAIN_16X9_V1"
    assert len(selection["scene_motion_templates"]["transition_recipes"]) == 10
    assert len(selection["scene_motion_templates"]["entrance_templates"]) == 10
    assert selection["scene_motion_templates"]["foreground_module_runtime"]["module_types"]
    assert selection["scene_motion_templates"]["topic_candidate_v3_template"]["path"] == "templates/topic_candidates_v3.template.json"
    assert selection["scene_motion_templates"]["prompt_pack_template"]["path"] == "templates/prompt_pack/fixed_background_visual_contract.md"
    assert selection["inheritance_contract"]["no_per_scene_random_art_direction"] is True
    assert selection["inheritance_contract"]["premium_motion_library_required"] is True
    assert selection["inheritance_contract"]["scene_motion_templates_drive_hyperframes"] is True
    assert selection["inheritance_contract"]["no_low_quality_motion_fallback"] is True
    assert selection["inheritance_contract"]["layout_manifest_required"] is True
    assert selection["motion_layout_contract"]["required_manifest"] == "internal/render_layout_manifest.json"
    assert "斜线扫光" in selection["motion_layout_contract"]["forbidden_low_grade_effects"]


def test_vertical_no_voice_uses_no_voice_profile(tmp_path: Path) -> None:
    project = tmp_path / "outputs" / "vertical"
    internal = project / "internal"
    state = tmp_path / "state.json"
    write_json(
        internal / "director_selection.json",
        {"scheme": {"id": "scheme_1_skill_recommendation_no_voice"}, "visual_system": {"visual_family": "vertical_tool_test_chamber"}},
    )

    selection = run_selector(
        project,
        state,
        "--director-selection",
        str(internal / "director_selection.json"),
        "--video-width",
        "1080",
        "--video-height",
        "1920",
    )

    assert selection["video"]["aspect"] == "9:16"
    assert selection["background_template"]["aspect"] == "9:16"
    assert selection["background_template"]["fixed_asset_exists"] is True
    assert Path(selection["background_template"]["fixed_asset_path"]).exists()
    assert selection["voice_mix_profile"]["id"] == "VOICE_NO_VOICE_SFX_ONLY_V1"


def test_rotation_state_advances_for_same_pool(tmp_path: Path) -> None:
    project = tmp_path / "outputs" / "rotate"
    internal = project / "internal"
    state = tmp_path / "state.json"
    write_json(internal / "director_selection.json", {"scheme": {"id": "scheme_2_source_led_tool_tutorial"}})

    first = run_selector(project, state, "--director-selection", str(internal / "director_selection.json"), "--video-width", "1920", "--video-height", "1080")
    second = run_selector(project, state, "--director-selection", str(internal / "director_selection.json"), "--video-width", "1920", "--video-height", "1080")

    assert first["background_template"]["state_key"] == second["background_template"]["state_key"]
    assert first["background_template"]["rotation_index"] == 0
    assert second["background_template"]["rotation_index"] == 1
