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

## Multi-Plugin Director Default

Do not treat HyperFrames as the only plugin. For AI tool, Codex, Agent, plugin, open-source, model, dataset, or source-backed tutorial videos, act as a multi-plugin director before final assembly. Read `references/codex_plugin_integration.md` before source gathering or storyboard work, then create `storyboard.codex_plugin_plan` documenting which Codex plugins are available, used, optional, blocked, or approval-required.

Default role split: Browser captures real UI/docs/product proof; GitHub inspects repos/issues/source evidence when relevant; Hugging Face inspects public models, datasets, papers, or Spaces when relevant; OpenAI Developers verifies OpenAI-specific claims against official docs; ImageGen/Remotion/Manim may create support visuals or component clips only when appropriate and documented; HyperFrames owns final timeline, captions, motion, inspect, render, and delivery; FFmpeg/ffprobe owns mechanical media checks. HeyGen is optional and never default because account, upload, and credit boundaries require explicit user approval.

Gate: a video that teaches or claims plugin/tool workflow must not pass as a HyperFrames-only production. If a plugin is named, show entry/source proof, operation proof, output proof, and viewer-value proof, or mark it optional/blocked with the reason. `provider_usage_audit.json` must show the multi-plugin/runtime decisions before `promote_final.py`.

## AI Knowledge Aspect Ratio

All AI knowledge videos owned by this skill must be 16:9 horizontal by default and by validation: `1920x1080`, `fps: 30`. This includes AI news, AI tools, ChatGPT, Gemini, OpenAI, Codex, Agent, automation, AI coding, AI workflow, plugin, and Skill tutorials. Do not switch AI knowledge videos to 9:16 just because the destination is Douyin. For Douyin publishing, deliver the 16:9 master and let the platform/player handle display; do not crop proof UI into a vertical frame.

## AI Background-First Rule

Before storyboard, assets, TTS, HyperFrames, render, or upload for any AI knowledge video, create `internal/background_prompt_pack.md` with descriptive background language, generate text-free `1920x1080` background plate(s), and register them in `asset_manifest.json` as `asset_role=background_plate`, `type=generated_visual`, `asset_source_type=generated`, and `is_evidence=false`. Generic gradients, neon grids, pseudo UI, background text, or linework behind captions are blocked.

Generated visuals must use `gpt-image-2` or Codex built-in ImageGen with the model/provider recorded. Every generated background, cover, support visual, metaphor visual, transition plate, or diagram base needs its own prompt card and manifest fields: `model`, `prompt_id`, `prompt_path`, `unique_prompt=true`, and `evidence_boundary`. A local PIL/canvas/HTML render may be used for deterministic diagrams or cover layout, but it must not be registered as an AI-generated `generated_visual` or counted as satisfying the ImageGen gate.

## HyperFrames Premium Motion Language Rule

Before storyboard or HyperFrames composition work, define premium motion as executable animation language, not adjectives. Use restrained terms such as `smooth`, `dramatic`, `subtle`, `cinematic`, `premium`, `clean`, `restrained`, and `snappy`; do not use vague requests such as `高级一点`, `炫酷`, `震撼`, `crazy`, `explosive`, `flashy`, `excessive`, or `chaotic`. Every scene's storyboard `motion` must document purpose, entrance, stagger, keyword motion, camera motion, layering, transition, caption motion, glow, audio-reactive behavior, and negative motion constraints. Gate: no structured motion craft means no HyperFrames HTML, preview, render, or final delivery.

## Continuous Narration Bed Rule
HyperFrames scene transitions are visual-only. The spoken narration must continue through every transition without restart, mute, fade-out, or a perceptible gap. Prefer one root-level continuous narration audio file that spans the full video, built after scene TTS duration lock. If per-scene audio clips are used during iteration, the final storyboard/audio lock must prove they play back-to-back with `max_audio_gap_ms <= 120`, stay outside timed visual scene containers, and are never controlled by scene entrance/transition/exit animations. After TTS lock, `storyboard.json`, `storyboard.director_shots[*].duration_sec`, scene `duration_target`, and `storyboard.audio_locked.json` must use the same real audio timing. Gate: no documented continuous narration strategy or mismatched storyboard/director/audio timings means no HyperFrames composition, render, final delivery, or publishing.

