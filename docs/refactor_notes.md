# V2 Refactor Notes

## Stage 0 - Audit

### Files Changed

- `docs/audit_report.md`
- `docs/refactor_notes.md`

### Why

The V2 work is a structural rewrite, so the current repository state must be recorded before changing production logic.

### Verification

- `quick_validate.py` confirmed the current skill manifest is valid.
- `python3 -m py_compile scripts/*.py` confirmed existing Python scripts compile.
- Manual inspection confirmed missing V2 directories, schemas, templates, tests, and gate scripts.

### Risks

- The repository currently contains a valid but oversized V1 skill. The next stages will replace the main workflow contract and add deterministic gates; care is needed to avoid losing useful quality rules while reducing the main `SKILL.md`.

## Stage 1-3 - V2 Structure And Workflow Contract

### Files Changed

- `SKILL.md`
- `agents/openai.yaml`
- `README.md`
- `references/workflow_contract.md`
- `references/topic_selection_rules.md`
- `references/ai_circle_content_rules.md`
- `references/script_quality_rules.md`
- `references/douyin_compliance_rules.md`
- `references/reference_video_rules.md`
- `references/visual_sync_rules.md`
- `references/post_publish_review.md`
- `schemas/*.schema.json`
- `templates/*`

### Why

The V1 skill mixed all rules into one long `SKILL.md`. V2 makes `SKILL.md` a concise director contract and moves detailed rules into references, schemas, and templates so Codex can load only what it needs.

### Verification

- `python3 -m py_compile scripts/*.py` passed after script creation.
- `scripts/doctor.py` now checks the required V2 files and current install paths.

### Risks

- V2 is stricter than V1. Some quick-draft flows will now stop at missing artifact gates unless the user explicitly asks for a narrow draft.

## Stage 4-15 - Executable Gates And Tests

### Files Changed

- `scripts/check_public_copy.py`
- `scripts/analyze_reference.py`
- `scripts/score_topic.py`
- `scripts/score_script.py`
- `scripts/build_storyboard.py`
- `scripts/validate_storyboard.py`
- `scripts/media_probe.py`
- `scripts/qa_gate.py`
- `scripts/doctor.py`
- `tests/test_skill_manifest.py`
- `tests/test_yaml_valid.py`
- `tests/test_scripts_compile.py`
- `tests/test_schema_examples.py`
- `tests/test_copy_checker.py`
- `tests/test_qa_gate.py`

### Why

V2 must be executable and verifiable. The new scripts turn the production gates into command-line checks, and the tests make sure future edits do not remove the manifest, schemas, copy checker, or QA behavior.

### Verification

- `python scripts/doctor.py`
- `python -m py_compile scripts/*.py`
- `python3 -m pytest -q`

### Risks

- `scripts/qa_gate.py` verifies required artifacts and scores, but it does not visually inspect MP4 pixels. HyperFrames inspect/contact-sheet review is still required during real video production.
