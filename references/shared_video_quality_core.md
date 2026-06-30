# Shared Video Quality Core

This reference is the common quality language shared by the AI, renovation, and beauty video skills. It is not a new genre rule and must not override each skill's domain-specific contract.

## Highest-Grade Floor

Formal video production defaults to the highest available quality level. Do not choose a cheaper, faster, or simpler route unless the user explicitly asks for a draft or the domain skill marks the result as non-final.

The shared floor for any final video is:

- scene-level timeline before rendering
- reference analysis and originality plan when a reference video is supplied
- domain-specific contract and truthfulness gates
- asset/source classification for every visual
- art-direction notes for generated/support visuals
- multiple caption templates when the scene type changes
- natural voice or approved voice sample for voice-led videos
- motion that reveals, compares, focuses, or follows sound
- clean voice-first audio; if background music is used, it must come from an approved music library or explicitly authorized same-platform reference music
- HyperFrames or the domain-approved final timeline renderer
- ffprobe/audio-duration proof and no early audio cutoff
- safe-zone review, contact sheet, and native-size detail-frame checks
- final QA with no blocking issues
- publish workflow guard passed before contract/promotion, including manual frame-review evidence, center-crop cover proof, dynamic background/template inheritance, Qingdou/text checks, and exact TOP5 rank lock when the video is a ranked AI list
- background plates provide premium atmosphere, material depth, light, and negative space; foreground components carry real information jobs such as proof, comparison, current step, state change, or caption support

If any required gate cannot pass, the output is `blocked` or `draft`, never `final`.

## AI Video Active Contract And Regression Gate

Use this section as the compact production boundary for AI knowledge and Douyin videos. During planning and storyboard work, follow the positive contract below. Historical failure wording is only for automated gate reports, focused QA, and tests; it is not a daily planning checklist or user-facing status script.

- Select the fixed premium background asset once per video, then use it as atmosphere, material depth, light, and protected reading space.
- Build foreground modules only from the current script's evidence, steps, proof crops, comparisons, captions, and timed state changes.
- Use named advanced transitions that carry an information handoff, such as source-focus handoff, proof-tray lock, node relay, citation wipe, terminal reveal, comparison morph, template lift-settle, or controlled convergence.
- Do not let repeated same-size mega-panels become the default foreground language. In a 45-75 second AI explainer, use at least four distinct scene structures when the scene count allows, such as cover hook, source proof, step rail, risk matrix, operation node map, comparison result, and final template. A panel is acceptable only when its shape, content, and motion are tied to that scene's job.
- Transitions must transfer a proof object, step node, result chip, source rail, cursor packet, or checklist state into the next scene. A decoration-only diagonal sweep, empty rail pass, or node animation may appear only as a brief layer under the handoff; if it holds the screen by itself for roughly 0.4s or more, the boundary must be restaged before final.
- Use the approved background-audio mode. For this user's AI/Douyin videos the default is clean narration only. Background music is allowed only from the music library or explicitly authorized same-platform reference music; self-created/generated music, ambience, noise, continuous SFX beds, electric buzz, texture beds, or whoosh beds are blocking.
- Embed the designed topic cover as frame 0 only by default, then prove frame 1 has returned to the main timeline.
- For 16:9 AI videos headed to Douyin, the cover is still a full horizontal first frame, but the public cover text must fit the platform's center preview crop. Generate and inspect `cover_publish_douyin_center_crop.png`; if the title or subtitle is cropped, shorten/rewrite the cover text before render or publishing.
- Treat cover text, on-screen text, subtitles, title, caption, and topics as one checked text set. If any field changes, rerun the required local/Qingdou check before publishing.
- Reuse the user's logged-in Chrome/session for Qingdou and Douyin publishing tasks, close extra tabs/windows created for the task, and never store passwords, cookies, SMS codes, or verification data.
- Final QA records evidence, not only a render success: ffprobe/audio duration, contact sheet or representative frames, first-frame cover evidence, visual review, text proofread, transition/SFX review, and voice/SFX mix review when both exist.
- Before publish-contract or promotion, `internal/workflow_guard.json` must be refreshed from current artifacts and passed. A stale or manually invented workflow report is a blocking failure; the video remains draft/blocked until the skipped workflow step is actually produced and reviewed.

## Boundary

