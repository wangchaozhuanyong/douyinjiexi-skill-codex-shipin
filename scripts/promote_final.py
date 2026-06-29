#!/usr/bin/env python3
"""Promote a pre-publish-gated draft package into the public final folder."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from artifact_fingerprint import collect_fingerprints, file_fingerprint, verify_report_inputs, write_report_with_fingerprints

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MIN_SIZE_BYTES = 500_000


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)


def frame_rate(value: str) -> float:
    numerator, _, denominator = value.partition("/")
    try:
        return round(float(numerator or 0) / float(denominator or 1), 3)
    except Exception:
        return 0.0


def probe_media(path: Path) -> dict[str, Any]:
    result = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ]
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or f"ffprobe failed for {path}")
    return json.loads(result.stdout)


def media_probe_issues(video: Path, metadata_path: Path) -> list[str]:
    issues: list[str] = []
    if not exists(video):
        return [f"video missing or empty: {video}"]
    if video.stat().st_size < DEFAULT_MIN_SIZE_BYTES:
        issues.append("video file is too small for publish-ready promotion")
    data = probe_media(video)
    streams = data.get("streams", [])
    fmt = data.get("format", {})
    video_stream = next((item for item in streams if item.get("codec_type") == "video"), {})
    audio_stream = next((item for item in streams if item.get("codec_type") == "audio"), {})
    if not video_stream:
        issues.append("video stream is missing")
    if not audio_stream:
        issues.append("audio stream is missing")
    width = int(video_stream.get("width") or 0)
    height = int(video_stream.get("height") or 0)
    fps = frame_rate(str(video_stream.get("avg_frame_rate") or video_stream.get("r_frame_rate") or "0/1"))
    video_duration = float(video_stream.get("duration") or fmt.get("duration") or 0)
    audio_duration = float(audio_stream.get("duration") or 0)
    metadata = load_json(metadata_path) if exists(metadata_path) else {}
    expected_width = int(metadata.get("target_width") or metadata.get("width") or 1920)
    expected_height = int(metadata.get("target_height") or metadata.get("height") or 1080)
    expected_fps = float(metadata.get("fps") or 30)
    expected_duration = float(metadata.get("duration") or 0)
    if width != expected_width or height != expected_height:
        issues.append(f"resolution mismatch: expected {expected_width}x{expected_height}, got {width}x{height}")
    if fps and abs(fps - expected_fps) > 0.1:
        issues.append(f"fps mismatch: expected {expected_fps}, got {fps}")
    if expected_duration and abs(expected_duration - video_duration) > 0.5:
        issues.append("duration does not match metadata")
    if audio_stream and abs(video_duration - audio_duration) > 0.3:
        issues.append("audio/video duration gap exceeds 0.3s")
    return issues


def required_artifact(contract: dict[str, Any], group: str, key: str = "source") -> Path:
    artifacts = contract.get("artifacts") if isinstance(contract.get("artifacts"), dict) else {}
    record = artifacts.get(group) if isinstance(artifacts.get(group), dict) else {}
    path = Path(str(record.get(key) or ""))
    if not exists(path):
        raise SystemExit(f"publish_contract artifact {group}.{key} missing or empty: {path}")
    return path


def optional_artifact(contract: dict[str, Any], group: str, key: str) -> Path | None:
    artifacts = contract.get("artifacts") if isinstance(contract.get("artifacts"), dict) else {}
    record = artifacts.get(group) if isinstance(artifacts.get(group), dict) else {}
    raw = str(record.get(key) or "").strip()
    if not raw:
        return None
    path = Path(raw)
    return path if exists(path) else None


def require_contract_ready(contract: dict[str, Any]) -> None:
    gate = contract.get("gate") if isinstance(contract.get("gate"), dict) else {}
    if gate.get("status") != "passed":
        issues = gate.get("issues") if isinstance(gate.get("issues"), list) else []
        detail = "\n".join(str(item) for item in issues) if issues else "run scripts/pre_publish_gate.py first"
        raise SystemExit("publish_contract.gate.status must be passed before promotion\n" + detail)


def run_provider_audit(project: Path) -> None:
    internal = project / "internal"
    result = run(
        [
            sys.executable,
            "scripts/audit_provider_usage.py",
            "--project",
            str(project),
            "--phase",
            "final",
            "--out",
            str(internal / "provider_usage_audit.json"),
            "--md-out",
            str(internal / "provider_usage_audit.md"),
        ]
    )
    if result.returncode != 0:
        detail = (result.stdout + "\n" + result.stderr).strip()
        raise SystemExit("final provider usage audit failed before promotion\n" + detail)


def require_fresh_promotion_inputs(project: Path, contract: dict[str, Any], contract_path: Path) -> None:
    internal = project / "internal"
    video = internal / "draft.mp4"
    metadata = internal / "metadata.json"
    issues: list[str] = []
    issues.extend(verify_report_inputs(contract, [path for path in [video, metadata] if exists(path)]))
    checks = contract.get("checks") if isinstance(contract.get("checks"), dict) else {}
    for name, expected in {
        "qa_report": [video, metadata],
        "provider_usage_audit": [video, metadata],
    }.items():
        path = Path(str((checks.get(name) or {}).get("path") or internal / f"{name}.json"))
        if not exists(path):
            issues.append(f"{name} missing or empty: {path}")
            continue
        report = load_json(path)
        issues.extend(f"{name}: {issue}" for issue in verify_report_inputs(report, [p for p in expected if exists(p)]))
    if issues:
        raise SystemExit(f"stale promotion inputs for {contract_path}:\n" + "\n".join(issues))


def cleanup_intermediates(project: Path, final_video: Path) -> dict[str, Any]:
    removed: list[str] = []
    missing_ok: list[str] = []
    final = project / "final"
    if final.exists():
        for path in final.iterdir():
            if path != final_video and path.is_file():
                path.unlink()
                removed.append(str(path))

    removable_dirs = [
        project / "assets" / "frames",
        project / "internal" / "hf_frames",
        project / "internal" / "frames",
    ]
    for path in removable_dirs:
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
            removed.append(str(path))
        else:
            missing_ok.append(str(path))

    internal = project / "internal"
    if internal.exists():
        removable_files: set[Path] = set(internal.glob("*.mp4"))
        removable_files.update(
            path
            for name in [
                "audio.aac",
                "silent_hf.aac",
                "root_audio.tmp.aac",
                "voice_sfx_mix.tmp.wav",
            ]
            for path in [internal / name]
        )
        for path in sorted(removable_files):
            if path.exists() and path.is_file():
                path.unlink()
                removed.append(str(path))
            else:
                missing_ok.append(str(path))
    report = {
        "status": "passed",
        "cleanup_status": "final_folder_mp4_with_manifests",
        "checked_at": now_iso(),
        "final_video": str(final_video),
        "removed": removed,
        "removed_count": len(removed),
        "missing_ok": missing_ok,
    }
    write_json(project / "internal" / "cleanup_report.json", report)
    return report


def promote(project: Path, contract_path: Path) -> dict[str, Any]:
    final = project / "final"
    run_provider_audit(project)
    if not exists(contract_path):
        raise SystemExit(f"publish contract missing or empty: {contract_path}")
    contract = load_json(contract_path)
    require_contract_ready(contract)
    metadata_path = required_artifact(contract, "metadata")
    required_artifact(contract, "cover")
    publish_copy_path = required_artifact(contract, "publish_copy")
    video_source = required_artifact(contract, "video")
    expected_video = project / "internal" / "draft.mp4"
    if video_source.resolve() != expected_video.resolve():
        raise SystemExit(f"promotion source must be internal/draft.mp4, got: {video_source}")
    media_issues = media_probe_issues(video_source, metadata_path)
    if media_issues:
        raise SystemExit("media probe failed before promotion:\n" + "\n".join(media_issues))
    require_fresh_promotion_inputs(project, contract, contract_path)
    optional_artifact(contract, "cover", "vertical")
    optional_artifact(contract, "cover", "horizontal")

    final.mkdir(parents=True, exist_ok=True)
    target = final / "final.mp4"
    shutil.copy2(video_source, target)
    final_inputs = [
        target,
        metadata_path,
        publish_copy_path,
        project / "internal" / "qa_report.json",
        project / "internal" / "provider_usage_audit.json",
        project / "internal" / "publish_contract.json",
    ]
    artifact_manifest = {
        "status": "passed",
        "created_at": now_iso(),
        "project": str(project),
        "final": {"final.mp4": file_fingerprint(target)},
        "inputs": collect_fingerprints([path for path in final_inputs if exists(path)]),
    }
    cleanup_report = cleanup_intermediates(project, target)
    promotion_report = {
        "status": "promoted",
        "promoted_at": now_iso(),
        "cleanup_status": "final_folder_mp4_with_manifests",
        "outputs": {"final.mp4": str(target)},
        "removed": cleanup_report["removed"],
        "cleanup_report": str(project / "internal" / "cleanup_report.json"),
    }
    write_report_with_fingerprints(promotion_report, [target, metadata_path, publish_copy_path])
    write_json(final / "artifact_manifest.json", artifact_manifest)
    write_json(final / "promotion_report.json", promotion_report)
    return promotion_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote pre-publish-gated draft artifacts to final/.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic>")
    parser.add_argument("--contract", help="Defaults to <project>/internal/publish_contract.json")
    parser.add_argument("--out", help="Optional promotion_report.json path")
    args = parser.parse_args()

    project = Path(args.project)
    contract = Path(args.contract) if args.contract else project / "internal" / "publish_contract.json"
    outputs = promote(project, contract)
    result = {"status": "promoted", **outputs}
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
