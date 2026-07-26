from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "skills" / "douyin-video-production-core" / "scripts" / "validate_project.py"


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def create_project(project: Path, source_kind: str = "real_capture") -> None:
    proof = project / "proof.png"
    proof.write_bytes(b"proof")
    write_json(
        project / "source_brief.json",
        {
            "format_type": "tool_explainer",
            "project_name": "AI工具实操讲解-测试工具01",
            "classification": {
                "level_1": "AI类视频",
                "level_2": "AI工具实操讲解类",
                "level_3": "测试工具",
                "category_code": "ai_tool_explainer",
            },
            "topic": "Test tool",
            "captured_at": "2026-07-26T00:00:00Z",
            "topic_selection": {
                "mode": "user_fixed",
                "interaction_mode": "autonomous",
                "material_scan_completed": True,
                "selection_basis": "The user fixed the topic and real proof is available",
                "proof_readiness": "passed",
                "confirmation_status": "not_requested",
            },
            "sources": [
                {
                    "id": "S1",
                    "title": "Official source",
                    "source_type": "official",
                    "locator": "https://example.com",
                    "captured_at": "2026-07-26T00:00:00Z",
                    "supports_claims": ["C1"],
                }
            ],
            "claims": [{"id": "C1", "text": "Visible result", "fact_status": "confirmed", "source_ids": ["S1"]}],
        },
    )
    write_json(
        project / "script.json",
        {
            "format_type": "tool_explainer",
            "title": "Test",
            "hook": "See the result",
            "viewer_task": "finish a task",
            "input_method": "type one request",
            "execution_process": "run",
            "visible_result": "a file",
            "before_after": "three steps to one",
            "safety_constraints": ["do not delete files"],
            "privacy_redactions": ["hide local username"],
            "result_acceptance": ["open the generated file"],
            "beginner_review": {
                "status": "passed",
                "task": "finish one task",
                "input": "type one request",
                "process": "the tool runs the request",
                "result": "a visible file",
                "old_method_difference": "fewer repeated steps",
                "read_aloud_passed": True,
            },
            "voice_lock": {
                "status": "locked",
                "provider": "edge-tts",
                "voice_id": "zh-CN-YunyangNeural",
                "persona": "clear adult Chinese male lecturer",
                "rate": "-2%",
                "pitch": "-2Hz",
                "confirmation_source": "user preference",
            },
            "risk_review": {
                "level": "low",
                "sensitive_domains": [],
                "demo_environment": "sanitized_local",
                "real_action_policy": "not_applicable",
                "stop_conditions": ["stop before login or payment"],
            },
            "beats": [{"id": "B1", "narration": "Result", "claim_ids": ["C1"], "proof_ids": ["P1"]}],
            "closing_takeaway": "Use it for this task",
        },
    )
    write_json(
        project / "storyboard.json",
        {
            "format_type": "tool_explainer",
            "width": 1080,
            "height": 1920,
            "fps": 30,
            "safe_area": {
                "top": 120,
                "left": 84,
                "right": 180,
                "bottom": 360,
                "caption_bottom": 380,
            },
            "creative_direction": {
                "visual_thesis": "Turn a real result into a readable proof trail",
                "reason_for_topic": "The tool is understood through its output and execution",
                "evidence_strategy": "Keep the real result and source in the foreground",
                "motion_logic": "Move only when a new claim or proof appears",
                "continuity_devices": ["one evidence cursor"],
                "rejected_defaults": ["generic dashboard", "repeating card stack"],
            },
            "render_plan": {
                "canonical_renderer": "remotion",
                "composition_id": "ToolExplainer",
                "optional_subrenderers": [],
            },
            "scenes": [
                {
                    "id": "SC1",
                    "start": 0,
                    "end": 3,
                    "beat_ids": ["B1"],
                    "claim_ids": ["C1"],
                    "proof_ids": ["P1"],
                    "visual_mode": "real_result",
                    "visual": "Show the real result",
                    "evidence_display": "P1 fills the readable center",
                    "motion_intent": "Reveal the exact output once",
                    "change_reason": "The result claim begins",
                    "caption": "Visible result",
                }
            ],
        },
    )
    write_json(
        project / "asset_manifest.json",
        {
            "assets": [
                {
                    "id": "P1",
                    "role": "proof",
                    "source_kind": source_kind,
                    "path": str(proof),
                    "source_locator": "local capture",
                    "captured_at": "2026-07-26T00:00:00Z",
                    "supports_claims": ["C1"],
                }
            ]
        },
    )


