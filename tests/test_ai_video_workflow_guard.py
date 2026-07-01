from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ai_video_workflow_guard import validate_ant_ai_extended_selection, validate_frame_review, validate_top5


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_scheme7_top5_requires_exactly_five_ranked_source_items(tmp_path: Path) -> None:
    internal = tmp_path / "internal"
    internal.mkdir()
    items = [
        {
            "rank": 1,
            "title": "AI update",
            "source_title": "Official source",
            "source_url_or_note": "https://example.com",
            "visible_date": "2026-06-29",
            "why_now": "current signal",
            "why_it_matters": "useful",
            "viewer_action": "try it",
            "rank_score": 90 - index,
            "score_breakdown": {
                "freshness": 20,
                "impact": 20,
                "practical_value": 20,
                "source_strength": 15,
                "visual_clarity": 8,
                "compliance_safety": 9,
            },
            "risk_flags": [],
        }
        for index in range(4)
    ]
    write_json(internal / "ai_hot_rank_top5.json", {"items": items})
    (internal / "hot_rank_scan_report.md").write_text("# scan\n", encoding="utf-8")
    (internal / "publish_cover_text.txt").write_text("AI 热榜 TOP5\n今天最值得看的 5 条\n", encoding="utf-8")

    issues: list[str] = []
    report = validate_top5(internal, issues, [])

    assert report["item_count"] == 4
    assert "scheme_7 ai_hot_rank_top5 must contain exactly five ranked items" in issues


def test_frame_review_requires_contact_sheets_and_manual_checklist(tmp_path: Path) -> None:
    internal = tmp_path / "internal"
    internal.mkdir()
    write_json(
        internal / "frame_review_report.json",
        {
            "status": "passed",
            "blocking_issues": [],
            "manual_review": {"status": "passed", "reviewer": "codex"},
            "artifacts": {},
        },
    )

    issues: list[str] = []
    validate_frame_review(internal, issues, [])

    assert "frame_review_report.artifacts.first_5s_contact_sheet is required" in issues
    assert "frame_review_report.manual_review.checklist.no_generic_background must be true" in issues


def test_ant_ai_extended_selection_requires_locked_assets_voice_and_cta(tmp_path: Path) -> None:
    bgm = tmp_path / "ant-ai-bgm.mp3"
    bgm.write_bytes(b"fake mp3 bytes")
    selection = {
        "content": {
            "scheme_variant": "ant_ai_hotlist_extended",
            "brand_name": "蚂蚁AI",
            "fixed_cta": "关注 蚂蚁AI",
        },
        "background_template": {"id": "BG_FIXED_11_ANT_AI_HOTLIST_NEBULA_9X16"},
        "audio_music_decision": {
            "default_bgm_source_id": "ant_ai_scheme7_top5_reference_bgm_7654135072895400421",
            "default_bgm_local_path": str(bgm),
            "voice_policy": "required_narration",
            "voice_priority": True,
            "voice_profile_id": "VOICE_MALE_THICK_YUNYANG_V1",
            "generated_bgm_allowed": False,
            "generated_background_audio_allowed": False,
        },
        "voice_mix_profile": {"id": "VOICE_MALE_THICK_YUNYANG_V1"},
    }

    issues: list[str] = []
    report = validate_ant_ai_extended_selection(selection, issues, [])

    assert report["status"] == "checked"
    assert issues == []
