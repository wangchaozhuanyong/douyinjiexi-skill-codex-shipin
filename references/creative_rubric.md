# Creative Rubric

Use this rubric when judging whether an AI-circle Douyin script is genuinely useful, not merely keyword-compliant.

## Hard Questions

- Does the first 3 seconds show a real conflict, visible mistake, surprising result, or before/after contrast?
- Can the target viewer name themselves in one sentence?
- Can the viewer reuse the method immediately after watching?
- Does every claim have a planned proof visual?
- Would the spoken copy sound natural if read aloud without the Markdown headings?
- Is there new information beyond generic AI enthusiasm?

## Required Review

Run:

```bash
python scripts/evaluate_copy_semantic.py \
  --copy outputs/demo/internal/copy_package.md \
  --copy-json outputs/demo/internal/copy_package.json \
  --out outputs/demo/internal/semantic_review.json
```

Gate:

- `semantic_review.status` must be `passed`.
- `composite_score >= 8.5`.
- `hard_fail_reasons` must be empty.
