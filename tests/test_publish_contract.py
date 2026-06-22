from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_CONTRACT = ROOT / "scripts" / "build_publish_contract.py"
PRE_PUBLISH_GATE = ROOT / "scripts" / "pre_publish_gate.py"
PROMOTE = ROOT / "scripts" / "promote_final.py"


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_visual_regression_gate(internal: Path, *, passed: bool = True) -> None:
    write_json(
        internal / "visual_regression_gate.json",
        {
            "status": "passed" if passed else "failed",
            "checks": {
                "no_legacy_renderer_source": passed,
                "hyperframes_source_present": True,
                "first_frame_cover_matches": True,
                "frame1_returns_to_main_timeline": True,
                "visual_review_passed": True,
                "frame_review_passed": True,
            },
            "issues": [] if passed else ["legacy renderer/source terms detected"],
            "legacy_source_hits": []
            if passed
            else [{"file": str(internal / "generate_video.py"), "rule": "legacy_pil_imagedraw_runtime"}],
            "first_frame": {
                "actual_frame_000_cover": str(internal / "actual_frame_000_cover.png"),
                "actual_frame_001_after_cover": str(internal / "actual_frame_001_after_cover.png"),
            },
        },
    )


def create_publish_ready_project(tmp_path: Path, qingdou: dict | None = None, frame_grab_used: bool = False) -> tuple[Path, Path]:
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    internal.mkdir(parents=True)
    (internal / "draft.mp4").write_bytes(b"video")
    (internal / "cover.png").write_bytes(b"cover")
    fixed_asset = internal / "fixed-cover-template.jpg"
    fixed_asset.write_bytes(b"fixed-cover")
    (internal / "cover_publish_vertical.png").write_bytes(b"vertical")
    (internal / "cover_publish_horizontal.png").write_bytes(b"horizontal")
    (internal / "publish_cover_text.txt").write_text("测试标题\n发布级 AI 知识视频\n", encoding="utf-8")
    (internal / "metadata.json").write_text('{"task_id":"demo","title":"测试标题"}\n', encoding="utf-8")
    (internal / "publish_copy.txt").write_text("发布文案\n", encoding="utf-8")
    write_json(
        internal / "qa_report.json",
        {"status": "passed", "blocking_issues": [], "hard_gates": {"qa": True}},
    )
    write_json(
        internal / "provider_usage_audit.json",
        {"status": "passed", "issues": []},
    )
    write_visual_regression_gate(internal)
    write_json(
        internal / "on_screen_and_publish_text_compliance_report.json",
        {
            "status": "passed",
            "checked_files": [str(internal / "publish_cover_text.txt"), str(internal / "publish_copy.txt")],
            "risk_items": [],
            "summary": {"error_count": 0, "warning_count": 0},
        },
    )
    write_json(
        internal / "publish_cover_report.json",
        {
            "status": "passed",
            "cover_type": "fixed_safe_template_first_frame",
            "frame_grab_used": frame_grab_used,
            "template_id": "H01",
            "canonical_id": "COV_AI_06",
            "template_path": str(fixed_asset),
            "template_aspect": "16:9",
            "template_rotation_index": 0,
            "selection_method": "sequential_by_size_pool",
            "template_library_size": 10,
            "outputs": {
                "primary": str(internal / "cover.png"),
                "vertical_3_4": str(internal / "cover_publish_vertical.png"),
                "horizontal_4_3": str(internal / "cover_publish_horizontal.png"),
                "cover_text": str(internal / "publish_cover_text.txt"),
            },
            "checks": {
                "cover_text_written": True,
                "not_video_screenshot": not frame_grab_used,
                "template_from_fixed_library": True,
                "fixed_safe_asset": True,
                "selected_by_video_size": True,
                "first_frame_required": True,
            },
        },
    )
    if qingdou is None:
        qingdou = {
            "status": "passed",
            "platform": "轻抖",
            "checked_fields": ["title", "caption", "topics"],
            "final_check": {"status": "passed", "message": "未检查到敏感词", "items": []},
            "final_title": "测试标题",
            "final_caption": "发布文案",
            "final_topics": ["#AI工具"],
        }
    write_json(internal / "qingdou_keyword_check.json", qingdou)
    return project, internal