def test_valid_preproduction_project_passes(tmp_path: Path) -> None:
    create_project(tmp_path)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_source_brief_requires_ai_video_classification(tmp_path: Path) -> None:
    create_project(tmp_path)
    source_path = tmp_path / "source_brief.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source.pop("classification")
    write_json(source_path, source)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "source_brief.classification is required" in result.stdout


def test_classification_must_match_format_type(tmp_path: Path) -> None:
    create_project(tmp_path)
    source_path = tmp_path / "source_brief.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source["classification"]["level_2"] = "AI新闻与产品更新解读类"
    source["classification"]["category_code"] = "ai_news_explainer"
    write_json(source_path, source)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "classification.level_2 must be AI工具实操讲解类" in result.stdout
    assert "classification.category_code must be ai_tool_explainer" in result.stdout


def test_project_name_uses_category_prefix_and_two_digit_sequence(tmp_path: Path) -> None:
    create_project(tmp_path)
    source_path = tmp_path / "source_brief.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source["project_name"] = "随便命名"
    write_json(source_path, source)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "project_name must start with AI工具实操讲解-" in result.stdout
    assert "project_name must end with a two-digit sequence" in result.stdout


def test_generated_support_cannot_be_fact_proof(tmp_path: Path) -> None:
    create_project(tmp_path, source_kind="generated_support")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "non-evidence source_kind" in result.stdout


def test_storyboard_requires_free_director_contract(tmp_path: Path) -> None:
    create_project(tmp_path)
    storyboard_path = tmp_path / "storyboard.json"
    storyboard = json.loads(storyboard_path.read_text(encoding="utf-8"))
    storyboard.pop("creative_direction")
    write_json(storyboard_path, storyboard)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "storyboard.creative_direction is required" in result.stdout


def test_tool_explainer_requires_material_scan_and_topic_selection(tmp_path: Path) -> None:
    create_project(tmp_path)
    source_path = tmp_path / "source_brief.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source.pop("topic_selection")
    write_json(source_path, source)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "source_brief.topic_selection must be an object" in result.stdout


def test_tool_explainer_requires_beginner_review_and_voice_lock(tmp_path: Path) -> None:
    create_project(tmp_path)
    script_path = tmp_path / "script.json"
    script = json.loads(script_path.read_text(encoding="utf-8"))
    script.pop("beginner_review")
    script.pop("voice_lock")
    write_json(script_path, script)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "script.beginner_review must be an object" in result.stdout
    assert "script.voice_lock must be an object" in result.stdout


def test_storyboard_requires_douyin_safe_area(tmp_path: Path) -> None:
    create_project(tmp_path)
    storyboard_path = tmp_path / "storyboard.json"
    storyboard = json.loads(storyboard_path.read_text(encoding="utf-8"))
    storyboard.pop("safe_area")
    write_json(storyboard_path, storyboard)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "storyboard.safe_area must be an object" in result.stdout


def test_hyperframes_cannot_own_final_timeline(tmp_path: Path) -> None:
    create_project(tmp_path)
    storyboard_path = tmp_path / "storyboard.json"
    storyboard = json.loads(storyboard_path.read_text(encoding="utf-8"))
    storyboard["render_plan"]["canonical_renderer"] = "hyperframes"
    write_json(storyboard_path, storyboard)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "canonical_renderer must be remotion" in result.stdout


