# Learning Bank

Use this file to preserve post-publish lessons that should influence future AI-circle Douyin videos.

## Format

Append one dated entry per published video:

```markdown
## 2026-06-13 video-id

- Topic:
- Format:
- Hook type:
- 24h metrics:
- Comment insights:
- What worked:
- What to fix:
- Next video ideas:
```

## Rules

- Do not treat one video as proof of a universal rule.
- Prefer concrete observations: retention, saves, comments, shares, and repeated audience questions.
- Feed repeated lessons back into topic selection, hook choice, proof visuals, and HyperFrames components.
- Run `scripts/score_topic.py --learning-bank references/learning_bank.md` or `scripts/apply_learning_bank.py` so repeated lessons create visible `learning_bank_adjustment` entries in topic candidates.
