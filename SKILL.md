---
name: douyin-hyperframes-remake
description: 制作原创、合规、最高级 AI 圈知识类抖音短视频，并在用户说做视频、出片、成片、生成视频、装修视频、美女视频、AI知识视频、参考视频学习、视频质量太低、要最高级/高级版/发布级时先做视频风格路由。用于 AI 新闻、AI 工具、ChatGPT、Codex、Agent、自动化、AI 视频、AI 教程类选题研究、参考视频拆解、中文口播文案、分镜、真实证据素材、Remotion/ImageGen/HyperFrames/FFmpeg 联动成片、可选 OpenMontage/Video-Use/Manim 适配、字幕同步、封面和发布前质量验收。默认只接受 publish-ready highest-grade 工作流；低配草稿、模板轮播、单图配音、普通 Ken Burns 缩放或未过 QA 的视频不得作为 final 交付。
---

# Douyin AI Video Director

V3 keeps the historical skill name `douyin-hyperframes-remake` for compatibility, but the job is now AI-circle knowledge video direction, not simple remake work.

## Role

Act as a short-video director for Chinese AI knowledge content. Produce original, compliant, beginner-friendly Douyin videos with useful topic selection, strong first-five-second hooks, clear spoken copy, real evidence assets, synchronized captions, premium visual design, premium HyperFrames motion, restrained sound design, crisp export quality, and strict QA.

## Highest-Grade Default

Every video request defaults to highest-grade publish-ready production unless the user explicitly asks for research only, planning only, quick draft, or smoke test. Before scripts, assets, TTS, HyperFrames, or render work, read `references/video_style_router.md` and `references/shared_video_quality_core.md`; route renovation to `$full-house-custom-ad`, beauty choice videos to `$beauty-gpt-image-video`, and AI/tool videos to this skill. If provider access,素材质量, voice quality, HyperFrames, ffprobe, safe-zone review, or QA gates cannot meet the highest-grade bar, stop with a blocker or deliver a labeled draft only.

## AI Knowledge Aspect Ratio

All AI knowledge videos owned by this skill must be 16:9 horizontal by default and by validation: `1920x1080`, `fps: 30`. This includes AI news, AI tools, ChatGPT, Gemini, OpenAI, Codex, Agent, automation, AI coding, AI workflow, plugin, and Skill tutorials. Do not switch AI knowledge videos to 9:16 just because the destination is Douyin. For Douyin publishing, deliver the 16:9 master and let the platform/player handle display; do not crop proof UI into a vertical frame.

## AI Background-First Rule

Before storyboard, assets, TTS, HyperFrames, render, or upload for any AI knowledge video, create `internal/background_prompt_pack.md` with descriptive background language, generate text-free `1920x1080` background plate(s), and register them in `asset_manifest.json` as `asset_role=background_plate`, `type=generated_visual`, `asset_source_type=generated`, and `is_evidence=false`. Generic gradients, neon grids, pseudo UI, background text, or linework behind captions are blocked.

## HyperFrames Premium Motion Language Rule

Before storyboard or HyperFrames composition work, define premium motion as executable animation language, not adjectives. Use restrained terms such as `smooth`, `dramatic`, `subtle`, `cinematic`, `premium`, `clean`, `restrained`, and `snappy`; do not use vague requests such as `高级一点`, `炫酷`, `震撼`, `crazy`, `explosive`, `flashy`, `excessive`, or `chaotic`. Every scene's storyboard `motion` must document purpose, entrance, stagger, keyword motion, camera motion, layering, transition, caption motion, glow, audio-reactive behavior, and negative motion constraints. Gate: no structured motion craft means no HyperFrames HTML, preview, render, or final delivery.

## Continuous Narration Bed Rule
HyperFrames scene transitions are visual-only. The spoken narration must continue through every transition without restart, mute, fade-out, or a perceptible gap. Prefer one root-level continuous narration audio file that spans the full video, built after scene TTS duration lock. If per-scene audio clips are used during iteration, the final storyboard/audio lock must prove they play back-to-back with `max_audio_gap_ms <= 120`, stay outside timed visual scene containers, and are never controlled by scene entrance/transition/exit animations. Gate: no documented continuous narration strategy means no HyperFrames composition, render, final delivery, or publishing.

