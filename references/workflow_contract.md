# Workflow Contract

This is the hard production contract for V3. Do not treat it as guidance. It defines what may happen next.

## Artifact Gates

0. Decide video style routing first for every video request. Read `references/video_style_router.md` and `references/shared_video_quality_core.md`; route renovation and beauty work to their owning skills before using this AI pipeline.
0.1. Highest-grade mode is the default. If the user did not explicitly ask for research-only, planning-only, quick draft, smoke test, or mock validation, treat the task as publish-ready and enforce all final gates.
0.2. A low-tier fallback MP4, template slideshow, single-image narration, generic Ken Burns render, no-audio render, unreviewed TTS render, or no-QA render must not be promoted, named, or described as final.
0.3. Decide input mode for AI knowledge videos. Reference provided -> Reference Mode. No reference -> Self-Research Mode with current AI-topic/source research.
0.3.1. For AI/tool/Codex videos, classify the production scheme with `references/ai_video_scheme_library.md` before copywriting or storyboard. A short vertical no-voice Skill/tool recommendation reference must be classified as `方案1: Skill 推荐无人声`; apply `references/ai_video_scheme_1_skill_recommendation_no_voice.md` and lock `content_job_lock` before rendering.
0.3.2. After QA for any reference-led AI video, update `references/ai_reference_video_outcome_registry.md` with scheme, reference source, output project, QA status, publish status, lessons, and reuse decision. This registry is the counting layer for future AI style-direction statistics.
0.4. If the video teaches, compares, or claims use of Codex plugins, or if an AI tool/tutorial needs source-backed proof, read `references/codex_plugin_integration.md` before copy/storyboard lock and include `storyboard.codex_plugin_plan`; if it says "six plugins", document Browser, GitHub, Hugging Face, HyperFrames, OpenAI Developers, and HeyGen with availability, role, boundary, fallback, and evidence requirements. HyperFrames is the final assembly engine, not the only plugin.
0.5. For every premium AI explainer, read `references/premium_ai_video_source_to_hyperframes_rule.md`, `references/visual_description_language_reference.md`, and `references/ai_generated_asset_prompt_system.md` before copywriting or HyperFrames work. Source research, plain-language copy, sentence-to-visual storyboard, asset/image prompt plan, and HyperFrames visual identity are required before rendering.
0.6. Proof-heavy AI knowledge videos and AI explainers must use 16:9 horizontal `1920x1080`. This includes AI news, AI tools, ChatGPT, Gemini, OpenAI, Codex, Agent, automation, AI coding, AI workflow, plugin, and Skill tutorials when they depend on readable sources, screenshots, code, docs, and diagrams. Do not switch to 9:16 merely because the destination is Douyin. Exception: reference-driven lightweight guide/list/card/poster explainers may use 9:16 `1080x1920` only under `references/reference_driven_production_rules.md`, with originality, safe-zone, text accuracy, compliance, and QA gates intact.
0.7. AI knowledge videos must pass the background-first and visual-asset-director gates before storyboard, assets, TTS, HyperFrames, render, or upload: create `internal/visual_style_plan.json`, `internal/background_prompt_pack.md`, and `internal/ai_asset_prompt_pack.md` or equivalent notes using `references/visual_description_language_reference.md`; generate/select text-free `1920x1080` background plate(s); and register generated support assets in `asset_manifest.json` with `asset_role=background_plate` or a specific support role, never proof. The visual style plan must lock `scene_function`, `visual_archetype`, `brightness_grade`, `palette_family`, `material_family`, `layout_family`, bright/dark rhythm, and diversity limits before individual prompts are written. The prompt pack and manifest must document `visual_thesis`, `topic_binding`, `beginner_usefulness`, `information_job`, `background_role`, `scene_id`, `narration_line_supported`, `viewer_takeaway`, `composition`, `foreground`, `midground`, `background`, `camera_lens`, `lighting`, `material_texture`, `color_hierarchy`, `color_system`, `depth_layering`, `text_safe_zones`, `motion_usage`, `animation_affordance`, `primary_animated_object`, `dark_light_motion_rule`, `negative_prompt`, `regeneration_criteria`, and `diversity_check` so every image is visibly connected to the selected topic instead of being a generic premium stage. Generated visuals must use `gpt-image-2` or Codex built-in ImageGen and must record `model`, `prompt_id`, `prompt_path`, `unique_prompt=true`, and `evidence_boundary`. Do not require the user to create `OPENAI_API_KEY` merely because they use paid Codex. If Codex built-in ImageGen cannot export a local file, a truthful local support background may pass only with explicit user approval through `asset_manifest.allow_local_support_background_plate=true`, complete visual-director fields, `generation_method=user_approved_local_support_background`, and `type=designed_card`, `asset_source_type=support`, `is_evidence=false`.
0.8. Do not hard-cut or replace the visual page while narration is mid-sentence. Storyboards must mark scene/page switches at sentence end, breath pause, chapter pause, or a documented visual handoff with an 8-14 frame overlap.
0.9. HyperFrames visual transitions must not control narration. Before render, lock a continuous root narration bed or prove root-level per-scene audio is scheduled back-to-back with `max_audio_gap_ms <= 120`; transitions may overlap visuals but must not restart, mute, fade, or gap the voice. TTS lock must write real durations back to scene `duration_target` and `storyboard.director_shots[*].duration_sec`; mismatched director/scenes/audio timings block render and promotion.
0.10. Before each new AI video, read `references/learning_bank.md`, `references/failed_case_library.md`, and `references/director_decision_patterns.md` as the soft learning layer. Apply repeated lessons to topic selection and storyboard decisions, but do not auto-edit hard rules without user approval.
0.11. Before writing public-facing title, caption, hashtag/topic, cover text, subtitle text, or on-screen text, read `references/forbidden_terms_learning_bank.md` and active records in `references/forbidden_terms_learning_bank.jsonl`; avoid learned forbidden/sensitive/risky terms in the first draft. If any local/Qingdou/Douyin/manual check later detects a risky term, run `scripts/update_forbidden_terms.py` and save `internal/forbidden_terms_update_report.json` before rewriting and rerunning checks.
0.12. Global Douyin text compliance applies across all owning skills and video types. Any designed text in the video, including title cards, subtitles, cover text, poster/card text, badges, labels, CTA, stickers, and text overlays, must be checked before final render/QA. The exact publish title, caption/body, and hashtags/topics must be checked together before upload or publish.
1. `topic_candidates.json` does not exist -> do not write full copy.
2. `selected_topic.json` does not exist -> do not create copy package.
3. `copy_package.md` and `copy_package.json` do not exist -> do not create storyboard.
4. `script_score.json` is missing or not strong enough -> do not create storyboard.
5. `semantic_review.json` is missing or not `passed` -> do not create storyboard.
5.1. `beginner_value_review.json` is missing, not `passed`, or below beginner thresholds -> do not create storyboard.
6. `compliance_report.json` is missing or not `passed` -> do not generate images, TTS, HyperFrames scenes, or video.
6.1. `compliance_report.json`, `on_screen_and_publish_text_compliance_report.json`, Qingdou, Douyin upload, or manual review detects any forbidden/sensitive/risky term -> record it in `references/forbidden_terms_learning_bank.jsonl` with `scripts/update_forbidden_terms.py`, then rewrite and rerun checks.
7. `reference_analysis.json` is required when the user provides a reference video/link/share text.
8. `storyboard.json` does not exist -> do not generate TTS or assets.
9. `storyboard_validation.json` is missing or not `passed` -> do not generate TTS or assets. Storyboard validation must include phone-safe margins and normal TTS speed metadata.
10. `asset_manifest.json` does not exist or lacks asset source classes/provider notes -> do not build HyperFrames.
10.0. `visual_style_plan.json` is missing for a publish-ready AI tutorial or generated visuals lack scene function, brightness grade, palette family, material family, layout family, color system, depth/layering, primary animated object, dark/light motion rule, or diversity check -> do not generate assets and do not build HyperFrames.
10.1. Generated/support visuals are planned or used, but `internal/ai_asset_prompt_pack.md` or equivalent production notes are missing, `internal/asset_prompt_validation.json` is missing/not passed, or generated visual manifest entries lack complete visual director fields -> do not generate assets and do not build HyperFrames.
11. `asset_validation.json` is missing or not `passed` -> do not build HyperFrames.
11.1. Generated/support visuals have been created but `visual_tone_report.json` reports over-dark L4/L5 scenes, crushed L1/L2 proof scenes, insufficient bright proof surfaces, or teal/blue-only palette bias -> regenerate or restage the visuals before HyperFrames.
12. `storyboard.audio_locked.json` does not exist -> do not render HyperFrames.
13. `metadata.json` does not exist or has accelerated `tts_speed` without explicit user approval and synced audio timing -> do not run final QA.
13.1. `metadata.voice` uses macOS `say`, Apple/system voices such as `Tingting`, scratch timing previews, or a relabeled local system provider without explicit lower-quality user approval -> do not run final QA or promote as publish-ready.
14. `draft.mp4` is missing or empty -> do not run final QA.
15. `audio_continuity_report.json` is missing or not `passed` -> do not run final QA, do not create `final/final.mp4`, and do not publish.
16. `video_technical_qa.json` is missing or not `passed` -> do not create `final/final.mp4`.
17. `frame_review_report.json` is missing -> do not create `final/final.mp4`.
18. `visual_review.json` is missing or not `passed` -> do not create `final/final.mp4`.
19. `qa_report.json` is missing or not `passed` -> do not create `final/final.mp4`, do not publish, and do not present the video as final.
20. `provider_usage_audit.json` is missing or not `passed` -> do not create `final/final.mp4`, do not publish, and do not present the video as final.
20.1. `qingdou_keyword_check.json` is missing, not `passed`, does not include `title`, `caption`, and `topics` in `checked_fields`, or its final check does not prove `未检查到敏感词` -> do not run `promote_final.py`, do not upload to Douyin, and do not publish. The exact title, publish caption, and hashtags/topics intended for Douyin must be checked together, rewritten if Qingdou reports sensitive words, and checked again before publishing.
20.2. Designed video text, including screen text, subtitles, cover text, poster/card text, labels, stickers, and CTA, has not been locally checked against Douyin risk rules and the learned forbidden-term bank -> do not promote, upload, or publish.
21. `production_postmortem.json` should be generated after QA for learning and debugging. It is not allowed to override failed QA and must not rewrite hard rules automatically. If the project is a reference-led AI video, `references/ai_reference_video_outcome_registry.md` should also be updated before the run is considered learned.
22. Only `scripts/promote_final.py` may copy QA-passed and provider-audited draft artifacts into `final/`.

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