- AI knowledge videos keep the `douyin-hyperframes-remake` evidence, compliance, storyboard, asset, QA, and no-auto-publish gates.
- Renovation videos keep L1/L2/L3/L4 truthfulness, sample-level walkthrough gates, stable motion rules, HyperFrames final delivery, Qingdou checks, and no auto-publishing.
- Beauty videos keep exactly 4 portraits, Chinese adult women age 25+, tasteful fully clothed fashion direction, TikTok safe zones, HyperFrames final delivery, and the required publishing checklist.
- Shared rules may raise the quality bar, but may not rename a domain output into something it is not.

## Common Rules

- Use free/local/open-source paths first: Codex session tools, local scripts, FFmpeg, Remotion, HyperFrames, screenshots, local recordings, and properly credited free/public sources.
- Global Douyin text compliance applies to every video family: AI, renovation, beauty, and any future Douyin-oriented type. Before drafting designed video text or publish-entry text, read `references/forbidden_terms_learning_bank.md` and active records in `references/forbidden_terms_learning_bank.jsonl`. Before render/final QA, check all designed text such as title cards, subtitles, cover text, poster/card text, badges, labels, CTA, and text overlays. Before publishing, check the exact title, caption/body, and hashtags/topics that will be typed into the platform.
- Do not enable paid video/design/avatar/stock/TTS providers by default. OpenAI/Codex is the allowed exception when the user is already using it; every other paid provider needs explicit approval.
- When a reference video is supplied, analyze it first, classify it as AI/renovation/beauty, make an original production plan, and only then render. Learn pacing, layout, filter mood, typography hierarchy, caption timing, music feeling, and motion language; do not copy original frames, subtitles, people, rooms, creator identity, watermark, or a highly similar full sequence.
- Final rendered on-screen text must be checked against the approved original text package. Major text blocks must stay within <= 10% character-level deviation; generated-image gibberish, wrong Chinese characters, or missing key words are blocking issues.
- If the reference has no narration, default to a no-narration/music-led edit unless the new topic needs voice. For user-provided Douyin reference videos intended for Douyin publishing, treat the reference music as user-authorized same-platform Douyin music and use the reference video's own music or same Douyin music-page track when technically possible. Do not synthesize/generate replacement BGM. If the same reference music cannot be obtained or used, record a blocker and ask for the music file, same-music platform selection, or explicit approval to proceed without BGM; do not silently substitute local stock, similar music, or generated audio.
- Every publish-ready plan needs a scene-level timeline before rendering. Do not create motion only to avoid stillness.
- Every scene must state: content goal, visual hierarchy, asset/source type, caption template, motion purpose, safe zone, and QA risk.
- One dense image/card with multiple steps must be split into multiple scenes. If an image has 4 steps, make 4 richer scenes instead of shaking or zooming one frame.
- Backgrounds are atmosphere stages, with readable foreground space protected by light, depth, local quieting, and negative space.
- Cards, slots, rails, dividers, checkbox lanes, source walls, and panels are foreground objects created only when they carry visible information, a proof crop, a step state, a comparison target, a checklist item, or a timed motion event.
- Repeated large rectangular panels are a warning sign even when they contain useful text. If contact sheets show the same panel size, same left-heavy position, and same bottom caption style across most scenes, redesign the storyboard with more varied information structures before render.
- AI/tech backgrounds use 2-4 abstract intelligence elements such as neural network, data nodes, glowing particles, data flow, digital ripple, or intelligent core, paired with concrete material, lighting, palette, and readability language.
- Daily AI background plates should randomly select one main style from `references/ai_background_random_style_pool.md` and record the selected ID/name/method. Dense full-frame style seeds must be adapted into readable video backgrounds with protected title, caption, and proof-safe zones.
- AI/tech videos that need a technological feel must use `references/enterprise_ai_control_console_visual_system.md` as a unified foreground system. Background, panels, captions, transitions, and SFX must inherit one visual seed; do not make the video feel like ordinary PPT cards pasted over a futuristic background.
- Local readability treatment is mandatory when foreground content sits over dense technology backgrounds: blur, darken, desaturate, and feather the region under the active panel instead of flattening the whole background or sacrificing readability.
- Motion must explain, reveal, compare, guide attention, or follow sound through purposeful scene events.
- Transitions carry an information-state change such as source focus, citation rail wipe, comparison handoff, operation node relay, terminal proof tray, template lift settle, or final controlled convergence. A publish-ready AI video uses multiple advanced transition recipes.
- Dynamic icons and status feedback should be readable from motion alone. Do not add self-created SFX beds or noise to make the motion feel active. If the user explicitly asks for music, choose only approved library/reference music and keep it below narration.
- Static images must not rely on plain Ken Burns movement as the main upgrade. Use image-layer reveals, focus masks, parallax, split-screen comparison, proof-wall assembly, designed portrait entrances, or domain-specific detail motion.
- Caption and title systems must be designed before render: one clear hierarchy per scene, enough negative space, and mobile-safe margins.
- Voice stays natural. If copy is too dense, shorten or split scenes rather than speeding up narration.
- For narration-led AI videos, voice must be clear, firm, thick enough, and clean. Do not add generated/self-created background sound to compensate for weak narration. If approved music is used, duck it below the voice and keep a voice/music QA report.
- Assets must be classified as `proof`, `support`, `generated`, or `free_stock`; generated assets must never impersonate proof and must record provider/model/prompt/evidence-boundary metadata when used in publish-ready videos.

