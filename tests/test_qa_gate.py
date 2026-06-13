import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "scripts" / "qa_gate.py"


def test_qa_gate_fails_when_required_files_missing(tmp_path):
    project = tmp_path / "outputs" / "demo"
    out = project / "internal" / "qa_report.json"
    result = subprocess.run(
        [sys.executable, str(QA), "--project", str(project), "--out", str(out)],
        text=True,
        capture_output=True,
    )
    report = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert report["status"] == "failed"
    assert report["blocking_issues"]


def test_qa_gate_passes_complete_project(tmp_path):
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    final = project / "final"
    internal.mkdir(parents=True)
    final.mkdir(parents=True)

    (internal / "topic_candidates.json").write_text((ROOT / "templates" / "topic_candidates.example.json").read_text(encoding="utf-8"), encoding="utf-8")
    (internal / "selected_topic.json").write_text('{"topic_id":"T001","reason":"highest score"}\n', encoding="utf-8")
    (internal / "copy_package.md").write_text("# Copy Package\n安全文案\n", encoding="utf-8")
    (internal / "compliance_report.json").write_text('{"status":"passed","checked_files":[],"risk_items":[],"claim_items":[],"summary":{"error_count":0,"warning_count":0}}\n', encoding="utf-8")
    storyboard = (ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8")
    (internal / "storyboard.json").write_text(storyboard, encoding="utf-8")
    (internal / "storyboard.audio_locked.json").write_text(storyboard, encoding="utf-8")
    (internal / "asset_manifest.json").write_text('{"assets":[]}\n', encoding="utf-8")
    (internal / "metadata.json").write_text('{"task_id":"demo","created_at":"2026-06-13","final_video_path":"final/final.mp4","duration":20,"scene_count":6,"target_width":1080,"target_height":1920,"fps":30}\n', encoding="utf-8")
    (internal / "script_score.json").write_text('{"script_score":8.7,"first_5_seconds_score":9.2}\n', encoding="utf-8")
    (internal / "storyboard_validation.json").write_text('{"status":"passed","issues":[],"evidence_runtime_ratio":0.58}\n', encoding="utf-8")
    (final / "final.mp4").write_bytes(b"placeholder")
    (final / "cover.png").write_bytes(b"placeholder")
    (final / "publish_copy.txt").write_text("发布文案\n", encoding="utf-8")

    out = internal / "qa_report.json"
    result = subprocess.run(
        [sys.executable, str(QA), "--project", str(project), "--out", str(out)],
        text=True,
        capture_output=True,
    )
    report = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert report["status"] == "passed"
    assert report["blocking_issues"] == []
