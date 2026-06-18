# Forbidden Terms Learning Bank

This file defines the operating rule for learned Douyin risk terms. The machine-readable ledger lives beside it at `references/forbidden_terms_learning_bank.jsonl`.

## Hard Rule

Before writing any public-facing Douyin copy, cover text, subtitle text, on-screen text, title, caption, or hashtag/topic list, read this file and the active records in `references/forbidden_terms_learning_bank.jsonl`.

Avoid active learned terms before drafting. Do not wait until the upload step to discover repeated forbidden words.

## When To Record

Record every term or phrase detected by any of these checks:

- local `scripts/check_public_copy.py`
- Qingdou (`轻抖`) forbidden/sensitive word check
- Douyin Creator Center or upload-page warning
- platform rejection, replacement suggestion, or moderation hint
- manual review that identifies a repeat risky phrase

This applies to all public text surfaces:

- video on-screen text
- subtitles/captions
- cover text
- title
- publish caption
- hashtags/topics
- comment-pinned copy if prepared

## Required Record Fields

Each active record should include:

- `term`: exact detected word or phrase
- `level`: `error` or `warning`
- `category`: why it is risky
- `source_platform`: local checker, Qingdou, Douyin, or manual review
- `source_report`: report file or evidence path
- `context`: nearby text or field where it appeared
- `suggestion`: safer wording or rewrite rule
- `first_seen_at`: ISO timestamp
- `status`: usually `active`

## Update Command

After a failed or warning-producing check, append new terms before rewriting:

```bash
python3 scripts/update_forbidden_terms.py \
  --report outputs/demo/internal/compliance_report.json \
  --bank references/forbidden_terms_learning_bank.jsonl \
  --out outputs/demo/internal/forbidden_terms_update_report.json
```

Multiple reports can be supplied:

```bash
python3 scripts/update_forbidden_terms.py \
  --report outputs/demo/internal/on_screen_and_publish_text_compliance_report.json \
  --report outputs/demo/internal/qingdou_keyword_check.json \
  --out outputs/demo/internal/forbidden_terms_update_report.json
```

## Current Status

No learned platform-detected forbidden term has been added yet from the latest corrected Skill video because its local on-screen and publish-copy check passed with `0 errors / 0 warnings`. Future detections must be appended to the JSONL ledger immediately.