def test_high_risk_tool_demo_blocks_real_actions(tmp_path: Path) -> None:
    create_project(tmp_path)
    script_path = tmp_path / "script.json"
    script = json.loads(script_path.read_text(encoding="utf-8"))
    script["risk_review"] = {
        "level": "medium",
        "sensitive_domains": ["financial_transaction", "otp", "banking"],
        "demo_environment": "real_environment",
        "real_action_policy": "read_only",
        "stop_conditions": ["stop if a transaction is submitted"],
    }
    write_json(script_path, script)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "level=high" in result.stdout
    assert "high-risk real actions must be blocked" in result.stdout
    assert "require test_sandbox" in result.stdout
    assert "unknown values: banking" in result.stdout


def test_high_risk_keywords_cannot_be_omitted_from_risk_review(tmp_path: Path) -> None:
    create_project(tmp_path)
    script_path = tmp_path / "script.json"
    script = json.loads(script_path.read_text(encoding="utf-8"))
    script["viewer_task"] = "登录真实网银，输入 OTP 并提交转账"
    write_json(script_path, script)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "missing inferred sensitive domains" in result.stdout
    assert "financial_account" in result.stdout
    assert "financial_transaction" in result.stdout
    assert "otp" in result.stdout


def test_high_risk_sandbox_with_visible_boundary_proof_passes(tmp_path: Path) -> None:
    create_project(tmp_path)
    script_path = tmp_path / "script.json"
    script = json.loads(script_path.read_text(encoding="utf-8"))
    disclosure = "本演示只用模拟数据，没有登录真实账户或执行真实转账。"
    script["viewer_task"] = "在测试环境演示网银 OTP 和转账流程"
    script["beats"][0]["narration"] = disclosure
    script["risk_review"] = {
        "level": "high",
        "sensitive_domains": ["financial_account", "financial_transaction", "otp"],
        "demo_environment": "test_sandbox",
        "real_action_policy": "blocked",
        "stop_conditions": ["遇到真实账户、OTP 或交易提交立即停止"],
        "blocked_actions": ["真实登录", "读取真实 OTP", "提交真实转账"],
        "visible_disclosure": disclosure,
        "boundary_proof_ids": ["P1"],
    }
    write_json(script_path, script)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_news_requires_structured_status_and_dates(tmp_path: Path) -> None:
    create_project(tmp_path)
    source_path = tmp_path / "source_brief.json"
    script_path = tmp_path / "script.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    script = json.loads(script_path.read_text(encoding="utf-8"))
    source["format_type"] = "news_explainer"
    script["format_type"] = "news_explainer"
    script.update(
        {
            "event": "A model was announced",
            "event_status": "announced",
            "what_changed": "availability was announced",
            "affected_audience": "developers",
            "next_step": "wait for release notes",
        }
    )
    write_json(source_path, source)
    write_json(script_path, script)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "source_brief.published_at is required" in result.stdout
    assert "source_brief.event_date is required" in result.stdout


def test_reported_news_separates_report_from_reported_fact(tmp_path: Path) -> None:
    create_project(tmp_path)
    source_path = tmp_path / "source_brief.json"
    script_path = tmp_path / "script.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    script = json.loads(script_path.read_text(encoding="utf-8"))
    source.update(
        {
            "format_type": "news_explainer",
            "published_at": "2026-07-26",
            "event_date": "unknown",
            "verification_cutoff": "2026-07-26T12:00:00Z",
            "official_channels_checked": ["official newsroom"],
        }
    )
    source["claims"][0]["claim_kind"] = "report_existence"
    script.update(
        {
            "format_type": "news_explainer",
            "event": "A media report",
            "event_status": "reported",
            "what_changed": "a new claim appeared",
            "affected_audience": "developers",
            "next_step": "wait for official confirmation",
        }
    )
    write_json(source_path, source)
    write_json(script_path, script)
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "reported_fact claim" in result.stdout
