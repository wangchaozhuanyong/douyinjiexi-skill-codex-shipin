# Visual Prompt And Motion Phrasebook

这份文档整理当前 AI 类视频里用于图片生成、背景板、辅助视觉、封面、分镜 motion、HyperFrames/Remotion 动态效果的描述词。它不是“堆高级词”的词库，而是把视觉味道翻译成可生成、可实现、可质检的导演语言。

## 1. 总原则

一句话：不要只写“高级、科技感、酷炫、震撼”，要写清楚画面做什么、观众一秒内看懂什么、证据放哪里、文字避开哪里、哪个层会动、什么时候动。

所有 AI 知识类视频默认使用 16:9 `1920x1080`，除非已经路由到非 AI 垂类技能。生成图只能做背景、封面、概念、转场、图解底板或支撑卡，不能伪装成真实 UI、官方截图、数据证明、评论、认证或用户反馈。

## 2. 每张生成图必须包含的字段

每一张图一张独立 prompt 卡，不复用同一条通用风格 prompt。

```text
Asset ID:
Scene ID:
Narration line supported:
Asset role:
Scene function:
Visual archetype:
Brightness grade:
Palette family:
Material family:
Layout family:
Energy level:
Visual thesis:
Topic binding:
Beginner usefulness:
Information job:
Background role / Support role:
Viewer takeaway:
Format and safe-zone plan:
Composition:
Foreground:
Midground:
Background:
Camera/lens:
Lighting:
Material/texture:
Color hierarchy:
Color system:
Depth/layering:
Text-safe zones:
Motion usage in HyperFrames/Remotion:
Animation affordance:
Primary animated object:
Dark/light motion rule:
Evidence boundary:
Negative prompt:
Regeneration criteria:
Provider/model:
Prompt ID/path:
Unique prompt:
Diversity check:
```

## 3. Visual System Selector

每张生成图在写具体 prompt 之前，先选择视觉系统。不要默认进入深色科技背景、玻璃卡片、蓝绿色光效。

Required selectors:

- `Scene function`: `hook_result_preview`, `beginner_problem`, `tutorial_step`, `before_after_compare`, `source_proof`, `news_explain`, `industry_context`, `template_summary`, `final_takeaway`
- `Visual archetype`: `bright_productivity_desk`, `clean_tutorial_canvas`, `warm_workspace_board`, `editorial_proof_stage`, `news_explainer_wall`, `industry_scene_plate`, `result_showcase_gallery`, `checklist_template_board`, `soft_3d_diagram_stage`, `split_before_after_lab`
- `Brightness grade`: `L1 deep focus dark`, `L2 dark with bright proof surfaces`, `L3 balanced editorial`, `L4 bright tutorial`, `L5 cover/result bright`
- `Palette family`: `daylight_productivity`, `warm_ivory_graphite`, `clean_blue_white`, `cream_cobalt_orange`, `graphite_ivory_teal`, `newsroom_white_red`, `soft_green_efficiency`, `amber_warning_compare`
- `Material family`: `paper_acrylic`, `whiteboard_marker`, `desk_stationery`, `matte_editorial`, `soft_3d_clay`, `newsroom_panel`, `product_keynote`, `glass_metal`
- `Layout family`: `hero_result_center`, `before_after_split`, `three_step_ladder`, `left_proof_right_steps`, `source_wall_grid`, `diagonal_workflow`, `checklist_stack`, `newsroom_lower_third`, `template_canvas`, `result_gallery`
- `Energy level`: `calm`, `useful`, `urgent`, `tutorial`, `reveal`, `warning`, `celebratory`

Dark/light relationship must describe how dark and light areas cooperate. Do not allow a full dark frame unless the scene is specifically `source_proof` or `warning`.

Beginner friendliness means the frame should feel usable, clear, and close to real work, not mysterious or technical.

Diversity rule: do not repeat the same visual archetype, palette family, and layout family in two consecutive scenes.

## 4. Dark / Light Rhythm Rule

For beginner AI tutorial videos:

- Hook and result preview should use `L4` or `L5`.
- Tutorial steps should usually use `L3` or `L4`.
- Source proof scenes may use `L2` or `L3`.
- Warning or mistake scenes may use `L2` with warm amber highlights.
- Final template or summary should use `L4` or `L5`.

Hard rule:

- No more than 2 dark scenes in a row.
- At least 40% of scenes must be `L4` or `L5` for beginner tutorials.
- At least one bright tutorial canvas must appear before the midpoint.
- If the background is dark, at least 35% of the frame must contain bright proof cards, warm panels, or clean text-safe surfaces.
- Avoid charcoal-on-charcoal, blue-on-black, teal-only palettes, and full-frame dark gradients.

## 5. Brightness Grade

- `L1 deep focus dark`: only for dramatic proof, risk, or warning moments. Important panels must still be bright.
- `L2 dark with bright proof surfaces`: dark background with warm ivory or soft gray proof surfaces. Good for source evidence and serious analysis.
- `L3 balanced editorial`: medium-light background, clear panels, balanced contrast. Good for most explainers.
- `L4 bright tutorial`: warm white, ivory, soft blue, or light gray base. Best for step-by-step operations, templates, and reusable checklists.
- `L5 cover/result bright`: high clarity, strong focal area, bright title-safe zone. Best for cover, first frame, and final takeaway.

## 6. Palette Families

- `daylight_productivity`: warm daylight, paper white, light gray surfaces, ink navy structure, cobalt active accent, amber result highlight. Use for office efficiency, reports, copywriting, tables, and repeated tasks.
- `clean_blue_white`: white and pale blue base, cobalt active states, gray dividers, navy text-safe surfaces. Use for tool tutorials and feature explanation.
- `warm_ivory_graphite`: warm ivory base, graphite frame, muted teal or cobalt accent, soft amber highlight. Use for trustworthy summaries and reusable templates.
- `cream_cobalt_orange`: cream base, cobalt method cards, orange result badge, graphite structure. Use for before/after, result showcase, and time-saving proof.
- `graphite_ivory_teal`: graphite base, large ivory proof panels, restrained teal edge light. Use for source proof and risk judgment only when readability stays high.
- `newsroom_white_red`: white newsroom wall, graphite zones, red only for alert labels, blue-gray context panels. Use for AI news and industry updates.
- `soft_green_efficiency`: soft mint, warm white, graphite, small green progress accents. Use for automation, task completion, and saved steps.
- `amber_warning_compare`: warm gray base, amber warning chip, ivory correction card. Use for mistake correction and do-this-not-that scenes.

## 7. Layout Families

- `hero_result_center`: cover, first 5 seconds, final result. One large result card in the center.
- `before_after_split`: wrong vs correct, manual vs automated, before AI vs after AI.
- `three_step_ladder`: beginner tutorials. Three cards rise vertically or diagonally with clear step slots.
- `left_proof_right_steps`: source-based tutorial. Left proof area, right step rail.
- `source_wall_grid`: evidence scenes only. Many source tiles, one dominant active source.
- `diagonal_workflow`: process explanation. Input starts bottom-left, output exits top-right.
- `checklist_stack`: saveable summary. Rows stack clearly with check icons added later.
- `newsroom_lower_third`: news explainer. Large headline zone, source strip, practical action card.
- `template_canvas`: prompt templates and formulas. Large blank template body with side labels and clean margins.
- `result_gallery`: multiple outputs or result options on a bright gallery wall.

Layout diversity rule:

- Do not use `left_proof_right_steps` for more than 2 scenes in one video.
- Do not repeat the same layout family in consecutive scenes.
- A 60-90 second video should use at least 4 layout families.
- At least one scene should use `before_after_split` or `result_gallery`.
- At least one beginner tutorial scene should use `three_step_ladder` or `checklist_stack`.

## 8. Material Families

- `paper_acrylic`: warm paper grain, matte acrylic tabs, soft card shadows, clean desk surface. Best for beginner tutorials, templates, reports, and copywriting.
- `whiteboard_marker`: clean whiteboard surface, marker rails, sticky-note placeholders, bright daylight. Best for simple concept explanation.
- `desk_stationery`: documents, folders, blank cards, calendar blocks, paper clips, soft desk shadows. Best for productivity and time-saving scenes.
- `matte_editorial`: matte graphite frame, warm ivory proof surface, subtle bevel, studio falloff. Best for source proof and serious explanation.
- `soft_3d_clay`: clay-like geometric nodes, rounded workflow blocks, gentle shadows, bright background. Best for simple abstract AI concepts.
- `newsroom_panel`: white editorial panels, small red alert marker, source strip, clean headline-safe area. Best for AI news and industry updates.
- `product_keynote`: bright stage, product card hero, spotlight, clean gradient, high-contrast title-safe zone. Best for feature reveal and result showcase.
- `glass_metal`: smoked glass, graphite, brushed metal, restrained rim light. Use as one style, not the default.

