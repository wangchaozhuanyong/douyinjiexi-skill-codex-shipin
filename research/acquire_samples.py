#!/usr/bin/env python3
"""Acquire public Douyin sample bodies declared in sample_registry.json.

The script uses Douyin's public mobile share page, records the public metadata
returned with that page, and downloads only samples that are explicitly listed
in the research registry. It does not read browser cookies or login state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from douyin_media_core import (  # noqa: E402
    MOBILE_MEDIA_HEADERS,
    ROUTER_DATA_RE,
    fetch_mobile_text,
    find_aweme_items,
    share_record_from_item,
    share_video_page_url,
)

FFMPEG = "/Users/wangchao/.local/bin/ffmpeg"
FFPROBE = "/Users/wangchao/.local/bin/ffprobe"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_public_record(video_id: str, attempts: int = 5) -> tuple[dict[str, Any], dict[str, Any]]:
    source_url = f"https://www.douyin.com/video/{video_id}"
    page_url = share_video_page_url(source_url)
    if not page_url:
        raise RuntimeError(f"cannot build public share page for {video_id}")
    last_error = ""
    for attempt in range(1, attempts + 1):
        try:
            match = ROUTER_DATA_RE.search(fetch_mobile_text(page_url))
            if not match:
                raise RuntimeError("public share page did not include router data")
            items = list(find_aweme_items(json.loads(match.group(1))))
            item = next((value for value in items if value.get("aweme_id") == video_id), None)
            if not item:
                raise RuntimeError("public share page did not include the requested video")
            return share_record_from_item(item, source_url, page_url), item
        except Exception as exc:  # network endpoint can be briefly rate limited
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt < attempts:
                time.sleep(attempt * 1.5)
    raise RuntimeError(f"metadata acquisition failed for {video_id}: {last_error}")


def probe(path: Path) -> dict[str, Any]:
    result = subprocess.run(
        [
            FFPROBE,
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=index,codec_type,width,height,r_frame_rate",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    streams = payload.get("streams") or []
    video = next((stream for stream in streams if stream.get("codec_type") == "video"), {})
    rate = str(video.get("r_frame_rate") or "0/1")
    numerator, denominator = (rate.split("/", 1) + ["1"])[:2]
    fps = float(numerator) / float(denominator or 1)
    return {
        "duration": round(float((payload.get("format") or {}).get("duration") or 0), 3),
        "width": int(video.get("width") or 0),
        "height": int(video.get("height") or 0),
        "fps": round(fps, 3),
        "has_audio": any(stream.get("codec_type") == "audio" for stream in streams),
    }


def download(urls: list[str], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    partial = output.with_suffix(".partial.mp4")
    for index, url in enumerate(urls, start=1):
        partial.unlink(missing_ok=True)
        command = [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-loglevel",
            "warning",
            "-headers",
            MOBILE_MEDIA_HEADERS,
            "-i",
            url,
            "-c",
            "copy",
            str(partial),
        ]
        result = subprocess.run(command, check=False)
        if result.returncode == 0 and partial.is_file() and partial.stat().st_size > 100_000:
            partial.replace(output)
            return
        print(f"  media URL {index}/{len(urls)} failed", file=sys.stderr)
    raise RuntimeError(f"all public media URLs failed for {output.name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="research/sample_registry.json")
    parser.add_argument("--sample", action="append", help="Acquire only these sample IDs")
    parser.add_argument("--metadata-only", action="store_true")
    args = parser.parse_args()

    registry_path = Path(args.registry).resolve()
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    wanted = set(args.sample or [])
    changed = False
    failures: list[str] = []

    for sample in registry.get("samples") or []:
        sample_id = str(sample.get("id") or "")
        if wanted and sample_id not in wanted:
            continue
        video_id = str(sample.get("video_id") or "")
        if not video_id or sample.get("source_locator") == "local user-provided video":
            continue
        print(f"{sample_id}: reading public metadata")
        try:
            record, item = load_public_record(video_id)
            stats = item.get("statistics") if isinstance(item.get("statistics"), dict) else {}
            author = item.get("author") if isinstance(item.get("author"), dict) else {}
            created = item.get("create_time")
            sample.update(
                {
                    "title": record.get("title"),
                    "author": author.get("nickname") or "not_observed",
                    "source_locator": f"https://www.douyin.com/video/{video_id}",
                    "captured_at": datetime.now(timezone.utc).date().isoformat(),
                    "published_at": (
                        datetime.fromtimestamp(float(created), timezone.utc).isoformat()
                        if created
                        else "not_observed"
                    ),
                    "visible_metrics": {
                        "likes": stats.get("digg_count"),
                        "comments": stats.get("comment_count"),
                        "favorites": stats.get("collect_count"),
                        "shares": stats.get("share_count"),
                        "views": "not_observed",
                    },
                    "platform_retention": "not_observed",
                    "metadata_source": "public mobile share page",
                }
            )
            output = Path(str(sample.get("local_path") or ""))
            if not output.is_absolute():
                output = (ROOT / output).resolve()
            sample["local_path"] = str(output)
            if not args.metadata_only and (not output.is_file() or output.stat().st_size < 100_000):
                print(f"{sample_id}: downloading playable body")
                download(list(record.get("video_urls") or []), output)
            if output.is_file() and output.stat().st_size > 100_000:
                sample.update(probe(output))
                sample["sha256"] = sha256(output)
                sample["playable_body_verified"] = True
            changed = True
        except Exception as exc:
            failures.append(f"{sample_id}: {type(exc).__name__}: {exc}")
            print(failures[-1], file=sys.stderr)

    if changed:
        registry_path.write_text(
            json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps({"updated": changed, "failures": failures}, ensure_ascii=False, indent=2))
    return 2 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
