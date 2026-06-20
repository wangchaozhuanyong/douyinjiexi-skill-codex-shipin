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
- subtle SFX for meaningful transitions when it improves the edit
- HyperFrames or the domain-approved final timeline renderer
- ffprobe/audio-duration proof and no early audio cutoff
- safe-zone review, contact sheet, and native-size detail-frame checks
- final QA with no blocking issues
- background plates are premium atmospheric stages, not unused visual skeletons; use light, material, depth, and negative space instead of empty rails, placeholder cards, or fake UI slots

If any required gate cannot pass, the output is `blocked` or `draft`, never `final`.

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
- If the reference has no narration, default to a no-narration/music-led edit unless the new topic needs voice. For user-provided Douyin reference videos intended for Douyin publishing, treat the reference music as user-authorized same-platform Douyin music and do not block production on music copyright checks. If the same music cannot be extracted or used technically, choose a track with similar mood/BPM/cut rhythm.
- Every publish-ready plan needs a scene-level timeline before rendering. Do not create motion only to avoid stillness.
- Every scene must state: content goal, visual hierarchy, asset/source type, caption template, motion purpose, safe zone, and QA risk.
- One dense image/card with multiple steps must be split into multiple scenes. If an image has 4 steps, make 4 richer scenes instead of shaking or zooming one frame.
- Backgrounds are stages, not competing content layers. Avoid readable background text, random white linework, pseudo UI, decorative grids, and texture that collides with foreground text.
- AI/tech backgrounds should be built from abstract intelligence elements, spatial depth, glowing material, restrained future color, and intentional negative space. Use only 2-4 elements such as neural network, data nodes, glowing particles, data flow, digital ripple, or intelligent core, paired with concrete material/lighting/palette language. Do not default to robots, full-frame circuit boards, dense code, complex HUDs, harsh neon, or unused skeleton layouts.
- Daily AI background plates should randomly select one main style from `references/ai_background_random_style_pool.md` and record the selected ID/name/method. Dense full-frame style seeds must be adapted into readable video backgrounds with protected title, caption, and proof-safe zones.
- AI/tech videos that need a technological feel must use `references/enterprise_ai_control_console_visual_system.md` as a unified foreground system. Background, panels, captions, transitions, and SFX must inherit one visual seed; do not make the video feel like ordinary PPT cards pasted over a futuristic background.
- Local readability treatment is mandatory when foreground content sits over dense technology backgrounds: blur, darken, desaturate, and feather the region under the active panel instead of flattening the whole background or sacrificing readability.
- Motion must explain, reveal, compare, guide attention, or follow sound. Reject page shaking, random drift, aggressive zoom, and transitions whose only purpose is "not static".
- Static images must not rely on plain Ken Burns movement as the main upgrade. Use image-layer reveals, focus masks, parallax, split-screen comparison, proof-wall assembly, designed portrait entrances, or domain-specific detail motion.
- Caption and title systems must be designed before render: one clear hierarchy per scene, enough negative space, and mobile-safe margins.
- Voice stays natural. If copy is too dense, shorten or split scenes rather than speeding up narration.
- For narration-led AI videos, voice must be clear, firm, and thick enough; transition SFX must remain audible below the voice. Do not let FFmpeg `amix` default normalization suppress the narration/SFX mix. Keep a voice/SFX QA report when both exist.
- Assets must be classified as `proof`, `support`, `generated`, or `free_stock`; generated assets must never impersonate proof and must record provider/model/prompt/evidence-boundary metadata when used in publish-ready videos.

## Shared Music Library

- The unified local music library is `~/Desktop/音乐/mp3`.
- When a video needs BGM and no already-authorized local track clearly fits, choose from Pixabay Music or Mixkit Music first.
- Treat Pixabay and Mixkit tracks as `free_stock` audio, not proof. Record source URL, platform, track title, artist/creator when available, license name or license page, download date, commercial-use status, attribution requirement, local path, duration, and file hash in the project's metadata or production notes.
- `$full-house-custom-ad` and `$beauty-gpt-image-video` should look there first when they need background music, then fall back to their local bundled music folders if needed.
- `$douyin-ai-premium-director` and `$douyin-hyperframes-remake` do not use background music by default for now. AI knowledge videos should prioritize proof clarity, narration, captions, and subtle SFX unless the user explicitly asks for music.
- Parsed Douyin MP3 files should be saved into the unified music library so the renovation and beauty skills can reuse authorized/local tracks.
- Do not use a track just because it exists in the folder. The skill still needs to check authorization/use boundary, fit, duration, audio quality, recent reuse, and whether the music competes with voice.
- Do not use YouTube, TikTok, streaming-service, reuploaded, or unknown-origin music unless the user provides explicit authorization for that exact track and usage. User-provided Douyin reference music is treated as authorized for Douyin-to-Douyin publishing, but not for cross-platform or non-Douyin use unless separately authorized.

## Common QA

- Confirm all designed text and publish-entry text passed Douyin risk-word checking, and record any detected terms into the forbidden-term learning bank before rewriting.
- Check safe zones for top/bottom overlays, right-side action buttons, captions, and crop risk.
- Check text/background collision, especially background words, white lines, screenshots, and decorative overlays behind titles.
- Check technology-system coherence: one selected style seed, inherited foreground tokens, distinct component families for title/proof/step/comparison/checklist, no overuse of English labels, no game-HUD clutter, and no more than two prominent motions per shot.
- Check visual density: no frame should contain several unrelated text systems competing for attention.
- Check audio duration, subtitle sync, bitrate/clarity, and whether final render is the correct HyperFrames output.
- Check voice/SFX balance for narration-led videos: narration first, SFX audible but supportive, no unintended silence, no clipping, and no voice thinness caused by post-processing.
- Check provider policy: reject unauthorized paid providers, uncredited stock, fake UI/proof, and copied reference material.
- Check that the result does not look like a generic template export: repeated bottom caption card, low-bitrate render, soft screenshots, same-face image batch, over-dark opening/ending, or motion with no information purpose.
