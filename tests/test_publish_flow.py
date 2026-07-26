from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "skills" / "douyin-video-production-core" / "scripts"


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def prepare_publish_project(tmp_path: Path, include_platform: bool = True) -> tuple[Path, Path]:
    video = tmp_path / "render" / "final.mp4"
    cover = tmp_path / "render" / "cover.png"
    video.parent.mkdir()
    video.write_bytes(b"video" * 100)
    cover.write_bytes(b"cover")
    write_json(
        tmp_path / "script.json",
        {
            "publish": {
                "title": "测试标题",
                "caption": "测试文案",
                "topics": ["AI工具"],
            }
        },
    )
    write_json(tmp_path / "qa_report.json", {"status": "passed"})
    viewer_text = tmp_path / "viewer_text.txt"
    publish_copy = tmp_path / "publish_copy.txt"
    viewer_text.write_text("测试标题\n片内字幕", encoding="utf-8")
    publish_copy.write_text("测试标题\n测试文案\n#AI工具", encoding="utf-8")
    local_check = subprocess.run(
        [
            sys.executable,
            str(CORE / "check_public_copy.py"),
            str(viewer_text),
            str(publish_copy),
            "--out",
            str(tmp_path / "public_text_check.json"),
        ],
        capture_output=True,
        text=True,
    )
    assert local_check.returncode == 0, local_check.stdout + local_check.stderr
    if include_platform:
        write_json(
            tmp_path / "platform_text_check.json",
            {
                "status": "passed",
                "checked_at": "2026-07-26T00:00:00Z",
                "fields_checked": ["title", "caption", "topics"],
                "final_title": "测试标题",
                "final_caption": "测试文案",
                "final_topics": ["#AI工具"],
                "visible_result": "未检查到敏感词",
            },
        )
    return viewer_text, publish_copy


def test_publish_package_and_gate(tmp_path: Path) -> None:
    prepare_publish_project(tmp_path)

    build = subprocess.run(
        [sys.executable, str(CORE / "build_publish_package.py"), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert build.returncode == 0, build.stdout + build.stderr
    gate = subprocess.run(
        [
            sys.executable,
            str(CORE / "pre_publish_gate.py"),
            "--package",
            str(tmp_path / "publish_package.json"),
        ],
        capture_output=True,
        text=True,
    )
    assert gate.returncode == 0, gate.stdout + gate.stderr


def test_package_blocks_without_visible_platform_check(tmp_path: Path) -> None:
    prepare_publish_project(tmp_path, include_platform=False)
    result = subprocess.run(
        [sys.executable, str(CORE / "build_publish_package.py"), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "passed real visible result" in result.stdout


def test_package_blocks_when_checked_public_text_changes(tmp_path: Path) -> None:
    _, publish_copy = prepare_publish_project(tmp_path)
    publish_copy.write_text("测试标题\n已经改过的文案\n#AI工具", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(CORE / "build_publish_package.py"), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "public_text_check is stale" in result.stdout


def test_package_blocks_when_platform_copy_does_not_match_script(tmp_path: Path) -> None:
    prepare_publish_project(tmp_path)
    platform_path = tmp_path / "platform_text_check.json"
    platform = json.loads(platform_path.read_text(encoding="utf-8"))
    platform["final_caption"] = "上一版文案"
    write_json(platform_path, platform)
    result = subprocess.run(
        [sys.executable, str(CORE / "build_publish_package.py"), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "final_caption does not match" in result.stdout


def test_pre_publish_gate_blocks_text_changed_after_package_build(tmp_path: Path) -> None:
    _, publish_copy = prepare_publish_project(tmp_path)
    build = subprocess.run(
        [sys.executable, str(CORE / "build_publish_package.py"), "--project", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert build.returncode == 0, build.stdout + build.stderr
    publish_copy.write_text("测试标题\n打包以后又改了文案\n#AI工具", encoding="utf-8")
    gate = subprocess.run(
        [
            sys.executable,
            str(CORE / "pre_publish_gate.py"),
            "--package",
            str(tmp_path / "publish_package.json"),
        ],
        capture_output=True,
        text=True,
    )
    assert gate.returncode == 2
    assert "local text check is stale" in gate.stdout
