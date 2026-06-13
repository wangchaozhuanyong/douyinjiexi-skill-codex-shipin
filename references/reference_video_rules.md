# Reference Video Rules

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
python scripts/analyze_reference.py --input "<douyin url/share text/local path>" --out reference_analysis.json
```

If `originality_plan.similarity_risk` is `high`, stop production and redesign the angle, evidence, structure, or visuals.
