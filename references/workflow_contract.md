# Workflow Contract

This is the hard production contract for V3. Do not treat it as guidance. It defines what may happen next.

## Artifact Gates

0. Decide video style routing first for every video request. Read `references/video_style_router.md` and `references/shared_video_quality_core.md`; route renovation and beauty work to their owning skills before using this AI pipeline.
0.1. Highest-grade mode is the default. If the user did not explicitly ask for research-only, planning-only, quick draft, smoke test, or mock validation, treat the task as publish-ready and enforce all final gates.
0.2. A low-tier fallback MP4, template slideshow, single-image narration, generic Ken Burns render, no-audio render, unreviewed TTS render, or no-QA render must not be promoted, named, or described as final.
0.3. Decide input mode for AI knowledge videos. Reference provided -> Reference Mode. No reference -> Self-Research Mode with current AI-topic/source research.
0.3.0. Self-Research Mode for the user's recurring AI videos must scan four current angles before copywriting: broad AI news, Codex/OpenAI, ChatGPT/OpenAI, and Gemini/Google AI. Start with the task date. If a direction has no strong same-day signal, expand only to the latest 7 calendar days and mark the source window in `hot_topic_scan_report.json`. Sources older than 7 days may be recorded as `background_only`, but they do not satisfy the current-angle scan and must not be used to make a stale topic look fresh.
0.3.1. For AI/tool/Codex videos, run the director orchestrator before copywriting or storyboard. Read `references/video_director_orchestrator.md`, then create `internal/director_selection.json`, `internal/style_recipe.json`, `internal/hook_variants.json`, `internal/hook_score_report.json`, and `internal/reference_overfit_audit.json`. The orchestrator must classify the production scheme with `references/ai_video_scheme_library.md`, select reference cards as candidates rather than templates, choose one main visual family for the whole video, choose a component/motion mix, write `audio_music_decision`, score at least 10 hook variants, and prove the latest reference is not the default. A short vertical no-voice Skill/tool recommendation reference must be classified as `方案1: Skill 推荐无人声`; apply `references/ai_video_scheme_1_skill_recommendation_no_voice.md` and lock `content_job_lock` before rendering. AI hot-rank/countdown requests such as `AI 热榜 TOP5`, `TOP5`, `榜单`, `排行`, or `排名` must be classified as `方案7: AI 热榜 TOP5 榜单`; apply `references/ai_video_scheme_7_hot_rank_top5.md`, fill `templates/ai_hot_rank_top5.template.json`, and lock exactly five scored source-backed rank items before copywriting or rendering.
0.3.1.2. `audio_music_decision` is required before storyboard, TTS, HyperFrames, BGM selection, or audio mix. It must record `music_policy` (`required_bgm`, `optional_low_bed`, or `no_bgm`), `bgm_source_priority`, `voice_policy`, `voice_priority`, `sfx_required`, and `mix_note`. Scheme 1 and Scheme 7 default to `required_bgm`; Scheme 2 and Scheme 6 default to `no_bgm`; Scheme 3, Scheme 4, and Scheme 5 default to `optional_low_bed`. Reference-led audio may override the default only when documented in reference analysis. Explicit no-music user requests set `music_policy=no_bgm`.
0.3.1.1. After `director_selection.json` and `style_recipe.json`, select reusable fixed production templates with `scripts/select_fixed_ai_templates.py` and write `internal/fixed_template_selection.json` before visual style planning, background prompts, storyboard, TTS, HyperFrames, render, or upload. This report must lock one dynamic background MP4 from `assets/ai_background_templates_dynamic/` through the fixed background choice in `references/fixed_ai_background_template_rotation.json`, lock one transition/SFX pack from `references/fixed_ai_transition_sfx_packs.json`, one foreground component pack from `references/fixed_ai_component_template_packs.json`, and one voice mix profile from `references/fixed_ai_voice_mix_profiles.json`. It must include `background_template.render_asset_path`, `background_template.render_asset_is_dynamic=true`, `inheritance_contract.dynamic_background_default=true`, and `inheritance_contract.static_background_fallback_removed=true`. `background_template.fixed_asset_path` may exist only as a legacy alias to the same dynamic MP4 path; it must not point to a static PNG. The selected templates govern the whole video; do not randomly switch art systems scene by scene.
0.3.2. After QA for any reference-led AI video, update `references/ai_reference_video_outcome_registry.md` with scheme, reference source, output project, QA status, publish status, lessons, and reuse decision. This registry is the counting layer for future AI style-direction statistics.
0.4. If the video teaches, compares, or claims use of Codex plugins, or if an AI tool/tutorial needs source-backed proof, read `references/codex_plugin_integration.md` before copy/storyboard lock and include `storyboard.codex_plugin_plan`; if it says "six plugins", document Browser, GitHub, Hugging Face, HyperFrames, OpenAI Developers, and HeyGen with availability, role, boundary, fallback, and evidence requirements. HyperFrames is the final assembly engine, not the only plugin.
0.5. For every premium AI explainer, read `references/premium_ai_video_source_to_hyperframes_rule.md`, `references/visual_description_language_reference.md`, `references/ai_generated_asset_prompt_system.md`, and `references/enterprise_ai_control_console_visual_system.md` before copywriting or HyperFrames work. Source research, plain-language copy, sentence-to-visual storyboard, asset/image prompt plan, foreground UI system, caption system, motion language, and HyperFrames visual identity are required before rendering.
0.6. Proof-heavy AI knowledge videos and AI explainers must use 16:9 horizontal `1920x1080`. This includes AI news, AI tools, ChatGPT, Gemini, OpenAI, Codex, Agent, automation, AI coding, AI workflow, plugin, and Skill tutorials when they depend on readable sources, screenshots, code, docs, and diagrams. Do not switch to 9:16 merely because the destination is Douyin. Exception: reference-driven lightweight guide/list/card/poster explainers may use 9:16 `1080x1920` only under `references/reference_driven_production_rules.md`, with originality, safe-zone, text accuracy, compliance, and QA gates intact.
0.7. AI knowledge videos must pass the background-first and visual-asset-director gates before storyboard, assets, TTS, HyperFrames, render, or upload: create `internal/visual_style_decision.json` first, then `internal/visual_style_plan.json`, `internal/background_prompt_pack.md`, and `internal/ai_asset_prompt_pack.md` or equivalent notes using `references/visual_description_language_reference.md`; select one text-free dynamic background MP4 through `internal/fixed_template_selection.json`; and register any additional generated support assets in `asset_manifest.json` with a specific support role, never proof. The visual style decision must be made by Codex from topic type, copy mood, evidence density, and reference-video rhythm when present; it must not reuse light, dark, or `daylight_productivity` as a fixed default. For recurring/daily AI videos, choose the background once per video by scheme, aspect, semantic fit, and sequential rotation; do not use the old random background style pool and do not regenerate a new background from prompts unless the user explicitly approves replacing the fixed library. The selected dynamic background asset must drive the whole foreground UI system, not only the background: `visual_style_plan.json` must document `foreground_ui_system`, `caption_system`, `local_readability_treatment`, `component_families`, `motion_vocabulary`, `transition_language`, `sfx_character`, and `technology_restraint_policy` according to `references/enterprise_ai_control_console_visual_system.md`. The visual style decision must record `style_intent`, `selected_brightness_grade`, `selected_palette_family`, `selected_material_family`, `selected_layout_family`, `why_this_style`, and `why_not_other_styles`. The visual style plan must match that decision and lock `scene_function`, `visual_archetype`, `brightness_grade`, `palette_family`, `material_family`, `layout_family`, bright/dark rhythm, and diversity limits before individual prompts are written. The prompt pack and manifest must document `visual_thesis`, `background_template_id`, `background_render_asset_path`, `topic_binding`, `beginner_usefulness`, `information_job`, `background_role`, `scene_id`, `narration_line_supported`, `viewer_takeaway`, `composition`, `foreground`, `midground`, `background`, `camera_lens`, `lighting`, `material_texture`, `color_hierarchy`, `color_system`, `depth_layering`, `text_safe_zones`, `motion_usage`, `animation_affordance`, `primary_animated_object`, `dark_light_motion_rule`, `negative_prompt`, `regeneration_criteria`, and `diversity_check` so every support image is visibly connected to the selected topic instead of being a generic premium stage. Generated support visuals must use `gpt-image-2` or Codex built-in ImageGen and must record `model`, `prompt_id`, `prompt_path`, `unique_prompt=true`, and `evidence_boundary`. Do not require the user to create `OPENAI_API_KEY` merely because they use paid Codex. If a dynamic background file is missing, stop and regenerate/replace the background library before continuing.
0.7.1. Premium AI foreground construction must use `references/foreground_module_system.md` before HyperFrames authoring. The readable design source is `references/foreground_art_module_library_v1.md`; the execution addendum is `references/foreground_art_module_library_v2.md` plus `references/foreground_art_module_library_v2.json`; the small embedded parts come from `references/foreground_micro_component_library_v1.md` plus `references/foreground_micro_component_library_v1.json`. For each storyboard scene, write `internal/foreground_module_plan.json` with one M01-M20 parent module, that module's text slots, two to five C01-C30 micro-components, anchors, phases, instance counts, transition ids, and scene aspect/layout mode. Run `scripts/check_foreground_module_plan.py --project <project>` and require `internal/foreground_module_plan_check.json.status="passed"`. Then run `scripts/render_foreground_module_pack.py --project <project>` and `scripts/check_foreground_module_render_pack.py --project <project>` to create and validate `internal/foreground_module_render_pack.html`, `internal/foreground_module_render_manifest.json`, `internal/foreground_module_render_check.json`, and `assets/hyperframes/foreground_modules/`. Require `foreground_module_render_check.status="passed"` before asset rendering, HyperFrames authoring, final render, QA, upload, or publishing. The render manifest must record `render_contract.glass_transparency.profile="glass_transparency_v2"`, prove the foreground stage is transparent, and keep large module/proof/caption/micro-component fills at or below alpha `0.34` so the selected dynamic MP4 remains visible behind readable text. The production artifact must record positive selected module ids, render pack paths, glass transparency evidence, and reasons; old failure reminders belong only in validators, QA reports, tests, or blocked audit output.
0.8. Do not hard-cut or replace the visual page while narration is mid-sentence. Storyboards must mark scene/page switches at sentence end, breath pause, chapter pause, or a documented visual handoff with an 8-14 frame overlap.
0.9. HyperFrames visual transitions must not control narration. Before render, lock a continuous root narration bed or prove root-level per-scene audio is scheduled back-to-back with `max_audio_gap_ms <= 120`; transitions may overlap visuals but must not restart, mute, fade, or gap the voice. TTS lock must write real durations back to scene `duration_target` and `storyboard.director_shots[*].duration_sec`; mismatched director/scenes/audio timings block render and promotion. After TTS lock, every narrated scene must expose enough `beat_map`, `visual_beats`, or equivalent timing records for the locked duration; the production gate uses a maximum of 5 seconds per visual beat.
0.10. Before each new AI video, read `references/learning_bank.md`, `references/failed_case_library.md`, and `references/director_decision_patterns.md` as the soft learning layer. Apply repeated lessons to topic selection and storyboard decisions, but do not auto-edit hard rules without user approval.
0.11. Before writing public-facing title, caption, hashtag/topic, cover text, subtitle text, or on-screen text, read `references/forbidden_terms_learning_bank.md` and active records in `references/forbidden_terms_learning_bank.jsonl`; avoid learned forbidden/sensitive/risky terms in the first draft. If any local/Qingdou/Douyin/manual check later detects a risky term, run `scripts/update_forbidden_terms.py` and save `internal/forbidden_terms_update_report.json` before rewriting and rerunning checks.
0.12. Global Douyin text compliance applies across all owning skills and video types. Any designed text in the video, including title cards, subtitles, cover text, poster/card text, badges, labels, CTA, stickers, and text overlays, must be checked before final render/QA. The exact publish title, caption/body, and hashtags/topics must be checked together before upload or publish.
0.13. AI topic titles must name the concrete object/source and the event/feature/news/official source before the practical takeaway. A title like `用 ChatGPT 和 Codex 前先写边界清单` is method-only and must be rejected; use a source/event-led shape such as `ChatGPT 新增应用调用确认：用 Codex 前先写三层边界清单`. If `title_direction` does not clearly name a software, website, company, model, feature, release, official doc, product page, or news event, do not select the topic and do not write copy.
0.14. AI video regression prevention is a hard gate. Before promoting or publishing, review `references/shared_video_quality_core.md#ai-video-regression-prevention` and prove the render did not fall back to old low-grade patterns: unused background modules, fake framework boxes, old/non-premium backgrounds, ordinary transitions, silent dynamic icons/status feedback, SFX that masks narration, missing or overlong first-frame cover, unchecked changed cover/on-screen/publish text, unnecessary new Chrome windows, or a render-only final without visual/audio evidence. If any item is present, stop and rework before final QA, upload, or publishing.
1. `topic_candidates.json` does not exist -> do not write full copy.
1.0.1. For `scheme_7_ai_hot_rank_top5`, `internal/ai_hot_rank_top5.json` or `internal/hot_rank_scan_report.md` does not exist -> do not write full copy. The rank file must contain exactly five items, each with source title, source URL or evidence note, visible date, rank score, score breakdown, why-it-matters, viewer action, and risk flags, sorted descending by `rank_score`.
1.1. `topic_candidates.scored.json` contains a selected candidate with `method-only topic title`, `topic title must name a concrete AI object`, or `topic title must name a concrete event/feature/news/official source` in `validation_issues` -> do not create `selected_topic.json`; research again.
2. `selected_topic.json` does not exist -> do not create copy package.
2.1. `director_selection.json`, `style_recipe.json`, `hook_variants.json`, `hook_score_report.json`, or `reference_overfit_audit.json` is missing/not passed for a publish-ready AI video -> do not write full copy, storyboard, generate assets, TTS, render, or upload. `director_selection.json` and `style_recipe.json` must include `audio_music_decision`; if it is missing, do not storyboard, choose BGM, generate TTS, or mix audio.
2.2. `fixed_template_selection.json` is missing/not passed for a publish-ready AI video -> do not create `visual_style_plan.json`, background prompts, storyboard visual shapes, TTS, HyperFrames scenes, render, or upload. The report must prove `background_template.render_asset_path` exists and is a dynamic MP4, `background_template.render_asset_is_dynamic=true`, `background_drives_foreground`, `dynamic_background_default`, `static_background_fallback_removed`, `fixed_background_asset_required`, `transition_pack_drives_sfx`, `component_pack_drives_storyboard_shapes`, and `voice_profile_drives_tts_and_mix`.
3. `copy_package.md` and `copy_package.json` do not exist -> do not create storyboard.
4. `script_score.json` is missing or not strong enough -> do not create storyboard.
5. `semantic_review.json` is missing or not `passed` -> do not create storyboard.
5.1. `beginner_value_review.json` is missing, not `passed`, or below beginner thresholds -> do not create storyboard.
5.2. `content_alignment_report.json` is missing or not `passed` -> do not create storyboard, TTS, HyperFrames, render, or final QA. It must prove source-claim alignment, copy progression, visual alignment, and Chinese-first visible text. Each important claim needs `source_ids` or concrete evidence, each scene needs one `new_information_job`, each visual needs a `visual_job` tied to the current copy/claim, and non-essential English visible text must be rewritten into Chinese.
6. `compliance_report.json` is missing or not `passed` -> do not generate images, TTS, HyperFrames scenes, or video.
6.1. `compliance_report.json`, `on_screen_and_publish_text_compliance_report.json`, Qingdou, Douyin upload, or manual review detects any forbidden/sensitive/risky term -> record it in `references/forbidden_terms_learning_bank.jsonl` with `scripts/update_forbidden_terms.py`, then rewrite and rerun checks.
7. `reference_analysis.json` is required when the user provides a reference video/link/share text.
8. `storyboard.json` does not exist -> do not generate TTS or assets.
9. `storyboard_validation.json` is missing or not `passed` -> do not generate TTS or assets. Storyboard validation must include phone-safe margins and normal TTS speed metadata.
10. `asset_manifest.json` does not exist or lacks asset source classes/provider notes -> do not build HyperFrames.
10.0. `visual_style_decision.json` or `visual_style_plan.json` is missing for a publish-ready AI tutorial, the decision fields are incomplete, the plan does not match the decision, or generated visuals lack scene function, brightness grade, palette family, material family, layout family, color system, depth/layering, primary animated object, dark/light motion rule, or diversity check -> do not generate assets and do not build HyperFrames.
10.0.1. `foreground_module_plan.json`, `foreground_module_plan_check.json`, `foreground_module_render_manifest.json`, or `foreground_module_render_check.json` is missing for a publish-ready AI knowledge video, or either check status is not `passed` -> do not generate foreground assets, do not author HyperFrames, do not render, and do not publish. The checks must prove parent M ids, C ids, text slots, anchors, phases, transition ids, visual budgets, motion budgets, visible instance counts, animation concurrency, scene DOM, micro-component DOM, runtime CSS/JS, parent-module render contract, and Glass Transparency v2 are valid for the selected aspect and layout.
10.1. Generated/support visuals are planned or used, but `internal/ai_asset_prompt_pack.md` or equivalent production notes are missing, `internal/asset_prompt_validation.json` is missing/not passed, or generated visual manifest entries lack complete visual director fields -> do not generate assets and do not build HyperFrames.
11. `asset_validation.json` is missing or not `passed` -> do not build HyperFrames.
11.1. Generated/support visuals have been created but `visual_tone_report.json` reports over-dark L4/L5 scenes, crushed L1/L2 proof scenes, insufficient bright proof surfaces, or teal/blue-only palette bias -> regenerate or restage the visuals before HyperFrames.
12. `storyboard.audio_locked.json` does not exist -> do not render HyperFrames.
12.0.1. After `storyboard.audio_locked.json` is written, long narrated scenes must be split into enough visible beats. `scripts/produce_ai_video.py` checks the locked duration and requires one visual beat per 5 seconds at minimum; if a scene falls short, add beat records, split the scene, or rewrite the line before render.
12.1. AI knowledge videos must select or design the publish cover before final render when the cover is intended to be the first frame. `internal/first_frame_cover.png`, `internal/cover.png`, `internal/publish_cover_text.txt`, and `internal/publish_cover_report.json` or an approved custom cover report must exist before final QA. For 16:9 proof-first videos, cover text must be compact and placed in the center-crop-safe text rectangle so Douyin's default middle cover preview can show the full topic text; also write `internal/cover_publish_douyin_center_crop.png` as the preview evidence. The final MP4 must contain the cover as frame 0 only by default, not as a long static intro. At 30fps this is about `0.033s`; do not insert a 0.5s/1s cover opening, do not add silence, and do not shift narration timing unless the user explicitly asks for a visible cover intro. If the renderer cannot place a true single-frame cover, post-process the final MP4 with FFmpeg overlay on `eq(n,0)` and preserve original duration/audio.
13. `metadata.json` does not exist or has accelerated `tts_speed` without explicit user approval and synced audio timing -> do not run final QA.
13.1. `metadata.voice` uses macOS `say`, Apple/system voices such as `Tingting`, scratch timing previews, or a relabeled local system provider without explicit lower-quality user approval -> do not run final QA or promote as publish-ready.
13.4. If HyperFrames PNG sequence is used, run `scripts/write_hyperframes_render_profile.py --project <project>` before export and write `hyperframes_render_profile.json`; the profile must use `render_mode=png_sequence`, `render_target=project_directory`, `command_cwd=<project>`, `worker_count=1`, `max_worker_count=1`, and `protocol_timeout_ms >= 900000`. Render from the project directory with `npx --yes hyperframes render --format png-sequence ...`; do not pass `index.html`, `assets/hyperframes/index.html`, or any other HTML file as the render target.
13.5. If HyperFrames PNG sequence is used, run `scripts/repair_hyperframes_leading_frames.py` before FFmpeg encoding and write `leading_frame_repair_report.json`; if the report status is not `passed`, do not encode `draft.mp4`.
14. `draft.mp4` is missing or empty -> do not run final QA.
15. `audio_continuity_report.json` is missing or not `passed` -> do not run final QA, do not create `final/final.mp4`, and do not publish.
16. `video_technical_qa.json` is missing or not `passed` -> do not create `final/final.mp4`.
17. `frame_review_report.json` is missing -> do not create `final/final.mp4`.
18. `visual_review.json` is missing or not `passed` -> do not create `final/final.mp4`.
19. `qa_report.json` is missing or not `passed` -> do not create `final/final.mp4`, do not publish, and do not present the video as final.
20.0.0. `layout_motion_contract_report.json` is missing or not `passed` when `fixed_template_selection.motion_layout_contract` exists -> do not pass `visual_regression_gate`. This report must be written by `scripts/check_motion_layout_contract.py` and prove no banned low-grade motion, enough named premium transition recipes, measured text boxes, no text overflow or collisions, and aligned three-column grid checks when a three-column component is used.
20. `visual_regression_gate.json` is missing or not `passed` -> do not create `final/final.mp4`, do not publish, and do not present the video as final. This gate must be written by `scripts/produce_ai_video.py` and must prove no legacy PIL/rawvideo/card renderer, HyperFrames final source exists, frame 0 matches `first_frame_cover.png`, frame 1 has returned to the main timeline, designed support cards/source-summary cards do not contain baked blank decorative highlight blocks, and foreground module render checks have not failed Glass Transparency v2.
20.0.2. If `visual_regression_gate.support_card_blank_blocks.status` is not `passed`, the video must be restaged before final promotion. The fix is to rebuild the support/source card as clean content or move the visual structure into foreground HTML/CSS/GSAP modules; do not keep image-baked empty white/gold/glass plates, decorative boards, or ornamental slabs.
20.0.1. `provider_usage_audit.json` is missing or not `passed` -> do not create `final/final.mp4`, do not publish, and do not present the video as final.
20.1. `qingdou_keyword_check.json` is missing, not `passed`, does not include `title`, `caption`, and `topics` in `checked_fields`, or its final check does not prove `未检查到敏感词` -> do not build a passing publish contract, do not run `promote_final.py`, do not upload to Douyin, and do not publish. The exact title, publish caption, and hashtags/topics intended for Douyin must be checked together, rewritten if Qingdou reports sensitive words, and checked again before publishing. Exception: `status: "user_override_accepted"` may continue only when Qingdou flags a user-required official/platform campaign topic, the user explicitly accepts that failed topic after seeing the result, and all title/caption body/on-screen hits have been rewritten cleanly.
20.1.0. The exact required hashtag `#我在抖音聊科技` has standing approval from the user as of 2026-06-21. If Qingdou only flags `抖音` inside this exact hashtag, set `qingdou_keyword_check.status="user_override_accepted"` with the standing approval text and continue without asking again. This remains a narrow topic override, not a Qingdou pass, and it must not cover any other term, topic, title, caption body, subtitle, cover text, or on-screen text.
20.1.1. The user has granted standing authorization for routine Qingdou/Douyin publish-chain browser actions, including text entry, paste/replace, clicking the check button, reading the visible result, and ordinary slider or image security verification when the active environment permits agent handling. Execute these routine steps directly; do not require the user to paste copy, click the check button, or handle normal Qingdou checks manually by default. Reuse the user's current logged-in Chrome tab/session, and close any extra tab/window opened for the task after completion. Current-environment browser automation may be used for page input and visible-result reading. The default route is the already logged-in Chrome Qingdou page/session; direct API probing is not a production route unless a dedicated checked tool exists and the browser route is unavailable. For the browser route, first run `scripts/qingdou_browser_check.py --project <project> --mode prepare --set-clipboard`, then use the prepared bookmarklet in the current Qingdou tab so the page itself clears the rich-text editor, inserts the exact publish text, verifies the text match, and clicks the check button. Chrome may strip a pasted `javascript:` prefix from bookmarklets; when that happens, type the ASCII prefix manually or paste `qingdou_check_text.txt` into the empty Qingdou input and verify the visible character count before clicking the page button. Record `passed` only with `scripts/qingdou_browser_check.py --project <project> --mode record-passed --visible-message "未检查到敏感词"` after reading the visible result. If Qingdou only flags `抖音` inside the fixed required hashtag `#我在抖音聊科技`, record the narrow standing override with `scripts/qingdou_browser_check.py --project <project> --mode record-user-approved-topic --visible-message "检查到敏感词 1 个" --term "抖音"`. If the page is blank, the text mismatches, the result is unreadable, or verification appears, run `record-blocked` and stop before `publish_contract`. Stop only for SMS verification, phone-only login recovery, real-name/account-owner checks, verification that clearly must be done by the user, or any active browser/tool safety rule that requires fresh action-time confirmation. Never bypass verification, guess codes, store credentials, cookies, SMS codes, verification codes, or verification data, and never mark Qingdou as passed without visible passed evidence.
20.2. Designed video text, including screen text, subtitles, cover text, poster/card text, labels, stickers, and CTA, has not been locally checked against Douyin risk rules and the learned forbidden-term bank -> do not promote, upload, or publish.
20.3. `publish_cover_report.json` is missing, not `passed`, uses `frame_grab_used=true`, or does not prove `publish_cover_text.txt` was written -> do not build a passing publish contract. A publish cover must be a standalone designed first-frame artifact from the fixed pure cover backgrounds in `assets/ai_cover_backgrounds_fixed_v2/`, selected through `references/fixed_ai_cover_background_rotation.json` and `scripts/select_fixed_cover_template.py`, or an explicitly reviewed one-off designed cover. Cover text must be generated during copywriting, written to `publish_cover_text.txt`, checked in local compliance before final production, and rendered with `--require-checked-cover-text` as a controlled post layer inside the manifest safe rectangle. For 16:9 covers, the controlled post layer must also fit the Douyin center crop preview: `checks.cover_text_fit_safe_rect=true`, `checks.primary_text_inside_douyin_center_crop=true`, `checks.douyin_center_crop_preview_generated=true`, and `checks.compact_cover_text_used=true`. The final MP4 must also prove the cover was actually inserted as frame 0 only: save `internal/actual_frame_000_cover.png` and `internal/actual_frame_001_after_cover.png`, record `metadata.quality_spec.first_frame_cover_overlay_frames=1`, and verify frame 1 has returned to the main video timeline. A long static cover intro is a failure unless explicitly user-approved.
20.3.1. For AI knowledge videos, `publish_cover_report.json` must record `cover_type=fixed_pure_background_runtime_text_first_frame`, `template_id`, `canonical_id`, `template_path`, `template_aspect`, `template_rotation_index`, `selection_method=sequential_by_size_pool`, `template_library_size=10`, `background_contains_text=false`, `recommended_text_safe_rect_px`, `cover_layout.text_bbox_px`, `cover_layout.douyin_center_crop_rect_px`, `accent_rgb`, and `checks.template_from_fixed_library=true`. Select the pool by final canvas first (`16x9` for 1920x1080 proof-first videos, `9x16` for rare 1080x1920 information-poster videos), then advance the next T01-T10 background in that pool. One-off generated covers require explicit user approval after seeing the design.
20.3.2. Before building `publish_contract.json`, `scripts/produce_ai_video.py` must write `publish_evidence_preflight.json` and prove the strict publish evidence exists: `provider_usage_audit.json`, `on_screen_and_publish_text_compliance_report.json`, `publish_cover_report.json`, and `qingdou_keyword_check.json`. If this preflight is not `passed`, stop before `build_publish_contract.py` so the missing evidence is explicit.
20.4. `publish_contract.json` is missing or `gate.status` is not `passed` after `scripts/pre_publish_gate.py` -> do not upload, publish, or copy anything into `final/`.
20.4.1. Third-party SAU upload may run only through `scripts/douyin_sau_publish.py`. Direct `sau douyin upload-video` is not a production route for this skill because it can click the platform publish button. The adapter must first verify `publish_contract.gate.status="passed"`, `final/final.mp4`, cover files, Qingdou title/caption/topics evidence, `video_technical_qa.status="passed"` with `audio.has_audio=true`, and `audio_continuity_report.status="passed"` with `audio.has_audio=true`. Default mode is dry-run and writes `internal/douyin_sau_upload_report.json`; real upload requires `--execute`. If no `--schedule` is supplied, real upload also requires explicit `--allow-immediate`.
20.5. After promotion, `final/` must contain only `final.mp4`. Stale cover, metadata, publish-copy, contract, or alternate cover files in `final/` are cleanup failures. Frame sequences and internal draft MP4 files must be removed unless the user explicitly asks to preserve debugging artifacts.
21. `production_postmortem.json` should be generated after QA for learning and debugging. It is not allowed to override failed QA and must not rewrite hard rules automatically. If the project is a reference-led AI video, `references/ai_reference_video_outcome_registry.md` should also be updated before the run is considered learned.
22. Only `scripts/promote_final.py` may copy pre-publish-gated artifacts into `final/`, and it must consume the passed `publish_contract.json`.

