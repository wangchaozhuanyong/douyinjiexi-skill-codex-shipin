from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIBRARY_VALIDATOR = ROOT / "scripts" / "validate_foreground_module_libraries.py"
PLAN_CHECKER = ROOT / "scripts" / "check_foreground_module_plan.py"
PACK_RENDERER = ROOT / "scripts" / "render_foreground_module_pack.py"
PACK_CHECKER = ROOT / "scripts" / "check_foreground_module_render_pack.py"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_example_plan() -> dict:
    return json.loads((ROOT / "templates" / "foreground_module_plan.example.json").read_text(encoding="utf-8"))


def run_plan_checker(project: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PLAN_CHECKER), "--project", str(project)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def run_pack_renderer(project: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PACK_RENDERER), "--project", str(project)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def run_pack_checker(project: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PACK_CHECKER), "--project", str(project)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_foreground_module_libraries_are_complete(tmp_path: Path) -> None:
    report_path = tmp_path / "foreground_library_report.json"

    result = subprocess.run(
        [sys.executable, str(LIBRARY_VALIDATOR), "--out", str(report_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["status"] == "passed"
    assert report["signals"]["art_module_count"] == 20
    assert report["signals"]["micro_component_count"] == 30
    assert report["signals"]["parent_adapter_count"] == 20


def test_foreground_module_plan_example_passes(tmp_path: Path) -> None:
    project = tmp_path / "outputs" / "foreground-demo"
    write_json(project / "internal" / "foreground_module_plan.json", load_example_plan())

    result = run_plan_checker(project)

    assert result.returncode == 0, result.stderr + result.stdout
    report = json.loads((project / "internal" / "foreground_module_plan_check.json").read_text(encoding="utf-8"))
    assert report["status"] == "passed"
    assert report["signals"]["scene_count"] == 1
    assert report["signals"]["scene_reports"][0]["parent_module_id"] == "M01"


def test_foreground_module_plan_rejects_text_overflow(tmp_path: Path) -> None:
    project = tmp_path / "outputs" / "foreground-overflow"
    plan = load_example_plan()
    plan["scenes"][0]["micro_components"][0]["text_slots"]["【参数值】"] = "这是一段超长参数值"
    write_json(project / "internal" / "foreground_module_plan.json", plan)

    result = run_plan_checker(project)

    assert result.returncode == 1
    report = json.loads((project / "internal" / "foreground_module_plan_check.json").read_text(encoding="utf-8"))
    assert report["status"] == "failed"
    assert any("max_chars" in issue for issue in report["blocking_issues"])


def test_foreground_module_plan_rejects_transition_outside_parent_module(tmp_path: Path) -> None:
    project = tmp_path / "outputs" / "foreground-transition"
    plan = load_example_plan()
    plan["scenes"][0]["transition_out"] = "TR08"
    write_json(project / "internal" / "foreground_module_plan.json", plan)

    result = run_plan_checker(project)

    assert result.returncode == 1
    report = json.loads((project / "internal" / "foreground_module_plan_check.json").read_text(encoding="utf-8"))
    assert report["status"] == "failed"
    assert any("not allowed for M01" in issue for issue in report["blocking_issues"])


def test_foreground_module_render_pack_passes_for_valid_plan(tmp_path: Path) -> None:
    project = tmp_path / "outputs" / "foreground-render"
    write_json(project / "internal" / "foreground_module_plan.json", load_example_plan())
    assert run_plan_checker(project).returncode == 0

    rendered = run_pack_renderer(project)
    checked = run_pack_checker(project)

    assert rendered.returncode == 0, rendered.stderr + rendered.stdout
    assert checked.returncode == 0, checked.stderr + checked.stdout
    manifest = json.loads((project / "internal" / "foreground_module_render_manifest.json").read_text(encoding="utf-8"))
    report = json.loads((project / "internal" / "foreground_module_render_check.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "rendered"
    assert Path(manifest["html"]).exists()
    assert manifest["render_contract"]["html_css_svg_gsap_ready"] is True
    assert report["status"] == "passed"
    assert report["signals"]["module_dom_count"] == 1
    assert report["signals"]["micro_dom_count"] == 5


def test_foreground_module_render_pack_rejects_missing_micro_dom(tmp_path: Path) -> None:
    project = tmp_path / "outputs" / "foreground-render-broken"
    write_json(project / "internal" / "foreground_module_plan.json", load_example_plan())
    assert run_plan_checker(project).returncode == 0
    assert run_pack_renderer(project).returncode == 0
    html_path = project / "internal" / "foreground_module_render_pack.html"
    html = html_path.read_text(encoding="utf-8")
    html_path.write_text(html.replace('data-component-id="C30"', 'data-broken-component-id="C30"', 1), encoding="utf-8")

    checked = run_pack_checker(project)

    assert checked.returncode == 1
    report = json.loads((project / "internal" / "foreground_module_render_check.json").read_text(encoding="utf-8"))
    assert report["status"] == "failed"
    assert any("micro DOM count" in issue for issue in report["blocking_issues"])
