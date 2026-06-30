# Reference Video Rules

This file is a compatibility entrypoint for older prompts and scripts. For current work, `references/reference_driven_production_rules.md` is the authority for reference-driven production across AI/tool, renovation/full-house custom, and beauty portrait videos.

Use this file only as a quick reminder:

- Analyze first, plan second, create independently third.
- For a video reference, obtain and inspect the playable video body first. Download the Douyin/local reference video or use the provided MP4, then inspect ffprobe metadata, contact sheets, first 3-5 seconds, scene rhythm, motion, text density, and audio/music before copywriting, storyboard, render, or delivery. Title/share text/URL metadata/music page alone are not enough.
- Learn pacing, hook logic, typography hierarchy, layout family, motion language, filter mood, music/voice relationship, safe zones, and why the reference works.
- Do not reuse original frames, screenshots, subtitles, written copy, people, rooms, product assets, voice, creator identity, logo, watermark, or a highly similar full sequence.
- If the reference has no narration, default to no narration unless the new topic genuinely needs voice.
- For user-provided Douyin references that will also publish to Douyin, reference music may be treated as user-authorized same-platform Douyin music; use the reference video's own music or same Douyin music-page track when technically possible. If it cannot be obtained, stop for the user's music file, platform same-music selection, or explicit no-BGM approval instead of generating/substituting BGM. Cross-platform or non-Douyin use needs separate authorization.
- Final rendered on-screen text must come from the approved new copy/storyboard/card plan and stay within <= 10% character-level deviation per major text block.
- If `originality_plan.similarity_risk` is high, stop and redesign the angle, evidence, structure, or visuals before rendering.

Required current reference:

```text
references/reference_driven_production_rules.md
```

Typical artifacts:

```text
reference_analysis.json
reference_shot_table.md
reference_style_profile.json
reference_originality_plan.md
reference_driven_production_plan.md
reference_contact_sheet.jpg
local playable reference video path or blocker
render_text_manifest.json or OCR/text audit
qa_report.json
```

Useful commands:

```bash
python3 scripts/extract_reference_frames.py \
  --input reference.mp4 \
  --out outputs/demo/internal/reference_frames \
  --interval 1.0

python3 scripts/analyze_reference.py \
  --input "<douyin url/share text/local path>" \
  --out outputs/demo/internal/reference_analysis.json
```
