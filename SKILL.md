---
name: douyin-hyperframes-remake
description: 制作原创、合规、最高级 AI 圈知识类抖音短视频，并在用户说做视频、出片、成片、生成视频、AI知识视频、参考视频学习、视频质量太低、要最高级/高级版/发布级时先做视频风格路由。用于 AI 新闻、AI 工具、ChatGPT、Codex、Agent、自动化、AI 视频、AI 教程类选题研究、参考视频拆解、中文口播文案、分镜、真实证据素材、Remotion/ImageGen/HyperFrames/FFmpeg 联动成片、可选 OpenMontage/Video-Use/Manim 适配、字幕同步、封面和发布前质量验收。默认只接受 publish-ready highest-grade 工作流；低配草稿、模板轮播、单图配音、普通 Ken Burns 缩放或未过 QA 的视频不得作为 final 交付。
---

# Douyin AI Video Director

V3 keeps the historical skill name `douyin-hyperframes-remake` for compatibility. The current job is not simple remake work; it is AI-circle knowledge video direction with source-backed copy, visual-director storyboards, strict compliance, HyperFrames assembly, and final QA.

## Operating Posture

Default to highest-grade publish-ready production unless the user explicitly asks for research only, planning only, quick draft, or smoke test. First read `references/video_style_router.md` and `references/shared_video_quality_core.md` before scripts, assets, TTS, HyperFrames, render, or publish-chain work.

Route by owning skill instead of forcing every video into this workflow:

- AI news, AI tools, ChatGPT, Codex, Agents, automation, plugins, API/docs, open-source AI, or AI tutorial videos stay in this skill.
- Renovation, full-house custom, interior design, cabinet, or home-ad work routes to `$full-house-custom-ad`.
- Beauty portrait or choice-video work routes to `$beauty-gpt-image-video`.

If provider access, asset quality, voice quality, HyperFrames, ffprobe, safe-zone review, Qingdou, or QA gates cannot meet the publish-ready bar, stop with a blocker or deliver a clearly labeled draft. Never silently downgrade to a slideshow, single-image narration, generic Ken Burns zoom, no-audio MP4, or no-QA final.

## Non-Negotiable Gates

Keep these gates intact even when simplifying the workflow:

- Topic first: create and score `topic_candidates.json`, then lock `selected_topic.json`; no topic below 8.0 enters copywriting.
- Beginner value first: copy must define the viewer task, visible result, first action, saved step, proof screen, plain-language takeaway, and concrete problem example. Run `scripts/score_script.py`, `scripts/evaluate_copy_semantic.py`, and `scripts/validate_beginner_copy.py`; `beginner_value_review.json` must pass and `problem_example_score >= 8.5`.
- Compliance before production: `compliance_report.json` must pass before images, TTS, HyperFrames, render, or publishing. Read `references/global_douyin_text_compliance_rule.md`, `references/forbidden_terms_learning_bank.md`, and active `references/forbidden_terms_learning_bank.jsonl` before writing Douyin-facing text.
- Reference originality: when given a Douyin link, share text, local MP4, screenshots, or "make similar" request, read `references/reference_driven_production_rules.md`; learn pacing, layout, typography, rhythm, filter mood, music/voice relationship, and motion language, but never reuse original frames, subtitles, voice, people, room/product assets, wording, watermark, creator identity, or a highly similar full sequence. Final major on-screen text must stay within 10% character-level deviation from approved original copy.
- 16:9 proof-first AI format: proof-heavy AI, Codex, Agent, ChatGPT, plugin, and Skill tutorials use `1920x1080`, `fps: 30`. Only lightweight vertical guide/list/card/poster references may use the `1080x1920` AI information-poster exception from `references/reference_driven_production_rules.md`.
- Visual director before HyperFrames: create `visual_style_plan.json`, background/prompt packs, `storyboard.director_shots`, evidence plan, structured motion, asset manifest, and validation reports before composition. Vague "高级/科技感/炫酷/4K/premium tech" prompt language is blocking.
- Natural voice honesty: publish-ready narration needs truthful `metadata.voice`, approved sample evidence, normal default `tts_speed` 0.95-1.03, and a continuous root narration bed. Faster voice such as `1.1x` is allowed only with explicit current-video approval, `tts_speed <= 1.10`, provider/sample metadata, and retimed storyboard/HTML from real audio durations.
- Screen text and empty frames: after render, produce `render_text_manifest.json`, proofread against approved storyboard text, check empty-frame risk, and run visual review. Unapproved large text, garbled characters, wrong Chinese, or subjectless frames block final delivery.
- Publish cover is its own artifact: before promotion, generate or review a standalone designed cover, save `internal/publish_cover_report.json`, and include `internal/publish_cover_text.txt` in local text compliance. A random frame grab cannot be promoted as the publish cover.
- Qingdou before promotion or upload: exact public title, caption, and topics must pass Qingdou (`轻抖`) together, recorded as `internal/qingdou_keyword_check.json` with `checked_fields=["title","caption","topics"]` and `未检查到敏感词` or equivalent passed status. Local scripts and Creator Center quick checks are not substitutes. Narrow exception: if Qingdou only flags a user-required official/platform campaign topic, and the user explicitly says to keep that exact topic after seeing the failed result, record `status: "user_override_accepted"` plus the failed term, risk note, and user approval, then continue; never label this as Qingdou passed, and still rewrite all non-topic title/caption/on-screen hits.
- Publish contract before promotion: build `internal/publish_contract.json`, run `scripts/pre_publish_gate.py`, and require `gate.status="passed"` before upload, publishing, or `final/` promotion.
- No auto-publish: `allow_auto_publish` remains false until the user explicitly authorizes publishing after QA.

## Runtime Direction

