# V2 Audit Report

## Repository State

- Branch before refactor: `main`
- Refactor branch: `refactor/v2-ai-video-director`
- Latest commits inspected:
  - `fdf5419 Tighten beginner-friendly video production gates`
  - `ab84764 Tighten video motion and Chinese visual rules`
  - `dd39cd8 Update Douyin video skill production rules`
  - `db6e4ce Update daily AI hot-topic scan rules`
  - `492e41e Add premium visual system rules`

## Current File Structure

```text
README.md
SKILL.md
agents/openai.yaml
references/beginner_visual_sync_rules.md
references/codex_skill_tutorial_video.md
references/douyin_rules.md
references/hyperframes_delivery.md
references/pixelle_pipeline_lessons.md
scripts/analyze_reference.py
scripts/check_public_copy.py
```

Missing V2 structure:

```text
docs/
schemas/
templates/
tests/
scripts/doctor.py
scripts/score_topic.py
scripts/score_script.py
scripts/build_storyboard.py
scripts/validate_storyboard.py
scripts/qa_gate.py
scripts/media_probe.py
references/workflow_contract.md
references/topic_selection_rules.md
references/ai_circle_content_rules.md
references/script_quality_rules.md
references/reference_video_rules.md
references/visual_sync_rules.md
references/post_publish_review.md
```

## Manifest And Loading

- `SKILL.md` frontmatter is syntactically valid YAML and contains `name` and `description`.
- Current skill name is `douyin-hyperframes-remake`; V2 should keep this name for compatibility but retarget the description to AI-circle knowledge videos.
- `agents/openai.yaml` is valid YAML.
- `agents/openai.yaml` does not yet include `policy.allow_implicit_invocation`.
- `README.md` still uses the older `~/.codex/skills` install path. Current Codex skill locations include `$HOME/.agents/skills` and repo-scoped `.agents/skills`.

## Script Health

- Existing scripts compile with `python3 -m py_compile scripts/*.py`.
- `scripts/check_public_copy.py` only scans a small fixed term list and does not output `compliance_report.json`.
- `scripts/analyze_reference.py` only accepts `--text`; it does not support a unified `--input` for Douyin URL, share text, or local video path.

## References

Keep and fold into V2:

- `references/beginner_visual_sync_rules.md`: useful beginner copy, sync, image prompt, and free-first rules.
- `references/codex_skill_tutorial_video.md`: useful evidence-led AI/Codex tutorial standards.
- `references/douyin_rules.md`: useful baseline safety categories.
- `references/hyperframes_delivery.md`: useful HyperFrames composition and render basics.
- `references/pixelle_pipeline_lessons.md`: useful storyboard, TTS, timing, metadata discipline.

Move or split into new V2 references:

- Move workflow gates into `references/workflow_contract.md`.
- Move topic scoring into `references/topic_selection_rules.md`.
- Move AI-circle evidence and asset hierarchy into `references/ai_circle_content_rules.md`.
- Move script quality thresholds into `references/script_quality_rules.md`.
- Move reference-remake boundaries into `references/reference_video_rules.md`.
- Move visual sync and motion QA into `references/visual_sync_rules.md`.
- Move analytics learning loop into `references/post_publish_review.md`.

## Why Current Skill Can Still Produce Weak Video

1. The main `SKILL.md` is too long and mixes daily automation, remake rules, scripting, image prompts, TTS, HyperFrames, QA, publishing, and post-publish analysis in one file.
2. Workflow gates are mostly prose, not machine-checkable artifacts.
3. There is no required `topic_candidates.json`, `selected_topic.json`, `copy_package.json`, `compliance_report.json`, `storyboard.audio_locked.json`, `asset_manifest.json`, or `qa_report.json` chain.
4. There are no JSON schemas or tests to prove example outputs are valid.
5. Local compliance checking is shallow and does not track facts, claims, warnings, or suggestions.
6. Reference analysis does not yet enforce similarity risk or support local video metadata paths.
7. There is no hard QA script preventing a draft from being treated as final.
8. Auto-publish behavior is still described as authorized in the old daily workflow; V2 should default to `allow_auto_publish: false` until quality is stable.
9. README does not explain the V2 production workflow or current skill installation path.

## Baseline Verification Commands

```bash
PYTHONPATH=/tmp/codex-pyyaml-validate python3 /Users/wangchao/.codex/skills/.system/skill-creator/scripts/quick_validate.py /tmp/douyin-skill-v2
python3 -m py_compile scripts/*.py
```

Both pass before the V2 rewrite begins.