## Use When

- The user asks for an AI, ChatGPT, Codex, Agent, automation, AI video, or AI tool Douyin video.
- The user gives a Douyin link, share text, local reference video, or AI topic and wants a high-quality original video.
- The user asks for topic research, copywriting, storyboard, HyperFrames production, QA, cover, or publish-ready package for AI-circle knowledge content.

## Do Not

- Do not copy reference frames, subtitles, voice, music, exact wording, person identity, or a highly similar full structure.
- Do not skip topic research and jump straight into video generation.
- Do not generate images, TTS, HyperFrames scenes, or video before compliance passes.
- Do not use single-image narration, low-quality image carousel, ordinary Ken Burns zoom, loop pulse, black/white frames, no-audio output, or audio/visual mismatch.
- Do not use page shaking, random camera drift, or decorative transitions to hide weak content. Add more proof scenes, richer image/card content, and better design instead.
- Do not ask HyperFrames for abstract "better", "cooler", or "more shocking" animation. Translate premium feel into easing, timing, stagger, layers, transitions, captions, glow, camera movement, and subtle audio response.
- Do not let scene transitions restart, mute, fade, or gap narration. Do not put narration audio inside a scene container that transitions out; keep narration on a separate root audio track or prove continuous scene-audio scheduling.
- Do not render AI knowledge, AI tool, Codex, Agent, ChatGPT, Gemini, plugin, or Skill tutorial videos as 9:16. These videos must use a 16:9 proof-first canvas so screenshots, code, docs, and workflow diagrams stay readable.
- Do not speed up Chinese narration to fit dense copy. Use normal speed only and split/shorten scenes instead.
- Do not use absolute claims, guaranteed results, fake authority,誘導互动, station-out diversion, contact details, QR codes, fake reviews, fake UI, or unsourced factual claims.
- Do not claim Remotion, HyperFrames, ImageGen, HeyGen, or a Codex Skill was installed, executed, or used unless there is real UI, local file, terminal, render, or documented evidence.
- Do not use third-party paid features, paid APIs, paid subscriptions, paid stock assets, paid cloud renderers, paid AI generation providers, or new credit-consuming services. Codex features already available inside the user's paid Codex session are allowed and do not count as blocked paid features. The production stack must stay Codex-included, free-first, local, or open-source whenever possible; if an external tool requires payment, mark it blocked instead of using it.
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
9. `background_prompt_pack.md`
10. `storyboard.json`
11. `storyboard_validation.json`
12. `asset_manifest.json`
13. `asset_validation.json`
14. `storyboard.audio_locked.json`
15. `metadata.json`
16. `draft.mp4`
17. `cover.png`
18. `publish_copy.txt`
19. `video_technical_qa.json`
20. `frame_review_report.json`
21. `visual_review.json`
22. `qa_report.json`
23. `provider_usage_audit.json`

Only after `qa_report.json` and `provider_usage_audit.json` pass may `outputs/<date-topic>/final/` contain:

- `final.mp4`
- `cover.png`
- `publish_copy.txt`
- `metadata.json`

## Core Workflow

Read `references/workflow_contract.md` first for the full gate contract.

For any publish-ready, high-quality, reference-level, premium, or polished video, also read `references/premium_video_quality_playbook.md` and `references/ai_generated_asset_prompt_system.md` before storyboard or asset work.

For any HyperFrames-rendered AI video, also read `references/premium_ai_video_source_to_hyperframes_rule.md` before storyboard work and apply the `Premium HyperFrames Animation Language` section. The storyboard must pass structured motion validation before HyperFrames composition.

For any publish-ready video after the open-source learning upgrade, also read `references/free_first_open_source_stack.md`, `references/runtime_decision_matrix.md`, and `references/timeline_contract.md` before storyboard or asset planning. If the user mentions the six-tool Codex video stack, classify HyperFrames, FFmpeg, OpenMontage, Remotion, Video-Use, and Manim through the runtime matrix before claiming a tool is installed, executed, or used.

For multi-style requests, shared-growth requests, or ambiguous video requests that could be AI, renovation, or beauty, read `references/video_style_router.md` and `references/shared_video_quality_core.md` before deciding the owning skill. Keep this skill focused on AI-circle knowledge videos.

