from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_motion_layout_contract.py"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def base_project(tmp_path: Path) -> Path:
    project = tmp_path / "outputs" / "motion-layout-demo"
    internal = project / "internal"
    write_json(
        internal / "fixed_template_selection.json",
        {
            "status": "passed",
            "transition_sfx_pack": {"id": "TRN_PACK_01", "recipe_id": "metal_aperture_handoff"},
            "motion_layout_contract": {
                "forbidden_low_grade_effects": ["斜线扫光", "diagonal line sweep", "ordinary fade"],
                "required_manifest": "internal/render_layout_manifest.json",
                "required_report": "internal/layout_motion_contract_report.json",
            },
        },
    )
    write_json(
        internal / "storyboard.json",
        {
            "scenes": [{"id": f"S{i}", "transition": "metal_aperture_handoff"} for i in range(1, 5)],
            "director_shots": [{"shot_id": f"S{i}", "primary_action": "信息节点交接"} for i in range(1, 5)],
        },
    )
    write_json(
        internal / "metadata.json",
        {
            "motion_layout_contract": {
                "used_transition_recipes": [
                    "metal_aperture_handoff",
                    "source_evidence_focus",
                    "checklist_matrix_assembly",
                ]
            }
        },
    )
    write_json(
        internal / "render_layout_manifest.json",
        {
            "status": "passed",
            "components": [
                {
                    "id": "three_column_aligned_checklist",
                    "text_overflow": False,
                    "collision": False,
                    "min_padding_px": 28,
                    "title_padding_px": 40,
                    "text_boxes": [
                        {"id": "col1", "overflow": False, "collides": False, "line_count": 2, "max_lines": 2},
                        {"id": "col2", "overflow": False, "collides": False, "line_count": 2, "max_lines": 2},
                        {"id": "col3", "overflow": False, "collides": False, "line_count": 2, "max_lines": 2},
                    ],
                }
            ],
            "three_column_groups": [
                {
                    "id": "three_column_aligned_checklist",
                    "grid_locked": True,
                    "equal_column_widths": True,
                    "icon_center_y_aligned": True,
                    "title_baseline_y_aligned": True,
                    "body_box_y_aligned": True,
                    "bottom_summary_gap_px": 64,
                    "max_baseline_delta_px": 2,
                }
            ],
            "decorative_paths": [{"id": "handoff_path", "crosses_text": False}],
            "glass_transparency": {
                "profile": "glass_transparency_v2",
                "dynamic_background_visible": True,
                "foreground_stage_transparent": True,
                "backdrop_filter_present": True,
                "max_background_fill_alpha": 0.28,
            },
        },
    )
    return project


def run_checker(project: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(CHECKER), "--project", str(project)], text=True, capture_output=True)


def test_motion_layout_contract_passes_premium_recipe_and_measured_grid(tmp_path: Path) -> None:
    project = base_project(tmp_path)

    result = run_checker(project)

    assert result.returncode == 0, result.stderr + result.stdout
    report = json.loads((project / "internal" / "layout_motion_contract_report.json").read_text(encoding="utf-8"))
    assert report["status"] == "passed"
    assert report["checks"]["layout_manifest_checks_ok"] is True
    assert report["signals"]["three_column_groups_checked"] == 1


def test_motion_layout_contract_rejects_low_grade_diagonal_sweep(tmp_path: Path) -> None:
    project = base_project(tmp_path)
    storyboard_path = project / "internal" / "storyboard.json"
    storyboard = json.loads(storyboard_path.read_text(encoding="utf-8"))
    storyboard["scenes"][0]["motion"] = "用斜线扫光做装饰转场"
    write_json(storyboard_path, storyboard)

    result = run_checker(project)

    assert result.returncode == 1
    report = json.loads((project / "internal" / "layout_motion_contract_report.json").read_text(encoding="utf-8"))
    assert report["status"] == "failed"
    assert any("斜线扫光" in issue for issue in report["blocking_issues"])


def test_motion_layout_contract_rejects_three_column_misalignment_and_overflow(tmp_path: Path) -> None:
    project = base_project(tmp_path)
    manifest_path = project / "internal" / "render_layout_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["components"][0]["text_boxes"][1]["overflow"] = True
    manifest["three_column_groups"][0]["title_baseline_y_aligned"] = False
    manifest["three_column_groups"][0]["max_baseline_delta_px"] = 9
    write_json(manifest_path, manifest)

    result = run_checker(project)

    assert result.returncode == 1
    report = json.loads((project / "internal" / "layout_motion_contract_report.json").read_text(encoding="utf-8"))
    assert any("overflows" in issue for issue in report["blocking_issues"])
    assert any("title_baseline_y_aligned" in issue for issue in report["blocking_issues"])


def test_motion_layout_contract_rejects_opaque_glass_manifest(tmp_path: Path) -> None:
    project = base_project(tmp_path)
    manifest_path = project / "internal" / "render_layout_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["glass_transparency"]["max_background_fill_alpha"] = 0.78
    manifest["glass_transparency"]["dynamic_background_visible"] = False
    write_json(manifest_path, manifest)

    result = run_checker(project)

    assert result.returncode == 1
    report = json.loads((project / "internal" / "layout_motion_contract_report.json").read_text(encoding="utf-8"))
    assert any("max_background_fill_alpha" in issue for issue in report["blocking_issues"])
    assert any("dynamic_background_visible" in issue for issue in report["blocking_issues"])
