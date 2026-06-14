# HyperFrames Delivery Checklist

Use this before writing or rendering a HyperFrames remake project.

## Project Structure

Recommended output folder:

```text
<work-dir>/
  reference-analysis.json
  DESIGN.md
  index.html
  assets/
    scene-01.png
    scene-02.png
  renders/
    final.mp4
  publish/
    cover.jpg
    caption.txt
    production-notes.md
```

## Composition Requirements

- 1080x1920 vertical root composition.
- Root composition is a normal `<div data-composition-id="...">` in `index.html`; do not wrap the root in `<template>`.
- Every timed clip needs `id`, `data-start`, `data-duration` when applicable, and `data-track-index`.
- Video must be muted and paired with separate audio if audio is used.
- Timelines must be synchronous and registered in `window.__timelines`.
- Use finite animation loops; never `repeat: -1`.
- Use transitions between all scenes.
- Use entrance animations on every scene.
- Do not use exit animations before scene transitions except at the final scene.

## Visual And Text Requirements

- Create `DESIGN.md` before HTML. Define mood, palette, typography, and what not to do.
- Use generated images as visual scenes, not copied source frames.
- For 1080x1920 vertical renders, design the real content inside a phone-safe inner canvas. Keep the top 240px and bottom 360px free of critical subject matter, proof UI, cards, subtitles, and CTA. Use these areas only for background texture, blur, or nonessential atmosphere.
- Add captions/subtitles as HTML text so they can be edited.
- Keep text large enough for mobile: headline 60px+, body/caption 24px+ in 1080x1920 renders.
- Avoid text overflows. Run inspect before render.
- Do not bake long Chinese text into generated images; keep text in HyperFrames.
- When generating images, prompt for generous top and bottom negative space. Do not crop key objects, UI evidence, or Chinese labels into the phone status/control areas.

## TTS And Duration Lock

- Generate one TTS file per scene.
- Use normal Mandarin speed only: default `tts_speed` 1.0, acceptable range 0.95-1.03. Do not use 1.1x/1.12x/1.2x to force a script into the target duration.
- After each scene TTS is generated, run `ffprobe` or `scripts/media_probe.py` to read the real duration.
- Write the real duration back to `storyboard.audio_locked.json`.
- HyperFrames scene durations must use the real audio durations.
- Do not hand-fill approximate scene timing.
- If subtitles do not fit the real audio duration, shorten the subtitle or regenerate that scene's voiceover.
- If voiceover does not fit, split the image into more visual beats or shorten the line. Do not accelerate narration.
- Do not render HyperFrames before `storyboard.audio_locked.json` exists.

## Commands

Run from the HyperFrames project directory:

```bash
npx hyperframes lint
npx hyperframes inspect --samples 15
npx hyperframes render --quality standard --output renders/final.mp4
```

If render fails:

```bash
npx hyperframes doctor
```

## Final Package Notes

`production-notes.md` should include:

- reference link or share text
- analysis summary
- generated scene list
- image prompt list
- what changed from the source
- compliance/risk checklist
- final file paths
- note that Douyin review is not guaranteed
