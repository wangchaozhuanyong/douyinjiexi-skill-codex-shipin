import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_content_alignment.py"


def run_alignment(tmp_path, copy_json, storyboard=None, copy_text="# Copy Package\n中文文案\n"):
    copy_md = tmp_path / "copy_package.md"
    copy_json_path = tmp_path / "copy_package.json"
    out = tmp_path / "content_alignment_report.json"
    copy_md.write_text(copy_text, encoding="utf-8")
    copy_json_path.write_text(json.dumps(copy_json, ensure_ascii=False) + "\n", encoding="utf-8")
    cmd = [
        sys.executable,
        str(SCRIPT),
        "--copy",
        str(copy_md),
        "--copy-json",
        str(copy_json_path),
        "--out",
        str(out),
    ]
    if storyboard is not None:
        storyboard_path = tmp_path / "storyboard.json"
        storyboard_path.write_text(json.dumps(storyboard, ensure_ascii=False) + "\n", encoding="utf-8")
        cmd.extend(["--storyboard", str(storyboard_path)])
    result = subprocess.run(cmd, text=True, capture_output=True)
    return result, json.loads(out.read_text(encoding="utf-8"))


def test_golden_content_alignment_passes(tmp_path):
    out = tmp_path / "content_alignment_report.json"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--copy",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "copy_package.md"),
            "--copy-json",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "copy_package.json"),
            "--storyboard",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "storyboard.json"),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    report = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert report["status"] == "passed"
    assert report["checks"]["source_claim_alignment"] == "passed"
    assert report["checks"]["copy_progression"] == "passed"
    assert report["checks"]["visual_alignment"] == "passed"
    assert report["checks"]["visual_rhythm"] == "passed"
    assert report["checks"]["sfx_cues"] == "passed"
    assert report["checks"]["chinese_first_text"] == "passed"


def test_repeated_progression_fails(tmp_path):
    copy_json = {
        "claim_ledger": [{"claim": "补限制后输出更可检查", "type": "advice", "source": "local demo"}],
        "copy_progression_plan": [
            {"scene_id": "S01", "stage": "result", "new_information_job": "展示补限制后输出更可检查"},
            {"scene_id": "S02", "stage": "result", "new_information_job": "展示补限制后输出更可检查"},
        ],
    }
    result, report = run_alignment(tmp_path, copy_json)
    assert result.returncode == 1
    assert report["checks"]["copy_progression"] == "failed"
    assert any("repeats the previous information job" in issue for issue in report["blocking_issues"])


def test_generic_visual_without_claim_binding_fails(tmp_path):
    copy_json = {
        "claim_ledger": [{"claim": "三步限制能减少空话", "type": "advice", "source": "local demo"}],
        "copy_progression_plan": [
            {"scene_id": "S01", "stage": "hook", "new_information_job": "先展示错误提示词"}
        ],
    }
    storyboard = {
        "title": "ChatGPT 文案先补限制",
        "scenes": [
            {
                "scene_id": "S01",
                "concept": "错误提示词",
                "voice": "先展示错误提示词。",
                "caption": "错误提示词",
                "on_screen_text": ["错误提示词"],
                "visual": {
                    "scene_type": "generated_visual",
                    "description": "generic AI futuristic technology background",
                    "asset_source_type": "generated",
                },
            }
        ],
    }
    result, report = run_alignment(tmp_path, copy_json, storyboard)
    assert result.returncode == 1
    assert report["checks"]["visual_alignment"] == "failed"
    assert any("visual looks generic" in issue for issue in report["blocking_issues"])


