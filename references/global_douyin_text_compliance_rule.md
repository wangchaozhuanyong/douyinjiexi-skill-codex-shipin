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

## No External-Diversion Copy For Skill Videos

For Skill/tool/plugin recommendation videos, explain the workflow without sending viewers to a link or contact path. Public text must not contain or imply:

- `网址`, `链接`, `URL`, raw `http://` or `https://`
- `复制链接`, `打开网站`, `打开某站`, `访问官网`, `进入官网`
- `扫码`, `二维码`, `私信`, `加群`, `加我`, `联系方式`
- `领取`, `下载`, or similar claim/download prompts tied to off-platform action

Use safer Skill phrasing instead:

- `输入页面内容，提炼重点，生成短视频结构。`
- `输入主题和素材，生成动态背景短视频。`
- `检查标题、封面和文案里的风险表达。`

Internal evidence fields may still store source URLs, local paths, or proof notes. The restriction applies to on-screen text, subtitles, cover text, title, caption, topics, and prepared comments.

## Required Timing

- Before drafting any text: read `references/forbidden_terms_learning_bank.md` and active records in `references/forbidden_terms_learning_bank.jsonl`.
- Before render/final QA: run local compliance on all designed video text and save a report such as `internal/on_screen_text_compliance_report.json` or `internal/on_screen_and_publish_text_compliance_report.json`.
- Before building a publish contract: include `internal/publish_cover_text.txt` and `internal/publish_copy.txt` in `internal/on_screen_and_publish_text_compliance_report.json`.
- Before upload/publish: run Qingdou (`轻抖`) or the current approved Douyin checker on the exact title, caption, and topics that will be typed into the platform.
- Qingdou browser verification: the user has granted standing authorization for routine publish-chain browser actions, including text entry, paste/replace, clicking the check button, reading the visible result, and ordinary slider or image security verification when the current environment permits agent handling. Execute these routine steps directly; do not ask the user to paste copy, click the check button, or complete normal Qingdou checks manually. Reuse the user's current logged-in Chrome tab/session, and close any extra tab/window opened for the task after completion. Current-environment browser automation may be used for page input and visible-result reading, but do not bypass verification, guess codes, or save credentials/cookies/SMS codes/verification data. Default to `scripts/qingdou_browser_check.py --project <project> --mode prepare --set-clipboard`; the generated bookmarklet works only inside the visible Qingdou page, clears the rich-text editor, inserts the exact publish text, verifies equality, and clicks the check button. Chrome may strip a pasted `javascript:` prefix; type that ASCII prefix manually or paste `qingdou_check_text.txt` into the empty Qingdou input and verify the visible character count before clicking the page button. Record `passed` only after the visible page result says `未检查到敏感词`; if only `抖音` inside fixed `#我在抖音聊科技` is flagged, record `record-user-approved-topic --term 抖音`; otherwise record a blocked result with the page state. Still stop for SMS codes, phone-only login recovery, real-name/account-owner verification, verification that clearly must be completed by the user, or any active browser/tool safety rule requiring fresh action-time confirmation.
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