For beginner tutorials, prefer `paper_acrylic`, `whiteboard_marker`, `desk_stationery`, or `soft_3d_clay`. Do not make `glass_metal` the default material family.

## 9. Color System

Replace vague `Color hierarchy` with a concrete color system:

```text
Color system:
Brightness grade:
Palette family:
Base color:
Surface color:
Primary text-safe surface:
Primary accent:
Secondary accent:
Warm/cool balance:
Light area ratio:
Dark area ratio:
Accent color ratio:
Contrast target:
Forbidden color failure:
```

Example:

```text
Color system:
Brightness grade: L4 bright tutorial.
Palette family: daylight_productivity.
Base color: warm ivory and soft daylight gray.
Surface color: white paper cards with slight cream tone.
Primary text-safe surface: clean warm-white panels for Chinese captions and labels.
Primary accent: cobalt blue for active step.
Secondary accent: warm amber for final result.
Warm/cool balance: 70% warm neutral, 20% cool blue structure, 10% amber result highlight.
Light area ratio: 65%.
Dark area ratio: 20%.
Accent color ratio: 15%.
Contrast target: high readability, no pale text on pale background, no charcoal-on-charcoal.
Forbidden color failure: no all-black background, no teal-only palette, no muddy gray, no over-saturated rainbow.
```

## 10. Texture And Premium Quality Translation

Do not say only `premium` or `high quality`. Translate texture into visible construction details:

- Layer separation: foreground, midground, and background have clear distance and overlap.
- Contact shadow: cards, panels, chips, and frames cast soft shadows on the surface behind them.
- Edge detail: panels have subtle bevels, thin borders, or acrylic edges.
- Material grain: use paper grain, brushed metal grain, matte surface texture, acrylic edge, or fine film grain.
- Lighting direction: define key light, fill light, rim light, and falloff.
- Specular control: glass or acrylic may have small edge highlights, not plastic shine or harsh bloom.
- Contrast hierarchy: the viewer immediately sees primary, secondary, and background layers.
- Clean negative space: empty areas feel intentionally designed, not like a dark blurry gradient.

Forbidden texture failures:

- flat dark gradient
- plastic glossy card
- low contrast charcoal-on-charcoal
- blurry background with no material
- fake neon glow as the only texture
- all panels using the same glass effect
- no contact shadows
- no clear foreground/midground/background separation

## 11. 图片生成常用描述词

### 11.1 Asset Role

- `background_plate`: 无文字背景板，给证据卡、字幕、标题和 callout 留舞台。
- `hero_poster`: 第一帧或封面主视觉，必须有强焦点和大标题安全区。
- `metaphor_visual`: 抽象概念视觉化，比如“任务进入验证门”“来源卡汇聚成证据墙”。
- `diagram_base`: 无文字图解底板，节点、轨道、卡片先生成，文字由 HTML/CSS 加。
- `transition_plate`: 场景过渡板，承接上一镜头元素进入下一镜头。
- `proof_support_card`: 真实截图外面的证明卡框或来源框，不生成假内容。
- `texture`: 细节纹理层，只服务层次，不抢正文。
- `cover`: 可发布封面，不直接截图凑数。

### 11.2 Visual Thesis

用一句具体隐喻，不用空泛风格。

- `repeated manual checking becomes a scheduled monitoring desk`
- `a vague task turns into a structured Codex workbench`
- `official sources assemble into a calm verification wall`
- `a risky prompt passes through an approval gate`
- `tool steps become a left-to-right operation rail`
- `browser evidence locks into a source citation tray`
- `a messy document pile becomes a clean three-step action board`
- `a vague AI request turns into a fill-in-the-blank prompt template`
- `thirty minutes of manual copy-paste becomes one clean output checklist`
- `a confusing AI update becomes one useful button and one clear workflow`
- `a news headline becomes a practical should-I-learn-this decision board`

### 11.3 Topic Binding

必须绑定具体主题：

- `ChatGPT Scheduled Tasks, OpenAI Release Notes, recurring monitoring`
- `Codex long-running agent workflow and repo/test evidence`
- `AI tool tutorial with source page, operation step, and output proof`
- `prompt improvement before/after comparison`
- `multi-plugin production workflow: ImageGen, Remotion, HyperFrames, FFmpeg`
- `writing a short video script from a rough idea`
- `summarizing messy notes into a weekly report`
- `turning a long article into three clear takeaways`
- `using AI to reduce repeated copy-paste work`
- `understanding one AI news update through one practical use case`

