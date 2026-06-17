# Workflow Contract

This is the hard production contract for V3. Do not treat it as guidance. It defines what may happen next.

## Artifact Gates

0. Decide video style routing first for every video request. Read `references/video_style_router.md` and `references/shared_video_quality_core.md`; route renovation and beauty work to their owning skills before using this AI pipeline.
0.1. Highest-grade mode is the default. If the user did not explicitly ask for research-only, planning-only, quick draft, smoke test, or mock validation, treat the task as publish-ready and enforce all final gates.
0.2. A low-tier fallback MP4, template slideshow, single-image narration, generic Ken Burns render, no-audio render, unreviewed TTS render, or no-QA render must not be promoted, named, or described as final.
0.3. Decide input mode for AI knowledge videos. Reference provided -> Reference Mode. No reference -> Self-Research Mode with current AI-topic/source research.
0.4. If the video teaches, compares, or claims use of Codex plugins, or if an AI tool/tutorial needs source-backed proof, read `references/codex_plugin_integration.md` before copy/storyboard lock and include `storyboard.codex_plugin_plan`; if it says "six plugins", document Browser, GitHub, Hugging Face, HyperFrames, OpenAI Developers, and HeyGen with availability, role, boundary, fallback, and evidence requirements. HyperFrames is the final assembly engine, not the only plugin.
0.5. For every premium AI explainer, read `references/premium_ai_video_source_to_hyperframes_rule.md` and `references/ai_generated_asset_prompt_system.md` before copywriting or HyperFrames work. Source research, plain-language copy, sentence-to-visual storyboard, asset/image prompt plan, and HyperFrames visual identity are required before rendering.
0.6. AI knowledge videos and AI explainers must use 16:9 horizontal `1920x1080`. This includes AI news, AI tools, ChatGPT, Gemini, OpenAI, Codex, Agent, automation, AI coding, AI workflow, plugin, and Skill tutorials. Do not switch to 9:16 merely because the destination is Douyin; keep the 16:9 proof-first master so screenshots, code, docs, and diagrams remain readable.
0.7. AI knowledge videos must pass the background-first gate before storyboard, assets, TTS, HyperFrames, render, or upload: create `internal/background_prompt_pack.md` with descriptive background language, generate/select text-free `1920x1080` background plate(s), and register them in `asset_manifest.json` as generated support with `asset_role=background_plate`, never proof. Generated visuals must use `gpt-image-2` or Codex built-in ImageGen and must record `model`, `prompt_id`, `prompt_path`, `unique_prompt=true`, and `evidence_boundary`; local PIL/canvas/HTML placeholders do not satisfy this gate.
0.8. Do not hard-cut or replace the visual page while narration is mid-sentence. Storyboards must mark scene/page switches at sentence end, breath pause, chapter pause, or a documented visual handoff with an 8-14 frame overlap.
0.9. HyperFrames visual transitions must not control narration. Before render, lock a continuous root narration bed or prove root-level per-scene audio is scheduled back-to-back with `max_audio_gap_ms <= 120`; transitions may overlap visuals but must not restart, mute, fade, or gap the voice. TTS lock must write real durations back to scene `duration_target` and `storyboard.director_shots[*].duration_sec`; mismatched director/scenes/audio timings block render and promotion.
0.10. Before each new AI video, read `references/learning_bank.md`, `references/failed_case_library.md`, and `references/director_decision_patterns.md` as the soft learning layer. Apply repeated lessons to topic selection and storyboard decisions, but do not auto-edit hard rules without user approval.
1. `topic_candidates.json` does not exist -> do not write full copy.
2. `selected_topic.json` does not exist -> do not create copy package.
3. `copy_package.md` and `copy_package.json` do not exist -> do not create storyboard.
4. `script_score.json` is missing or not strong enough -> do not create storyboard.
5. `semantic_review.json` is missing or not `passed` -> do not create storyboard.
6. `compliance_report.json` is missing or not `passed` -> do not generate images, TTS, HyperFrames scenes, or video.
7. `reference_analysis.json` is required when the user provides a reference video/link/share text.
8. `storyboard.json` does not exist -> do not generate TTS or assets.
9. `storyboard_validation.json` is missing or not `passed` -> do not generate TTS or assets. Storyboard validation must include phone-safe margins and normal TTS speed metadata.
10. `asset_manifest.json` does not exist or lacks asset source classes/provider notes -> do not build HyperFrames.
10.1. Generated/support visuals are planned or used, but `internal/ai_asset_prompt_pack.md` or equivalent production notes are missing -> do not generate assets and do not build HyperFrames.
11. `asset_validation.json` is missing or not `passed` -> do not build HyperFrames.
12. `storyboard.audio_locked.json` does not exist -> do not render HyperFrames.
13. `metadata.json` does not exist or has accelerated `tts_speed` -> do not run final QA.
14. `draft.mp4` is missing or empty -> do not run final QA.
15. `audio_continuity_report.json` is missing or not `passed` -> do not run final QA, do not create `final/final.mp4`, and do not publish.
16. `video_technical_qa.json` is missing or not `passed` -> do not create `final/final.mp4`.
17. `frame_review_report.json` is missing -> do not create `final/final.mp4`.
18. `visual_review.json` is missing or not `passed` -> do not create `final/final.mp4`.
19. `qa_report.json` is missing or not `passed` -> do not create `final/final.mp4`, do not publish, and do not present the video as final.
20. `provider_usage_audit.json` is missing or not `passed` -> do not create `final/final.mp4`, do not publish, and do not present the video as final.
21. `production_postmortem.json` should be generated after QA for learning and debugging. It is not allowed to override failed QA and must not rewrite hard rules automatically.
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
- background prompts describe spatial role, material, lighting, camera, text-safe zones, and avoid rules instead of vague "high-tech" words
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
- Default narration speed is normal `tts_speed: 1.0`; allowed range is 0.95-1.03.
- If a line is too long, split the scene or shorten the copy. Do not use accelerated TTS to force timing.

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
5. Compliance Check -> `compliance_report.json`
6. Reference Analysis -> `reference_analysis.json` when applicable
7. Background Art Direction -> `background_prompt_pack.md`, selected/generated text-free 1920x1080 background plate(s)
8. Storyboard -> `storyboard.json`, `storyboard_validation.json`
9. Assets -> `asset_manifest.json`
10. Asset Validation -> `asset_validation.json`
11. TTS + Duration Lock -> `storyboard.audio_locked.json`, synced `storyboard.json`, synced `director_shots.duration_sec`
12. HyperFrames Production -> `draft.mp4`, `metadata.json`
13. Audio Continuity Check -> `audio_continuity_report.json`
14. Technical QA + Frame Review -> `video_technical_qa.json`, `frame_review_report.json`
15. Visual Review -> `visual_review.json`
16. QA Gate -> `qa_report.json`
17. Production Postmortem -> `production_postmortem.json`
18. Provider Usage Audit -> `provider_usage_audit.json`
19. Promote Final -> `final/final.mp4` only if QA and provider usage audit passed

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
    compliance_report.json
    reference_analysis.json
    background_prompt_pack.md
    storyboard.json
    storyboard_validation.json
    timeline_contract.md
    ai_asset_prompt_pack.md
    storyboard.audio_locked.json
    asset_manifest.json
    asset_validation.json
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
- 5 consecutive videos have no audio/visual sync issue.
- 5 consecutive videos are not single-image narration.
- At least 3 videos have clear save-value structure.
- The user explicitly authorizes publishing for the current video.
