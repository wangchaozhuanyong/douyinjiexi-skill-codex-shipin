# Visual Aesthetic Rules

Use this after `frame_review.py` and before `qa_gate.py`.

## What To Check

- First 5 seconds have at least 2 meaningful visual changes.
- Text stays readable and does not cover UI, title, CTA, or right-side platform buttons.
- `quality_spec` exists in storyboard and metadata for publish-ready work.
- Every scene has at least 3 design layers, such as background, framed proof, callout, subtitle rail, cursor, marker, or texture layer.
- Every scene's `visual.quality_checks` confirms source resolution, text safety, non-template feel, and no static dump.
- Every scene reserves top title, bottom caption, and right interaction zones.
- Every AI knowledge scene reserves a 1920x1080 proof-safe canvas with lower-third caption room and side annotation space. For non-AI 1080x1920 renders, reserve enough physical phone-safe space: top margin >= 240px and bottom margin >= 360px. Generated images must place the subject, proof UI, cards, and readable text inside the safe canvas, not flush to frame edges.
- Each scene has at least 2 motion layers unless it is an intentional held proof frame.
- Scene types vary enough that the video does not become a text-card slideshow.
- Proof frames, UI frames, comparisons, timelines, and result reveals are preferred over decorative backgrounds.
- Narration uses normal Mandarin speed. If a scene feels rushed, reduce copy density or add a scene; do not use accelerated TTS.

## Required Review

Run:

```bash
python scripts/visual_aesthetic_review.py \
  --storyboard outputs/demo/internal/storyboard.json \
  --frame-review outputs/demo/internal/frame_review_report.json \
  --metadata outputs/demo/internal/metadata.json \
  --out outputs/demo/internal/visual_review.json
```

Gate:

- `visual_review.status` must be `passed`.
- `overall_visual_score >= 8.2`.
- `first_5s_score >= 8.5`.
- `readability_score >= 8`.
- `composition_score >= 8`.
- `layering_score >= 8`.
- `quality_check_score >= 8`.
- `sound_design_score >= 8` when SFX is planned.
- `export_readiness_score >= 8`.
- `unsafe_margin_scenes = 0`.