不能写：

- `AI background`
- `tech video`
- `future interface`
- `premium technology mood`

### 11.4 Information Job

画面必须服务信息：

- `hold official source crop`
- `hold before/after comparison cards`
- `hold task setup simulation`
- `hold output checklist`
- `hold citation rail`
- `hold terminal proof tray`
- `hold reusable template rows`
- `reserve lower-third caption band`
- `support right-side annotation chips`
- `hold three beginner steps`
- `hold one copyable prompt template`
- `hold wrong prompt and corrected prompt`
- `hold time-saving proof`
- `hold who-should-use-this decision card`
- `hold one visible final result`
- `hold before-AI / after-AI workflow`

### 11.5 Composition

- `large clean left proof-safe area`
- `center workflow lane`
- `right annotation rail`
- `lower-third caption-safe band`
- `one dominant focal object`
- `Swiss editorial grid`
- `source wall on the left, checklist rail on the right`
- `wide horizontal keynote frame`
- `stable proof-first canvas`
- `strong negative space for Chinese title`

### 11.6 Foreground / Midground / Background

Foreground:

- `smoked-glass rails`
- `soft contact shadows`
- `blank anchor panels`
- `thin proof frame edge`
- `cursor path with no fake text`
- `matte card lip`

Midground:

- `abstract browser-frame silhouettes`
- `scheduled timeline checkpoints`
- `blank checklist card bases`
- `source wall placeholders`
- `operation rail`
- `terminal proof tray`
- `evidence gate`

Background:

- `matte graphite editorial control room depth`
- `quiet architectural depth`
- `soft falloff`
- `restrained negative space`
- `charcoal paper stage`
- `studio proof table`
- `software keynote canvas`
- `archive board without clutter`

### 11.7 Camera / Lens

- `35mm straight-on editorial wide shot`
- `50mm product keynote still`
- `stable keynote framing`
- `overhead desk view`
- `macro material detail`
- `straight-on proof board`
- `no tilted camera`
- `no Dutch angle`
- `foreground stable, background slow push-in`

### 11.8 Lighting

- `soft upper-left key light`
- `restrained rim light on panel edges`
- `low ambient glow`
- `realistic contact shadows`
- `softbox reflections`
- `controlled reflections`
- `ambient falloff`
- `subtle screen glow`
- `warm ivory text-safe zones`

### 11.9 Material / Texture

- `smoked glass`
- `matte graphite`
- `brushed aluminum`
- `paper fiber`
- `acrylic`
- `ceramic`
- `OLED black`
- `fine film grain`
- `crisp non-plastic edges`
- `matte card surface`
- `subtle construction texture under 2% contrast`

### 11.10 Color Hierarchy

必须写颜色角色：

- `charcoal base`
- `warm ivory text-safe zones`
- `teal focus accent`
- `amber warning accent`
- `muted blue source verification`
- `soft red only for risk boundary`
- `one accent color reserved for focus`

避免：

- 全片单一蓝紫渐变
- 彩虹渐变
- 霓虹网格
- 大面积黑底压暗
- 亮线穿过字幕区

### 11.11 Text-Safe Zones

- `left proof card area remains clean`
- `right annotation rail remains clean`
- `lower third remains dark and quiet`
- `center-safe title area`
- `no baked text`
- `no pseudo Chinese`
- `no generated labels`
- `HTML/CSS owns all readable text`

### 11.12 Evidence Boundary

必须写清：

- `support only; not evidence`
- `generated background only; not official UI`
- `conceptual metaphor; not screenshot`
- `diagram base; labels added later`
- `proof frame only; real screenshot inserted by HyperFrames`

### 11.13 Negative Prompt

默认负面词：

```text
No fake UI, no fake official screenshot, no fake analytics, no fake review,
no pseudo Chinese, no readable micro text, no random English filler,
no generic robot, no cyberpunk city, no neon grid, no floating particles,
no white lines crossing caption zones, no dense dashboard, no QR code,
no watermark, no contact info, no stock-photo people, no clutter,
no overexposed highlight, no plastic shine, no blurry gradient wallpaper.
no all-black background, no full charcoal frame, no muddy gray palette,
no teal-only color scheme, no blue-on-black low contrast,
no repeated glass card system, no low-contrast caption area.
```

### 11.14 Regeneration Criteria

出现这些情况必须重生成：

