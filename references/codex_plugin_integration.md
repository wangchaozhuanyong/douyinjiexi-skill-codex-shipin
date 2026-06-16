# Codex Plugin Integration

Use this when the user asks whether the current Codex plugins can be used, asks for a video about plugins, or a storyboard names Codex plugins as production tools.

## Core Six Plugins

Treat these as the six useful Codex plugins for this AI video skill:

| Plugin | Default status | Use it for | Evidence required | Boundary |
| --- | --- | --- | --- | --- |
| Browser | allowed when available | open/test local or web targets, capture UI proof, inspect pages for screenshots | URL, screenshot/contact sheet, page state, operation note | Use Chrome only when logged-in Chrome state is required. |
| GitHub | allowed for read/triage work | inspect repos, issues, PRs, source files, CI logs, release evidence | repo URL/path, issue/PR/log reference, local artifact or summary | Do not commit, push, open PR, or change repo state unless the user explicitly asks. |
| Hugging Face | allowed for public/open model research | inspect models, datasets, papers, Spaces, open-source references | model/dataset/paper URL, license/source note, downloaded or referenced artifact | Cloud Jobs, paid hardware, or training runs need explicit approval. |
| HyperFrames | primary production plugin | final timeline, captions, motion, TTS/transcribe when available, inspect, render, delivery | composition path, lint/inspect/render logs, MP4, QA report | Do not call a draft final until QA passes. |
| OpenAI Developers | allowed for official OpenAI docs and OpenAI app/API guidance | verify OpenAI docs, Agents SDK/App SDK patterns, API troubleshooting, model guidance | official docs/source link, code path, terminal output when executed | New API keys, external paid API calls, or credential writes require the OpenAI credential gate and user approval. |
| HeyGen | optional, not default | avatar/presenter/lipsync/video-agent segments when the user explicitly wants them | HeyGen asset/job/session ID, script, generated media path, user approval note | Treat as approval-required if it consumes credits, uses paid features, uploads identity media, or needs account auth. |

Chrome, Computer Use, PDF, Documents, Presentations, and Spreadsheets are useful fallback/specialized plugins, but they are not part of this skill's core six unless the user names them or the task clearly requires them.

## Plugin Plan Requirement

When a script/storyboard teaches, compares, or claims use of Codex plugins, add top-level `codex_plugin_plan` to `storyboard.json`:

```json
{
  "codex_plugin_plan": {
    "use_case": "six-plugin AI video workflow",
    "plugins": [
      {
        "name": "Browser",
        "availability": "available_in_session",
        "role": "capture web/UI evidence and verify local previews",
        "allowed_by_default": true,
        "evidence_required": ["URL", "screenshot", "operation note"],
        "cost_or_auth_boundary": "Codex-included; Chrome login state only when needed",
        "fallback": "self-captured local screenshot or terminal/file proof"
      }
    ],
    "blocked_plugins": [],
    "approval_required_for": ["HeyGen credit-consuming avatar generation"]
  }
}
```

Use these availability values:

- `available_in_session`
- `available_if_authenticated`
- `local_cli_or_skill`
- `needs_user_approval`
- `optional_blocked`
- `not_available`

If the video says "six plugins", `codex_plugin_plan.plugins` must include Browser, GitHub, Hugging Face, HyperFrames, OpenAI Developers, and HeyGen. Mark HeyGen as approval-required unless the user already authorized the specific HeyGen operation.

## Claim Rules

- Say a plugin is "available" only when it is exposed in the current Codex session, installed as a plugin/skill, or verified by a real command/UI result.
- Say a plugin is "used" only when there is an operation proof and output proof.
- Say a plugin is "optional" or "blocked" when it needs auth, payment, credits, upload consent, or an install that has not happened.
- Prefer real evidence assets from Browser, GitHub, Hugging Face, local files, terminal output, and HyperFrames render logs.
- Do not let HeyGen, paid cloud providers, or paid generation APIs become required for the default publish-ready path.

## Production Mapping

Default plugin route for AI-tool tutorial videos:

1. Browser captures real UI/docs/product proof.
2. GitHub and Hugging Face supply open-source/product evidence when relevant.
3. OpenAI Developers verifies OpenAI-specific claims against official docs.
4. HyperFrames assembles the final timeline, captions, sound cues, inspect output, and render.
5. HeyGen is used only for approved avatar/presenter/lipsync scenes; otherwise record it as optional/blocked and use voiceover plus proof cards.

Every plugin scene still must pass the normal workflow gates: compliance, source classification, phone-safe layout, caption sync, audio duration, frame review, visual review, and final QA.