## Visual Director Script Rule

For AI knowledge videos, HyperFrames is only the executor. Before any HyperFrames composition, create a machine-checkable visual director script in `storyboard.director_shots`. Do not let HyperFrames invent the visual structure from generic "premium" language. Each `director_shots` item must use enum-like fields for `shot_type`, `layout_family`, `camera_scale`, `camera_motion`, `visual_subject`, `primary_action`, `operation_elements`, `evidence.type`, and approved on-screen text.

Gate before HyperFrames: director shots must pass visual diversity, real-operation feel, evidence authenticity, and approved-text checks. Videos that repeat the same glass-card layout, lack task/workspace/test/evidence operation shots, use tiny/fake evidence panels, or have empty primary actions are blocked before HTML is written.

## Final Screen Text And Empty Frame Rule

After render, export or produce `internal/render_text_manifest.json` containing every final on-screen text item with role, shot ID, and start/end time. Run a final proofread gate against `storyboard.director_shots[*].on_screen_text` and `approved_primary_text`. Large titles, captions, and CTA text not approved by the storyboard are blocking issues. Final video QA must also check empty-frame risk; any unintentional empty visual longer than 0.5s or any frame without a primary visual subject is blocked.

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

For publish-ready work, create the artifact chain in `references/workflow_contract.md` under `outputs/<date-topic>/internal/`. Only after `qa_report.json` and `provider_usage_audit.json` pass may `outputs/<date-topic>/final/` contain `final.mp4`, `cover.png`, `publish_copy.txt`, and `metadata.json`.

## Core Workflow

Read `references/workflow_contract.md` first for the full gate contract.

For any publish-ready, high-quality, reference-level, premium, or polished video, also read `references/premium_video_quality_playbook.md` and `references/ai_generated_asset_prompt_system.md` before storyboard or asset work.

For any HyperFrames-rendered AI video, also read `references/premium_ai_video_source_to_hyperframes_rule.md` before storyboard work and apply the `Premium HyperFrames Animation Language` section. The storyboard must pass structured motion validation before HyperFrames composition.

For any publish-ready video after the open-source learning upgrade, also read `references/free_first_open_source_stack.md`, `references/runtime_decision_matrix.md`, and `references/timeline_contract.md` before storyboard or asset planning. If the user mentions the six-tool Codex video stack, classify HyperFrames, FFmpeg, OpenMontage, Remotion, Video-Use, and Manim through the runtime matrix before claiming a tool is installed, executed, or used.

For AI tool/tutorial videos that can benefit from Codex plugins, also read `references/codex_plugin_integration.md` before evidence collection. HyperFrames is the final assembly engine, not the whole production brain.

For multi-style requests, shared-growth requests, or ambiguous video requests that could be AI, renovation, or beauty, read `references/video_style_router.md` and `references/shared_video_quality_core.md` before deciding the owning skill. Keep this skill focused on AI-circle knowledge videos.

For Codex Skill, Agent, plugin, Remotion, HyperFrames, or ImageGen tutorial videos, also read `references/codex_skill_tutorial_video.md`, `references/beginner_visual_sync_rules.md`, `references/codex_three_skill_video_playbook.md`, and `references/codex_plugin_integration.md` before scripting or storyboard work.

For every new AI video, also read the soft learning layer: `references/learning_bank.md`, `references/failed_case_library.md`, and `references/director_decision_patterns.md`. After QA, generate `production_postmortem.json` so observations and user feedback can influence the next run. Proposed rule changes from postmortems require user approval before becoming hard gates.

## Input Mode Routing

Before topic research, decide the production mode:

- **Style Router Mode**: If the user asks for three video styles, shared skill growth, renovation videos, beauty choice videos, or a non-AI video, route by `references/video_style_router.md` before using this AI workflow. Do not force renovation or beauty work through the AI knowledge pipeline.
- **Reference Mode**: If the user provides a Douyin link, share text, local video, image set, or says to imitate a reference, first run reference analysis. Imitate the reference's pacing, structure, information density, hook logic, caption rhythm, and visual progression, but do not copy exact wording, frames, voice, music, identity, or a highly similar full structure.
- **Three-Skill Tutorial Mode**: If the reference or topic is about multiple Codex Skills/plugins, Remotion, HyperFrames, ImageGen, or HeyGen, apply `references/codex_three_skill_video_playbook.md` and `references/codex_plugin_integration.md`. The storyboard must document `production_stack`; plugin videos must also document `codex_plugin_plan`; every named tool must have an entry/source proof, operation proof, output proof, and viewer-value reason.
- **Multi-Plugin Evidence Mode**: If the video is about an AI tool, Codex workflow, open-source model/tool, plugin stack, API, repo, dataset, or official documentation, decide which plugins should participate before script lock. Use Browser by default for UI/docs proof, GitHub for repo/source proof when relevant, Hugging Face for model/dataset/paper proof when relevant, OpenAI Developers for official OpenAI claims, and HyperFrames only after the evidence plan is clear.
- **Self-Research Mode**: If the user only says to use this skill to make a video, or gives a broad AI/video request without a reference, do not reuse evergreen copy or Codex-only topics by default. First research current AI-circle hot topics and high-quality source material across the broader AI industry, then create topic candidates from that research.

Self-Research Mode must include recent, source-backed material before copywriting:

- Search current AI industry topics across OpenAI, Anthropic, Google, Meta, xAI, AI agents, AI video tools, coding agents, enterprise AI, AI safety/regulation, and creator workflows.
- Prefer official product/news pages, reputable technology/business media, launch notes, docs, demos, benchmarks, and real product screenshots or recordings.
- Save the chosen sources and the claim each source supports in `topic_candidates.json`.
- Do not choose a generic evergreen topic unless it clearly beats current topics on pain, novelty, save value, visual potential, and compliance safety.

1. Research and decide: score recent topic candidates, lock one selected topic, then write copy. No topic below 8.0 enters copywriting.
2. Score and review copy: run script scoring, semantic review, and compliance before any assets, TTS, HyperFrames, render, or publish work.
3. Direct the visuals before rendering: create background prompt pack, optional reference analysis, `storyboard.director_shots`, structured scene motion, evidence plan, and asset manifest. No `director_shots`, no HyperFrames.
4. Validate pre-render gates: run storyboard and asset validation. The storyboard must enforce 16:9 AI format, premium motion language, visual diversity, real-operation feel, evidence authenticity, approved screen text, and continuous narration planning.
5. Lock audio and timeline: build a continuous root narration bed, produce `storyboard.audio_locked.json`, and compose HyperFrames only from locked timing. Visual transitions must never restart, mute, fade, or gap narration.
6. Render and inspect: render high quality, then run audio continuity, technical QA, frame review, final screen-text proofread, empty-frame check, visual review, QA gate, and provider audit.
7. Promote only after gates pass: run `scripts/promote_final.py` only when `qa_report.json` and `provider_usage_audit.json` pass with no blocking issues.
8. For skill changes, run `scripts/check_golden_project.py` to verify the bundled golden project still reaches high-quality QA.

## Required References

Always use the relevant files under `references/`, especially `workflow_contract.md`, `video_quality_contract.md`, `premium_video_quality_playbook.md`, `ai_generated_asset_prompt_system.md`, `video_style_router.md`, `topic_selection_rules.md`, `script_quality_rules.md`, `douyin_compliance_rules.md`, `visual_sync_rules.md`, `hyperframes_delivery.md`, `hyperframes_components.md`, `codex_three_skill_video_playbook.md`, `codex_plugin_integration.md`, `post_publish_review.md`, and `learning_bank.md`.

## Required Commands

Before committing changes to this skill: `python3 scripts/doctor.py`, `python3 -m py_compile scripts/*.py`, and `python3 -m pytest -q`; if any command fails, fix the cause before publishing.
