# Beginner Copy And Visual Sync Rules

Use this reference before topic selection, scripting, image prompting, HyperFrames authoring, rendering, or publishing whenever the video teaches a tool, software, AI workflow, Codex Skill, productivity method, or any idea meant for non-professional viewers.

## Goal

The viewer should finish the video thinking:

- I understand what this software is for.
- I know the next simple action to try.
- The software looks convenient, not intimidating.
- The image, screen, and narration always point to the same idea.

If the video is accurate but only professionals understand it, rewrite it. If the narration is clear but the picture shows something else, rebuild the scene.

## Topic Lock

Before writing the script, lock one plain-language topic in `production-notes.md`.

Required fields:

- `plain_topic`: one sentence a beginner can repeat.
- `viewer`: who this is for, such as a shop owner, creator, designer, student, or office worker.
- `beginner_problem`: the annoying task or confusion they have today.
- `software_promise`: what becomes easier after using the software.
- `final_takeaway`: the one thing the viewer should remember.

Good topic examples:

- `不会剪辑的人，怎么用这个软件把图片做成一条短视频。`
- `小白怎么用 Codex Skill 少走弯路，直接做出成片。`
- `不用懂提示词，也能让 AI 帮你生成更像样的产品图。`

Reject vague topics:

- `AI 工具介绍`
- `高级工作流`
- `效率提升方法`
- `软件能力解析`

## Audience Value Gate

Do not make a video that is only correct. Make a video a busy viewer would keep watching.

Before scripting, define:

- `hook_reason`: why a viewer stops in the first 2 seconds.
- `watch_reason`: what question or promise keeps them watching after the hook.
- `save_reason`: what checklist, method, shortcut, or before/after result makes the video worth saving.
- `share_reason`: who the viewer would send it to and why.
- `trust_reason`: what real screenshot, proof, result, or concrete workflow makes the viewer believe it.

Good content patterns:

- problem to solution: `不会剪辑 -> 上传图片 -> 自动生成 -> 检查 -> 导出`
- mistake correction: `你不是不会用 AI，是第一步没有给它正确素材`
- before/after: `原来要手动剪，现在只需要按三步走`
- checklist: `小白只看这三处，就知道成片能不能用`
- proof first: show the result quickly, then explain how it was made

Reject content if:

- the first 5 seconds only says hello or introduces the topic slowly
- the viewer cannot see a result, proof, or useful method early
- every sentence sounds like a feature list
- the ending gives no reason to save, share, or try the software

## Beginner Copy Gate

Write as if explaining to a smart friend who has never used the tool.

Required style:

- Start from a real-life problem before naming features.
- Use short spoken Chinese sentences.
- Explain one action at a time: open, upload, choose, click, wait, check, export.
- Say what the viewer gets after each action.
- Use product names only when they help the viewer identify the tool.
- Translate jargon into everyday meaning before using the jargon.

Avoid:

- abstract feature lists
- long setup paragraphs
- stacked professional terms
- unexplained English-heavy tool language
- claims such as `提升效率` without showing what became faster
- a script that could be pasted into a blog post without changing anything

Before production, run the beginner repeat test:

- Could a beginner say the topic back in one sentence?
- Could they name the first action to try?
- Could they explain why the software is convenient?

If any answer is no, rewrite the script before Qingdou, image generation, TTS, or rendering.

## Copy Lock And Compliance Gate

Lock all public-facing copy before making assets or video.

Required copy package:

- video title
- first-5-second hook
- voiceover script
- subtitles/captions
- on-screen labels and callouts
- cover text
- publish caption
- hashtags
- any text requested inside generated images

Run `scripts/check_public_copy.py` or an equivalent local compliance review first, then Qingdou or the current approved sensitivity checker when publishing is intended. Do not generate images, TTS, HyperFrames scenes, or final renders until this package is checked, rewritten if needed, and recorded in `production-notes.md`.

Treat these terms and patterns as unsafe by default unless the user explicitly provides a compliant, evidence-backed reason:

- absolute/exaggerated claims: `最强`, `第一`, `唯一`, `保证`, `100%`, `永久`, `必火`, `必爆`, `包成功`
- false authority: `官方认证`, `国家级`, `央视推荐`, `权威背书`, `专家推荐` without proof
- money or result promises: `秒赚`, `暴富`, `无风险`, `稳赚`, `包过`, `躺赚`
- diversion/contact: `微信`, `VX`, `QQ`, `加群`, `扫码`, `电话`, `私信领取`, `联系方式`
- sensitive domains without qualification: adult, gambling, political/military, medical/financial promises, illegal or dangerous behavior
- fake proof: fake customer reviews, fake case studies, fake analytics, fake official notices

When a useful phrase is risky, rewrite it to a softer practical wording: use `适合`, `可以`, `建议`, `更容易`, `更清楚`, `减少重复步骤`, or `结合实际情况`.

The first-5-second hook must also pass compliance. Do not use fear bait, exaggerated results, guaranteed outcomes, or sensitive terms just to improve retention.

## Voice-To-Visual Beat Map

Every storyboard scene must include a beat map. Do not use loose scene descriptions.

Minimum scene fields:

```json
{
  "index": 1,
  "beginner_goal": "what the viewer should understand in this scene",
  "voice": "spoken line",
  "screen_text": "short Chinese title, caption, or callout",
  "visual": "exact image, screenshot, UI state, diagram, or proof shown now",
  "motion": "how the visual appears, highlights, or changes while the voice speaks",
  "safe_zone": "where title, subtitle, CTA, and media are allowed",
  "sync_check": "why this visual matches this voice line"
}
```

Hard sync rules:

- If the voice says `上传图片`, show uploading or a selected image state.
- If the voice says `自动生成视频`, show generation progress or the resulting video.
- If the voice says `检查效果`, show preview, comparison, or error/fix state.
- If the voice says `导出`, show export, final file, or delivery folder.
- If the voice says `很方便`, prove it with fewer steps, a before/after, or an obvious saved action.

Do not show decorative images while explaining operational steps. If no real UI proof is available, use a clearly labeled concept diagram and do not imply it is a real screen.

## One Idea Per Beat

Do not dump five points on screen and narrate them one by one while the frame stays still.

Use one of these structures:

- Split: one scene or image per knowledge point.
- Build: show the base image first, then reveal one callout at a time.
- Focus: keep the same screenshot but move a highlight/cursor/zoom frame to the exact area being explained.
- Compare: show before/after or old/new states when the point is about improvement.

Rules:

- A viewer should know where to look within 1 second of each spoken point.
- No scene may introduce more than one new concept without a visual reveal or focus change.
- If a generated image contains multiple useful areas, choreograph the narration by area instead of treating the image as a static background.

## GPT-Image-2 Prompt Contract

Use image generation to create premium scene assets, not vague background pictures.

Every generated-image prompt should include:

- `Design a premium, information-rich, commercial-grade image...`
- the exact scene purpose and beginner takeaway
- target aspect ratio and where clean text-safe space must remain
- foreground, middle-ground, and background layers
- a clear focal point and visual hierarchy
- realistic or editorial lighting
- crisp details, high resolution, sharp edges, no blur
- Chinese-first visual context when text is unavoidable
- no fake UI claims, watermarks, logos, unreadable filler text, or random English words
- no sensitive words, exaggerated claims, contact information, QR codes, fake reviews, fake certificates, or fake official badges
- no pseudo-Chinese, malformed Chinese-like glyphs, random Chinese characters, or unreadable baked-in text

Reusable prompt skeleton:

```text
Design a premium, information-rich, commercial-grade image for a Chinese software tutorial video.
Scene purpose: [what the beginner should understand].
Main subject: [software/user/result/diagram].
Composition: [9:16 or 16:9], clear focal point, layered foreground/midground/background, premium product-demo/editorial style.
Safe zones: leave clean negative space for Chinese headline at [top/left/right] and subtitles at [bottom]; no important image elements in those areas.
Detail quality: crisp, high-resolution, realistic lighting, tactile materials, sharp UI-like panels, readable hierarchy, no blur, no low-quality template feeling.
Text policy: do not bake long text into the image; avoid pseudo-Chinese, malformed Chinese-like glyphs, random Chinese characters, random English filler, and unreadable UI text. Leave important Chinese text for HyperFrames HTML overlays.
Compliance policy: do not generate sensitive words, exaggerated claims, contact information, QR codes, fake customer reviews, fake official certification, fake platform notices, or fake authority badges.
Do not include: watermarks, platform logos, fake official UI, celebrity likeness, phone numbers, or elements covering future captions.
```

