import importlib.util
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_run_pipeline():
    spec = importlib.util.spec_from_file_location("run_pipeline", ROOT / "scripts" / "run_pipeline.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_produce_pipeline():
    spec = importlib.util.spec_from_file_location("produce_ai_video", ROOT / "scripts" / "produce_ai_video.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_produce_promote_runs_provider_contract_gate_before_promotion(tmp_path, monkeypatch):
    module = load_produce_pipeline()
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    internal.mkdir(parents=True)
    for name in ["draft.mp4", "metadata.json", "storyboard.audio_locked.json"]:
        (internal / name).write_text("placeholder\n", encoding="utf-8")
    (internal / "publish_copy.txt").write_text("发布文案\n", encoding="utf-8")
    (internal / "publish_cover_text.txt").write_text("封面标题\n封面副标题\n", encoding="utf-8")
    (internal / "publish_cover_report.json").write_text(
        '{"status":"passed","outputs":{"cover_text":"' + str(internal / "publish_cover_text.txt") + '"},"checks":{"cover_text_written":true}}\n',
        encoding="utf-8",
    )

    commands = []

    def fake_run(command):
        commands.append(command)

    monkeypatch.setattr(module, "run", fake_run)
    module.promote_after_visual_gate(project)

    script_names = [Path(command[1]).name for command in commands]
    assert "check_public_copy.py" in script_names
    assert "audit_provider_usage.py" in script_names
    assert "build_publish_contract.py" in script_names
    assert "pre_publish_gate.py" in script_names
    assert "promote_final.py" in script_names
    assert script_names.index("check_public_copy.py") < script_names.index("audit_provider_usage.py")
    assert script_names.index("audit_provider_usage.py") < script_names.index("build_publish_contract.py")
    assert script_names.index("build_publish_contract.py") < script_names.index("pre_publish_gate.py")
    assert script_names.index("pre_publish_gate.py") < script_names.index("promote_final.py")


def test_run_pipeline_promote_mode_is_disabled(tmp_path, monkeypatch):
    module = load_run_pipeline()
    project = tmp_path / "outputs" / "demo"
    monkeypatch.setattr(sys, "argv", ["run_pipeline.py", "--project", str(project), "--mode", "qa-promote"])

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert "produce_ai_video.py" in str(exc.value)


def test_qa_only_runs_beginner_value_review_for_copy(tmp_path, monkeypatch):
    module = load_run_pipeline()
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    internal.mkdir(parents=True)
    (internal / "copy_package.md").write_text("# Copy\n", encoding="utf-8")
    (internal / "copy_package.json").write_text("{}\n", encoding="utf-8")

    commands = []

    def fake_run(command):
        commands.append(command)

    monkeypatch.setattr(module, "run", fake_run)
    module.qa_only(project)

    script_names = [Path(command[1]).name for command in commands]
    assert "score_script.py" in script_names
    assert "evaluate_copy_semantic.py" in script_names
    assert "validate_beginner_copy.py" in script_names
    assert "check_public_copy.py" in script_names
    assert script_names.index("evaluate_copy_semantic.py") < script_names.index("validate_beginner_copy.py")
    assert script_names.index("validate_beginner_copy.py") < script_names.index("check_public_copy.py")
