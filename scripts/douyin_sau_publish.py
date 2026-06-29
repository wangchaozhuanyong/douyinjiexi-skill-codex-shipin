#!/usr/bin/env python3
"""Gate Douyin uploads through social-auto-upload's `sau` CLI."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEDULE_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")
REQUIRED_QINGDOU_FIELDS = {"title", "caption", "topics"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def exists(path: Path | None) -> bool:
    return bool(path and path.is_file() and path.stat().st_size > 0)


def load_json(path: Path | None) -> dict[str, Any]:
    if not exists(path):
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_existing_path(raw: Any, project: Path) -> Path:
    value = str(raw or "").strip()
    if not value:
        return Path("")
    path = Path(value)
    if path.is_absolute():
        return path
    candidates = [
        Path.cwd() / path,
        ROOT / path,
        project / path,
        project.parent / path,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return (ROOT / path).resolve()


def checked_fields(report: dict[str, Any]) -> set[str]:
    raw = (
        report.get("checked_fields")
        or report.get("checked_text_fields")
        or report.get("checked", {}).get("fields")
        or []
    )
    return {str(item).strip().lower() for item in raw if str(item).strip()} if isinstance(raw, list) else set()


def topic_override_allowed(report: dict[str, Any]) -> bool:
    if report.get("status") != "user_override_accepted":
        return False
    final_check = report.get("final_check") if isinstance(report.get("final_check"), dict) else {}
    override = final_check.get("user_override") if isinstance(final_check.get("user_override"), dict) else {}
    topics_text = " ".join(str(item) for item in (report.get("final_topics") or report.get("topics") or []))
    items = final_check.get("items") if isinstance(final_check.get("items"), list) else []
    terms = [
        str(item.get("term") or "").strip()
        for item in items
        if isinstance(item, dict) and str(item.get("term") or "").strip()
    ]
    return (
        override.get("accepted") is True
        and override.get("allowed_by_skill_rule") is True
        and str(override.get("scope") or "") == "required_official_platform_topic"
        and bool(terms)
        and len(terms) == len(items)
        and all(term in topics_text for term in terms)
    )


def qingdou_is_publishable(report: dict[str, Any]) -> bool:
    if report.get("status") == "passed":
        final_check = report.get("final_check") if isinstance(report.get("final_check"), dict) else {}
        return str(final_check.get("status") or "") == "passed" or "未检查到敏感词" in str(final_check.get("message") or "")
    return topic_override_allowed(report)


def normalize_topic(topic: Any) -> str:
    text = str(topic or "").strip()
    return text[1:] if text.startswith("#") else text


def resolve_sau_bin(raw: str) -> str:
    if raw:
        candidate = Path(raw).expanduser()
        if candidate.exists():
            return str(candidate)
        found = shutil.which(raw)
        if found:
            return found
        return raw
    env_bin = os.environ.get("DOUYIN_SAU_BIN", "").strip()
    if env_bin:
        return resolve_sau_bin(env_bin)
    found = shutil.which("sau")
    return found or "sau"


def report_status(path: Path, required_name: str, issues: list[str]) -> dict[str, Any]:
    report = load_json(path)
    if not report:
        issues.append(f"{required_name} missing or empty: {path}")
        return {}
    if report.get("status") != "passed":
        issues.append(f"{required_name}.status must be passed")
    return report


def audio_reports_pass(project: Path, issues: list[str]) -> dict[str, Any]:
    internal = project / "internal"
    technical = report_status(internal / "video_technical_qa.json", "video_technical_qa", issues)
    continuity = report_status(internal / "audio_continuity_report.json", "audio_continuity_report", issues)
    for name, report in (("video_technical_qa", technical), ("audio_continuity_report", continuity)):
        audio = report.get("audio") if isinstance(report.get("audio"), dict) else {}
        if audio.get("has_audio") is not True:
            issues.append(f"{name}.audio.has_audio must be true before upload")
    return {"video_technical_qa": technical, "audio_continuity_report": continuity}


def read_music_policy(project: Path) -> tuple[str, list[str]]:
    policies: list[str] = []
    sources = [
        project / "internal" / "metadata.json",
        project / "internal" / "fixed_template_selection.json",
        project / "internal" / "style_recipe.json",
        project / "internal" / "director_selection.json",
    ]
    for source in sources:
        data = load_json(source)
        candidates = [
            data.get("audio_music_decision") if isinstance(data.get("audio_music_decision"), dict) else {},
            data.get("quality_spec", {}).get("audio_music_decision")
            if isinstance(data.get("quality_spec"), dict)
            and isinstance(data.get("quality_spec", {}).get("audio_music_decision"), dict)
            else {},
        ]
        for item in candidates:
            policy = str(item.get("music_policy") or "").strip()
            if policy:
                policies.append(policy)
    return (policies[0] if policies else "", policies)


def bgm_evidence_exists(project: Path) -> bool:
    metadata = load_json(project / "internal" / "metadata.json")
    for key in ("music", "bgm"):
        value = metadata.get(key)
        if isinstance(value, dict) and any(str(v or "").strip() for v in value.values()):
            return True
        if isinstance(value, str) and value.strip():
            return True
    return False


def validate_inputs(args: argparse.Namespace, project: Path, contract: dict[str, Any]) -> tuple[dict[str, Any], list[str], list[str]]:
    issues: list[str] = []
    warnings: list[str] = []
    skip_thumbnails = bool(getattr(args, "skip_thumbnails", False))
    internal = project / "internal"
    artifacts = contract.get("artifacts") if isinstance(contract.get("artifacts"), dict) else {}
    publish = contract.get("publish") if isinstance(contract.get("publish"), dict) else {}
    checks = contract.get("checks") if isinstance(contract.get("checks"), dict) else {}

    if contract.get("gate", {}).get("status") != "passed":
        issues.append("publish_contract.gate.status must be passed before SAU upload")

    video_record = artifacts.get("video") if isinstance(artifacts.get("video"), dict) else {}
    video_path = resolve_existing_path(video_record.get("final") or project / "final" / "final.mp4", project)
    if not exists(video_path):
        issues.append(f"final video missing or empty: {video_path}")

    cover_record = artifacts.get("cover") if isinstance(artifacts.get("cover"), dict) else {}
    cover_portrait = resolve_existing_path(cover_record.get("vertical") or internal / "cover_publish_vertical.png", project)
    cover_landscape = resolve_existing_path(cover_record.get("horizontal") or internal / "cover_publish_horizontal.png", project)
    cover_source = resolve_existing_path(cover_record.get("source") or internal / "cover.png", project)
    if not exists(cover_source):
        issues.append(f"cover source missing or empty: {cover_source}")
    if not exists(cover_portrait):
        warnings.append(f"portrait cover not found; SAU will rely on source/auto cover: {cover_portrait}")
        cover_portrait = Path("")
    if not exists(cover_landscape):
        warnings.append(f"landscape cover not found; SAU will rely on portrait/source cover: {cover_landscape}")
        cover_landscape = Path("")

    title = str(publish.get("title") or "").strip()
    caption = str(publish.get("caption") or "").strip()
    topics = publish.get("topics") if isinstance(publish.get("topics"), list) else []
    if not title:
        issues.append("publish.title is required")
    if len(title) > 30 and not args.allow_title_truncate:
        issues.append("publish.title exceeds Douyin 30-character upload limit; rewrite title or pass --allow-title-truncate")
    if not caption:
        issues.append("publish.caption is required")
    if not topics:
        issues.append("publish.topics must be non-empty")

    qingdou_path = resolve_existing_path((checks.get("qingdou_keyword_check") or {}).get("path") or internal / "qingdou_keyword_check.json", project)
    qingdou = load_json(qingdou_path)
    if not qingdou:
        issues.append(f"qingdou_keyword_check missing or empty: {qingdou_path}")
    elif not qingdou_is_publishable(qingdou):
        issues.append("qingdou_keyword_check must be passed or an allowed narrow topic override")
    missing_fields = REQUIRED_QINGDOU_FIELDS - checked_fields(qingdou)
    if missing_fields:
        issues.append("qingdou checked_fields missing: " + ", ".join(sorted(missing_fields)))

    audio_reports = audio_reports_pass(project, issues)
    music_policy, music_policies = read_music_policy(project)
    require_bgm = args.require_bgm or music_policy == "required_bgm"
    if require_bgm and not bgm_evidence_exists(project):
        issues.append("BGM is required, but metadata.json has no music/bgm evidence")

    if args.schedule and not SCHEDULE_RE.match(args.schedule):
        issues.append("schedule must use YYYY-MM-DD HH:MM")
    if args.execute and not args.schedule and not args.allow_immediate:
        issues.append("execute requires --schedule or explicit --allow-immediate")

    sau_bin = resolve_sau_bin(args.sau_bin)
    if args.execute and shutil.which(sau_bin) is None and not Path(sau_bin).exists():
        issues.append(f"sau binary not found: {sau_bin}")

    tags = [normalize_topic(item) for item in topics if normalize_topic(item)]
    command = [
        sau_bin,
        "douyin",
        "upload-video",
        "--account",
        args.account,
        "--file",
        str(video_path),
        "--title",
        title[:30] if args.allow_title_truncate else title,
        "--desc",
        caption,
        "--tags",
        ",".join(tags),
    ]
    if args.schedule:
        command.extend(["--schedule", args.schedule])
    if not skip_thumbnails and exists(cover_landscape):
        command.extend(["--thumbnail-landscape", str(cover_landscape)])
    if not skip_thumbnails and exists(cover_portrait):
        command.extend(["--thumbnail-portrait", str(cover_portrait)])
    command.append("--headed" if args.headed else "--headless")
    if args.debug:
        command.append("--debug")

    plan = {
        "project": str(project),
        "contract": str(project / "internal" / "publish_contract.json"),
        "sau_bin": sau_bin,
        "account": args.account,
        "publication_mode": "scheduled" if args.schedule else "immediate",
        "schedule": args.schedule or "",
        "allow_immediate": args.allow_immediate,
        "artifacts": {
            "video": str(video_path),
            "cover_source": str(cover_source),
            "cover_portrait": str(cover_portrait) if exists(cover_portrait) else "",
            "cover_landscape": str(cover_landscape) if exists(cover_landscape) else "",
            "skip_thumbnails": skip_thumbnails,
        },
        "publish": {"title": title, "caption": caption, "topics": topics, "tags": tags},
        "audio": {
            "required": True,
            "music_policy": music_policy,
            "music_policies": music_policies,
            "bgm_required": require_bgm,
            "bgm_evidence": bgm_evidence_exists(project),
            "video_technical_qa_status": audio_reports["video_technical_qa"].get("status"),
            "audio_continuity_status": audio_reports["audio_continuity_report"].get("status"),
        },
        "qingdou": {"path": str(qingdou_path), "status": qingdou.get("status", "missing")},
        "command": command,
    }
    return plan, issues, warnings


def run_command(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, text=True, capture_output=True)
    return {
        "returncode": result.returncode,
        "stdout": result.stdout[-4000:],
        "stderr": result.stderr[-4000:],
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    project = Path(args.project).resolve()
    contract_path = Path(args.contract).resolve() if args.contract else project / "internal" / "publish_contract.json"
    contract = load_json(contract_path)
    if not contract:
        result = {
            "status": "blocked",
            "mode": "execute" if args.execute else "dry_run",
            "checked_at": now_iso(),
            "issues": [f"publish contract missing or empty: {contract_path}"],
            "warnings": [],
        }
        write_json(Path(args.out) if args.out else project / "internal" / "douyin_sau_upload_report.json", result)
        return result

    plan, issues, warnings = validate_inputs(args, project, contract)
    report_path = Path(args.out) if args.out else project / "internal" / "douyin_sau_upload_report.json"
    result: dict[str, Any] = {
        "status": "blocked" if issues else ("executing" if args.execute else "planned"),
        "mode": "execute" if args.execute else "dry_run",
        "checked_at": now_iso(),
        "issues": issues,
        "warnings": warnings,
        "plan": plan,
        "third_party": {
            "tool": "social-auto-upload",
            "cli": "sau douyin upload-video",
            "safety_boundary": "SAU only runs after publish_contract and local upload gates pass",
        },
    }
    if issues:
        write_json(report_path, result)
        return result

    if not args.execute:
        write_json(report_path, result)
        return result

    check_command = [plan["sau_bin"], "douyin", "check", "--account", args.account]
    account_check = run_command(check_command)
    result["account_check"] = account_check
    if account_check["returncode"] != 0:
        result["status"] = "blocked"
        result["issues"].append(f"SAU account check failed for account: {args.account}")
        write_json(report_path, result)
        return result

    upload_result = run_command(plan["command"])
    result["upload_result"] = upload_result
    result["status"] = "submitted_to_sau" if upload_result["returncode"] == 0 else "failed"
    if upload_result["returncode"] != 0:
        result["issues"].append("SAU upload command failed")
    result["finished_at"] = now_iso()
    write_json(report_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and optionally upload a passed Douyin video package with SAU.")
    parser.add_argument("--project", required=True, help="outputs/<project> directory")
    parser.add_argument("--contract", help="Defaults to <project>/internal/publish_contract.json")
    parser.add_argument("--account", required=True, help="SAU Douyin account name")
    parser.add_argument("--sau-bin", default="", help="Path to sau executable, or rely on DOUYIN_SAU_BIN/PATH")
    parser.add_argument("--schedule", default="", help="Optional scheduled publish time: YYYY-MM-DD HH:MM")
    parser.add_argument("--execute", action="store_true", help="Actually run SAU after all gates pass")
    parser.add_argument("--allow-immediate", action="store_true", help="Allow execute without --schedule")
    parser.add_argument("--allow-title-truncate", action="store_true", help="Allow uploading title[:30]")
    parser.add_argument("--skip-thumbnails", action="store_true", help="Do not pass thumbnail files to SAU; use the video's checked first-frame cover.")
    parser.add_argument("--require-bgm", action="store_true", help="Require metadata music/bgm evidence before upload")
    parser.add_argument("--headed", action="store_true", help="Run SAU browser with UI")
    parser.add_argument("--debug", action="store_true", help="Pass --debug to SAU upload")
    parser.add_argument("--out", help="Defaults to <project>/internal/douyin_sau_upload_report.json")
    args = parser.parse_args()

    result = run(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] in {"planned", "submitted_to_sau"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