def build_and_gate(project: Path, internal: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
    contract = internal / "publish_contract.json"
    built = subprocess.run(
        [sys.executable, str(BUILD_CONTRACT), "--project", str(project), "--out", str(contract)],
        text=True,
        capture_output=True,
    )
    assert built.returncode == 0
    result = subprocess.run(
        [sys.executable, str(PRE_PUBLISH_GATE), "--contract", str(contract)],
        text=True,
        capture_output=True,
    )
    return result, json.loads(contract.read_text(encoding="utf-8"))


def test_publish_contract_promotes_only_after_gate_passed(tmp_path):
    project, internal = create_publish_ready_project(tmp_path)
    gate, contract = build_and_gate(project, internal)

    assert gate.returncode == 0
    assert contract["gate"]["status"] == "passed"

    promoted = subprocess.run(
        [sys.executable, str(PROMOTE), "--project", str(project), "--contract", str(internal / "publish_contract.json")],
        text=True,
        capture_output=True,
    )

    assert promoted.returncode == 0
    assert (project / "final" / "final.mp4").read_bytes() == b"video"
    assert (project / "final" / "cover.png").read_bytes() == b"cover"
    assert (project / "final" / "publish_contract.json").exists()
    assert (project / "final" / "cover_vertical_3_4.png").exists()
    assert (project / "final" / "cover_horizontal_4_3.png").exists()


def test_pre_publish_gate_accepts_labeled_publish_copy_package(tmp_path):
    project, internal = create_publish_ready_project(tmp_path)
    (internal / "publish_copy.txt").write_text(
        "标题：测试标题\n\n发布文案：发布文案\n\n话题：#AI工具\n",
        encoding="utf-8",
    )
    gate, contract = build_and_gate(project, internal)

    assert gate.returncode == 0
    assert contract["gate"]["status"] == "passed"


def test_pre_publish_gate_rejects_frame_grab_cover(tmp_path):
    project, internal = create_publish_ready_project(tmp_path, frame_grab_used=True)
    gate, contract = build_and_gate(project, internal)

    assert gate.returncode == 1
    assert contract["gate"]["status"] == "failed"
    assert "publish_cover_report.frame_grab_used must be false" in contract["gate"]["issues"]


def test_pre_publish_gate_rejects_legacy_visual_regression_gate(tmp_path):
    project, internal = create_publish_ready_project(tmp_path)
    write_visual_regression_gate(internal, passed=False)
    gate, contract = build_and_gate(project, internal)

    assert gate.returncode == 1
    assert contract["gate"]["status"] == "failed"
    assert "visual_regression_gate.legacy_source_hits must be empty" in contract["gate"]["issues"]


def test_pre_publish_gate_allows_only_user_required_platform_topic_override(tmp_path):
    qingdou = {
        "status": "user_override_accepted",
        "platform": "轻抖",
        "checked_fields": ["title", "caption", "topics"],
        "final_check": {
            "status": "failed",
            "message": "命中用户要求保留的话题",
            "items": [{"term": "#我在抖音聊科技"}],
            "user_override": {
                "accepted": True,
                "allowed_by_skill_rule": True,
                "scope": "required_official_platform_topic",
                "approved_by_user": True,
            },
        },
        "final_title": "测试标题",
        "final_caption": "发布文案",
        "final_topics": ["#我在抖音聊科技", "#AI工具"],
    }
    project, internal = create_publish_ready_project(tmp_path, qingdou=qingdou)
    gate, contract = build_and_gate(project, internal)

    assert gate.returncode == 0
    assert contract["publish"]["first_topic"] == "#我在抖音聊科技"
    assert contract["gate"]["status"] == "passed"
