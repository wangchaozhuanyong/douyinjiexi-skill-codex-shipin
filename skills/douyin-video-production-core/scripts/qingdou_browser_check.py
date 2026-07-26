#!/usr/bin/env python3
"""Prepare and record the visible Qingdou browser check.

This helper deliberately does not read Chrome cookies or local storage.  It
builds the exact public text that must be checked, emits a browser bookmarklet
for the already logged-in Qingdou tab, and records only visible check results.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = ["title", "caption", "topics"]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    return path.read_text(encoding="utf-8").strip()


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_lines(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines()).strip()


def publish_text(project: Path) -> dict[str, Any]:
    internal = project / "internal"
    title = read_text(internal / "publish_title.txt")
    caption = read_text(internal / "publish_copy.txt")
    topics = [line.strip() for line in read_text(internal / "publish_topics.txt").splitlines() if line.strip()]
    if not title and caption:
        title = caption.splitlines()[0].strip()
    if not caption:
        raise SystemExit(f"missing publish copy: {internal / 'publish_copy.txt'}")
    if not topics:
        topics = [item for item in caption.split() if item.startswith("#")]
    exact = normalize_lines("\n".join(part for part in [title, caption, *topics] if part))
    return {
        "title": title,
        "caption": caption,
        "topics": topics,
        "exact_text": exact,
        "sha256": hashlib.sha256(exact.encode("utf-8")).hexdigest(),
    }


def qingdou_bookmarklet(exact_text: str) -> str:
    payload = base64.b64encode(exact_text.encode("utf-8")).decode("ascii")
    js = f"""
