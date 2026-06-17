# Failed Case Library

This file records repeated failure patterns from AI-circle video production.
Use it before storyboard and before HyperFrames composition.

## Known Failure Patterns

### Moving Slide Deck

- Symptom: the video feels like one dark slide changing titles.
- Causes: repeated `layout_family`, no operation simulation, no real source closeup, and no visual subject/action per shot.
- Fix: redesign as a visual director script with conflict, source evidence, operation simulation, method template, and final collectible template.

### Fake Evidence Panel

- Symptom: a tiny panel looks like an official screenshot but cannot be read.
- Causes: generated source-looking cards, weak source crop, no minimum display width, or no `must_be_readable` flag.
- Fix: use a real source crop, clean citation card, or abstract non-official diagram; never fake an official screenshot.

### Empty Template Frame

- Symptom: a rendered span has background and UI lines but no clear subject.
- Causes: scene transition filler, missing primary action, or final CTA not populated.
- Fix: run empty-frame check and require every director shot to name `visual_subject` and `primary_action`.

### Wrong Large Text

- Symptom: a big title contains a typo or unapproved phrase.
- Causes: composition text diverged from storyboard or model improvised during render.
- Fix: export `render_text_manifest.json` and run final screen-text proofread before promotion.

## Promotion Rule

Do not turn one failure into a hard rule immediately. When the same failure appears repeatedly, propose a rule change in `production_postmortem.json`, then wait for human approval before modifying hard gates.
