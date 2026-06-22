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
- Current-source scan boundary: for recurring AI videos, scan AI, Codex/OpenAI, ChatGPT/OpenAI, and Gemini/Google AI before copywriting. Prefer the task date. If a direction has no strong same-day signal, expand only to the latest 7 calendar days and state that in the scan report. Older sources may be kept as background context, but they do not satisfy the required current-angle coverage and must not be used to make the topic look fresh.
- Director orchestrator before copy: for publish-ready AI videos, create `director_selection.json`, `style_recipe.json`, `hook_variants.json`, `hook_score_report.json`, and `reference_overfit_audit.json` before full copy, storyboard, images, TTS, HyperFrames, render, or upload. The newest reference video is only a candidate style card; it must not become the default template.
- Source-led topic title: every AI topic title must first name the concrete software, website, company, model, product feature, release, official doc, or news event, then the practical takeaway. Method-only titles such as `用 ChatGPT 和 Codex 前先写边界清单` are blocking; use source/event-led titles such as `ChatGPT 新增应用调用确认：用 Codex 前先写三层边界清单`.
- Beginner value first: copy must define the viewer task, visible result, first action, saved step, proof screen, plain-language takeaway, and concrete problem example. Run `scripts/score_script.py`, `scripts/evaluate_copy_semantic.py`, and `scripts/validate_beginner_copy.py`; `beginner_value_review.json` must pass and `problem_example_score >= 8.5`.
- Compliance before production: `compliance_report.json` must pass before images, TTS, HyperFrames, render, or publishing. Read `references/global_douyin_text_compliance_rule.md`, `references/forbidden_terms_learning_bank.md`, and active `references/forbidden_terms_learning_bank.jsonl` before writing Douyin-facing text.
- Reference originality: when given a Douyin link, share text, local MP4, screenshots, or "make similar" request, read `references/reference_driven_production_rules.md`; learn pacing, layout, typography, rhythm, filter mood, music/voice relationship, and motion language, but never reuse original frames, subtitles, voice, people, room/product assets, wording, watermark, creator identity, or a highly similar full sequence. Final major on-screen text must stay within 10% character-level deviation from approved original copy.
- 16:9 proof-first AI format: proof-heavy AI, Codex, Agent, ChatGPT, plugin, and Skill tutorials use `1920x1080`, `fps: 30`. Only lightweight vertical guide/list/card/poster references may use the `1080x1920` AI information-poster exception from `references/reference_driven_production_rules.md`.
- Visual director before HyperFrames: create `visual_style_decision.json` before `visual_style_plan.json`, then background/prompt packs, `storyboard.director_shots`, evidence plan, structured motion, asset manifest, and validation reports before composition. Codex must choose brightness, palette, material, and layout from the topic, copy mood, evidence density, and reference rhythm; do not lock the skill to a light, dark, or repeated default style. Vague "高级/科技感/炫酷/4K/premium tech" prompt language is blocking.
- Fixed production templates before visual work: after `director_selection.json` and `style_recipe.json`, run `scripts/select_fixed_ai_templates.py` and write `internal/fixed_template_selection.json`. This locks one reusable background image asset from `assets/ai_background_templates_fixed/`, one transition/SFX pack, one foreground component pack, and one voice mix profile for the whole video. The report must include `background_template.fixed_asset_path` and `inheritance_contract.fixed_background_asset_required=true`; HyperFrames must use that fixed background file as the base visual layer instead of regenerating a new background. These templates reduce token waste and quality drift, but do not replace topic-specific copy, proof, screenshots, or compliance checks.
- Active video contract and regression gate: every AI video must follow `references/shared_video_quality_core.md#ai-video-active-contract-and-regression-gate` before final QA, upload, or publishing. During production, use the positive contract only: fixed premium background as atmosphere, topic-bound foreground modules with real information jobs, named advanced transitions, audible voice-safe SFX, true one-frame cover, checked public text, and the user's current Chrome/session. Historical failure wording belongs in automated gate reports and tests only; it is not a planning step or user-facing work note. A failed gate remains blocking and must be reworked before the result can be called final.
- Layout and transition quality gate: foreground modules may use panels, trays, rails, chips, proof crops, and checklist rows only when they carry the current scene's information. A 45-75 second AI explainer must avoid repeated same-size left-heavy mega-panels as the dominant look; use at least four distinct scene structures when scene count allows. Transitions must visibly move information from the outgoing scene into the next scene. A short abstract sweep is acceptable only as a sub-layer; if contact sheets show 0.4s+ of decoration-only diagonal lines, empty rails, or node sweeps without a source/step/result handoff, restage that boundary before final.
- Natural voice honesty: publish-ready narration needs truthful `metadata.voice`, approved sample evidence, normal default `tts_speed` 0.95-1.03, and a continuous root narration bed. For this user's recurring AI knowledge / daily AI tip videos, the standing voice direction is a powerful professional Chinese male lecturer: firm, energetic, thick enough, and precise; default free-first voice is `edge_tts` `zh-CN-YunyangNeural` at provider rate around `+10%`, with `voice_speed_policy=user_approved_1_1x` when metadata uses `tts_speed: 1.1`. Faster voice such as `1.1x` is allowed only with explicit current-video or standing-user approval, `tts_speed <= 1.10`, provider/sample metadata, and retimed storyboard/HTML from real audio durations. If the user says the voice is too small, SFX disappeared, or the voice is not thick enough, do not just raise MP4 volume: rebuild/remix root audio with `references/hyperframes_delivery.md` voice/SFX rules and record a voice mix QA report. If the video and voice are already approved but transition/status SFX is inaudible, preserve the final picture and narration, overlay the root-level SFX bed with `amix normalize=0`, and require `sfx_audibility.status=passed` or `internal/sfx_audibility_report.json.status=passed`; cue metadata alone is not enough.
- Screen text and empty frames: after render, produce `render_text_manifest.json`, proofread against approved storyboard text, check empty-frame risk, and run visual review. Unapproved large text, garbled characters, wrong Chinese, or subjectless frames block final delivery.
- Publish cover is its own artifact and also the designed first frame of the video: before promotion, use the fixed safe cover assets from `assets/ai_cover_templates_fixed/` through `references/fixed_ai_cover_template_rotation.json` and `scripts/select_fixed_cover_template.py`, or an explicitly reviewed one-off topic-specific cover. Select by canvas first (`horizontal_16x9` for 1920x1080, `vertical_9x16` for 1080x1920), then rotate sequentially inside that size pool; do not randomly choose across all 10. Save `internal/first_frame_cover.png`, `internal/cover.png`, `internal/publish_cover_report.json`, and `internal/publish_cover_text.txt`, then include cover text in local text compliance. The cover must be actually inserted into the final MP4 as frame 0 only by default, not as a long static intro; at 30fps this means about `0.033s`. If HyperFrames/Remotion cannot emit a true one-frame cover, use FFmpeg overlay on `eq(n,0)` after render while preserving duration and audio timing. Save `internal/actual_frame_000_cover.png` and `internal/actual_frame_001_after_cover.png`; frame 0 must be the cover and frame 1 must already return to the main timeline. Do not use the old programmatic glass-card preview covers. A random frame grab cannot be promoted as the publish cover.
- Qingdou before promotion or upload: exact public title, caption, and topics must pass Qingdou (`轻抖`) together, recorded as `internal/qingdou_keyword_check.json` with `checked_fields=["title","caption","topics"]` and `未检查到敏感词` or equivalent passed status. Local scripts and Creator Center quick checks are not substitutes. The user has given standing authorization for routine Qingdou/Douyin publish-chain browser actions, including text entry, paste/replace, clicking the check button, reading the visible result, and ordinary slider or image security verification when the current environment permits agent handling; execute these routine steps yourself instead of handing the copy/check back to the user. Reuse the user's current logged-in Chrome tab/session, and close any extra tab/window opened for the task after completion. Current-environment browser automation may be used for page input and visible-result reading, but never extract or store credentials, cookies, SMS codes, verification codes, or verification data. Still stop for SMS codes, phone-only login, real-name or account-owner verification, verification that clearly must be completed by the user, or any active browser/tool safety policy that requires fresh action-time confirmation. Narrow exception: if Qingdou only flags a user-required official/platform campaign topic, and the user explicitly says to keep that exact topic after seeing the failed result, record `status: "user_override_accepted"` plus the failed term, risk note, and user approval, then continue; never label this as Qingdou passed, and still rewrite all non-topic title/caption/on-screen hits. Standing topic override: as of 2026-06-21, `#我在抖音聊科技` is approved permanently; if Qingdou only flags `抖音` inside that exact hashtag, record `status: "user_override_accepted"` and do not ask again.
- Publish contract before promotion: use `scripts/produce_ai_video.py` as the only production entrypoint. It must write passed `internal/visual_regression_gate.json`, then build `internal/publish_contract.json`, run `scripts/pre_publish_gate.py`, and require `gate.status="passed"` before upload, publishing, or `final/` promotion.
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
-> director_selection + style_recipe + hook_variants + hook_score_report + reference_overfit_audit
-> fixed_template_selection
-> ai_scheme_classification when relevant
-> copy_package + script_score + semantic_review + beginner_value_review
-> compliance_report + forbidden-term learning when needed
-> codex_plugin_plan / production_stack when tool workflow is involved
-> reference_analysis when a reference exists
-> visual_style_decision + visual_style_plan + background_prompt_pack + asset_prompt_validation
-> storyboard + storyboard_validation + asset_manifest + visual_tone_report + asset_validation
-> storyboard.audio_locked + continuous narration bed
-> fixed cover template selection + first_frame_cover
-> voice/SFX mix report when narration and transition effects coexist
-> SFX audibility report when dynamic icons, transitions, status nodes, or checklist ticks are visible
-> draft.mp4 + metadata
-> audio_continuity_report + video_technical_qa + frame_review
-> render_text_manifest + screen_text_proofread + empty_frame_report + visual_review
-> qa_report + production_postmortem
-> publish_cover_report + on_screen_and_publish_text_compliance_report
-> visual_regression_gate
-> provider_usage_audit + qingdou_keyword_check
-> publish_contract + pre_publish_gate
-> promote_final
-> final/final.mp4
```

`scripts/produce_ai_video.py` is the canonical production entrypoint. It runs QA, blocks legacy PIL/rawvideo/card-renderer regressions, verifies real frame 0 / frame 1 cover evidence, and only then allows contract gating and promotion. `scripts/run_pipeline.py` is an internal QA-order compatibility runner, not a production entrypoint. `scripts/qa_gate.py` checks the internal draft package and writes QA only. `scripts/build_publish_contract.py` collects final artifacts and reports into one contract. `scripts/pre_publish_gate.py` validates QA, visual regression, provider usage, Qingdou, text compliance, and cover checks. `scripts/promote_final.py` copies only `final/final.mp4` into `final/` after the contract gate passes, deletes stale extra final artifacts, removes frame sequences and internal draft MP4 files, and records `cleanup_status=final_folder_mp4_only`.

For skill changes, run `scripts/check_golden_project.py` so the bundled golden project still reaches high-quality QA.

## Reference Loading Map

Load only the relevant references for the task:

- Always for full production: `workflow_contract.md`, `video_quality_contract.md`, `premium_video_quality_playbook.md`, `shared_video_quality_core.md`, `free_first_open_source_stack.md`, `runtime_decision_matrix.md`, `timeline_contract.md`.
- Topic and copy: `topic_selection_rules.md`, `beginner_copywriting_rules.md`, `script_quality_rules.md`, `creative_rubric.md`.
- Compliance and publishing: `global_douyin_text_compliance_rule.md`, `forbidden_terms_learning_bank.md`, `douyin_compliance_rules.md`, `post_publish_review.md`.
- Reference-led work: `reference_driven_production_rules.md`, `reference_video_rules.md`, `video_style_router.md`; for short Codex operation references, also read `codex_operation_micro_tutorial_style.md`.
- AI schemes and orchestration: `video_director_orchestrator.md`, `reference_style_cards.json`, `component_motion_registry.json`, `hook_pattern_bank.md`, `copy_hook_scoring_rules.md`, `ai_video_scheme_library.md`, `ai_video_scheme_1_skill_recommendation_no_voice.md`, `ai_reference_video_outcome_registry.md`.
- Visual direction and assets: `fixed_ai_production_templates.md`, `fixed_ai_background_template_rotation.json`, `fixed_ai_transition_sfx_packs.json`, `fixed_ai_component_template_packs.json`, `fixed_ai_voice_mix_profiles.json`, `visual_description_language_reference.md`, `visual_prompt_motion_phrasebook.md`, `ai_generated_asset_prompt_system.md`, `visual_sync_rules.md`, `visual_aesthetic_rules.md`, `hyperframes_components.md`.
- Cover system: `fixed_ai_cover_template_rotation.md`, `fixed_ai_cover_template_rotation.json`, and `ai_cover_template_library.md`.
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