## Shared Music Library

- The unified local music library is `~/Desktop/音乐/mp3`.
- For this user's AI/Douyin knowledge videos, only two background-audio modes are allowed: `library_music_bgm` using an approved local/library/reference track, or `voice_only_clean` with no background sound at all. `voice_only_clean` is the default for narrated tutorials.
- When a video needs BGM and it is not a user-provided Douyin reference-music case, choose already-authorized local files first; if no local track clearly fits, choose from Pixabay Music or Mixkit Music.
- Treat Pixabay and Mixkit tracks as `free_stock` audio, not proof. Record source URL, platform, track title, artist/creator when available, license name or license page, download date, commercial-use status, attribution requirement, local path, duration, and file hash in the project's metadata or production notes.
- `$full-house-custom-ad` and `$beauty-gpt-image-video` should look there first when they need background music, then fall back to their local bundled music folders if needed.
- `$douyin-ai-premium-director` and `$douyin-hyperframes-remake` do not use background music by default for proof-led narrated videos. If the user provides a Douyin reference with BGM, the reference music rule wins: use that same reference music when technically possible, or block for user confirmation instead of generating/substituting BGM.
- `$douyin-ai-premium-director` and `$douyin-hyperframes-remake` must not create their own music, ambience, SFX bed, noise bed, electric buzz, whoosh bed, texture bed, or other continuous background sound. Do not ship `sfx-bed.wav`-style generated/self-made background audio as a final mix.
- Parsed Douyin MP3 files should be saved into the unified music library so the renovation and beauty skills can reuse authorized/local tracks.
- Do not use a track just because it exists in the folder. The skill still needs to check authorization/use boundary, fit, duration, audio quality, recent reuse, and whether the music competes with voice.
- Do not use YouTube, TikTok, streaming-service, reuploaded, unknown-origin music, or locally synthesized/generated music as a replacement BGM unless the user explicitly authorizes that exact track and usage. User-provided Douyin reference music is treated as authorized for Douyin-to-Douyin publishing, but not for cross-platform or non-Douyin use unless separately authorized.

## Common QA

- Confirm all designed text and publish-entry text passed Douyin risk-word checking, and record any detected terms into the forbidden-term learning bank before rewriting.
- Check safe zones for top/bottom overlays, right-side action buttons, captions, and crop risk.
- Check text/background collision, especially background words, white lines, screenshots, and decorative overlays behind titles.
- Check technology-system coherence: one selected style seed, inherited foreground tokens, distinct component families for title/proof/step/comparison/checklist, no overuse of English labels, no game-HUD clutter, and no more than two prominent motions per shot.
- Check that every visible frame, rail, card, divider, and line has an information job in the current scene.
- Check that transition-only frames still show an information handoff. Decoration-only sweeps, diagonal lines, or loose node fields must be brief and cannot replace the source/step/result transfer.
- Check visual density: no frame should contain several unrelated text systems competing for attention.
- Check audio duration, subtitle sync, bitrate/clarity, and whether final render is the correct HyperFrames output.
- Check transition quality and variety against the selected named advanced transition recipes.
- Check background audio policy: the final audio is either clean narration only, or narration plus approved library/reference music. Reject generated/self-created background audio, continuous SFX beds, noise beds, electric buzz, harsh whooshes, or texture ambience.
- Check voice/music balance for narration-led videos: narration first, approved music ducked below it, no unintended silence, no clipping, and no voice thinness caused by post-processing.
- Check provider policy: reject unauthorized paid providers, uncredited stock, fake UI/proof, and copied reference material.
- Check that the result does not look like a generic template export: repeated bottom caption card, low-bitrate render, soft screenshots, same-face image batch, over-dark opening/ending, or motion with no information purpose.
