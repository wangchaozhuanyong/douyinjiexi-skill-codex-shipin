# AI Circle Content Rules

AI-circle knowledge videos must feel credible. Do not rely on abstract AI imagery.

## Topic Identity

Every AI-circle topic must be source-led. The viewer should know the concrete object before the tutorial starts:

- software, website, company, model, product feature, release, official documentation, or news event
- what changed, what was published, what feature/page is being used, or what source is being explained
- what practical takeaway the viewer will get

Reject method-only topics that only say a workflow, checklist, trick, or habit without naming the object/source. For example, `用 ChatGPT 和 Codex 前先写边界清单` is too vague; `ChatGPT 新增应用调用确认：用 Codex 前先写三层边界清单` is acceptable because it names the product and feature/news hook.

## Asset Priority

1. Real UI screenshot.
2. Real operation recording.
3. Real terminal, code, or output result.
4. Real web page or official documentation screenshot.
5. Self-designed information card.
6. AI-generated visual.

## AI-Generated Visuals Are Allowed For

- Cover atmosphere.
- Abstract concept explanation.
- Transition background.
- Mood or metaphor.
- Non-factual scene support.

## AI-Generated Visuals Must Not

- Pretend to be a real product interface.
- Pretend to be an official screenshot.
- Pretend to be a user review.
- Pretend to be data proof.
- Generate fake chat records.
- Generate fake authority certification.
- Include pseudo-Chinese, garbled Chinese-like text, QR codes, phone numbers, contact handles, or exaggerated claims.

## Evidence Ratio

For AI tool tutorials, at least 50% of runtime should be real evidence or output proof unless the user explicitly asks for a concept-only draft.

- Publishable minimum: 50%.
- High-quality target: 60%.
- Excellent target: 70%.

`asset_manifest.json` must identify whether each asset is evidence. Evidence assets should use real UI screenshots, real recordings, terminal/code/file proof, real output results, or official documentation screenshots. AI-generated visuals and abstract backgrounds do not count as evidence.

Run `scripts/validate_assets.py` before final QA. It must block missing files, empty files, high-risk evidence, AI images pretending to be real proof, contact information, QR codes, and private information.