If any item is missing, stop and report the missing gate instead of delivering `final`.

## Phone-Safe Canvas And Voice Speed

- In 1920x1080 AI knowledge videos, proof panels, screenshots, code, captions, titles, and CTA must stay inside a horizontal proof-safe canvas with lower-third caption space and a side annotation rail.
- In rare non-AI 1080x1920 vertical videos, critical content must stay inside top >= 240px, bottom >= 360px, left >= 72px, and right >= 180px. Generated images must include this top/bottom breathing room before text is added; do not rely on later overlays to hide cropped content.
- Default narration speed is normal `tts_speed: 1.0`; allowed default range is 0.95-1.03.
- If a line is too long, split the scene or shorten the copy. Do not use accelerated TTS to force timing.
- If the user explicitly asks for a faster voice style such as `1.1x`, set `voice_speed_policy=user_approved_1_1x`, keep `tts_speed <= 1.10`, document the approval, regenerate the voice sample, rebuild the continuous root narration bed, and sync storyboard/director/HTML timing from real audio durations.

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
3. Copy Package -> `copy_package.md`, `copy_package.json`, `script_score.json`
4. Semantic Review -> `semantic_review.json`
5. Beginner Value Review -> `beginner_value_review.json`
6. Compliance Check -> `compliance_report.json`
7. Reference Analysis -> `reference_analysis.json` when applicable
8. Visual Style Plan -> `visual_style_plan.json` with brightness, palette, material, layout, and diversity sequence
9. Background Art Direction -> `background_prompt_pack.md`, selected/generated text-free 1920x1080 background plate(s)
10. Asset Prompt Validation -> `asset_prompt_validation.json`
11. Storyboard -> `storyboard.json`, `storyboard_validation.json`
12. Assets -> `asset_manifest.json`, `visual_tone_report.json` when generated/support visuals exist
13. Asset Validation -> `asset_validation.json`
14. TTS + Duration Lock -> `storyboard.audio_locked.json`, synced `storyboard.json`, synced `director_shots.duration_sec`
15. HyperFrames Production -> `draft.mp4`, `metadata.json`
16. Audio Continuity Check -> `audio_continuity_report.json`
17. Technical QA + Frame Review -> `video_technical_qa.json`, `frame_review_report.json`
18. Visual Review -> `visual_review.json`
19. QA Gate -> `qa_report.json`
20. Production Postmortem -> `production_postmortem.json`
21. Reference Outcome Registry -> update `references/ai_reference_video_outcome_registry.md` for reference-led AI videos
22. Provider Usage Audit -> `provider_usage_audit.json`
23. Qingdou Keyword Check -> `qingdou_keyword_check.json`
24. Promote Final -> `final/final.mp4` only if QA, provider usage audit, and Qingdou keyword check passed

## Output Layout

```text
outputs/<date-topic>/
  final/
    final.mp4
    cover.png
    publish_copy.txt
    metadata.json
  internal/
    topic_candidates.json
    selected_topic.json
    copy_package.md
    copy_package.json
    script_score.json
    semantic_review.json
    beginner_value_review.json
    compliance_report.json
    reference_analysis.json
    visual_style_plan.json
    background_prompt_pack.md
    asset_prompt_validation.json
    storyboard.json
    storyboard_validation.json
    timeline_contract.md
    ai_asset_prompt_pack.md
    storyboard.audio_locked.json
    asset_manifest.json
    asset_validation.json
    visual_tone_report.json
    draft.mp4
    audio_continuity_report.json
    cover.png
    publish_copy.txt
    video_technical_qa.json
    frame_review_report.json
    visual_review.json
    qa_report.json
    production_postmortem.json
    provider_usage_audit.json
    provider_usage_audit.md
    qingdou_keyword_check.json
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
