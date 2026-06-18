import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_beginner_checker(text, tmp_path, copy_json=None):
    copy = tmp_path / "copy_package.md"
    out = tmp_path / "beginner_value_review.json"
    copy.write_text(text, encoding="utf-8")
    command = [
        sys.executable,
        str(ROOT / "scripts" / "validate_beginner_copy.py"),
        "--copy",
        str(copy),
        "--out",
        str(out),
    ]
    if copy_json is not None:
        json_path = tmp_path / "copy_package.json"
        json_path.write_text(json.dumps(copy_json, ensure_ascii=False), encoding="utf-8")
        command.extend(["--copy-json", str(json_path)])
    result = subprocess.run(command, text=True, capture_output=True)
    return result, json.loads(out.read_text(encoding="utf-8"))


def test_beginner_copy_review_passes_task_result_copy(tmp_path):
    copy_json = {
        "beginner_task_card": {
            "target_viewer": "第一次用 ChatGPT 写短视频文案的小白创作者",
            "task": "把产品介绍改成 30 秒短视频口播",
            "visible_result": "左边套话，右边能直接检查的口播",
            "why_watch_now": "很多人会打开 AI，但不会把需求说清楚",
            "first_action": "打开 ChatGPT，先填目标观众",
            "time_saving_claim": "少来回改 3 次，减少重复复制需求",
        },
        "title_options": [
            "小白用 ChatGPT 写口播，先填这 5 格",
            "别只说帮我写文案，3 步让输出能直接检查",
            "把 AI 套话改成能发口播，就看前后对比",
        ],
        "first_5_seconds_hook": {
            "line": "不会写口播，先别怪 ChatGPT。看左边是空话，看右边填 5 格后直接能检查。",
            "visual_changes": ["左边空话输出", "右边五格模板"],
        },
        "proof_visual_plan": [{"claim": "补五格后更可检查", "proof_visual": "真实截图和左右对比", "asset_needed": "改前改后截图"}],
        "before_after_plan": {"before": "一句泛需求", "after": "五格模板", "visual_comparison": "左右对比"},
        "save_value": {"reason": "保存模板", "reusable_asset": "对象 + 场景 + 格式 + 禁区 + 证据"},
        "terminology_explained": [{"term": "Prompt", "plain_explanation": "也就是交给 AI 的任务说明"}],
    }
    result, report = run_beginner_checker(
        """
# Copy Package

## Voiceover

第一步，打开 ChatGPT，不要先说帮我写文案。
第二步，填使用场景：抖音 30 秒口播。
第三步，填输出格式：标题、前 5 秒、完整口播。
这样少来回改 3 次，少复制粘贴重复需求。

## Proof Visual Plan

真实截图、左右对比、改前改后输出。

## Save Value

保存这个模板，下次直接套。
""",
        tmp_path,
        copy_json,
    )
    assert result.returncode == 0
    assert report["status"] == "passed"
    assert report["total_score"] >= 8.8


def test_beginner_copy_review_rejects_generic_ai_copy(tmp_path):
    result, report = run_beginner_checker(
        """
# Copy Package

## Title Options

1. ChatGPT 新功能太强了

## First 5 Seconds

今天给大家介绍一个 AI 工具，它可以提升效率，改变工作流。

## Voiceover

AI 时代已经来了。这个工具很方便，也很强。大家一定要学会使用它。
""",
        tmp_path,
    )
    assert result.returncode == 1
    assert report["status"] == "failed"
    assert report["rewrite_required"]


def test_beginner_copy_review_requires_problem_example(tmp_path):
    copy_json = {
        "beginner_task_card": {
            "target_viewer": "第一次用 ChatGPT 写文案的小白创作者",
            "task": "写一条短视频口播",
            "visible_result": "左边空话，右边能直接检查",
            "why_watch_now": "很多人会打开 AI，但需求说不清楚",
            "first_action": "打开 ChatGPT，先填目标观众",
            "time_saving_claim": "少来回改 3 次",
        },
        "title_options": ["小白用 ChatGPT 写口播，先填这 5 格"],
        "first_5_seconds_hook": {
            "line": "小白不会写口播，先别怪 ChatGPT。看左边是空话，右边填 5 格后能直接检查。",
            "visual_changes": ["左边空话输出", "右边五格模板"],
        },
        "proof_visual_plan": [{"claim": "补五格后更可检查", "proof_visual": "真实截图和左右对比", "asset_needed": "改前改后截图"}],
        "before_after_plan": {"before": "一句泛需求", "after": "五格模板", "visual_comparison": "左右对比"},
        "save_value": {"reason": "保存模板", "reusable_asset": "对象 + 场景 + 格式 + 禁区 + 证据"},
    }
    result, report = run_beginner_checker(
        """
# Copy Package

## Voiceover

小白不会写口播，这个问题很常见。
第一步，打开 ChatGPT，先填目标观众。
第二步，填使用场景。
第三步，填输出格式。
少来回改 3 次。

## Save Value

保存这个模板，下次直接套。
""",
        tmp_path,
        copy_json,
    )
    assert result.returncode == 1
    assert report["status"] == "failed"
    assert report["scores"]["problem_example_score"] < 8.5
    assert any("problem_example_score" in item for item in report["rewrite_required"])


def test_beginner_copy_training_runs_ten_iterations(tmp_path):
    out_dir = tmp_path / "training" / "internal"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "train_beginner_copy.py"),
            "--iterations",
            "10",
            "--out-dir",
            str(out_dir),
        ],
        text=True,
        capture_output=True,
    )
    report = json.loads((out_dir / "beginner_copy_training_report.json").read_text(encoding="utf-8"))
    review = json.loads((out_dir / "beginner_value_review.json").read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert len(report["iterations"]) == 10
    assert review["status"] == "passed"
    assert review["total_score"] >= 8.8
