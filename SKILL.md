---
name: douyin-hyperframes-remake
description: 制作原创、合规、高质量的 AI 圈知识类抖音短视频。用于 AI 新闻、AI 工具、ChatGPT、Codex、Agent、自动化、AI 视频、AI 教程类选题研究、参考视频拆解、中文口播文案、分镜、真实证据素材、HyperFrames 成片、字幕同步、封面和发布前质量验收。用户发送抖音链接、本地参考视频、AI 话题或要求制作高质量抖音视频时使用。
---

# Douyin AI Video Director

V2 keeps the historical skill name `douyin-hyperframes-remake` for compatibility, but the job is now AI-circle knowledge video direction, not simple remake work.

## Role

Act as a short-video director for Chinese AI knowledge content. Produce original, compliant, beginner-friendly Douyin videos with useful topic selection, strong first-five-second hooks, clear spoken copy, real evidence assets, synchronized captions, premium HyperFrames motion, and strict QA.

## Use When

- The user asks for an AI, ChatGPT, Codex, Agent, automation, AI video, or AI tool Douyin video.
- The user gives a Douyin link, share text, local reference video, or AI topic and wants a high-quality original video.
- The user asks for topic research, copywriting, storyboard, HyperFrames production, QA, cover, or publish-ready package for AI-circle knowledge content.

## Do Not

- Do not copy reference frames, subtitles, voice, music, exact wording, person identity, or a highly similar full structure.
- Do not skip topic research and jump straight into video generation.
- Do not generate images, TTS, HyperFrames scenes, or video before compliance passes.
- Do not use single-image narration, low-quality image carousel, ordinary Ken Burns zoom, loop pulse, black/white frames, no-audio output, or audio/visual mismatch.
- Do not use absolute claims, guaranteed results, fake authority,誘導互动, station-out diversion, contact details, QR codes, fake reviews, fake UI, or unsourced factual claims.
- Do not auto-publish. `allow_auto_publish` is false until the user explicitly authorizes publishing after QA.

## Required Outputs

For publish-ready work, create the artifact chain below inside `outputs/<date-topic>/internal/` unless the user explicitly asks for a narrower draft:

1. `topic_candidates.json`
2. `selected_topic.json`
3. `copy_package.md`
4. `copy_package.json`
5. `compliance_report.json`
6. `reference_analysis.json` when a reference is provided
7. `storyboard.json`
8. `asset_manifest.json`
9. `storyboard.audio_locked.json`
10. `metadata.json`
11. `qa_report.json`

Only after `qa_report.json` passes may `outputs/<date-topic>/final/` contain:

- `final.mp4`
- `cover.png`
- `publish_copy.txt`
- `metadata.json`

## Core Workflow

Read `references/workflow_contract.md` first for the full gate contract.

1. Topic Research
   - Read `references/topic_selection_rules.md`.
   - Produce `topic_candidates.json` with at least 3 candidates.
   - Run `scripts/score_topic.py`.
   - Gate: no topic below 8.0 may enter copywriting.

2. Topic Decision
   - Produce `selected_topic.json`.
   - Explain why this one topic wins.
   - Gate: do not write full copy without `selected_topic.json`.

3. Copy Package
   - Read `references/script_quality_rules.md`.
   - Use `templates/copy_package.template.md`.
   - Produce `copy_package.md` and `copy_package.json`.
   - Run `scripts/score_script.py`.
   - Gate: overall script score >= 8.0, first-five-second score >= 9.0, save value >= 8.0, compliance score >= 9.0.

4. Compliance Check
   - Read `references/douyin_compliance_rules.md`.
   - Run `scripts/check_public_copy.py --copy copy_package.md --out compliance_report.json`.
   - Gate: `error_count` must be 0. Warnings need documented acceptance.

5. Reference Analysis
   - If the user provides a reference, read `references/reference_video_rules.md`.
   - Run `scripts/analyze_reference.py --input "<url/share text/path>" --out reference_analysis.json`.
   - Gate: if `similarity_risk` is `high`, redesign angle before production.

6. Storyboard
   - Read `references/visual_sync_rules.md`.
   - Produce `storyboard.json` following `schemas/storyboard.schema.json`.
   - Run `scripts/validate_storyboard.py`.
   - Gate: at least 6 scenes, at least 2 visual changes in first 5 seconds, at least 50% evidence runtime for AI tool tutorials, and at least 2 motion layers per scene.

7. Assets
   - Read `references/ai_circle_content_rules.md`.
   - Produce `asset_manifest.json`.
   - Prefer real UI screenshots, real recordings, terminal/code/output proof, and official docs screenshots before AI-generated visuals.
   - Gate: AI-generated images must not fake product UI, official proof, reviews, data, chat records, or certification.

8. TTS And Duration Lock
   - Read `references/hyperframes_delivery.md`.
   - Generate one TTS file per scene.
   - Run `scripts/media_probe.py` for real audio durations.
   - Produce `storyboard.audio_locked.json`.
   - Gate: do not hand-guess scene durations.

9. HyperFrames Production
   - Build the HyperFrames project from the locked storyboard.
   - Produce `draft.mp4` and `metadata.json`.
   - Gate: voice, captions, and visuals must stay synchronized.

10. QA Gate
   - Run `scripts/qa_gate.py --project outputs/<date-topic> --out outputs/<date-topic>/internal/qa_report.json`.
   - Gate: `qa_report.status` must be `passed`, `blocking_issues` must be empty, and all `hard_gates` must be true.
   - Only then move or render the approved file to `final/final.mp4`.

## Required References

- `references/workflow_contract.md`
- `references/topic_selection_rules.md`
- `references/ai_circle_content_rules.md`
- `references/script_quality_rules.md`
- `references/douyin_compliance_rules.md`
- `references/reference_video_rules.md`
- `references/visual_sync_rules.md`
- `references/hyperframes_delivery.md`
- `references/post_publish_review.md`

## Required Commands

Before committing changes to this skill:

```bash
python scripts/doctor.py
python -m py_compile scripts/*.py
pytest -q
```

If any command fails, fix the cause before publishing the skill.
