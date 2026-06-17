# Shared Video Quality Core

This reference is the common quality language shared by the AI, renovation, and beauty video skills. It is not a new genre rule and must not override each skill's domain-specific contract.

## Highest-Grade Floor

Formal video production defaults to the highest available quality level. Do not choose a cheaper, faster, or simpler route unless the user explicitly asks for a draft or the domain skill marks the result as non-final.

The shared floor for any final video is:

- scene-level timeline before rendering
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

If any required gate cannot pass, the output is `blocked` or `draft`, never `final`.

## Boundary

- AI knowledge videos keep the `douyin-hyperframes-remake` evidence, compliance, storyboard, asset, QA, and no-auto-publish gates.
- Renovation videos keep L1/L2/L3/L4 truthfulness, sample-level walkthrough gates, stable motion rules, HyperFrames final delivery, Qingdou checks, and no auto-publishing.
- Beauty videos keep exactly 4 portraits, Chinese adult women age 25+, tasteful fully clothed fashion direction, TikTok safe zones, HyperFrames final delivery, and the required publishing checklist.
- Shared rules may raise the quality bar, but may not rename a domain output into something it is not.

## Common Rules

- Use free/local/open-source paths first: Codex session tools, local scripts, FFmpeg, Remotion, HyperFrames, screenshots, local recordings, and properly credited free/public sources.
- Do not enable paid video/design/avatar/stock/TTS providers by default. OpenAI/Codex is the allowed exception when the user is already using it; every other paid provider needs explicit approval.
- Every publish-ready plan needs a scene-level timeline before rendering. Do not create motion only to avoid stillness.
- Every scene must state: content goal, visual hierarchy, asset/source type, caption template, motion purpose, safe zone, and QA risk.
- One dense image/card with multiple steps must be split into multiple scenes. If an image has 4 steps, make 4 richer scenes instead of shaking or zooming one frame.
- Backgrounds are stages, not competing content layers. Avoid readable background text, random white linework, pseudo UI, decorative grids, and texture that collides with foreground text.
- Motion must explain, reveal, compare, guide attention, or follow sound. Reject page shaking, random drift, aggressive zoom, and transitions whose only purpose is "not static".
- Static images must not rely on plain Ken Burns movement as the main upgrade. Use image-layer reveals, focus masks, parallax, split-screen comparison, proof-wall assembly, designed portrait entrances, or domain-specific detail motion.
- Caption and title systems must be designed before render: one clear hierarchy per scene, enough negative space, and mobile-safe margins.
- Voice stays natural. If copy is too dense, shorten or split scenes rather than speeding up narration.
- Assets must be classified as `proof`, `support`, `generated`, or `free_stock`; generated assets must never impersonate proof and must record provider/model/prompt/evidence-boundary metadata when used in publish-ready videos.

## Shared Music Library

- The unified local music library is `~/Desktop/音乐/mp3`.
- When a video needs BGM and no already-authorized local track clearly fits, choose from Pixabay Music or Mixkit Music first.
- Treat Pixabay and Mixkit tracks as `free_stock` audio, not proof. Record source URL, platform, track title, artist/creator when available, license name or license page, download date, commercial-use status, attribution requirement, local path, duration, and file hash in the project's metadata or production notes.
- `$full-house-custom-ad` and `$beauty-gpt-image-video` should look there first when they need background music, then fall back to their local bundled music folders if needed.
- `$douyin-ai-premium-director` and `$douyin-hyperframes-remake` do not use background music by default for now. AI knowledge videos should prioritize proof clarity, narration, captions, and subtle SFX unless the user explicitly asks for music.
- Parsed Douyin MP3 files should be saved into the unified music library so the renovation and beauty skills can reuse authorized/local tracks.
- Do not use a track just because it exists in the folder. The skill still needs to check authorization/use boundary, fit, duration, audio quality, recent reuse, and whether the music competes with voice.
- Do not use YouTube, Douyin, TikTok, streaming-service, reuploaded, or unknown-origin music unless the user provides explicit authorization for that exact track and usage.

## Common QA

- Check safe zones for top/bottom overlays, right-side action buttons, captions, and crop risk.
- Check text/background collision, especially background words, white lines, screenshots, and decorative overlays behind titles.
- Check visual density: no frame should contain several unrelated text systems competing for attention.
- Check audio duration, subtitle sync, bitrate/clarity, and whether final render is the correct HyperFrames output.
- Check provider policy: reject unauthorized paid providers, uncredited stock, fake UI/proof, and copied reference material.
- Check that the result does not look like a generic template export: repeated bottom caption card, low-bitrate render, soft screenshots, same-face image batch, over-dark opening/ending, or motion with no information purpose.
