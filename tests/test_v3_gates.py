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


def test_storyboard_validation_rejects_fast_voice_and_unsafe_margins(tmp_path):
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    storyboard["target"]["tts_speed"] = 1.12
    storyboard["scenes"][0]["safe_zone"]["bottom_margin_px"] = 120
    path = tmp_path / "storyboard.json"
    out = tmp_path / "storyboard_validation.json"
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert any("tts_speed" in issue for issue in data["issues"])
    assert any("bottom_margin_px" in issue for issue in data["issues"])


def test_storyboard_validation_rejects_missing_quality_design(tmp_path):
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    storyboard.pop("quality_spec", None)
    storyboard["scenes"][0]["visual"].pop("design_layers", None)
    storyboard["scenes"][0]["visual"]["quality_checks"]["not_template_like"] = False
    path = tmp_path / "storyboard.json"
    out = tmp_path / "storyboard_validation.json"
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert data["signals"]["quality_spec_valid"] is False
    assert data["signals"]["layered_scene_count"] == 5
    assert data["signals"]["quality_check_scene_count"] == 5
    assert any("quality_spec" in issue for issue in data["issues"])
    assert any("design_layers" in issue for issue in data["issues"])
    assert any("quality_checks" in issue for issue in data["issues"])


def test_storyboard_validation_requires_three_skill_production_stack(tmp_path):
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    storyboard["title"] = "3 个 Codex Skill 怎么配合做视频"
    storyboard["scenes"][0]["concept"] = "Remotion 负责组件化动画"
    storyboard["scenes"][0]["voice"] = "第一个 Remotion，负责把复杂画面做成组件化动画。"
    storyboard["scenes"][0]["caption"] = "Remotion 做组件动画"
    storyboard["scenes"][0]["on_screen_text"] = ["Remotion", "组件化动画"]
    storyboard["scenes"][1]["concept"] = "HyperFrames 负责最终时间线"
    storyboard["scenes"][1]["voice"] = "第二个 HyperFrames，负责字幕、时间线和最终成片。"
    storyboard["scenes"][1]["caption"] = "HyperFrames 做成片"
    storyboard["scenes"][1]["on_screen_text"] = ["HyperFrames", "最终时间线"]
    storyboard["scenes"][2]["concept"] = "ImageGen 负责视觉素材"
    storyboard["scenes"][2]["voice"] = "第三个 ImageGen，先把封面、概念图和案例图做出来。"
    storyboard["scenes"][2]["caption"] = "ImageGen 做素材"
    storyboard["scenes"][2]["on_screen_text"] = ["ImageGen", "视觉素材"]

    path = tmp_path / "storyboard.json"
    out = tmp_path / "storyboard_validation.json"
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["signals"]["production_stack_required"] is True
    assert any("production_stack" in issue for issue in data["issues"])

    proof_chain = {
        "entry_or_source": "真实入口或官方/本地证据",
        "operation_or_step": "展示一次可复现操作",
        "output_or_result": "展示生成结果或文件",
        "viewer_value": "说明观众为什么要保存",
    }
    storyboard["production_stack"] = {
        "reference_learning_applied": True,
        "reference_pattern": "three_skill_reference",
        "workflow_order": ["ImageGen 先做视觉素材", "Remotion 做组件化动画", "HyperFrames 做最终成片"],
        "primary_tools": [
            {"name": "Remotion", "role": "组件化动画和数据驱动画面", "evidence_chain": proof_chain},
            {"name": "HyperFrames", "role": "最终时间线、字幕、音画同步和渲染", "evidence_chain": proof_chain},
            {"name": "ImageGen", "aliases": ["Image Gen"], "role": "封面、概念图和结果图素材", "evidence_chain": proof_chain},
        ],
    }
    for scene in storyboard["scenes"][:3]:
        scene["visual"]["proof_chain"] = proof_chain

    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["status"] == "passed"
    assert data["signals"]["production_stack_valid"] is True
    assert data["signals"]["tool_proof_chain_count"] == 3


def test_score_script_rejects_accelerated_voiceover(tmp_path):
    copy_path = tmp_path / "copy.md"
    out = tmp_path / "script_score.json"
    source = (ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "copy_package.md").read_text(encoding="utf-8")
    copy_path.write_text(source + "\n语速：1.12x\n", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "score_script.py"),
            "--copy",
            str(copy_path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert "voiceover speed must stay normal; do not use accelerated narration" in data["issues"]


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