(() => {{
  const payload = "{payload}";
  const text = new TextDecoder().decode(Uint8Array.from(atob(payload), c => c.charCodeAt(0)));
  const visible = el => !!(el && el.offsetParent !== null);
  const editors = Array.from(document.querySelectorAll('[contenteditable="true"], textarea, [role="textbox"]')).filter(visible);
  const editor = editors.find(el => el.isContentEditable) || editors[0];
  if (!editor) {{
    alert("Qingdou input not found or page not loaded");
    return;
  }}
  editor.focus();
  if ("value" in editor) {{
    editor.value = text;
  }} else {{
    editor.textContent = text;
  }}
  editor.dispatchEvent(new InputEvent("input", {{ bubbles: true, inputType: "insertText", data: text }}));
  editor.dispatchEvent(new Event("change", {{ bubbles: true }}));
  const actual = ("value" in editor ? editor.value : editor.innerText || editor.textContent || "").trim();
  if (actual !== text.trim()) {{
    alert("Qingdou exact text mismatch. Expected " + text.length + " chars, got " + actual.length);
    return;
  }}
  const nodes = Array.from(document.querySelectorAll('button, [role="button"], div, span')).filter(visible);
  const check = nodes.find(el => (el.innerText || el.textContent || "").trim() === "敏感词检测");
  if (!check) {{
    alert("Qingdou check button not found");
    return;
  }}
  window.__codex_qingdou_expected_text = text;
  window.__codex_qingdou_expected_length = text.length;
  check.click();
}})();
""".strip()
    return "javascript:" + js.replace("\n", " ")


def prepare(project: Path, set_clipboard: bool) -> dict[str, Any]:
    internal = project / "internal"
    data = publish_text(project)
    text_path = internal / "qingdou_check_text.txt"
    bookmarklet_path = internal / "qingdou_bookmarklet.txt"
    text_path.write_text(data["exact_text"] + "\n", encoding="utf-8")
    bookmarklet = qingdou_bookmarklet(data["exact_text"])
    bookmarklet_path.write_text(bookmarklet + "\n", encoding="utf-8")
    if set_clipboard:
        clipboard_text = bookmarklet.removeprefix("javascript:")
        subprocess.run(["pbcopy"], input=clipboard_text, text=True, check=True)
    report = {
        "status": "prepared",
        "prepared_at": now_iso(),
        "project": str(project),
        "tool": "qingdou_visible_browser_check",
        "checked_fields": REQUIRED_FIELDS,
        "final_title": data["title"],
        "final_caption": data["caption"],
        "final_topics": data["topics"],
        "exact_text_path": str(text_path),
        "bookmarklet_path": str(bookmarklet_path),
        "exact_text_sha256": data["sha256"],
        "browser_action_sequence": [
            "reuse current logged-in Chrome Qingdou tab",
            "type ASCII javascript: into the address bar, then paste the bookmarklet body from clipboard and press Enter",
            "if Chrome or input method blocks bookmarklet execution, paste qingdou_check_text.txt into the empty Qingdou input and verify the visible character count",
            "read the visible Qingdou result",
            "run record-passed only when the visible result says 未检查到敏感词",
            "run record-user-approved-topic only when Qingdou flags the required #我在抖音聊科技 topic term already approved by user",
        ],
        "safety": {
            "no_cookie_extraction": True,
            "no_password_storage": True,
            "no_sms_or_verification_storage": True,
            "direct_api_is_not_production_route": True,
        },
        "blocked_conditions": [
            "Qingdou page is blank or not loaded",
            "bookmarklet reports exact text mismatch",
            "visible result cannot be read",
            "SMS, real-name, or account-owner verification appears",
        ],
    }
    write_json(internal / "qingdou_browser_check_contract.json", report)
    return report


def approved_topic_override_items(terms: list[str], topics: list[str]) -> list[dict[str, Any]]:
    topics_text = " ".join(topics)
    allowed_topic = "#我在抖音聊科技"
    if allowed_topic not in topics_text:
        raise SystemExit("approved topic override requires final topics containing #我在抖音聊科技")
    cleaned_terms = [term.strip() for term in terms if term.strip()]
    if not cleaned_terms:
        raise SystemExit("approved topic override requires at least one --term")
    allowed_terms = {"抖音", "我在抖音聊科技", "#我在抖音聊科技"}
    invalid = [term for term in cleaned_terms if term not in allowed_terms]
    if invalid:
        raise SystemExit("approved topic override only allows required topic terms: " + ", ".join(invalid))
    if not all(term in allowed_topic for term in cleaned_terms):
        raise SystemExit("approved topic override terms must be inside #我在抖音聊科技")
    return [
        {
            "term": term,
            "source": "required_topic",
            "matched_text": allowed_topic,
            "user_preapproved": True,
        }
        for term in cleaned_terms
    ]


def write_qingdou_report(
    project: Path,
    status: str,
    visible_message: str,
    reason: str = "",
    terms: list[str] | None = None,
) -> dict[str, Any]:
    internal = project / "internal"
    data = publish_text(project)
    visible_message = visible_message.strip()
    items: list[Any] = []
    if status == "user_override_accepted":
        items = approved_topic_override_items(terms or [], data["topics"])
    final_status = "passed" if status in {"passed", "user_override_accepted"} else "blocked"
    report = {
        "status": status,
        "platform": "轻抖",
        "checked_platform": "斗音",
        "checked_fields": REQUIRED_FIELDS,
        "final_title": data["title"],
        "final_caption": data["caption"],
        "final_topics": data["topics"],
        "exact_text_sha256": data["sha256"],
        "checked_at": now_iso(),
        "tool": "qingdou_visible_browser_check",
        "final_check": {
            "status": final_status,
            "message": visible_message,
            "items": items,
            "visible_browser_result_required": True,
        },
        "evidence": {
            "source": "current_logged_in_chrome_qingdou_tab",
            "no_cookie_extraction": True,
            "reason": reason,
        },
    }
    if status == "passed" and "未检查到敏感词" not in visible_message:
        raise SystemExit("record-passed requires visible message containing: 未检查到敏感词")
    if status == "user_override_accepted":
        if "检查到敏感词" not in visible_message:
            raise SystemExit("record-user-approved-topic requires visible Qingdou sensitive-word result")
        report["final_check"]["user_override"] = {
            "accepted": True,
            "allowed_by_skill_rule": True,
            "scope": "required_official_platform_topic",
            "approved_topic": "#我在抖音聊科技",
            "approval_memory": "user explicitly required keeping #我在抖音聊科技 and not asking again",
        }
        report["evidence"]["reason"] = reason or "Qingdou flagged only the required user-approved official platform topic"
    if status not in {"passed", "user_override_accepted"} and not reason:
        raise SystemExit("record-blocked requires --reason")
    write_json(internal / "qingdou_keyword_check.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare or record a visible Qingdou browser check.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic> project path")
    parser.add_argument(
        "--mode",
        choices=["prepare", "record-passed", "record-blocked", "record-user-approved-topic"],
        default="prepare",
    )
    parser.add_argument("--visible-message", default="", help="Visible Qingdou result text.")
    parser.add_argument("--reason", default="", help="Blocker reason when mode=record-blocked.")
    parser.add_argument(
        "--term",
        action="append",
        default=[],
        help="Qingdou flagged term for record-user-approved-topic. May be repeated.",
    )
    parser.add_argument("--set-clipboard", action="store_true", help="Copy the prepared bookmarklet to the macOS clipboard.")
    args = parser.parse_args()

    project = Path(args.project)
    if args.mode == "prepare":
        report = prepare(project, args.set_clipboard)
    elif args.mode == "record-passed":
        report = write_qingdou_report(project, "passed", args.visible_message)
    elif args.mode == "record-user-approved-topic":
        report = write_qingdou_report(project, "user_override_accepted", args.visible_message, args.reason, args.term)
    else:
        message = args.visible_message or "Qingdou visible browser check blocked"
        report = write_qingdou_report(project, "blocked", message, args.reason)
    print(json.dumps({"status": report["status"], "project": str(project)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
