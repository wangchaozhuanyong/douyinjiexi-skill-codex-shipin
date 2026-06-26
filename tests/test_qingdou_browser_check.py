import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "qingdou_browser_check.py"


def write_publish_files(project: Path) -> None:
    internal = project / "internal"
    internal.mkdir(parents=True)
    (internal / "publish_title.txt").write_text("ChatGPT 到 Codex：三步交接清单\n", encoding="utf-8")
    (internal / "publish_copy.txt").write_text(
        "ChatGPT 到 Codex：三步交接清单\n"
        "OpenAI 今天的 Omio 案例给了一个很实用的工作流。\n"
        "#gtp #codex #我在抖音聊科技 #ChatGPT #AI工作流\n",
        encoding="utf-8",
    )
    (internal / "publish_topics.txt").write_text(
        "#gtp\n#codex\n#我在抖音聊科技\n#ChatGPT\n#AI工作流\n",
        encoding="utf-8",
    )


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_prepare_writes_exact_text_contract_and_bookmarklet(tmp_path):
    project = tmp_path / "outputs" / "demo"
    write_publish_files(project)

    result = run_script("--project", str(project), "--mode", "prepare")

    assert result.returncode == 0, result.stderr
    internal = project / "internal"
    contract = json.loads((internal / "qingdou_browser_check_contract.json").read_text(encoding="utf-8"))
    bookmarklet = (internal / "qingdou_bookmarklet.txt").read_text(encoding="utf-8")
    exact_text = (internal / "qingdou_check_text.txt").read_text(encoding="utf-8")
    assert contract["status"] == "prepared"
    assert contract["checked_fields"] == ["title", "caption", "topics"]
    assert contract["safety"]["no_cookie_extraction"] is True
    assert contract["safety"]["direct_api_is_not_production_route"] is True
    assert bookmarklet.startswith("javascript:")
    assert "contenteditable" in bookmarklet
    assert "敏感词检测" in bookmarklet
    assert "ChatGPT 到 Codex：三步交接清单" in exact_text
    assert "OpenAI 今天的 Omio 案例" in exact_text
    assert "#我在抖音聊科技" in exact_text


def test_record_passed_requires_visible_clean_result(tmp_path):
    project = tmp_path / "outputs" / "demo"
    write_publish_files(project)

    result = run_script(
        "--project",
        str(project),
        "--mode",
        "record-passed",
        "--visible-message",
        "未检查到敏感词",
    )

    assert result.returncode == 0, result.stderr
    report = json.loads((project / "internal" / "qingdou_keyword_check.json").read_text(encoding="utf-8"))
    assert report["status"] == "passed"
    assert report["final_check"]["status"] == "passed"
    assert report["final_check"]["items"] == []
    assert report["evidence"]["no_cookie_extraction"] is True


def test_record_passed_rejects_non_clean_visible_result(tmp_path):
    project = tmp_path / "outputs" / "demo"
    write_publish_files(project)

    result = run_script(
        "--project",
        str(project),
        "--mode",
        "record-passed",
        "--visible-message",
        "检查到敏感词1个",
    )

    assert result.returncode != 0
    assert "record-passed requires visible message" in result.stderr


def test_record_user_approved_topic_accepts_required_topic_only(tmp_path):
    project = tmp_path / "outputs" / "demo"
    write_publish_files(project)

    result = run_script(
        "--project",
        str(project),
        "--mode",
        "record-user-approved-topic",
        "--visible-message",
        "检查到敏感词 1 个",
        "--term",
        "抖音",
    )

    assert result.returncode == 0, result.stderr
    report = json.loads((project / "internal" / "qingdou_keyword_check.json").read_text(encoding="utf-8"))
    assert report["status"] == "user_override_accepted"
    assert report["final_check"]["status"] == "passed"
    assert report["final_check"]["items"][0]["term"] == "抖音"
    assert report["final_check"]["user_override"]["scope"] == "required_official_platform_topic"


def test_record_user_approved_topic_rejects_unapproved_terms(tmp_path):
    project = tmp_path / "outputs" / "demo"
    write_publish_files(project)

    result = run_script(
        "--project",
        str(project),
        "--mode",
        "record-user-approved-topic",
        "--visible-message",
        "检查到敏感词 1 个",
        "--term",
        "违规词",
    )

    assert result.returncode != 0
    assert "only allows required topic terms" in result.stderr


def test_record_blocked_writes_structured_final_check(tmp_path):
    project = tmp_path / "outputs" / "demo"
    write_publish_files(project)

    result = run_script(
        "--project",
        str(project),
        "--mode",
        "record-blocked",
        "--visible-message",
        "Qingdou page blank",
        "--reason",
        "page stalled on blank loading state",
    )

    assert result.returncode == 0, result.stderr
    report = json.loads((project / "internal" / "qingdou_keyword_check.json").read_text(encoding="utf-8"))
    assert report["status"] == "blocked"
    assert report["final_check"]["status"] == "blocked"
    assert report["final_check"]["message"] == "Qingdou page blank"
    assert report["evidence"]["reason"] == "page stalled on blank loading state"
