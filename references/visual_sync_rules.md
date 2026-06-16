# Visual Sync Rules

Visuals exist to explain the current spoken idea.

## Scene Requirements

- Every scene must have a clear purpose.
- The current image must match the current voice line.
- The first 5 seconds must contain at least 2 visual changes.
- Do not use a single image with full-section narration.
- Do not use low-quality image carousel.
- Do not use a single image plus heavy text.
- Do not keep screenshots static for the whole scene.
- Do not use loop pulse or ordinary Ken Burns zoom as the main motion.
- Do not let subtitles cover UI, title, CTA, or important buttons.
- Do not allow captions, voice, and visual state to drift apart.
- Do not render black frames, white frames, no-audio video, or stuck frames.
- Do not place critical visual content near frame edges. For AI knowledge videos, use 1920x1080 with a wide proof-safe canvas, lower-third caption rail, and side annotation space. In rare non-AI 1080x1920 vertical renders, keep generated-image subjects, proof cards, screenshots, titles, subtitles, and CTA inside a phone-safe content box: top margin >= 240px, bottom margin >= 360px, left margin >= 72px, right margin >= 180px.
- Do not solve dense narration by speeding up voiceover. Use normal Mandarin speed only (`tts_speed` 0.95-1.03, default 1.0); shorten lines or split scenes instead.

## Storyboard Minimums

- At least 6 scenes.
- Codex Skill/plugin/tutorial videos must include top-level `production_stack` when they name tools such as Remotion, HyperFrames, ImageGen, HeyGen, or Codex Skills.
- Each scene that names a primary tool must include `visual.proof_chain` with `entry_or_source`, `operation_or_step`, `output_or_result`, and `viewer_value`.
- Each scene has `voice`, `caption`, `on_screen_text`, `visual`, `motion`, `sync`, and `safe_zone`.
- Each scene has exactly one `concept`.
- Each scene has `beat_map` entries that bind a voice fragment to a visual action, caption, proof/explanation, and motion trigger.
- Each scene's `safe_zone` must record `top_margin_px`, `bottom_margin_px`, `left_margin_px`, `right_margin_px`, and `critical_content_inside_safe_area`.
- Each scene has at least two motion layers: background, foreground, callout, or transition.
- AI tool tutorials should keep real evidence runtime at 50% or higher.
- V3 high-quality target is 60% real evidence runtime, with 70% treated as excellent for AI tool tutorials.

## Named Tool Proof Chain

For every named Skill, plugin, or tool, the scene sequence must prove four things:

- Entry/source: official page, GitHub repo, Codex skill list, plugin list, local folder, command output, or real UI.
- Operation/step: a prompt, command, click, component, timeline, upload, render, or file generation action.
- Output/result: generated image, MP4, rendered frame, final folder, comparison, result grid, or proof wall.
- Viewer value: a plain Chinese reason the viewer should use or save this tool.

If any of the four parts is missing, do not hide the gap with generic visual motion. Add a scene, replace the asset, or change the claim.
