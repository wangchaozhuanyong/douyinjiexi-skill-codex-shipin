# Premium Video Quality Playbook

Use this before storyboard, asset generation, HyperFrames authoring, rendering, and final QA whenever the user asks for a high-quality, polished, reference-level, premium, or publish-ready AI-circle short video.

## Quality Principle

High quality is not motion on top of weak content. High quality means:

- the first frame looks like a designed poster
- every named claim is supported by visible proof
- every scene has foreground, middle-ground, and background hierarchy
- screenshots and cards are readable on a phone
- movement explains a step, reveals a detail, or guides attention
- sound effects are subtle but present when UI/proof cards switch
- final export is crisp enough for platform recompression

## Required `quality_spec`

Every publish-ready storyboard and metadata package must document `quality_spec`.

```json
{
  "quality_spec": {
    "target_quality_level": "high_quality",
    "visual_system": "blackboard-grid proof tutorial",
    "motion_policy": "useful motion only; no shake, no random drift, no Ken Burns as main motion",
    "still_image_policy": "split dense images into steps; reveal one point per voice beat",
    "evidence_policy": "real UI / source / output proof first; generated visuals support but do not replace proof",
    "sfx_policy": "subtle click, whoosh, card insert, marker sweep below narration",
    "render_policy": "HyperFrames quality high plus high-bitrate H.264 pass when needed",
    "cover_policy": "standalone poster cover, not a random frame grab",
    "frame_review_policy": "first 5 seconds, full contact sheet, and crowded detail frames must be reviewed"
  }
}
```

## Scene-Level Design Contract

Every scene must document:

- `visual.design_layers`: at least 3 layers, such as background grid, framed screenshot, callout marker, subtitle rail, cursor/highlight.
- `visual.quality_checks.source_resolution_ok`: the screenshot/generated asset is not a low-res upscale.
- `visual.quality_checks.text_safe`: titles, subtitles, proof cards, and CTA do not collide.
- `visual.quality_checks.not_template_like`: the frame does not look like a generic template or empty stock background.
- `visual.quality_checks.not_static_dump`: one image is not carrying several points without reveal/focus/split.

If any of these cannot be truthfully set to `true`, the scene is not ready.

## Minimum Premium Structure

For a 60-90 second AI/Codex tutorial:

- 0-3s: poster-grade hook with a proof/result hint.
- 3-8s: proof wall or before/after, not a slow intro.
- 8-12s: promise/setup in plain Chinese.
- Body: each chapter shows entry/source, operation, result, and viewer value.
- Final 3-5s: recap formula, save reason, and clean end frame.

## Asset Quality Rules

- Do not scale a 1280x720 screenshot to fill a 1920x1080 proof frame.
- For 1920x1080 output, large screenshots should be captured at 1920x1080 or higher.
- For 1080x1920 output, screenshots/cards must be readable in the central safe area.
- If a proof frame looks soft, recapture the source, crop less aggressively, or render with higher bitrate.
- If generated images contain pseudo-Chinese, malformed text, random English filler, fake UI, fake logos, or unreadable labels, reject them.

## Motion Craft Rules

Allowed useful motion:

- cursor-led highlight
- card insertion
- mask wipe
- split-screen slide
- proof-wall assembly
- timeline rail draw
- marker sweep
- component/frame reveal
- localized parallax between layers

Rejected motion:

- page shaking
- full-screen random drift
- Ken Burns zoom as the main motion
- repeated pulse glow
- transition spam with no information change

## Sound And Export Rules

- Use restrained SFX when cards land, pages switch, proof frames insert, or marker sweeps happen.
- Keep SFX below narration and never mask Chinese speech.
- Use normal Mandarin speed only.
- Render HyperFrames with `--quality high` for publish-ready work.
- If HyperFrames audio is truncated, remux the full source audio and re-run QA.
- `metadata.quality_spec.min_bitrate` should normally be at least `3500000`; raise it for screenshot-heavy or horizontal proof-wall videos.

## Final Review

Before `promote_final.py`:

- inspect the first 5 seconds
- inspect the cover at full size
- inspect the full contact sheet
- inspect crowded proof/detail frames at original size
- confirm no title/subtitle/card collision
- confirm no low-res upscaled proof frame
- confirm SFX policy is documented
- confirm final MP4 duration, audio duration, resolution, fps, and bitrate