## Highest-Grade Release Bar

Before any final delivery, prove the output passed the highest-grade bar for its domain:

- correct owning skill selected by `video_style_router`
- domain-specific contract passed
- `shared_video_quality_core` checks applied
- scene timeline and caption-template plan exist
- AI explainer format decision exists; AI knowledge/tutorial videos use the required 16:9 `1920x1080` proof-first canvas
- generated/support visuals have art-direction notes and evidence boundaries
- generated/support visuals have a prompt pack with asset role, scene/narration purpose, composition, camera, material, lighting, text-safe zones, negative prompt, regeneration criteria, per-asset `prompt_id`, and provider/model proof for `gpt-image-2` or Codex built-in ImageGen
- background prompts describe `visual_thesis`, `topic_binding`, `information_job`, `background_role`, spatial role, material, lighting, camera, text-safe zones, and avoid rules instead of vague "high-tech" words
- foreground UI, captions, transitions, and SFX inherit one selected AI visual system from `references/enterprise_ai_control_console_visual_system.md`; the result must not look like PPT cards pasted over a technology background
- fixed production templates are locked once per video in `internal/fixed_template_selection.json`; background must cite `background_template.render_asset_path`, and foreground components, transitions/SFX, and voice mix must cite the selected template ids
- foreground construction plan and render pack exist and passed: each scene selects one M01-M20 parent module from the v1/v2 library, uses compatible C01-C30 micro-components only as embedded information parts, records anchors, phases, transition ids, text slots, budgets, and animation concurrency, then produces HyperFrames-ready HTML/CSS/JS foreground DOM
- motion prompts describe information purpose, actor, path, timing, easing, continuity, and audio bridge
- production postmortem records what worked, what failed, bottlenecks, next-run decisions, and proposed rule changes
- narration uses a continuous root audio bed or documented root-level scene audio schedule; visual transitions never cut voice playback
- style frames or representative native-size frames were inspected
- source-to-visual mapping exists for every important voiceover sentence
- visual/page transitions are locked to sentence/breath/chapter boundaries and do not break speech
- ImageGen prompts, if used, document use case, visual metaphor, safe composition, material/light/texture, and negative prompts
- contact sheet and crowded-frame detail checks exist
- audio duration is not shorter than video duration
- transition boundaries do not introduce voice gaps, restarts, muting, or fade-outs
- captions match the current visual scene
- final render uses high-quality settings and is not visibly soft or template-like
- final folder contains only `final/final.mp4`, with required cover, metadata, contract, and publish-copy artifacts kept in `internal/` instead of duplicated into `final/`