For Codex Skill, Agent, plugin, Remotion, HyperFrames, or ImageGen tutorial videos, also read `references/codex_skill_tutorial_video.md`, `references/beginner_visual_sync_rules.md`, `references/codex_three_skill_video_playbook.md`, and `references/codex_plugin_integration.md` before scripting or storyboard work.

## Input Mode Routing

Before topic research, decide the production mode:

- **Style Router Mode**: If the user asks for three video styles, shared skill growth, renovation videos, beauty choice videos, or a non-AI video, route by `references/video_style_router.md` before using this AI workflow. Do not force renovation or beauty work through the AI knowledge pipeline.
- **Reference Mode**: If the user provides a Douyin link, share text, local video, image set, or says to imitate a reference, first run reference analysis. Imitate the reference's pacing, structure, information density, hook logic, caption rhythm, and visual progression, but do not copy exact wording, frames, voice, music, identity, or a highly similar full structure.
- **Three-Skill Tutorial Mode**: If the reference or topic is about multiple Codex Skills/plugins, Remotion, HyperFrames, ImageGen, or HeyGen, apply `references/codex_three_skill_video_playbook.md` and `references/codex_plugin_integration.md`. The storyboard must document `production_stack`; plugin videos must also document `codex_plugin_plan`; every named tool must have an entry/source proof, operation proof, output proof, and viewer-value reason.
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

6. Background Art Direction
   - Read `references/ai_generated_asset_prompt_system.md` and produce `internal/background_prompt_pack.md` with 3-5 text-free background descriptions before storyboard, assets, TTS, or HyperFrames work.
   - Generate/select `1920x1080` background plate(s) and document them later in `asset_manifest.json` as generated support, never proof.
   - Gate: no background prompt pack means no storyboard or video production.

7. Reference Analysis
   - If the user provides a reference, read `references/reference_video_rules.md`.
   - Run `scripts/analyze_reference.py --input "<url/share text/path>" --out reference_analysis.json`.
   - Gate: if `similarity_risk` is `high`, redesign angle before production.

8. Storyboard
   - Read `references/visual_sync_rules.md`.
   - Include top-level `quality_spec` and scene-level `visual.design_layers` / `visual.quality_checks` for publish-ready work.
   - Include `target.provider_policy`, `quality_spec.provider_policy`, `quality_spec.runtime_choice`, `quality_spec.caption_template_plan`, and `quality_spec.timeline_contract_ref`.
   - Every scene must include `visual.asset_source_type` and `visual.caption_template`.
   - For Codex Skill/plugin tutorials, include top-level `production_stack`, `codex_plugin_plan` when plugins are named, and `visual.proof_chain` for every scene that names a primary tool.
   - Produce `storyboard.json` following `schemas/storyboard.schema.json`.
   - Run `scripts/validate_storyboard.py`.
   - Gate: target format must be `1920x1080` for AI knowledge videos, at least 6 scenes, at least 2 visual changes in first 5 seconds, at least 50% evidence runtime for AI tool tutorials, at least 2 motion layers per scene, safe margins documented, and normal TTS speed metadata (`tts_speed` 0.95-1.03).
   - Gate: every scene must include structured premium motion craft: `purpose`, `entrance`, `stagger`, `keyword_motion`, `camera_motion`, `layering`, `transition`, `caption_motion`, `glow`, `audio_reactive`, and `negative_motion`.

9. Assets
   - Read `references/ai_circle_content_rules.md`.
   - Read `references/free_first_open_source_stack.md`.
   - Read `references/ai_generated_asset_prompt_system.md` before generating any AI-made asset.
   - Produce `internal/ai_asset_prompt_pack.md` or equivalent production notes whenever generated/support visuals are used.
   - Produce `asset_manifest.json`.
   - Run `scripts/validate_assets.py --manifest outputs/<date-topic>/internal/asset_manifest.json --project outputs/<date-topic> --out outputs/<date-topic>/internal/asset_validation.json`.
   - Prefer real UI screenshots, real recordings, terminal/code/output proof, and official docs screenshots before AI-generated visuals.
   - Every asset must document `asset_source_type` and provider/source role.
   - Gate: AI-generated images must not fake product UI, official proof, reviews, data, chat records, or certification; every AI video must include a generated text-free background plate registered as `asset_role=background_plate`.

