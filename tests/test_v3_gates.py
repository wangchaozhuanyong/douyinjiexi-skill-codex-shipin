import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_semantic_review_passes_golden_copy(tmp_path):
    out = tmp_path / "semantic_review.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "evaluate_copy_semantic.py"),
            "--copy",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "copy_package.md"),
            "--copy-json",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "copy_package.json"),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["status"] == "passed"
    assert data["composite_score"] >= 8.5


def test_visual_review_passes_golden_storyboard(tmp_path):
    frame_review = tmp_path / "frame_review_report.json"
    metadata = tmp_path / "metadata.json"
    out = tmp_path / "visual_review.json"
    frame_review.write_text('{"status":"review_required","artifacts":{},"blocking_issues":[],"warnings":[]}\n', encoding="utf-8")
    metadata.write_text((ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "metadata.json").read_text(encoding="utf-8"), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "visual_aesthetic_review.py"),
            "--storyboard",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "storyboard.json"),
            "--frame-review",
            str(frame_review),
            "--metadata",
            str(metadata),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["status"] == "passed"
    assert data["overall_visual_score"] >= 8.2


def test_score_topic_can_apply_learning_bank(tmp_path):
    bank = tmp_path / "learning_bank.md"
    out = tmp_path / "topics.json"
    bank.write_text("- What worked:\n  - 真实截图\n  - 对比\n- What to fix:\n  - 抽象背景\n", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "score_topic.py"),
            "--input",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "topic_candidates.json"),
            "--out",
            str(out),
            "--learning-bank",
            str(bank),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["status"] == "passed"
    assert data["learning_bank_applied"]["worked_terms"]
    assert data["candidates"][0]["learning_bank_adjustment"]["score_delta"] > 0