If any item is missing, stop and report the missing gate instead of delivering `final`.

## Phone-Safe Canvas And Voice Speed

- In 1920x1080 AI knowledge videos, proof panels, screenshots, code, captions, titles, and CTA must stay inside a horizontal proof-safe canvas with lower-third caption space and a side annotation rail.
- In rare non-AI 1080x1920 vertical videos, critical content must stay inside top >= 240px, bottom >= 360px, left >= 72px, and right >= 180px. Generated images must include this top/bottom breathing room before text is added; do not rely on later overlays to hide cropped content.
- Default narration speed is normal `tts_speed: 1.0`; allowed default range is 0.95-1.03.
- If a line is too long, split the scene or shorten the copy. Do not use accelerated TTS to force timing.
- If the user explicitly asks for a faster voice style such as `1.1x`, set `voice_speed_policy=user_approved_1_1x`, keep `tts_speed <= 1.10`, document the approval, regenerate the voice sample, rebuild the continuous root narration bed, and sync storyboard/director/HTML timing from real audio durations.
- Standing user preference for recurring AI knowledge / daily AI tip videos: use a powerful professional Chinese male lecturer voice, not a soft or generic explainer voice. Preferred free-first voice is `edge_tts` `zh-CN-YunyangNeural` with provider rate around `+10%`; metadata must record male voice direction, real provider, voice id, rate, approval basis, and regenerated audio-lock timing.
- Legacy automation or prompt text that asks for `1.2x`, `1.12x`, `约 1.2 倍语速`, or any `tts_speed > 1.10` is obsolete and must be treated as invalid. Rewrite the automation/run instructions before TTS, storyboard lock, QA, render, or upload; never encode `tts_speed=1.2` in metadata to satisfy an old prompt.

