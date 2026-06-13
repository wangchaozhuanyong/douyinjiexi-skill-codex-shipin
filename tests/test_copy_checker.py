import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_public_copy.py"


def run_checker(text, tmp_path):
    copy = tmp_path / "copy_package.md"
    out = tmp_path / "compliance_report.json"
    copy.write_text(text, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--copy", str(copy), "--out", str(out)],
        text=True,
        capture_output=True,
    )
    return result, json.loads(out.read_text(encoding="utf-8"))


def test_safe_copy_passes(tmp_path):
    result, report = run_checker(
        """
# Copy Package

## First 5 Seconds Hook
口播：你写 AI 文案总是空，是因为少了三个限制。

## Claim Ledger
| Claim | Type | Source | Risk | How to phrase safely |
|---|---|---|---|---|
| 提示词越具体，输出越可控 | fact | OpenAI docs | low | 根据官方文档，具体提示更容易得到可控输出 |
""",
        tmp_path,
    )
    assert result.returncode == 0
    assert report["status"] == "passed"
    assert report["summary"]["error_count"] == 0


def test_risky_copy_fails(tmp_path):
    result, report = run_checker(
        """
# Copy Package

这是全网最强方法，100% 保证涨粉，加微信领取模板。

## Claim Ledger
| Claim | Type | Source | Risk | How to phrase safely |
|---|---|---|---|---|
| Codex 一定能让视频必火 | fact | 待补充 | high | 改为经验建议 |
""",
        tmp_path,
    )
    assert result.returncode == 1
    assert report["status"] == "failed"
    assert report["summary"]["error_count"] >= 1
