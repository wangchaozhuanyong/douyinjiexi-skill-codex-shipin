---
name: douyin-hyperframes-remake
description: 制作原创、合规、高质量的 AI 圈知识类抖音短视频。用于 AI 新闻、AI 工具、ChatGPT、Codex、Agent、自动化、AI 视频、AI 教程类选题研究、参考视频拆解、中文口播文案、分镜、真实证据素材、HyperFrames 成片、字幕同步、封面和发布前质量验收。用户发送抖音链接、本地参考视频、AI 话题或要求制作高质量抖音视频时使用。
---

# Douyin AI Video Director

V3 keeps the historical skill name `douyin-hyperframes-remake` for compatibility, but the job is now AI-circle knowledge video direction, not simple remake work.

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
5. `script_score.json`
6. `semantic_review.json`
7. `compliance_report.json`
8. `reference_analysis.json` when a reference is provided
9. `storyboard.json`
10. `storyboard_validation.json`
11. `asset_manifest.json`
12. `asset_validation.json`
13. `storyboard.audio_locked.json`
14. `metadata.json`
15. `draft.mp4`
16. `cover.png`
17. `publish_copy.txt`
18. `video_technical_qa.json`
19. `frame_review_report.json`
20. `visual_review.json`
21. `qa_report.json`

Only after `qa_report.json` passes may `outputs/<date-topic>/final/` contain:

- `final.mp4`
- `cover.png`
- `publish_copy.txt`
- `metadata.json`

## Core Workflow

Read `references/workflow_contract.md` first for the full gate contract.

## Input Mode Routing

Before topic research, decide the production mode:

- **Reference Mode**: If the user provides a Douyin link, share text, local video, image set, or says to imitate a reference, first run reference analysis. Imitate the reference's pacing, structure, information density, hook logic, caption rhythm, and visual progression, but do not copy exact wording, frames, voice, music, identity, or a highly similar full structure.
- **Self-Research Mode**: If the user only says to use this skill to make a video, or gives a broad AI/video request without a reference, do not reuse evergreen copy or Codex-only topics by default. First research current AI-circle hot topics and high-quality source material across the broader AI industry, then create topic candidates from that research.

Self-Research Mode must include recent, source-backed material before copywriting:

- Search current AI industry topics across OpenAI, Anthropic, Google, Meta, xAI, AI agents, AI video tools, coding agents, enterprise AI, AI safety/regulation, and creator workflows.
- Prefer official product/news pages, reputable technology/business media, launch notes, docs, demos, benchmarks, and real product screenshots or recordings.
- Save the chosen sources and the claim each source supports in `topic_candidates.json`.
- Do not choose a generic evergreen topic unless it clearly beats current topics on pain, novelty, save value, visual potential, and compliance safety.

1. Topic Research
   - Read `references/topic_selection_rules.md`.
   - Produce `topic_candidates.json` with at least 5 candidates.
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
   - Gate: first-three-second score >= 9.2, first-five-second score >= 9.0, script score >= 8.5, save value >= 8.5, proof score >= 8.5, compliance score >= 9.5, and empty talk ratio <= 0.18.

4. Semantic Review
   - Read `references/creative_rubric.md`.
   - Run `scripts/evaluate_copy_semantic.py --copy copy_package.md --copy-json copy_package.json --out semantic_review.json`.
   - Gate: semantic review must pass, composite score >= 8.5, and hard fail reasons must be empty.

5. Compliance Check
   - Read `references/douyin_compliance_rules.md`.
   - Run `scripts/check_public_copy.py --copy copy_package.md --out compliance_report.json`.
   - Gate: `error_count` must be 0. Warnings need documented acceptance.

6. Reference Analysis
   - If the user provides a reference, read `references/reference_video_rules.md`.
   - Run `scripts/analyze_reference.py --input "<url/share text/path>" --out reference_analysis.json`.
   - Gate: if `similarity_risk` is `high`, redesign angle before production.

7. Storyboard
   - Read `references/visual_sync_rules.md`.
   - Produce `storyboard.json` following `schemas/storyboard.schema.json`.
   - Run `scripts/validate_storyboard.py`.
   - Gate: at least 6 scenes, at least 2 visual changes in first 5 seconds, at least 50% evidence runtime for AI tool tutorials, and at least 2 motion layers per scene.

8. Assets
   - Read `references/ai_circle_content_rules.md`.
   - Produce `asset_manifest.json`.
   - Run `scripts/validate_assets.py --manifest outputs/<date-topic>/internal/asset_manifest.json --project outputs/<date-topic> --out outputs/<date-topic>/internal/asset_validation.json`.
   - Prefer real UI screenshots, real recordings, terminal/code/output proof, and official docs screenshots before AI-generated visuals.
   - Gate: AI-generated images must not fake product UI, official proof, reviews, data, chat records, or certification.

9. TTS And Duration Lock
   - Read `references/hyperframes_delivery.md`.
   - Generate one TTS file per scene.
   - Run `scripts/media_probe.py` for real audio durations.
   - Produce `storyboard.audio_locked.json`.
   - Gate: do not hand-guess scene durations.

10. HyperFrames Production
   - Build the HyperFrames project from the locked storyboard.
   - Produce `draft.mp4` and `metadata.json`.
   - Gate: voice, captions, and visuals must stay synchronized.

11. QA Gate
   - Run `scripts/video_technical_qa.py --video outputs/<date-topic>/internal/draft.mp4 --metadata outputs/<date-topic>/internal/metadata.json --out outputs/<date-topic>/internal/video_technical_qa.json`.
   - Run `scripts/frame_review.py --video outputs/<date-topic>/internal/draft.mp4 --out-dir outputs/<date-topic>/internal/frame_review --report outputs/<date-topic>/internal/frame_review_report.json`.
   - Run `scripts/visual_aesthetic_review.py --storyboard outputs/<date-topic>/internal/storyboard.json --frame-review outputs/<date-topic>/internal/frame_review_report.json --metadata outputs/<date-topic>/internal/metadata.json --out outputs/<date-topic>/internal/visual_review.json`.
   - Run `scripts/qa_gate.py --project outputs/<date-topic> --out outputs/<date-topic>/internal/qa_report.json`.
   - Gate: `qa_report.status` must be `passed`, `blocking_issues` must be empty, and all `hard_gates` must be true.
   - Only then run `scripts/promote_final.py --project outputs/<date-topic>` to copy approved files into `final/`.

12. Golden Regression
   - For skill changes, run `scripts/check_golden_project.py` to verify the bundled golden project still reaches high-quality QA.

## Required References

- `references/workflow_contract.md`
- `references/video_quality_contract.md`
- `references/content_formats.md`
- `references/topic_selection_rules.md`
- `references/ai_circle_content_rules.md`
- `references/creative_rubric.md`
- `references/script_quality_rules.md`
- `references/douyin_compliance_rules.md`
- `references/reference_video_rules.md`
- `references/visual_sync_rules.md`
- `references/visual_aesthetic_rules.md`
- `references/hyperframes_delivery.md`
- `references/hyperframes_components.md`
- `references/post_publish_review.md`
- `references/learning_bank.md`

## Required Commands

Before committing changes to this skill:

```bash
python scripts/doctor.py
python -m py_compile scripts/*.py
pytest -q
```

If any command fails, fix the cause before publishing the skill.