## Free-First Runtime And Timeline

- Default provider policy is `free_first_local_or_authorized_openai_only`.
- Do not use ElevenLabs, Runway, Kling, HeyGen, Resemble, Veo, paid stock/design/video platforms, subscription asset services, Pinterest scraping, or unapproved paid APIs.
- Storyboards must document runtime choice, caption template plan, and timeline contract reference.
- AI tool/plugin/tutorial storyboards must document `codex_plugin_plan`; HeyGen must be approval-required unless the user explicitly authorized that specific account/credit/upload path.
- Every scene visual must document `asset_source_type` and `caption_template`.
- Every asset manifest item must document provider/source role and `asset_source_type`.
- Remotion is for component clips/data visuals, HyperFrames is the final timeline, and FFmpeg/MoviePy are only for mechanical media processing.

## Ten-Step Flow

0. Input Mode Routing -> reference analysis when provided, or current AI hot-topic research when no reference is provided
1. Topic Research -> `topic_candidates.json`
2. Topic Decision -> `selected_topic.json`
3. Director Orchestrator -> `director_selection.json`, `style_recipe.json`, `hook_variants.json`, `hook_score_report.json`, `reference_overfit_audit.json`
3.1. Audio/Music Decision -> `audio_music_decision` inside `director_selection.json`, `style_recipe.json`, and `fixed_template_selection.json`
3.5. Fixed Production Templates -> `fixed_template_selection.json` selecting background, transition/SFX, component pack, and voice mix profile
4. Copy Package -> `copy_package.md`, `copy_package.json`, `script_score.json`
5. Semantic Review -> `semantic_review.json`
5.5. Content Alignment -> `content_alignment_report.json`
6. Beginner Value Review -> `beginner_value_review.json`
7. Compliance Check -> `compliance_report.json`
8. Reference Analysis -> `reference_analysis.json` when applicable
9. Visual Style Decision -> `visual_style_decision.json` with style intent, selected brightness/palette/material/layout, and reasons
9.1. Visual Style Plan -> `visual_style_plan.json` aligned to the decision with brightness, palette, material, layout, and diversity sequence
9.2. Dynamic Background Asset -> select one dynamic background asset from `assets/ai_background_templates_dynamic/` through `scripts/select_fixed_ai_templates.py` and record `background_template.id`, `background_template.render_asset_path`, and selection method
9.3. Enterprise AI Control Console System -> define foreground UI tokens, local readability treatment, component families, caption system, motion vocabulary, transition language, SFX character, and QA checks from `references/enterprise_ai_control_console_visual_system.md`
10. Background Art Direction -> `background_prompt_pack.md`, selected fixed text-free background asset, and any topic-specific support asset prompts
11. Asset Prompt Validation -> `asset_prompt_validation.json`
12. Storyboard -> `storyboard.json`, `storyboard_validation.json`
12.5. Foreground Module Plan -> `foreground_module_plan.json`, `foreground_module_plan_check.json`
12.6. Foreground Module Render Pack -> `foreground_module_render_pack.html`, `foreground_module_render_manifest.json`, `foreground_module_render_check.json`, `assets/hyperframes/foreground_modules/`
13. Assets -> `asset_manifest.json`, `visual_tone_report.json` when generated/support visuals exist
14. Asset Validation -> `asset_validation.json`
15. TTS + Duration Lock -> `storyboard.audio_locked.json`, synced `storyboard.json`, synced `director_shots.duration_sec`, scene visual beat records
15.5. Fixed Cover Selection -> run `scripts/select_fixed_cover_template.py` before final timeline render; use `first_frame_cover.png` as scene 0 / first frame
15.6. HyperFrames Render Profile -> `hyperframes_render_profile.json`
15.7. HyperFrames Leading Frame Repair -> `leading_frame_repair_report.json`
16. HyperFrames Production -> `draft.mp4`, `metadata.json`
17. Audio Continuity Check -> `audio_continuity_report.json`
18. Technical QA + Frame Review -> `video_technical_qa.json`, `frame_review_report.json`
19. Visual Review -> `visual_review.json`
20. Layout/Motion Contract -> `render_layout_manifest.json`, then `scripts/check_motion_layout_contract.py` writes `layout_motion_contract_report.json`
21. QA Gate -> `qa_report.json`
22. Production Postmortem -> `production_postmortem.json`
23. Reference Outcome Registry -> update `references/ai_reference_video_outcome_registry.md` for reference-led AI videos
24. Publish Cover -> choose one fixed pure background by size and sequential pool rotation from `references/fixed_ai_cover_background_rotation.json`, render checked runtime cover text inside the safe rectangle with `--require-checked-cover-text`, then write `publish_cover_report.json`, `publish_cover_text.txt`, `first_frame_cover.png`, `cover.png`, `cover_publish_vertical.png`, `cover_publish_horizontal.png`, and for 16:9 Douyin delivery `cover_publish_douyin_center_crop.png`
25. Local Text Compliance Refresh -> `on_screen_and_publish_text_compliance_report.json` covering render text, cover text, and publish copy
26. Visual Regression Gate -> `scripts/produce_ai_video.py --mode visual-gate` writes `visual_regression_gate.json`, including designed support-card blank-block detection
27. Provider Usage Audit -> `provider_usage_audit.json`
28. Qingdou Keyword Check -> `qingdou_keyword_check.json`
29. Publish Evidence Preflight -> `publish_evidence_preflight.json`
30. Publish Contract -> `publish_contract.json`
31. Pre-Publish Gate -> `scripts/pre_publish_gate.py` sets `publish_contract.gate.status`
32. Promote Final -> `final/final.mp4` only if the publish contract gate passed
33. Optional SAU Douyin Upload -> `scripts/douyin_sau_publish.py` writes `douyin_sau_upload_report.json`; dry-run first, then `--execute` only when the user-authorized publish route and schedule/immediate policy are explicit

