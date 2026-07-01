# 方案7 Extended: 蚂蚁AI 热榜 TOP5 玻璃星云版

Canonical profile: `ant_ai_hotlist_extended`

Use this profile when the user asks to make an AI 热榜 TOP5 video to the same production standard as the analyzed AI研究所 reference, while keeping the work original and branded as `蚂蚁AI`.

This profile is a fixed production workflow, not a fixed script. Every episode must use fresh, real, source-backed content.

## Fixed Identity

- Brand name: `蚂蚁AI`
- Fixed CTA text: `关注 蚂蚁AI`
- Scheme id: `scheme_7_ai_hot_rank_top5`
- Scheme variant: `ant_ai_hotlist_extended`
- Format: 1080x1920, 9:16
- Target duration: 50-60 seconds
- Voice: fixed template male narration, `VOICE_MALE_THICK_YUNYANG_V1`, `zh-CN-YunyangNeural`
- BGM source id: `ant_ai_scheme7_top5_reference_bgm_7654135072895400421`
- BGM local path: `/Users/wangchao/Desktop/音乐/mp3/蚂蚁AI_方案7_TOP5_参考BGM_7654135072895400421.mp3`
- BGM boundary: user-provided Douyin reference music for same-platform Douyin use only. Do not reuse cross-platform without fresh user approval.
- Background template id: `BG_FIXED_11_ANT_AI_HOTLIST_NEBULA_9X16`
- Dynamic background: `assets/ai_background_templates_dynamic/BG_DYNAMIC_11_蚂蚁AI热榜星云_9x16.mp4`
- Template preview: `assets/ai_background_templates_dynamic/BG_DYNAMIC_11_蚂蚁AI热榜星云_9x16.poster.png`
- Design contract: `references/ant_ai_hotlist_galaxy_design_contract.md`
- Quality checklist: `references/ant_ai_hotlist_galaxy_quality_checklist.md`
- Preview console: `templates/ant_ai_hotlist_galaxy/preview.html`

## Reference Learning Summary

The reference's useful production standard is:

- One clear vertical hot-rank identity in the first viewport.
- A dense but readable 5-item information rhythm.
- Continuous dynamic background, not isolated static cards.
- Glass foreground layers that reveal background motion while keeping text readable.
- High-contrast title block, rank rows, and source/date pins.
- Music carries speed and urgency; narration explains why the item matters.
- CTA is short and brand-owned at the end.

Do not copy:

- Reference creator name, watermark, subtitles, exact wording, frame pixels, exact layout proportions, original proof screens, voice, or complete shot order.
- `关注AI研究所` or similar creator identity. Always use `关注 蚂蚁AI`.

## Background Design Standard

The fixed background should read as a high-end AI hotlist environment, and it must follow `references/ant_ai_hotlist_galaxy_design_contract.md`:

- Base: deep blue-black space with real nebula texture, cyan/violet atmosphere, subtle warm magenta highlights, vignette, fine grain, and depth of field.
- Locked plate: the base plate stays stable. Do not use full-frame scale, Ken Burns push, whole-image pan, or whole-image drift.
- Galaxy layer: a separate elliptical galaxy disk rotates locally inside the frame with `centerX=0.52`, `centerY=0.44`, `width=1.18`, `tiltDeg=-17`, `scaleY=0.62`, `rotationDuration=42`, `opacity=0.58`, and `maskFeather=0.72`.
- Quality layer: star dust twinkle and rare meteors are restrained; the background should be darker, steadier, and more layered instead of brighter and busier.
- Foreground support: center darkening is local and feathered; it cannot become a solid black panel.
- Material: transparent glass, thin luminous rails, star dust, orbital glow, and local text shadows.
- Contrast target: foreground glass panel default alpha is about `0.26`, allowed range `0.24-0.34`. Background motion must remain visible through the card.
- Readability: large title area, calm center, no baked text, no logo, no fake UI labels.
- Row rhythm: countdown rows should lock in on beats; each row gets one source/date tick.

The preview is a contract sample, not final episode content. Replace sample rows with real ranked items every time.

Before a new final render, open `templates/ant_ai_hotlist_galaxy/preview.html` or an equivalent local preview, check card alpha, galaxy speed, and cover frame, then run `python3 scripts/check_ant_ai_galaxy_template.py`.

## Episode Structure

Use this order unless the user explicitly asks otherwise:

1. Frame 0 cover: `蚂蚁AI 热榜TOP5` plus date or trend thesis.
2. Opening identity, 2-4 seconds: date + `AI热榜TOP5`.
3. Trend thesis, 3-6 seconds: one sentence explaining what today's five items have in common.
4. Rank 5 to Rank 2, about 7-9 seconds each:
   `rank -> concrete object/event -> source/date -> why now -> viewer action`.
5. Rank 1, about 9-12 seconds: larger emphasis, strongest reason, clearer action.
6. Closing lock, 2-4 seconds: saveable takeaway + `关注 蚂蚁AI`.

## Title Formula

Title should identify the episode and the shared trend, not use a vague slogan.

```text
第N集 | M.D AI热榜TOP5 | {{五条内容背后的共同趋势}}
```

Examples of valid title shapes:

- `第3集 | 6.22 AI热榜TOP5 | 从跨App智能体到开源模型加速`
- `第4集 | 6.30 AI热榜TOP5 | 大厂模型更新正在变成可用工具`

Do not invent the date, episode number, or trend. If date or episode is unknown, derive it from the project plan or ask the user before publishing.

## Copywriting Grammar

This is the fixed writing method. The actual content changes every episode.

### Opening

```text
今天的 AI 热榜 TOP5，核心不是谁声音大，而是谁已经有真实来源、真实更新、真实可用动作。
```

Adapt the sentence to the scanned sources. It must not claim platform-wide ranking unless an official ranking source proves it.

### Rank Item

Each ranked item uses the same logic:

```text
第{{rank}}条，{{具体AI产品/模型/功能/事件}}。
来源是{{source_title}}，时间是{{visible_date}}。
它现在值得看，是因为{{why_now}}。
对普通用户来说，最直接的动作是{{viewer_action}}。
```

For shorter rows, compress but keep all five parts:

```text
TOP{{rank}}：{{object}}。{{source/date}}，关键变化是{{why_now}}，你可以{{viewer_action}}。
```

### Rank 1

Rank 1 needs one extra layer:

```text
今天最值得排第一的，是{{object}}。
不是因为它热闹，而是因为{{practical_reason}}。
如果你只看一条，先看它能不能帮你{{viewer_task}}。
```

### Closing

```text
这就是今天的 AI 热榜 TOP5。想继续看真实来源整理后的 AI 更新，关注 蚂蚁AI。
```

The close may be rewritten, but must keep the brand-owned CTA and must not copy the reference creator identity.

## Search And Evidence Standard

Every episode must search real current content before writing:

- Prefer the task date first.
- If fewer than five usable signals exist, expand only to the latest 7 calendar days and record that in `internal/hot_rank_scan_report.md`.
- Ranked items require visible date and source title.
- Prefer primary or near-primary sources: official company blog/docs, GitHub releases/repos, Hugging Face model/dataset/paper pages, official research pages, verified product release notes, or credible event pages.
- Social posts, repost summaries, rumor threads, and unsourced articles can be supporting context only; they cannot be the ranked evidence source.
- No invented hot signals, fake rankings, fake dates, fake URLs, fake screenshots, or vague claims such as `全网都在说`.
- If a claim cannot be sourced, remove it or mark it as background context outside the rank item.

## Ranking Data Contract

`internal/ai_hot_rank_top5.json` must contain exactly five items sorted by `rank_score` descending. Each item must include:

- `rank`
- `title`
- `source_title`
- `source_url_or_note`
- `visible_date`
- `why_now`
- `why_it_matters`
- `viewer_action`
- `rank_score`
- `score_breakdown`
- `risk_flags`

Default score weights:

- freshness: 25
- impact: 20
- practical_value: 20
- source_strength: 15
- visual_clarity: 10
- compliance_safety: 10

## Rendering And QA

- Run `scripts/select_fixed_ai_templates.py` after director/style lock. Extended profile must select `BG_FIXED_11_ANT_AI_HOTLIST_NEBULA_9X16`.
- Fixed template selection must record `fixed_cta=关注 蚂蚁AI`, `voice_policy=required_narration`, and the Ant AI BGM source id.
- BGM must be ducked below narration and verified in the final audio QA.
- Cover text and all public text still go through local compliance and Qingdou.
- The glass card must use transparent material; large fills above alpha `0.34` are blocking.
- The dynamic background must prove local galaxy rotation and no full-frame push/scale.
- The online preview console must exist before MP4 export for this profile.
- Workflow guard must pass before final or publish contract.
