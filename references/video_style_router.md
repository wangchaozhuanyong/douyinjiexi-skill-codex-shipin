# Video Style Router

Use this before accepting any video task. Routing happens before scripting, asset generation, TTS, HyperFrames authoring, or rendering.

## Highest-Grade Default

Every request to make, generate, render, remake, upgrade, or deliver a video defaults to highest-grade publish-ready production unless the user explicitly says research only, planning only, quick draft, smoke test, or mock validation.

Highest-grade means:

- choose the owning domain skill first
- apply `references/shared_video_quality_core.md`
- require scene-level timeline, asset/source classification, safe-zone plan, caption-template plan, motion purpose, audio-duration proof, contact-sheet/detail-frame review, and final QA
- require global Douyin text compliance for designed video text and publish-entry title/caption/topics, regardless of whether the owning style is AI, renovation, or beauty
- never deliver a low-tier fallback as `final`

If the correct owning skill or required runtime cannot meet the bar, stop with a blocker or a clearly labeled draft. Do not silently downgrade to a template slideshow, single-image narration, generic Ken Burns zoom, or no-QA MP4.

## Routing

- AI knowledge, AI news, AI tools, Codex, Agent, plugins, automation, AI tutorial, or reference-led AI explainer: use `$douyin-ai-premium-director` or `$douyin-hyperframes-remake`.
- Renovation, full-house custom cabinets, interior design, home walkthrough, cabinet detail, luxury home ad, designer portfolio, or Qingdou/publish-copy renovation workflow: use `$full-house-custom-ad`.
- Beauty portrait choice video, four-image commercial fashion portrait set, TikTok/Douyin beauty prompt batch, or send-smoke beauty workflow: use `$beauty-gpt-image-video`.

## Reference-Driven Routing

When the user provides a reference video, Douyin link, share text, local MP4, or screenshot set, read `references/reference_driven_production_rules.md` before choosing the production route.

First classify the reference:

- AI/tool/tutorial/productivity/Codex/plugin/automation/list guide -> AI workflow.
- Renovation/interior/cabinet/room/material/walkthrough/home ad -> renovation workflow.
- Beauty/portrait/four-choice/fashion woman/TikTok selection -> beauty workflow.

Then analyze the reference's aspect ratio, duration, hook, pacing, scene density, layout family, typography, filter, music/voice relationship, and motion language. Only after that, create an original production plan. Do not reuse original reference frames, people, room photos, screenshots, subtitles, wording, identity, watermark, or a highly similar full sequence.

## AI Knowledge Format Rule

Any proof-heavy task routed to the AI knowledge workflow must produce a 16:9 `1920x1080` master. Do not use 9:16 for AI knowledge, AI news, AI tools, ChatGPT, Gemini, OpenAI, Codex, Agent, automation, AI coding, AI workflow, plugin, or Skill tutorial videos when the video depends on readable proof screens, code, docs, diagrams, or workflow evidence. Vertical-native non-AI requests must be routed to their owning skill instead.

Reference exception: if the user provides a vertical reference and asks to match that style, and the content is a lightweight guide/list/card/poster explainer rather than proof-heavy screen teaching, AI workflow may use 9:16 `1080x1920` information-poster mode. This exception must still pass originality, source/evidence, text accuracy <= 10%, safe-zone, compliance, Qingdou, and QA gates.

For AI/tool videos after routing, classify the specific AI production scheme with `references/ai_video_scheme_library.md`. If the reference is a short vertical no-voice Skill/tool recommendation list, use `方案1: Skill 推荐无人声`.

## Shared Growth Rule

All three styles must use `references/shared_video_quality_core.md` concepts for formal production: free-first provider policy, scene-level timeline, asset classification, safe-zone design, caption template planning, natural voice, style-frame review, contact-sheet/detail-frame review, audio-duration proof, and QA gates.

All three styles must also use `references/global_douyin_text_compliance_rule.md`: every designed text surface and every publish-entry title/caption/topic field must be checked for Douyin risk words, detected terms must be learned into the forbidden-term bank, and publish text must pass Qingdou before upload.

All three styles must also honor `references/reference_driven_production_rules.md` when a reference is supplied: analyze first, plan second, create independently third, and verify final on-screen text against approved original copy with <= 10% deviation.

Do not merge the three styles into one prompt. Keep each skill's own identity and hard rules. The shared core is a quality base, not a replacement for domain contracts.

## When The User Is Ambiguous

- If the subject is AI or tools, route to AI.
- If the subject is homes, cabinets, rooms, materials, or walkthroughs, route to renovation.
- If the subject is four portrait choices, adult Chinese fashion portraits, or beauty TikTok selection videos, route to beauty.
- If the user asks to combine domains, split the plan by scene and name which skill owns each scene before production.

## Final Delivery Rule

Only the owning skill may promote a video to final. A video can be called final only after its domain gates and the shared highest-grade checks pass. Otherwise report the exact missing gate as `blocked` or label the output as `draft`.
