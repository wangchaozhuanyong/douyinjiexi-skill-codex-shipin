# Director Decision Patterns

Use this file as the reasoning layer before storyboard. It helps the agent
choose a visual strategy instead of blindly following a template.

## Topic To Visual Strategy

- AI short vertical Skill/tool recommendation with no narration: use `方案1: Skill 推荐无人声`; lock content job as Skill/tool recommendation before visual design; use large Skill headline, numbered rows, icon tiles, divider, concrete usage notes, staggered row reveal, and music-led pacing.
- AI hot-rank TOP5 / countdown ranking: use `方案7: AI 热榜 TOP5 榜单`; lock exactly five current source-backed ranked items, use vertical rank rows, source/date pins, countdown motion from 5 to 1, BGM-led pacing when the reference has music, and a larger but non-absolute rank-one emphasis.
- AI news with official source: use `source_evidence`, `concept_shift`, and `final_template`.
- AI tool tutorial: use `hook_conflict`, `operation_simulation`, `test_or_check_output`, and `evidence_result_card`.
- Codex/Skill workflow: use a Codex-like workspace, task brief panel, repo/file tree, checklist, test output, and evidence package.
- Reference-video remake: learn pacing, hook logic, information density, and shot rhythm; do not copy exact frames or wording.

## Shot Choice Questions

Before HyperFrames composition, answer these:

- What does the viewer see in the first two seconds?
- What is the reference's content job, and did we preserve that job with original text?
- Is this shot a conflict, proof, operation, transformation, template, or CTA?
- Does the shot have a visible subject and action?
- Is there at least one real source/proof moment?
- Are there at least two operation-feel moments?
- Does this shot look different from the previous two shots?
- Is any text too small to read at native 1920x1080?

## When To Stop And Redesign

- More than two consecutive shots share the same layout family.
- The visual plan is mostly card titles with no operation.
- The plan learns a reference's layout but changes the viewer task, such as turning Skill recommendation into generic usage tips.
- Evidence is a fake screenshot or unreadable source panel.
- The final CTA has no collectible template.
- The storyboard cannot explain why each motion exists.

## Learning Loop

After QA, read `production_postmortem.json` before starting the next video.
Use `next_run_decisions` as soft guidance. Use `proposed_rule_changes` only
after the user approves writing them into hard rules.