HyperFrames is the final timeline and delivery engine, not the whole production brain. For AI tool, Codex, Agent, plugin, open-source, model, dataset, API, or official-documentation videos, read `references/codex_plugin_integration.md` before evidence collection and document `storyboard.codex_plugin_plan`.

Default proof roles:

- Browser: real UI, docs, product pages, screenshots, and visual review.
- GitHub: repos, releases, source files, issues, PRs, and CI evidence when relevant.
- Hugging Face: public models, datasets, papers, and Spaces when relevant.
- OpenAI Developers: official OpenAI docs/API/Agents/App SDK claims.
- ImageGen, Remotion, and Manim: support visuals or component clips only when appropriate and truthfully documented.
- HyperFrames: final composition, captions, motion, inspect, render, and delivery.
- FFmpeg/ffprobe: media probing, frame extraction, remux, bitrate, duration, and audio checks.
- HeyGen: optional only with explicit user approval for account, upload, and credit boundaries.

Do not claim any runtime, plugin, model, or provider was installed or used without real file, terminal, UI, render, or documented evidence. If external paid API, paid asset, paid subscription, paid cloud render, or credit-consuming service is required, mark it blocked and choose a Codex-included, free, local, or open-source path.

## Core Workflow

Read `references/workflow_contract.md` first for the full artifact contract. For publish-ready AI videos, the expected chain is:

```text
topic_candidates
-> selected_topic
-> ai_scheme_classification when relevant
-> copy_package + script_score + semantic_review + beginner_value_review
-> compliance_report + forbidden-term learning when needed
-> codex_plugin_plan / production_stack when tool workflow is involved
-> reference_analysis when a reference exists
-> visual_style_plan + background_prompt_pack + asset_prompt_validation
-> storyboard + storyboard_validation + asset_manifest + visual_tone_report + asset_validation
-> storyboard.audio_locked + continuous narration bed
-> draft.mp4 + metadata
-> audio_continuity_report + video_technical_qa + frame_review
-> render_text_manifest + screen_text_proofread + empty_frame_report + visual_review
-> qa_report + production_postmortem
-> publish_cover_report + on_screen_and_publish_text_compliance_report
-> provider_usage_audit + qingdou_keyword_check
-> publish_contract + pre_publish_gate
-> promote_final
-> final/final.mp4
```

`scripts/qa_gate.py` checks the internal draft package and writes QA only. `scripts/build_publish_contract.py` collects final artifacts and reports into one contract. `scripts/pre_publish_gate.py` validates QA, provider usage, Qingdou, text compliance, and cover checks. `scripts/promote_final.py` copies artifacts to `final/` only when the contract gate already passed.

For skill changes, run `scripts/check_golden_project.py` so the bundled golden project still reaches high-quality QA.

## Reference Loading Map

Load only the relevant references for the task:

- Always for full production: `workflow_contract.md`, `video_quality_contract.md`, `premium_video_quality_playbook.md`, `shared_video_quality_core.md`, `free_first_open_source_stack.md`, `runtime_decision_matrix.md`, `timeline_contract.md`.
- Topic and copy: `topic_selection_rules.md`, `beginner_copywriting_rules.md`, `script_quality_rules.md`, `creative_rubric.md`.
- Compliance and publishing: `global_douyin_text_compliance_rule.md`, `forbidden_terms_learning_bank.md`, `douyin_compliance_rules.md`, `post_publish_review.md`.
- Reference-led work: `reference_driven_production_rules.md`, `reference_video_rules.md`, `video_style_router.md`.
- AI schemes: `ai_video_scheme_library.md`, `ai_video_scheme_1_skill_recommendation_no_voice.md`, `ai_reference_video_outcome_registry.md`.
- Visual direction and assets: `visual_description_language_reference.md`, `visual_prompt_motion_phrasebook.md`, `ai_generated_asset_prompt_system.md`, `visual_sync_rules.md`, `visual_aesthetic_rules.md`, `hyperframes_components.md`.
- HyperFrames delivery: `premium_ai_video_source_to_hyperframes_rule.md`, `hyperframes_delivery.md`, `codex_three_skill_video_playbook.md`, `codex_skill_tutorial_video.md`.
- Evidence plugins: `codex_plugin_integration.md`.
- Learning layer: `learning_bank.md`, `failed_case_library.md`, `director_decision_patterns.md`.

## Use When

- The user asks for AI, ChatGPT, Codex, Agent, automation, AI video, AI tool, plugin, model, or source-backed tutorial Douyin content.
- The user provides a Douyin link, share text, reference video, screenshot set, or AI topic and wants a high-quality original video.
- The user asks for topic research, copywriting, storyboard, HyperFrames production, QA, cover, publish copy, or publish-ready package for AI-circle knowledge content.

## Do Not

- Do not skip topic research and jump straight into script, image generation, TTS, render, or upload.
- Do not copy reference assets, exact wording, voice, subtitles, person identity, watermark, or sequence.
- Do not use fake UI, fake official proof, fake reviews, unsourced claims, absolute guarantees, station-out diversion, QR codes, contact details, or诱导互动.
- Do not use single-image narration, low-quality image carousel, repeated glass-card pages, all-dark canvases, static slides, black/white frames, no-audio output, or audio/visual mismatch as final.
- Do not place narration audio inside transitioning scene containers or allow transitions to restart, mute, fade, or gap narration.
- Do not relabel macOS `say`, Apple/system voices, scratch timing audio, local renders, or placeholders as publish-ready TTS or AI-generated visuals.

## Required Commands

Before finishing changes to this skill, run:

```bash
python3 scripts/doctor.py
python3 -m py_compile scripts/*.py
python3 -m pytest -q
python3 scripts/check_golden_project.py
```