## Output Layout

```text
outputs/<date-topic>/
  final/
    final.mp4
  internal/
    topic_candidates.json
    selected_topic.json
    director_selection.json
    style_recipe.json
    fixed_template_selection.json
    hook_variants.json
    hook_score_report.json
    reference_overfit_audit.json
    copy_package.md
    copy_package.json
    script_score.json
    semantic_review.json
    content_alignment_report.json
    beginner_value_review.json
    compliance_report.json
    reference_analysis.json
    visual_style_decision.json
    visual_style_plan.json
    background_prompt_pack.md
    asset_prompt_validation.json
    storyboard.json
    storyboard_validation.json
    foreground_module_plan.json
    foreground_module_plan_check.json
    foreground_module_render_pack.html
    foreground_module_render_manifest.json
    foreground_module_render_check.json
    timeline_contract.md
    ai_asset_prompt_pack.md
    storyboard.audio_locked.json
    hyperframes_render_profile.json
    asset_manifest.json
    asset_validation.json
    visual_tone_report.json
    draft.mp4
    audio_continuity_report.json
    cover.png
    cover_publish_vertical.png
    cover_publish_horizontal.png
    cover_publish_douyin_center_crop.png
    publish_cover_text.txt
    publish_cover_report.json
    publish_copy.txt
    video_technical_qa.json
    frame_review_report.json
    visual_review.json
    render_layout_manifest.json
    layout_motion_contract_report.json
    qa_report.json
    production_postmortem.json
    provider_usage_audit.json
    provider_usage_audit.md
    qingdou_keyword_check.json
    on_screen_and_publish_text_compliance_report.json
    publish_evidence_preflight.json
    publish_contract.json
    douyin_sau_upload_report.json
    production_notes.md
  assets/
    screenshots/
    generated/
    audio/
    subtitles/
    hyperframes/
```

## Auto-Publish

`allow_auto_publish: false`

Auto-publishing stays off until all conditions are true:

- 5 consecutive videos have `qa_report.status = passed`.
- 5 consecutive videos have no compliance warnings.
- 5 consecutive videos have `qingdou_keyword_check.status = passed` for title, caption, and topics.
- 5 consecutive videos have no audio/visual sync issue.
- 5 consecutive videos are not single-image narration.
- At least 3 videos have clear save-value structure.
- The user explicitly authorizes publishing for the current video.
- If third-party SAU is used, the upload must go through `scripts/douyin_sau_publish.py`; direct SAU commands are allowed only for isolated login/check troubleshooting, not production upload.