- 看起来像通用科技壁纸。
- 有文字、伪 UI、乱码、假 logo。
- 没有清晰证明区、字幕区或标题区。
- 背景线条碰到字幕、标题、CTA 或证据文本。
- 和本期主题无关，只是好看。
- 画面太暗、太糊、太满、太像模板。
- 生成图被误用成证据。

## 12. 常用图片 Prompt 骨架

### 12.1 背景板

```text
Create a 16:9 premium editorial background plate for a Chinese AI explainer about [topic].
Visual thesis: [topic-specific metaphor].
Topic binding: [specific tool/source/workflow].
Information job: hold [source proof / operation simulation / comparison cards / checklist / final template].
Background role: text-free generated support stage, never official proof.
Composition: wide horizontal frame, large clean proof area, quiet annotation rail, lower-third caption-safe band.
Foreground: smoked-glass rails, soft shadow anchors, blank panels, no readable fake text.
Midground: [source wall / browser silhouette / operation rail / evidence gate] with empty overlay zones.
Background: matte graphite editorial depth, realistic falloff, restrained negative space.
Camera/lens: 35mm straight-on editorial wide shot.
Lighting: soft upper-left key light, restrained rim light, low ambient glow, realistic contact shadows.
Material/texture: smoked glass, brushed metal, matte graphite, fine film grain.
Color hierarchy: charcoal base, warm ivory text-safe zones, one accent color for focus.
Motion usage: slow 100%-103% push-in, subtle parallax; proof cards and captions animate above it.
Avoid: fake UI, pseudo text, neon grid, random particles, white lines crossing captions, clutter.
```

### 12.2 封面 / Hero Poster

```text
Create a 16:9 premium hero poster background for a Chinese AI explainer.
Subject: [one exact concept], not a robot mascot.
Visual metaphor: [AI task becomes verified output / source enters evidence gate].
Composition: one dominant focal object, strong negative space for large Chinese title.
Lighting: restrained product-keynote lighting, one key light, one rim light, soft shadow.
Material: matte metal, smoked glass, paper texture, OLED black, controlled reflection.
Text ownership: HTML/CSS adds title and subtitle; no baked text in image.
Avoid: fake UI, pseudo Chinese, robot face, random charts, cyberpunk city, messy cables.
```

### 12.3 图解底板

```text
Create a clean 16:9 diagram base for an AI workflow explainer.
Diagram idea: [pipeline / comparison / risk matrix / checklist].
Do not generate readable text. Use blank nodes, rails, cards, and placeholders only.
Composition: large shapes, clear left-to-right flow, lower-third caption safe.
Motion usage: nodes light up one by one in HyperFrames; labels added later.
Avoid: pseudo labels, dense lines, random icons, tiny text, fake logos.
```

### 12.4 转场板

```text
Create a 16:9 transition plate from [scene A] to [scene B].
Continuity anchor: [same cursor / source tag / rail / chapter marker] remains visible.
Composition: old idea recedes while new proof area opens.
Motion plan: old panel remains 8-14 frames while new panel slides over it.
Avoid: full-screen flash, unrelated new background, hard reset, random wipe.
```

## 13. 动态效果描述词

### 13.1 Motion Brief 字段

```text
Motion thesis:
Rhythm:
Camera policy:
Visual hierarchy lock:
Information reveal:
Focus cue:
Transition logic:
SFX pairing:
Hold policy:
Negative motion:
```

### 13.2 Motion Purpose

- `reveal`: 让一个新信息出现。
- `verify`: 让证据进入并锁定。
- `compare`: 左右/前后对比。
- `warn`: 风险边界、错误提示、敏感点。
- `connect`: 节点串联、流程传递。
- `summarize`: 模板、清单、结论稳定收束。

### 13.3 Motion Actors

- `source card`
- `proof screenshot`
- `citation rail`
- `cursor highlight`
- `risk chip`
- `approval gate`
- `operation node`
- `workflow packet`
- `terminal proof tray`
- `template row`
- `caption rail`
- `focus lens`
- `marker sweep`

### 13.4 入口动效

- `fade-up from y=20px opacity 0`
- `slides from x=-64 to x=0`
- `mask reveal`
- `clip-path reveal`
- `card lift 20px then settle`
- `source crop enters through soft lens mask`
- `rows lift in one by one`
- `terminal lines scan in`
- `risk chip pulses once then locks`
- `cursor draws a soft rectangular highlight`

### 13.5 镜头运动

