import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_run_pipeline():
    spec = importlib.util.spec_from_file_location("run_pipeline", ROOT / "scripts" / "run_pipeline.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_qa_promote_runs_audio_check_provider_audit_before_promotion(tmp_path, monkeypatch):
    module = load_run_pipeline()
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    internal.mkdir(parents=True)
    for name in ["draft.mp4", "metadata.json", "storyboard.audio_locked.json"]:
        (internal / name).write_text("placeholder\n", encoding="utf-8")

    commands = []

    def fake_run(command):
        commands.append(command)

    monkeypatch.setattr(module, "run", fake_run)
    module.qa_only(project, promote=True)

    script_names = [Path(command[1]).name for command in commands]
    assert "check_audio_continuity.py" in script_names
    assert "video_technical_qa.py" in script_names
    assert "qa_gate.py" in script_names
    assert "generate_production_postmortem.py" in script_names
    assert "audit_provider_usage.py" in script_names
    assert "promote_final.py" in script_names
    assert script_names.index("check_audio_continuity.py") < script_names.index("video_technical_qa.py")
    assert script_names.index("qa_gate.py") < script_names.index("generate_production_postmortem.py")
    assert script_names.index("generate_production_postmortem.py") < script_names.index("audit_provider_usage.py")
    assert script_names.index("qa_gate.py") < script_names.index("audit_provider_usage.py")
    assert script_names.index("audit_provider_usage.py") < script_names.index("promote_final.py")