Prompt quality checks:

- Does the prompt say the image is premium and information-rich?
- Does it name the beginner takeaway?
- Does it reserve safe space for text?
- Does it ask for layered composition and crisp details?
- Does it avoid baking long text into the image?
- Does it explicitly ban sensitive words and pseudo-Chinese text?

If the generated image is flat, generic, low-texture, blurry, English-heavy, or has no safe text area, regenerate or redesign before HyperFrames authoring.

Generated image text rules:

- Prefer no baked-in text. Add titles, subtitles, labels, captions, buttons, and CTA in HyperFrames as real editable Chinese text.
- If text inside the image is unavoidable, keep it to 1-4 simple Chinese words, pre-check the words, and inspect the output manually.
- Reject and regenerate any image with pseudo-Chinese, garbled characters, random Chinese-like strokes, risky claims, contact details, fake badges, or text that cannot be read on a phone.
- Never rely on generated image text for legal, pricing, official, testimonial, medical, financial, or performance claims.

## Free-First Tool Stack

Use available/free or already-authorized tools before paid services.

Default tool order:

- Use real screenshots, screen recordings, local files, and product proof before generated imagery.
- Use HyperFrames and local HTML/CSS/JS for layout, typography, labels, subtitles, animation, SFX mixing, preview, and render.
- Use Browser for local preview, screenshots, layout inspection, and text-over-image collision checks.
- Use Chrome only when current logged-in state is needed, such as Qingdou checking, Douyin creator upload, or creator analytics. Do not store credentials, cookies, or SMS codes.
- Use Computer Use only as a fallback for UI operations that Browser or Chrome tools cannot handle.
- Use local scripts, ffmpeg/ffprobe/image extraction, contact sheets, and full-size frame review for QA.
- Use built-in image generation or `gpt-image-2` only when it is available in the current context and the task budget/authorization is clear. If the cost is uncertain or many images are needed, ask before large-batch generation.
- Avoid paid HeyGen avatars, paid stock assets, paid voice services, and other cost-incurring services unless the user explicitly approves.

## Motion And Layout Rules

The video must not feel paused.

Required:

- Every scene must have a useful movement within the first 1-2 seconds.
- Each spoken point must trigger a visual change: reveal, highlight, cursor move, mask wipe, panel insert, card stack, split-screen slide, checklist tick, or comparison switch.
- A still image must have at least two animated layers, such as background drift plus foreground insert, screenshot push plus callout reveal, or product frame plus subtitle build.
- No image may sit unchanged while multiple points are spoken.
- Screenshots, generated images, cards, and callouts must stay out of title, subtitle, and CTA safe zones.
- Motion paths must not pass through text areas unless masked and intentional.

Reject:

- one static image with narration
- five points visible from the first frame
- only Ken Burns zoom or pulse as the motion plan
- image panels covering or squeezing Chinese titles/subtitles
- animation that explains nothing

## Validation Gates

Before final render:

- Run the audience value review: hook reason, watch reason, save reason, share reason, trust reason.
- Run a beginner clarity review: topic, first action, convenience promise.
- Run a voice-to-visual sync review for every scene.
- Check that each image prompt follows the prompt contract.
- Inspect crowded frames at full size for text/image collision.
- Confirm that multi-point scenes build or split the points instead of dumping them.

After render:

- Watch or inspect the first 5 seconds separately.
- Sample representative frames and verify the visible image matches the current voice/caption.
- Confirm no important image, card, or page blocks the designed text.
- Confirm the video never stays visually unchanged while the narration advances.
- If the final video does not make the software feel easy for a beginner, rewrite and rerender.

Record these results in `production-notes.md`:

- `plain_topic`
- audience value review result
- beginner repeat test result
- voice-to-visual sync result
- image prompt quality result
- multi-point reveal/split decisions
- layout safety result
- whether the final video makes the software feel convenient for a beginner
