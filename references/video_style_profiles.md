# Video Style Profiles

This skill uses explicit visual style profiles instead of vague taste words.

## Default Proof-Heavy AI Profile

`premium_editorial_proof_board_v1` is the default profile for proof-heavy AI, Codex,
Agent, ChatGPT, plugin, and tutorial videos. It is not the only style in the
system; `visual_style_decision.json` may choose another concrete profile when the
topic, source density, or reference rhythm justifies it.

Required source:

- `templates/visual_style_profile.premium_editorial_proof_board.json`

Production rules:

- Treat generated background plates as support atmosphere, not evidence.
- Keep real proof large enough for phone reading.
- Use proof stage, annotation rail, and lower-third caption as information jobs.
- Avoid empty rails, pseudo UI, generic gradients, neon grids, robots, random particles, and long caption blocks.
- Optional 9:16 delivery must be a separate adaptation with its own QA, not a crop of the 16:9 proof master.