- `slow 100% to 103% push-in`
- `subtle parallax`
- `foreground stable, background moves quietly`
- `static hold for readability`
- `tracking only when following a workflow rail`
- `no rotation`
- `no page shaking`
- `no random drift`
- `no whole screenshot movement while reading`

### 13.6 转场 Recipe

- `source_focus_lens_reveal`: 来源截图裁切进入、镜头聚焦、citation callout 出现。
- `citation_rail_wipe`: 来源/日期/信号卡稳定落位，细轨道从左到右擦入。
- `comparison_split_handoff`: 错/对两侧面板从两边进入，风险 chip 依次出现。
- `operation_node_relay`: 流程节点依次点亮，光标/packet 沿轨道传递。
- `terminal_scan_proof_tray`: 终端或代码输出扫描出现，证据托盘从下方滑入。
- `template_lift_settle`: 清单行逐个抬起，最后进入稳定可读状态。
- `final_controlled_zoom`: 只在最终 CTA/模板上做一次克制推进。

45-75 秒 AI 视频至少要用 5 种，不允许全片只有同一种 fade 或 slide。

### 13.7 字幕/关键词动效

- `keyword highlight only`
- `subtle scale-pop max 1.08x for 0.25s`
- `caption fades in over 160ms`
- `caption remains in stable lower third`
- `no every-word bouncing`
- `no long typewriter effect`
- `caption style changes by scene type`
- `caption never overlaps proof panel`

### 13.8 Glow / Audio Reactive / SFX

- `ambient glow opacity 8%-18%`
- `text reactive scale 3%-5%`
- `background glow 10%-15%`
- `one soft tick when card locks`
- `marker sweep sound below narration`
- `soft thump for card settle`
- `no whoosh spam`
- `SFX stays below voice`

### 13.9 Negative Motion

禁止默认使用：

- `page shaking`
- `random camera drift`
- `loop pulse`
- `generic zoom`
- `full-screen flash`
- `spinning cards`
- `glitch spam`
- `chaotic movement`
- `decorative particles`
- `white line animation behind captions`
- `multiple labels moving in one reading zone`
- `transition for transition's sake`

## 14. 当前实际项目里的常用组合

最近项目 `chatgpt-scheduled-tasks` 使用的典型组合：

- 背景世界：`scheduled monitoring desk`
- 视觉系统：`dark editorial proof desk`
- 证明区：`source proof zone`
- 流程区：`task setup lane`
- 模板区：`template rail`
- 材质：`smoked glass`, `brushed metal`, `matte graphite`, `fine film grain`
- 光线：`soft upper-left key light`, `amber rim`, `muted teal ambient glow`
- 动作：`slow 100%-103% push-in`, `quiet parallax`, `card lock`, `keyword highlight`
- 字幕：`stable lower third`, `keyword highlight only`
- 负面约束：`no fake UI`, `no pseudo Chinese`, `no neon grid`, `no particles`

## 15. 我看到的当前问题

1. 最近项目的 `background_prompt_pack.md` 字段是完整的，但记录显示 ImageGen 返回的是内联图，没有稳定保存到 workspace 的本地文件路径。以后生成图必须补强“图片文件可追溯路径 + asset_manifest 记录 + 样帧验收”。
2. 实际 storyboard 里部分 motion 仍然偏模板化，例如大量使用 `blur crossfade`、`smooth push slide`、`foreground panel fade-up`。这能跑通，但高级感不够稳定；后续应按每个镜头的信息目的强制换 recipe。
3. 图片描述词已经避免了“高级科技感”这类空词，但还要继续加强“每张图的 topic binding”，否则会变成好看的通用背景。
4. 动态效果不能只写给 HyperFrames 看，还要能让人验收：哪个元素动、为什么动、何时动、停在哪里读，必须写清楚。
5. 生成图不能承担证据功能。真实证据必须来自截图、网页、终端、文件、QA 报告或可验证来源。

## 16. 快速验收清单

- 每张图是不是一图一 prompt？
- 有没有 `visual_thesis`、`topic_binding`、`information_job`？
- 有没有前景/中景/背景？
- 有没有镜头、光线、材质、色彩角色？
- 有没有字幕/标题/证明区安全区？
- 有没有 `motion_usage` 和 `animation_affordance`？
- 有没有证据边界？
- 有没有负面词和重生成标准？
- 动效是不是绑定口播节奏？
- 45-75 秒视频是否至少 5 种有效转场 recipe？
- 最终样帧里文字、白线、截图文字、字幕有没有互相打架？
