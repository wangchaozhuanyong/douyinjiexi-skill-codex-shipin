---
name: douyin-hyperframes-remake
description: 制作原创、合规、最高级 AI 圈知识类抖音短视频，并在用户说做视频、出片、成片、生成视频、AI知识视频、参考视频学习、视频质量太低、要最高级/高级版/发布级时先做视频风格路由。用于 AI 新闻、AI 工具、ChatGPT、Codex、Agent、自动化、AI 视频、AI 教程类选题研究、参考视频拆解、中文口播文案、分镜、真实证据素材、Remotion/ImageGen/HyperFrames/FFmpeg 联动成片、可选 OpenMontage/Video-Use/Manim 适配、字幕同步、封面和发布前质量验收。默认只接受 publish-ready highest-grade 工作流；低配草稿、模板轮播、单图配音、普通 Ken Burns 缩放或未过 QA 的视频不得作为 final 交付。
---

# Douyin AI Video Director

V3 keeps the historical skill name `douyin-hyperframes-remake` for compatibility. The current job is not simple remake work; it is AI-circle knowledge video direction with source-backed copy, visual-director storyboards, strict compliance, HyperFrames assembly, and final QA.

## Operating Posture

Default to highest-grade publish-ready production unless the user explicitly asks for research only, planning only, quick draft, or smoke test. First read `references/video_style_router.md` and `references/shared_video_quality_core.md` before scripts, assets, TTS, HyperFrames, render, or publish-chain work.

Route by owning skill instead of forcing every video into this workflow:

- AI news, AI hot-rank/TOP5 lists, AI tools, ChatGPT, Codex, Agents, automation, plugins, API/docs, open-source AI, or AI tutorial videos stay in this skill.
- Renovation, full-house custom, interior design, cabinet, or home-ad work routes to `$full-house-custom-ad`.
- Beauty portrait or choice-video work routes to `$beauty-gpt-image-video`.

If provider access, asset quality, voice quality, HyperFrames, ffprobe, safe-zone review, Qingdou, or QA gates cannot meet the publish-ready bar, stop with a blocker or deliver a clearly labeled draft. Never silently downgrade to a slideshow, single-image narration, generic Ken Burns zoom, no-audio MP4, or no-QA final.

## Non-Negotiable Gates

Keep these gates intact even when simplifying the workflow:

- Topic first: create and score `topic_candidates.json`, then lock `selected_topic.json`; no topic below 8.0 enters copywriting.
- Current-source scan boundary: for recurring AI videos, scan AI, Codex/OpenAI, ChatGPT/OpenAI, and Gemini/Google AI before copywriting. Prefer the task date. If a direction has no strong same-day signal, expand only to the latest 7 calendar days and state that in the scan report. Older sources may be kept as background context, but they do not satisfy the required current-angle coverage and must not be used to make the topic look fresh.
- AI 热榜 TOP5 mode: when the user asks for `AI 热榜`, `TOP5`, `榜单`, `排行`, or `排名` as current AI news or hot signals, classify it as `scheme_7_ai_hot_rank_top5`, apply `references/ai_video_scheme_7_hot_rank_top5.md`, fill `templates/ai_hot_rank_top5.template.json`, and lock exactly five scored source-backed rank items in `internal/ai_hot_rank_top5.json` before copywriting or rendering. Do not convert TOP5 into a one-topic explainer, and do not invent a hot ranking. When the user asks for the analyzed AI研究所-style reference standard or `蚂蚁AI` hotlist template, set `scheme_variant=ant_ai_hotlist_extended` and follow `references/ai_video_scheme_7_ant_ai_hotlist_extended.md`: fixed CTA `关注 蚂蚁AI`, fixed male voice `VOICE_MALE_THICK_YUNYANG_V1`, fixed Ant AI glass-nebula background, approved same-platform Douyin reference BGM from the local music library, and source-backed copywriting grammar instead of fixed copied wording.
- Skill-first short list mode: for recurring vertical AI list videos aimed at beginners, especially when the user says `Skill`, `新手`, `清单`, `推荐`, `插件`, or asks what a skill can do, prefer `scheme_1_skill_recommendation_no_voice` over news ranking unless the user explicitly requests current news. Before copywriting or rendering, create `internal/skill_source_manifest.json` from real sources: official Codex documentation or web scan for the Skill mechanism, plus actual installed/curated `SKILL.md` entries, `agents/openai.yaml` display names, and icon files when a left icon is shown. The manifest must set `copy_mode=source_quoted_or_source_paraphrase` and each public row must include `source_description`, `public_note`, and `claim_evidence` tied to exact `SKILL.md` or `agents/openai.yaml` source text. Run `scripts/check_skill_source_manifest.py`; if the manifest fails, a row is invented, or the public note is inferred from adjacent capabilities instead of source text, stop. Do not require or invent `input/purpose/output` fields; if such fields appear, each one needs its own claim evidence. Public on-screen and publish copy must not ask viewers to provide, copy, open, visit, download, scan, or message through a website/link/QR/contact path; keep any URLs only in internal evidence fields.
- Director orchestrator before copy: for publish-ready AI videos, create `director_selection.json`, `style_recipe.json`, `hook_variants.json`, `hook_score_report.json`, and `reference_overfit_audit.json` before full copy, storyboard, images, TTS, HyperFrames, render, or upload. The newest reference video is only a candidate style card; it must not become the default template.
- Source-led topic title: every AI topic title must first name the concrete software, website, company, model, product feature, release, official doc, or news event, then the practical takeaway. Method-only titles such as `用 ChatGPT 和 Codex 前先写边界清单` are blocking; use source/event-led titles such as `ChatGPT 新增应用调用确认：用 Codex 前先写三层边界清单`.
- Beginner value first: copy must define the viewer task, visible result, first action, saved step, proof screen, plain-language takeaway, and concrete problem example. Run `scripts/score_script.py`, `scripts/evaluate_copy_semantic.py`, and `scripts/validate_beginner_copy.py`; `beginner_value_review.json` must pass and `problem_example_score >= 8.5`.
- Compliance before production: `compliance_report.json` must pass before images, TTS, HyperFrames, render, or publishing. Read `references/global_douyin_text_compliance_rule.md`, `references/forbidden_terms_learning_bank.md`, and active `references/forbidden_terms_learning_bank.jsonl` before writing Douyin-facing text.
- Reference originality: when given a Douyin link, share text, local MP4, screenshots, or "make similar" request, read `references/reference_driven_production_rules.md`; learn pacing, layout, typography, rhythm, filter mood, music/voice relationship, and motion language, but never reuse original frames, subtitles, voice, people, room/product assets, wording, watermark, creator identity, or a highly similar full sequence. Final major on-screen text must stay within 10% character-level deviation from approved original copy.
- Reference video body first: when the user gives a video reference by Douyin link, share text, local MP4, or says "参考这个视频/做得像这个视频", obtain the playable video body before topic lock, copy, storyboard, HyperFrames, render, or delivery. Download the reference video or otherwise create a local playable analysis file, then actually inspect it with ffprobe plus contact sheets/detail frames/manual viewing. The analysis must record duration, aspect, first 3-5 seconds, scene rhythm, layout, text density, motion, and audio/music. Title, thumbnail, share text, URL metadata, music page, or author page alone are not enough. If the video body cannot be obtained, stop with a blocker and ask for the video file, a downloadable reference, screenshots-only approval, or permission to continue without video-reference matching.
- Reference music: if a user-provided Douyin reference video contains background music and the final output is for Douyin, use the reference video's own music or the same Douyin music-page track when technically possible. Do not synthesize/generate a replacement BGM. If the same reference music cannot be obtained or used, record a blocker and ask for the music file, platform same-music selection, or explicit approval to proceed without BGM; do not silently use local generated music, similar stock music, or a rhythm substitute.
- 16:9 proof-first AI format: proof-heavy AI, Codex, Agent, ChatGPT, plugin, and Skill tutorials use `1920x1080`, `fps: 30`. Only lightweight vertical guide/list/card/poster references may use the `1080x1920` AI information-poster exception from `references/reference_driven_production_rules.md`.
- Visual director before HyperFrames: create `visual_style_decision.json` before `visual_style_plan.json`, then background/prompt packs, `storyboard.director_shots`, evidence plan, structured motion, asset manifest, and validation reports before composition. Codex must choose brightness, palette, material, and layout from the topic, copy mood, evidence density, and reference rhythm; do not lock the skill to a light, dark, or repeated default style. Vague "高级/科技感/炫酷/4K/premium tech" prompt language is blocking.
- Fixed production templates before visual work: after `director_selection.json` and `style_recipe.json`, run `scripts/select_fixed_ai_templates.py` and write `internal/fixed_template_selection.json`. This locks one reusable background image asset from `assets/ai_background_templates_fixed/`, one transition/SFX pack, one foreground component pack, and one voice mix profile for the whole video. The report must include `background_template.fixed_asset_path` and `inheritance_contract.fixed_background_asset_required=true`; HyperFrames must use that fixed background file as the base visual layer instead of regenerating a new background. These templates reduce token waste and quality drift, but do not replace topic-specific copy, proof, screenshots, or compliance checks.
- Foreground module construction before HyperFrames: after storyboard and visual style planning, read `references/foreground_module_system.md`, select one M01-M20 parent module per scene, add two to five C01-C30 micro-components that carry the scene's real information, write `internal/foreground_module_plan.json`, run `scripts/check_foreground_module_plan.py`, then generate the HyperFrames-ready foreground render pack with `scripts/render_foreground_module_pack.py` and validate it with `scripts/check_foreground_module_render_pack.py`. Require both `internal/foreground_module_plan_check.json.status="passed"` and `internal/foreground_module_render_check.json.status="passed"` before HyperFrames authoring. The production note should state selected module ids, anchors, phases, text slots, transition ids, render pack paths, and the passed reports, not repeat historical failure reminders.
- Active video contract and regression gate: every AI video must follow `references/shared_video_quality_core.md#ai-video-active-contract-and-regression-gate` before final QA, upload, or publishing. During production, use the positive contract only: fixed premium background as atmosphere, topic-bound foreground modules with real information jobs, named advanced transitions, the approved background-audio mode, true one-frame cover, checked public text, and the user's current Chrome/session. Historical failure wording belongs in automated gate reports and tests only; it is not a planning step or user-facing work note. A failed gate remains blocking and must be reworked before the result can be called final.
- Workflow guard before final: before building or accepting `publish_contract.json`, run `scripts/ai_video_workflow_guard.py --project <project> --phase publish` and require `internal/workflow_guard.json.status="passed"`. This guard is not a report-writing shortcut; it blocks skipped skill workflow artifacts, missing manual frame-review evidence, weak visual-review scores, non-dynamic background/template inheritance, missing center-crop cover proof, missing Qingdou/text checks, and `scheme_7_ai_hot_rank_top5` projects that do not have exactly five scored source-backed rank items. `scripts/produce_ai_video.py` and `scripts/pre_publish_gate.py` must refresh this report automatically, so stale or post-hoc reports cannot be used to call a video final.
- Positive execution language across all steps: topic scan, copy, compliance, voice, cover, layout, render, Qingdou, publish, and cleanup artifacts must state the selected action, selected asset, exact report, exact command, or exact blocker. Do not use old-problem reminders as production work items, such as "avoid old logic", "do not use the previous bad version", "don't forget X", or repeated lists of historical failures. Keep negative vocabulary inside validators, compliance/risk reports, QA failure messages, and tests; when the gate passes, the next step should cite the passed report and continue.
- Public content boundary for recurring daily AI news/tip videos: Qingdou, QA, compliance checks, publish checks, upload checks, and internal workflow names are backstage gates only. Do not put `青豆`, `Qingdou`, `QA`, `发布前检测`, `上传前通过`, `敏感词检测`, or similar internal process wording in public titles, hooks, scripts, subtitles, covers, on-screen text, captions, or topics unless the selected market topic is itself content-compliance tooling. Public copy must be driven by the latest AI/Codex/ChatGPT/Gemini market scan and teach the selected advanced practical insight.
- Layout and transition quality gate: foreground modules may use panels, trays, rails, chips, proof crops, and checklist rows only when they carry the current scene's information. A 45-75 second AI explainer must avoid repeated same-size left-heavy mega-panels as the dominant look; use at least four distinct scene structures when scene count allows. Transitions must visibly move information from the outgoing scene into the next scene. A short abstract sweep is acceptable only as a sub-layer; if contact sheets show 0.4s+ of decoration-only diagonal lines, empty rails, or node sweeps without a source/step/result handoff, restage that boundary before final.
- Premium motion/layout contract: read `references/premium_motion_layout_contract.md` before HyperFrames authoring. During production, write only positive execution choices: named premium information-handoff recipe ids, topic-bound foreground modules, measured three-column grids, aligned icon/title/body baselines, minimum padding, and bottom summary spacing. The historical failure vocabulary is owned by automated QA reports and tests, not by storyboard notes or user-facing work updates. Write `internal/render_layout_manifest.json`, run `scripts/check_motion_layout_contract.py`, and require `internal/layout_motion_contract_report.json.status="passed"` before visual regression or final delivery.
- Background audio hard rule: this user's AI knowledge/Douyin videos have only two allowed background-audio modes. Mode 1 is approved music from the user's music library or an explicitly authorized same-platform Douyin reference track, recorded with source/path/license or reference evidence and ducked below narration. Mode 2 is no background sound: clean human voice/TTS narration only. Do not synthesize, generate, procedurally build, or self-create music, ambience, noise beds, SFX beds, whoosh beds, electric buzz, texture noise, or `sfx-bed.wav`-style continuous background audio. Default for narrated AI tutorials is `voice_only_clean`.
- Natural voice honesty: publish-ready narration needs truthful `metadata.voice`, approved sample evidence, normal default `tts_speed` 0.95-1.03, and a continuous root narration bed. For this user's recurring AI knowledge / daily AI tip videos, the standing voice direction is a powerful professional Chinese male lecturer: firm, energetic, thick enough, and precise; default free-first voice is `edge_tts` `zh-CN-YunyangNeural` at provider rate around `+10%`, with `voice_speed_policy=user_approved_1_1x` when metadata uses `tts_speed: 1.1`. Faster voice such as `1.1x` is allowed only with explicit current-video or standing-user approval, `tts_speed <= 1.10`, provider/sample metadata, and retimed storyboard/HTML from real audio durations. If the user says the voice is too small or not thick enough, do not just raise MP4 volume: rebuild/remix the clean root narration with `references/hyperframes_delivery.md` voice rules and record a voice mix QA report. Do not add background SFX to make the voice feel stronger.
- TTS lock visual rhythm: after real TTS duration is locked, every narrated scene must carry enough visual beats for the locked duration. Use `beat_map`, `visual_beats`, or equivalent scene timing records so the primary information changes at least every 5 seconds. `scripts/produce_ai_video.py` checks this before final delivery.
- Screen text and empty frames: after render, produce `render_text_manifest.json`, proofread against approved storyboard text, check empty-frame risk, and run visual review. Unapproved large text, garbled characters, wrong Chinese, or subjectless frames block final delivery.
- Publish cover is its own artifact and also the designed first frame of the video: before promotion, use the fixed pure cover backgrounds from `assets/ai_cover_backgrounds_fixed_v2/` through `references/fixed_ai_cover_background_rotation.json`, `references/fixed_ai_cover_background_rotation.md`, and `scripts/select_fixed_cover_template.py`, or an explicitly reviewed one-off topic-specific cover. Generate the cover title text during the copy stage, write it to `internal/publish_cover_text.txt`, include that exact text in local compliance with title, caption, topics, subtitles, and screen text, then render the checked text onto the selected pure background inside `recommended_text_safe_rect_px` with `--require-checked-cover-text`. Select by canvas first (`16x9` for 1920x1080, `9x16` for 1080x1920), then rotate sequentially inside that size pool across T01-T10. Save `internal/first_frame_cover.png`, `internal/cover.png`, `internal/publish_cover_report.json`, and `internal/publish_cover_text.txt`; the report must use `cover_type=fixed_pure_background_runtime_text_first_frame`, record `background_contains_text=false`, and prove `checks.dynamic_text_overlay_used=true`. The cover must be actually inserted into the final MP4 as frame 0 only by default, not as a long static intro; at 30fps this means about `0.033s`. If HyperFrames/Remotion cannot emit a true one-frame cover, use FFmpeg overlay on `eq(n,0)` after render while preserving duration and audio timing. Save `internal/actual_frame_000_cover.png` and `internal/actual_frame_001_after_cover.png`; frame 0 must be the cover and frame 1 must already return to the main timeline.
- Qingdou before promotion or upload: exact public title, caption, and topics must pass Qingdou (`轻抖`) together, recorded as `internal/qingdou_keyword_check.json` with `checked_fields=["title","caption","topics"]` and `未检查到敏感词` or equivalent passed status. Local scripts and Creator Center quick checks are not substitutes. The user has given standing authorization for routine Qingdou/Douyin publish-chain browser actions, including text entry, paste/replace, clicking the check button, reading the visible result, and ordinary slider or image security verification when the current environment permits agent handling; execute these routine steps yourself instead of handing the copy/check back to the user. Reuse the user's current logged-in Chrome tab/session, and close any extra tab/window opened for the task after completion. Current-environment browser automation may be used for page input and visible-result reading, but never extract or store credentials, cookies, SMS codes, verification codes, or verification data. Still stop for SMS codes, phone-only login, real-name or account-owner verification, verification that clearly must be completed by the user, or any active browser/tool safety policy that requires fresh action-time confirmation. Narrow exception: if Qingdou only flags a user-required official/platform campaign topic, and the user explicitly says to keep that exact topic after seeing the failed result, record `status: "user_override_accepted"` plus the failed term, risk note, and user approval, then continue; never label this as Qingdou passed, and still rewrite all non-topic title/caption/on-screen hits. Standing topic override: as of 2026-06-21, `#我在抖音聊科技` is approved permanently; if Qingdou only flags `抖音` inside that exact hashtag, record `status: "user_override_accepted"` and do not ask again.
- Qingdou route default: use the user's already logged-in Chrome Qingdou page/session first. Direct API probing is not a production route unless a dedicated checked tool exists and the browser route is unavailable.
- Publish contract before promotion: use `scripts/produce_ai_video.py` as the only production entrypoint. It must write passed `internal/visual_regression_gate.json`, then build `internal/publish_contract.json`, run `scripts/pre_publish_gate.py`, and require `gate.status="passed"` before upload, publishing, or `final/` promotion.
- SAU upload adapter: when the user authorizes using third-party `social-auto-upload`, only enter it through `scripts/douyin_sau_publish.py` after `promote_final` has produced `final/final.mp4`. The adapter must verify `publish_contract.gate=passed`, Qingdou fields, final video, cover files, `video_technical_qa.json`, and `audio_continuity_report.json`; it writes `internal/douyin_sau_upload_report.json`. Default mode is dry-run. Real upload requires `--execute`, and scheduled publishing via `--schedule` is preferred unless the user explicitly authorizes immediate publishing with `--allow-immediate`.
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
-> ai_hot_rank_top5 when scheme_7_ai_hot_rank_top5
-> director_selection + style_recipe + hook_variants + hook_score_report + reference_overfit_audit
-> fixed_template_selection
-> ai_scheme_classification when relevant
-> copy_package + script_score + semantic_review + content_alignment_report + beginner_value_review
-> compliance_report + forbidden-term learning when needed
-> codex_plugin_plan / production_stack when tool workflow is involved
-> reference_analysis when a reference exists
-> visual_style_decision + visual_style_plan + background_prompt_pack + asset_prompt_validation
-> storyboard + storyboard_validation + content_alignment_report refresh + asset_manifest + visual_tone_report + asset_validation
-> foreground_module_plan + foreground_module_plan_check
-> foreground_module_render_manifest + foreground_module_render_check
-> storyboard.audio_locked + continuous narration bed + visual beat lock
-> hyperframes_render_profile + HyperFrames PNG sequence + leading_frame_repair_report
-> fixed pure-background cover selection + first_frame_cover
-> background_audio_decision / metadata background-audio policy
-> voice mix report when narration is processed or music is ducked below narration
-> draft.mp4 + metadata
-> audio_continuity_report + video_technical_qa + frame_review
-> render_text_manifest + screen_text_proofread + empty_frame_report + visual_review
-> render_layout_manifest + layout_motion_contract_report
-> qa_report + production_postmortem
-> publish_cover_report + on_screen_and_publish_text_compliance_report
-> visual_regression_gate
-> provider_usage_audit + qingdou_keyword_check
-> workflow_guard
-> publish_contract + pre_publish_gate
-> promote_final
-> final/final.mp4
-> optional douyin_sau_publish dry-run/execute report when user authorizes upload
```

`scripts/write_hyperframes_render_profile.py` runs before HyperFrames PNG sequence export and writes `internal/hyperframes_render_profile.json` with the stable 1920x1080/30fps serial PNG route. `scripts/repair_hyperframes_leading_frames.py` runs after HyperFrames PNG sequence export and before FFmpeg encoding. It preserves the first sequence file as the later cover slot, moves the first content-bearing main-timeline frame forward to the next frame when the export starts with blank/initialization frames, and writes `internal/leading_frame_repair_report.json`. `scripts/produce_ai_video.py` is the canonical production entrypoint. It runs QA, blocks legacy PIL/rawvideo/card-renderer regressions, verifies stable render profile, audio-locked visual beats, leading-frame repair, real frame 0 / frame 1 cover evidence, and the publish workflow guard, then allows contract gating and promotion. `scripts/run_pipeline.py` is an internal QA-order compatibility runner, not a production entrypoint. `scripts/qa_gate.py` checks the internal draft package and writes QA only. `scripts/build_publish_contract.py` collects final artifacts and reports into one contract. `scripts/pre_publish_gate.py` refreshes `internal/workflow_guard.json`, then validates QA, visual regression, workflow guard, provider usage, Qingdou, text compliance, and cover checks. `scripts/promote_final.py` copies only `final/final.mp4` into `final/` after the contract gate passes, deletes stale extra final artifacts, removes frame sequences and internal draft/intermediate MP4 files, writes `internal/cleanup_report.json`, and records `cleanup_status=final_folder_mp4_only`. `scripts/douyin_sau_publish.py` is a gated upload adapter only; it never replaces QA, Qingdou, workflow guard, cover, audio, or publish-contract gates.

For skill changes, run `scripts/check_golden_project.py` so the bundled golden project still reaches high-quality QA.

## Reference Loading Map

Load only the relevant references for the task:

- Always for full production: `workflow_contract.md`, `video_quality_contract.md`, `premium_video_quality_playbook.md`, `shared_video_quality_core.md`, `free_first_open_source_stack.md`, `runtime_decision_matrix.md`, `timeline_contract.md`.
- Topic and copy: `topic_selection_rules.md`, `beginner_copywriting_rules.md`, `script_quality_rules.md`, `creative_rubric.md`.
- Compliance and publishing: `global_douyin_text_compliance_rule.md`, `forbidden_terms_learning_bank.md`, `douyin_compliance_rules.md`, `post_publish_review.md`.
- Reference-led work: `reference_driven_production_rules.md`, `reference_video_rules.md`, `video_style_router.md`; for short Codex operation references, also read `codex_operation_micro_tutorial_style.md`.
- AI schemes and orchestration: `video_director_orchestrator.md`, `reference_style_cards.json`, `component_motion_registry.json`, `hook_pattern_bank.md`, `copy_hook_scoring_rules.md`, `ai_video_scheme_library.md`, `ai_video_scheme_1_skill_recommendation_no_voice.md`, `ai_video_scheme_7_hot_rank_top5.md`, `ai_video_scheme_7_ant_ai_hotlist_extended.md`, `ai_reference_video_outcome_registry.md`.
- Visual direction and assets: `fixed_ai_production_templates.md`, `fixed_ai_background_template_rotation.json`, `fixed_ai_transition_sfx_packs.json`, `fixed_ai_component_template_packs.json`, `fixed_ai_voice_mix_profiles.json`, `foreground_module_system.md`, `foreground_art_module_library_v1.md`, `foreground_art_module_library_v2.md`, `foreground_art_module_library_v2.json`, `foreground_micro_component_library_v1.md`, `foreground_micro_component_library_v1.json`, `premium_motion_layout_contract.md`, `visual_description_language_reference.md`, `visual_prompt_motion_phrasebook.md`, `ai_generated_asset_prompt_system.md`, `visual_sync_rules.md`, `visual_aesthetic_rules.md`, `hyperframes_components.md`.
- Cover system: `fixed_ai_cover_background_rotation.md`, `fixed_ai_cover_background_rotation.json`, and `assets/ai_cover_backgrounds_fixed_v2/README.md`.
- HyperFrames delivery: `premium_ai_video_source_to_hyperframes_rule.md`, `hyperframes_delivery.md`, `codex_three_skill_video_playbook.md`, `codex_skill_tutorial_video.md`.
- Evidence plugins: `codex_plugin_integration.md`.
- Learning layer: `learning_bank.md`, `failed_case_library.md`, `director_decision_patterns.md`.

## Use When

- The user asks for AI, AI 热榜/TOP5/榜单, ChatGPT, Codex, Agent, automation, AI video, AI tool, plugin, model, or source-backed tutorial Douyin content.
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
