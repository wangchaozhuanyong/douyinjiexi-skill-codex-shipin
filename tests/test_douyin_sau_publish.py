import json
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import douyin_sau_publish


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_args(project: Path, **overrides) -> Namespace:
    data = {
        "project": str(project),
        "contract": None,
        "account": "creator",
        "sau_bin": "/bin/echo",
        "schedule": "2026-07-01 21:30",
        "execute": False,
        "allow_immediate": False,
        "allow_title_truncate": False,
        "require_bgm": False,
        "headed": False,
        "debug": False,
        "out": None,
    }
    data.update(overrides)
    return Namespace(**data)


def make_publishable_project(tmp_path: Path, title: str = "测试标题") -> Path:
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    final = project / "final"
    final.mkdir(parents=True)
    internal.mkdir(parents=True)

    (final / "final.mp4").write_bytes(b"video")
    (internal / "cover.png").write_bytes(b"cover")
    (internal / "cover_publish_vertical.png").write_bytes(b"portrait")
    (internal / "cover_publish_horizontal.png").write_bytes(b"landscape")
    (internal / "publish_copy.txt").write_text("发布文案\n", encoding="utf-8")
    write_json(internal / "metadata.json", {"duration": 8})
    write_json(internal / "video_technical_qa.json", {"status": "passed", "audio": {"has_audio": True}})
    write_json(internal / "audio_continuity_report.json", {"status": "passed", "audio": {"has_audio": True}})
    write_json(
        internal / "qingdou_keyword_check.json",
        {
            "status": "passed",
            "checked_fields": ["title", "caption", "topics"],
            "final_check": {"status": "passed", "message": "未检查到敏感词", "items": []},
        },
    )
    write_json(
        internal / "publish_contract.json",
        {
            "gate": {"status": "passed", "issues": []},
            "artifacts": {
                "video": {"final": str(final / "final.mp4")},
                "cover": {
                    "source": str(internal / "cover.png"),
                    "vertical": str(internal / "cover_publish_vertical.png"),
                    "horizontal": str(internal / "cover_publish_horizontal.png"),
                },
            },
            "publish": {
                "title": title,
                "caption": "这是一条测试发布文案",
                "topics": ["#AI工具", "#我在抖音聊科技"],
            },
            "checks": {"qingdou_keyword_check": {"path": str(internal / "qingdou_keyword_check.json")}},
        },
    )
    return project


def test_dry_run_writes_sau_upload_plan(tmp_path: Path) -> None:
    project = make_publishable_project(tmp_path)

    result = douyin_sau_publish.run(make_args(project))

    assert result["status"] == "planned"
    command = result["plan"]["command"]
    assert command[:3] == ["/bin/echo", "douyin", "upload-video"]
    assert "--thumbnail-landscape" in command
    assert "--thumbnail-portrait" in command
    assert "--schedule" in command
    assert result["plan"]["publish"]["tags"] == ["AI工具", "我在抖音聊科技"]
    assert (project / "internal" / "douyin_sau_upload_report.json").exists()


def test_blocks_when_publish_contract_gate_failed(tmp_path: Path) -> None:
    project = make_publishable_project(tmp_path)
    contract = json.loads((project / "internal" / "publish_contract.json").read_text(encoding="utf-8"))
    contract["gate"] = {"status": "failed", "issues": ["qa failed"]}
    write_json(project / "internal" / "publish_contract.json", contract)

    result = douyin_sau_publish.run(make_args(project))

    assert result["status"] == "blocked"
    assert "publish_contract.gate.status must be passed before SAU upload" in result["issues"]


def test_execute_requires_schedule_or_immediate_override(tmp_path: Path) -> None:
    project = make_publishable_project(tmp_path)

    result = douyin_sau_publish.run(make_args(project, execute=True, schedule=""))

    assert result["status"] == "blocked"
    assert "execute requires --schedule or explicit --allow-immediate" in result["issues"]


def test_require_bgm_needs_music_evidence(tmp_path: Path) -> None:
    project = make_publishable_project(tmp_path)

    blocked = douyin_sau_publish.run(make_args(project, require_bgm=True))
    assert blocked["status"] == "blocked"
    assert "BGM is required, but metadata.json has no music/bgm evidence" in blocked["issues"]

    write_json(
        project / "internal" / "metadata.json",
        {"duration": 8, "music": {"mode": "local_library", "path": "assets/audio/bgm.mp3"}},
    )
    planned = douyin_sau_publish.run(make_args(project, require_bgm=True))
    assert planned["status"] == "planned"
    assert planned["plan"]["audio"]["bgm_evidence"] is True


def test_long_title_blocks_unless_truncate_allowed(tmp_path: Path) -> None:
    project = make_publishable_project(tmp_path, title="这是一个超过三十个字符的测试标题需要在上传前被拦住否则会被抖音自动截断")

    blocked = douyin_sau_publish.run(make_args(project))
    assert blocked["status"] == "blocked"
    assert any("30-character" in issue for issue in blocked["issues"])

    planned = douyin_sau_publish.run(make_args(project, allow_title_truncate=True))
    assert planned["status"] == "planned"
    assert len(planned["plan"]["command"][planned["plan"]["command"].index("--title") + 1]) == 30
