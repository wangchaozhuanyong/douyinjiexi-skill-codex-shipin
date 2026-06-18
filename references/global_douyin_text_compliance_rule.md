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
- Before upload/publish: run Qingdou (`轻抖`) or the current approved Douyin checker on the exact title, caption, and topics that will be typed into the platform.
- If any checker flags a term: record it with `scripts/update_forbidden_terms.py`, rewrite naturally, and rerun the checks.

## Minimum Evidence

Every publish-ready video package should include:

- a manifest or source file listing all designed text, for example `render_text_manifest.json`, `copy_package.json`, `publish_manifest.json`, or `compliance-text.txt`
- a local text compliance report covering designed text and publish-entry text
- `qingdou_keyword_check.json` for the exact final title, caption, and topics before publishing
- `forbidden_terms_update_report.json` when any term was detected or when the report proves no new terms were found

## Promotion Boundary

Do not call a video publish-ready and do not publish it if:

- designed video text has not been checked
- publish title/caption/topics have not been checked together
- any detected term has not been recorded into the learning bank
- rewritten text has not been rechecked
- Qingdou is blocked and the blocker is not recorded truthfully
