# Visual Aesthetic Rules

Use this after `frame_review.py` and before `qa_gate.py`.

## What To Check

- First 5 seconds have at least 2 meaningful visual changes.
- Text stays readable and does not cover UI, title, CTA, or right-side platform buttons.
- Every scene reserves top title, bottom caption, and right interaction zones.
- Each scene has at least 2 motion layers unless it is an intentional held proof frame.
- Scene types vary enough that the video does not become a text-card slideshow.
- Proof frames, UI frames, comparisons, timelines, and result reveals are preferred over decorative backgrounds.

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