def test_static_page_without_visual_beats_fails(tmp_path):
    copy_json = {
        "content_alignment_map": [
            {
                "claim_id": "C01",
                "claim": "五格提示词能减少反复改",
                "source_ids": ["local-demo"],
                "scene_id": "S01",
                "visual_job": "展示五格模板如何拆开任务",
            }
        ],
        "copy_progression_plan": [
            {"scene_id": "S01", "stage": "method", "new_information_job": "拆开五格提示词模板"}
        ],
    }
    storyboard = {
        "title": "提示词先拆五格",
        "quality_spec": {"sfx_policy": "轻提示音必须低于口播"},
        "scenes": [
            {
                "scene_id": "S01",
                "duration_target": 8.0,
                "new_information_job": "拆开五格提示词模板",
                "source_claim_ids": ["C01"],
                "voice": "把提示词拆成对象、场景、格式、禁区和证据素材。",
                "caption": "五格提示词模板",
                "visual_job": "展示五格模板如何拆开任务",
                "visual": {"description": "五格模板逐项展开", "evidence_source": "local-demo"},
                "sfx_cues": [{"event": "模板锁定", "sound": "轻提示音"}],
            }
        ],
    }
    result, report = run_alignment(tmp_path, copy_json, storyboard)
    assert result.returncode == 1
    assert report["checks"]["visual_rhythm"] == "failed"
    assert any("static-page narration" in issue for issue in report["blocking_issues"])


def test_dynamic_storyboard_without_sfx_cues_fails(tmp_path):
    copy_json = {
        "content_alignment_map": [
            {
                "claim_id": f"C{index:02d}",
                "claim": claim,
                "source_ids": ["local-demo"],
                "scene_id": f"S{index:02d}",
                "visual_job": visual_job,
            }
            for index, claim, visual_job in [
                (1, "先看错误提示词的问题", "展示错误输入和输出对比"),
                (2, "再补对象和场景", "高亮对象和场景两个槽位"),
                (3, "最后补禁区和证据", "高亮禁区和证据素材"),
            ]
        ],
        "copy_progression_plan": [
            {"scene_id": "S01", "stage": "problem", "new_information_job": "指出错误提示词的问题"},
            {"scene_id": "S02", "stage": "method", "new_information_job": "补对象和场景"},
            {"scene_id": "S03", "stage": "proof", "new_information_job": "补禁区和证据素材"},
        ],
    }
    storyboard = {
        "title": "提示词先补限制",
        "quality_spec": {"sfx_policy": "转场和状态变化必须有低音量提示音"},
        "scenes": [
            {
                "scene_id": f"S{index:02d}",
                "duration_target": 3.0,
                "new_information_job": job,
                "source_claim_ids": [f"C{index:02d}"],
                "voice": voice,
                "caption": caption,
                "visual_job": visual_job,
                "visual": {"description": visual_job, "evidence_source": "local-demo"},
                "beat_map": [{"time_offset_sec": 0.3, "visual_change": "高亮当前槽位"}],
            }
            for index, job, voice, caption, visual_job in [
                (1, "指出错误提示词的问题", "先看错误提示词为什么空。", "错误提示词", "展示错误输入和输出对比"),
                (2, "补对象和场景", "再补对象和场景。", "对象和场景", "高亮对象和场景两个槽位"),
                (3, "补禁区和证据素材", "最后补禁区和证据素材。", "禁区和证据", "高亮禁区和证据素材"),
            ]
        ],
    }
    result, report = run_alignment(tmp_path, copy_json, storyboard)
    assert result.returncode == 1
    assert report["checks"]["sfx_cues"] == "failed"
    assert any("missing sfx_cues" in issue for issue in report["blocking_issues"])


def test_nonessential_english_visible_text_fails(tmp_path):
    copy_json = {
        "title_options": ["AI Workflow Template"],
        "claim_ledger": [{"claim": "补限制后输出更可检查", "type": "advice", "source": "local demo"}],
        "copy_progression_plan": [
            {"scene_id": "S01", "stage": "hook", "new_information_job": "展示改前改后对比"}
        ],
    }
    result, report = run_alignment(tmp_path, copy_json)
    assert result.returncode == 1
    assert report["checks"]["chinese_first_text"] == "failed"
    assert any("Chinese-first" in issue for issue in report["blocking_issues"])
