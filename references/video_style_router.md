# Video Style Router

Use this before accepting any video task. Routing happens before scripting, asset generation, TTS, HyperFrames authoring, or rendering.

## Highest-Grade Default

Every request to make, generate, render, remake, upgrade, or deliver a video defaults to highest-grade publish-ready production unless the user explicitly says research only, planning only, quick draft, smoke test, or mock validation.

Highest-grade means:

- choose the owning domain skill first
- apply `references/shared_video_quality_core.md`
- require scene-level timeline, asset/source classification, safe-zone plan, caption-template plan, motion purpose, audio-duration proof, contact-sheet/detail-frame review, and final QA
- never deliver a low-tier fallback as `final`

If the correct owning skill or required runtime cannot meet the bar, stop with a blocker or a clearly labeled draft. Do not silently downgrade to a template slideshow, single-image narration, generic Ken Burns zoom, or no-QA MP4.

## Routing

- AI knowledge, AI news, AI tools, Codex, Agent, plugins, automation, AI tutorial, or reference-led AI explainer: use `$douyin-ai-premium-director` or `$douyin-hyperframes-remake`.
- Renovation, full-house custom cabinets, interior design, home walkthrough, cabinet detail, luxury home ad, designer portfolio, or Qingdou/publish-copy renovation workflow: use `$full-house-custom-ad`.
- Beauty portrait choice video, four-image commercial fashion portrait set, TikTok/Douyin beauty prompt batch, or send-smoke beauty workflow: use `$beauty-gpt-image-video`.

## AI Knowledge Format Rule

Any task routed to the AI knowledge workflow must produce a 16:9 `1920x1080` master. Do not use 9:16 for AI knowledge, AI news, AI tools, ChatGPT, Gemini, OpenAI, Codex, Agent, automation, AI coding, AI workflow, plugin, or Skill tutorial videos, even when the destination is Douyin. Vertical-native non-AI requests must be routed to their owning skill instead.

## Shared Growth Rule

All three styles must use `references/shared_video_quality_core.md` concepts for formal production: free-first provider policy, scene-level timeline, asset classification, safe-zone design, caption template planning, natural voice, style-frame review, contact-sheet/detail-frame review, audio-duration proof, and QA gates.

Do not merge the three styles into one prompt. Keep each skill's own identity and hard rules. The shared core is a quality base, not a replacement for domain contracts.

## When The User Is Ambiguous

- If the subject is AI or tools, route to AI.
- If the subject is homes, cabinets, rooms, materials, or walkthroughs, route to renovation.
- If the subject is four portrait choices, adult Chinese fashion portraits, or beauty TikTok selection videos, route to beauty.
- If the user asks to combine domains, split the plan by scene and name which skill owns each scene before production.

## Final Delivery Rule

Only the owning skill may promote a video to final. A video can be called final only after its domain gates and the shared highest-grade checks pass. Otherwise report the exact missing gate as `blocked` or label the output as `draft`.