10. TTS And Duration Lock
   - Read `references/hyperframes_delivery.md`.
   - Generate one TTS file per scene.
   - Build or declare a continuous root narration bed from the locked scene TTS files before HyperFrames render.
   - Use normal Mandarin speed only: default `tts_speed` 1.0, acceptable range 0.95-1.03. If audio is too long, shorten the line or add visual beats; never use 1.1x/1.12x/1.2x speed-up.
   - Run `scripts/media_probe.py` for real audio durations.
   - Produce `storyboard.audio_locked.json`.
   - Gate: do not hand-guess scene durations, do not render with accelerated narration, and do not render unless transition audio continuity is documented with `max_audio_gap_ms <= 120`.

11. HyperFrames Production
   - Build the HyperFrames project from the locked storyboard.
   - Apply `references/runtime_decision_matrix.md`: Remotion for component clips/data visuals, HyperFrames for final timeline, FFmpeg/MoviePy only for mechanical media operations.
   - Use Remotion only when a real Remotion project/component/render is part of the planned evidence or production stack. If used, follow the installed `remotion-best-practices` skill and record the produced frames/clips as evidence assets before HyperFrames final assembly.
   - Put narration in a root `<audio>` track with its own `data-track-index`; visual scene clips and transitions must not control voice playback. Put BGM/SFX on separate lower-volume tracks.
   - Use `--quality high` for publish-ready renders. If the output is screenshot-heavy, soft, or low-bitrate, remux or transcode to a higher-quality H.264 pass.
   - Produce `draft.mp4` and `metadata.json` with `quality_spec`.
   - Gate: voice must stay continuous through transitions, and captions/visuals must stay synchronized to that continuous narration.

12. QA Gate
   - Run `scripts/video_technical_qa.py --video outputs/<date-topic>/internal/draft.mp4 --metadata outputs/<date-topic>/internal/metadata.json --out outputs/<date-topic>/internal/video_technical_qa.json`.
   - Run `scripts/frame_review.py --video outputs/<date-topic>/internal/draft.mp4 --out-dir outputs/<date-topic>/internal/frame_review --report outputs/<date-topic>/internal/frame_review_report.json`.
   - Run `scripts/visual_aesthetic_review.py --storyboard outputs/<date-topic>/internal/storyboard.json --frame-review outputs/<date-topic>/internal/frame_review_report.json --metadata outputs/<date-topic>/internal/metadata.json --out outputs/<date-topic>/internal/visual_review.json`.
   - Run `scripts/qa_gate.py --project outputs/<date-topic> --out outputs/<date-topic>/internal/qa_report.json`.
   - Gate: `qa_report.status` must be `passed`, `blocking_issues` must be empty, and all `hard_gates` must be true.
   - Run `scripts/audit_provider_usage.py --project outputs/<date-topic> --phase final --out outputs/<date-topic>/internal/provider_usage_audit.json --md-out outputs/<date-topic>/internal/provider_usage_audit.md`.
   - Gate: `provider_usage_audit.status` must be `passed`; HyperFrames, FFmpeg, and visual review must have evidence; optional providers must be `used`, `blocked`, or `not_applicable` with reasons.
   - Only then run `scripts/promote_final.py --project outputs/<date-topic>` to copy approved files into `final/`.

13. Golden Regression
   - For skill changes, run `scripts/check_golden_project.py` to verify the bundled golden project still reaches high-quality QA.

## Required References

Always use the relevant files under `references/`, especially `workflow_contract.md`, `video_quality_contract.md`, `premium_video_quality_playbook.md`, `ai_generated_asset_prompt_system.md`, `video_style_router.md`, `topic_selection_rules.md`, `script_quality_rules.md`, `douyin_compliance_rules.md`, `visual_sync_rules.md`, `hyperframes_delivery.md`, `hyperframes_components.md`, `codex_three_skill_video_playbook.md`, `codex_plugin_integration.md`, `post_publish_review.md`, and `learning_bank.md`.

## Required Commands

Before committing changes to this skill: `python3 scripts/doctor.py`, `python3 -m py_compile scripts/*.py`, and `python3 -m pytest -q`.

If any command fails, fix the cause before publishing the skill.
