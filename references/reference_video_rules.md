# Reference Video Rules

Use this when the user provides a Douyin link, share text, local video, screenshot set, or explicitly asks to imitate a reference.

## Reference Mode Contract

- Imitate the reference's usable strengths: hook speed, rhythm, scene density, narrative structure, caption timing, visual progression, and save/comment trigger.
- Do not copy exact wording, subtitle lines, frames, camera shots, character identity, voice, music, logo use, watermark, or a highly similar full sequence.
- Turn the reference into an original AI-circle knowledge video with a fresh angle, fresh examples, fresh public copy, and compliant visuals.
- If a reference has 5 knowledge points in one image, either reveal those points progressively with motion that matches the voice, or split them into multiple scenes. Do not let one static image carry a whole section.
- Save the reference analysis to `reference_analysis.json` before copywriting or storyboard work.

## Self-Research Fallback

If no reference is provided, do not invent a "reference-like" old topic. Switch to Self-Research Mode in `topic_selection_rules.md`: search current AI-circle hot topics and source-backed material before selecting the topic.

Use reference videos for learning structure, not for copying.

## Learn

- Topic direction.
- Rhythm.
- Scene count.
- Information density.
- Hook structure.
- CTA structure.
- Visual organization.

## Do Not Copy

- Original frames.
- Original subtitles.
- Original voice.
- Original music.
- Original wording.
- Original creator identity or personal expression.
- Full structure when it becomes highly similar.

## Required Output

Run:

```bash
python scripts/extract_reference_frames.py --input reference.mp4 --out outputs/demo/internal/reference_frames --interval 1.0
python scripts/analyze_reference.py --input "<douyin url/share text/local path>" --out reference_analysis.json
```

If `originality_plan.similarity_risk` is `high`, stop production and redesign the angle, evidence, structure, or visuals.

For local videos, the analysis must create or reference:

- `reference_contact_sheet.jpg`
- `reference_shot_table.md`
- `reference_frames/metadata.json`
