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
- Add captions/subtitles as HTML text so they can be edited.
- Keep text large enough for mobile: headline 60px+, body/caption 24px+ in 1080x1920 renders.
- Avoid text overflows. Run inspect before render.
- Do not bake long Chinese text into generated images; keep text in HyperFrames.

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
