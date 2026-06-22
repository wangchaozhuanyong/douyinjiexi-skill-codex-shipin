# Global Douyin Text Compliance Rule

This rule applies to every video family the user asks Codex to produce or publish: AI/tool videos, renovation/full-house custom videos, beauty portrait choice videos, and any future Douyin-oriented video type.

## Hard Rule

Any designed text that may appear in a video or be entered during publishing must pass Douyin risk-word checking.

Do not limit checking to the publish caption. The check must cover both:

1. **Designed video text**:
   - on-screen title
   - subtitles/captions
   - cover text
   - poster/card text
   - badges, labels, stickers, CTA, corner marks, choice numbers with text, and any text baked into generated images or overlays
2. **Publish-entry text**:
   - upload title
   - publish caption/body
   - hashtags/topics
   - pinned comment or prepared comment text when used

## Required Timing

- Before drafting any text: read `references/forbidden_terms_learning_bank.md` and active records in `references/forbidden_terms_learning_bank.jsonl`.
- Before render/final QA: run local compliance on all designed video text and save a report such as `internal/on_screen_text_compliance_report.json` or `internal/on_screen_and_publish_text_compliance_report.json`.
- Before building a publish contract: include `internal/publish_cover_text.txt` and `internal/publish_copy.txt` in `internal/on_screen_and_publish_text_compliance_report.json`.
- Before upload/publish: run Qingdou (`轻抖`) or the current approved Douyin checker on the exact title, caption, and topics that will be typed into the platform.
- Qingdou browser verification: the user has granted standing authorization for routine publish-chain browser actions, including text entry, paste/replace, clicking the check button, reading the visible result, and ordinary slider or image security verification when the current environment permits agent handling. Execute these routine steps directly; do not ask the user to paste copy, click the check button, or complete normal Qingdou checks manually. Reuse the user's current logged-in Chrome tab/session, and close any extra tab/window opened for the task after completion. Current-environment browser automation may be used for page input and visible-result reading, but do not bypass verification, guess codes, or save credentials/cookies/SMS codes/verification data. Still stop for SMS codes, phone-only login recovery, real-name/account-owner verification, verification that clearly must be completed by the user, or any active browser/tool safety rule requiring fresh action-time confirmation.
- If any checker flags a term: record it with `scripts/update_forbidden_terms.py`, rewrite naturally, and rerun the checks.
- Narrow manual override: when Qingdou only flags a user-required official/platform campaign topic and the user explicitly says to keep that exact topic after seeing the failed result, record the failed term and user approval in `qingdou_keyword_check.json` with `status: "user_override_accepted"`. This permits upload/publish continuation for that topic only; it is not a Qingdou pass, and title, caption body, cover, subtitles, and on-screen text still need rewritten clean results.
- Standing topic override: the exact hashtag `#我在抖音聊科技` has standing user approval from 2026-06-21. If Qingdou only flags `抖音` inside this exact hashtag, record `status: "user_override_accepted"` and continue without asking again. Do not label it as `passed`, and do not reuse the override for any other hit or any non-topic field.

## Minimum Evidence

Every publish-ready video package should include:

- a manifest or source file listing all designed text, for example `render_text_manifest.json`, `copy_package.json`, `publish_manifest.json`, or `compliance-text.txt`
- a local text compliance report covering designed text and publish-entry text
- `publish_cover_report.json` plus `publish_cover_text.txt` when a cover is prepared
- `qingdou_keyword_check.json` for the exact final title, caption, and topics before publishing
- `publish_contract.json` with `gate.status="passed"` before upload, publish, or `final/` promotion
- `forbidden_terms_update_report.json` when any term was detected or when the report proves no new terms were found

## Promotion Boundary

Do not call a video publish-ready and do not publish it if:

- designed video text has not been checked
- publish title/caption/topics have not been checked together
- any detected term has not been recorded into the learning bank
- rewritten text has not been rechecked
- Qingdou is blocked and the blocker is not recorded truthfully
- Qingdou failed outside the narrow user-approved official/platform topic override
