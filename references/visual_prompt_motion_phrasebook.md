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
Background style pool selection:
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

## 3. Video-Level Dynamic Style Decision

每条 AI 视频在写 `visual_style_plan.json` 之前，必须先写 `internal/visual_style_decision.json`。这一步不是让用户选择，而是 Codex 导演根据内容自主判断：选题类型、文案情绪、证据密度、参考视频节奏/色彩/排版/音乐氛围，以及最终要证明的观众价值。

Required decision fields:

```json
{
  "style_intent": "light_tutorial / dark_evidence / news_editorial / blackboard_grid / product_launch / warning_compare / vertical_list / codex_director_choice",
  "selected_brightness_grade": "L1-L5 with a concrete label",
  "selected_palette_family": "one palette family",
  "selected_material_family": "one material family",
  "selected_layout_family": "one layout family",
  "why_this_style": "content-specific reason tied to topic, copy mood, evidence density, or reference rhythm",
  "why_not_other_styles": "why the obvious alternatives were rejected"
}
```

Style candidates:

- `light_tutorial`: templates, step-by-step workflows, reusable checklists, efficiency tools.
- `dark_evidence`: source code, terminal proof, serious analysis, dense real UI/source evidence.
- `news_editorial`: AI updates, model/tool launches, industry news, policy or timeline explanation.
- `blackboard_grid`: Codex/Skill/plugin tutorials where concepts need a teachable board and proof lanes.
- `product_launch`: new feature, new tool, new solution, release-like reveal.
- `warning_compare`: pitfalls, mistake correction, risk reminders, before/after judgment.
- `vertical_list`: lightweight Skill/tool recommendation references, especially no-voice list/card style.

If the rules do not clearly choose a style, write `style_intent=codex_director_choice` and let Codex decide from the script. The decision must still record `selected_brightness_grade`, `selected_palette_family`, `selected_material_family`, `selected_layout_family`, `why_this_style`, and `why_not_other_styles`.

Hard rules:

- No fixed default color system. Do not choose light, dark, graphite, blue, or `daylight_productivity` just because recent videos used it successfully.
- `daylight_productivity` is only a candidate for content that truly benefits from bright tutorial readability.
- If multiple recent AI videos used the same bright productivity style, the new decision must cite a content reason; otherwise it is a lazy style repeat and fails QA.
- A reference video may inform rhythm, contrast, layout density, and music atmosphere, but not copied frames, subtitles, people, assets, wording, or full sequence.
- Deep/dark styles are allowed when the content needs proof weight, but never all-black, unreadable, blue-black template-like, or subtitle-crushing.

## 4. Visual System Selector

每张生成图在写具体 prompt 之前，先选择视觉系统，并且必须服从 `visual_style_decision.json`。不要默认进入浅色教学卡片、深色科技背景、玻璃卡片、蓝绿色光效。

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

## 5. Dark / Light Rhythm Rule

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

## 6. Brightness Grade

- `L1 deep focus dark`: only for dramatic proof, risk, or warning moments. Important panels must still be bright.
- `L2 dark with bright proof surfaces`: dark background with warm ivory or soft gray proof surfaces. Good for source evidence and serious analysis.
- `L3 balanced editorial`: medium-light background, clear panels, balanced contrast. Good for most explainers.
- `L4 bright tutorial`: warm white, ivory, soft blue, or light gray base. Best for step-by-step operations, templates, and reusable checklists.
- `L5 cover/result bright`: high clarity, strong focal area, bright title-safe zone. Best for cover, first frame, and final takeaway.

## 7. Palette Families

- `daylight_productivity`: warm daylight, paper white, light gray surfaces, ink navy structure, cobalt active accent, amber result highlight. Candidate only; use for office efficiency, reports, copywriting, tables, repeated tasks, or beginner templates when `visual_style_decision.json` gives a content-specific reason.
- `clean_blue_white`: white and pale blue base, cobalt active states, gray dividers, navy text-safe surfaces. Use for tool tutorials and feature explanation.
- `warm_ivory_graphite`: warm ivory base, graphite frame, muted teal or cobalt accent, soft amber highlight. Use for trustworthy summaries and reusable templates.
- `cream_cobalt_orange`: cream base, cobalt method cards, orange result badge, graphite structure. Use for before/after, result showcase, and time-saving proof.
- `graphite_ivory_teal`: graphite base, large ivory proof panels, restrained teal edge light. Use for source proof and risk judgment only when readability stays high.
- `newsroom_white_red`: white newsroom wall, graphite zones, red only for alert labels, blue-gray context panels. Use for AI news and industry updates.
- `soft_green_efficiency`: soft mint, warm white, graphite, small green progress accents. Use for automation, task completion, and saved steps.
- `amber_warning_compare`: warm gray base, amber warning chip, ivory correction card. Use for mistake correction and do-this-not-that scenes.

## 8. Layout Families

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

## 9. Material Families

- `paper_acrylic`: warm paper grain, matte acrylic tabs, soft card shadows, clean desk surface. Best for beginner tutorials, templates, reports, and copywriting.
- `whiteboard_marker`: clean whiteboard surface, marker rails, sticky-note placeholders, bright daylight. Best for simple concept explanation.
- `desk_stationery`: documents, folders, blank cards, calendar blocks, paper clips, soft desk shadows. Best for productivity and time-saving scenes.
- `matte_editorial`: matte graphite frame, warm ivory proof surface, subtle bevel, studio falloff. Best for source proof and serious explanation.
- `soft_3d_clay`: clay-like geometric nodes, rounded workflow blocks, gentle shadows, bright background. Best for simple abstract AI concepts.
- `newsroom_panel`: white editorial panels, small red alert marker, source strip, clean headline-safe area. Best for AI news and industry updates.
- `product_keynote`: bright stage, product card hero, spotlight, clean gradient, high-contrast title-safe zone. Best for feature reveal and result showcase.
- `glass_metal`: smoked glass, graphite, brushed metal, restrained rim light. Use as one style, not the default.

For beginner tutorials, prefer `paper_acrylic`, `whiteboard_marker`, `desk_stationery`, or `soft_3d_clay`. Do not make `glass_metal` the default material family.

## 10. Color System

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

Example for a content-grounded beginner template tutorial, not a default:

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

## 11. Texture And Premium Quality Translation

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

## 12. 图片生成常用描述词

### 12.1 Asset Role

- `background_plate`: 无文字背景板，给证据卡、字幕、标题和 callout 留舞台。
- `hero_poster`: 第一帧或封面主视觉，必须有强焦点和大标题安全区。
- `metaphor_visual`: 抽象概念视觉化，比如“任务进入验证门”“来源卡汇聚成证据墙”。
- `diagram_base`: 无文字图解底板，节点、轨道、卡片先生成，文字由 HTML/CSS 加。
- `transition_plate`: 场景过渡板，承接上一镜头元素进入下一镜头。
- `proof_support_card`: 真实截图外面的证明卡框或来源框，不生成假内容。
- `texture`: 细节纹理层，只服务层次，不抢正文。
- `cover`: 可发布封面，不直接截图凑数。

### 12.2 Visual Thesis

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

### 12.3 Topic Binding

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

### 12.4 Information Job

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

### 12.5 Composition

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

### 12.6 Foreground / Midground / Background

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

### 12.7 Camera / Lens

- `35mm straight-on editorial wide shot`
- `50mm product keynote still`
- `stable keynote framing`
- `overhead desk view`
- `macro material detail`
- `straight-on proof board`
- `no tilted camera`
- `no Dutch angle`
- `foreground stable, background slow push-in`

### 12.8 Lighting

- `soft upper-left key light`
- `restrained rim light on panel edges`
- `low ambient glow`
- `realistic contact shadows`
- `softbox reflections`
- `controlled reflections`
- `ambient falloff`
- `subtle screen glow`
- `warm ivory text-safe zones`

### 12.9 Material / Texture

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

### 12.10 Color Hierarchy

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

### 12.11 Text-Safe Zones

- `left proof card area remains clean`
- `right annotation rail remains clean`
- `lower third remains dark and quiet`
- `center-safe title area`
- `no baked text`
- `no pseudo Chinese`
- `no generated labels`
- `HTML/CSS owns all readable text`

### 12.12 Evidence Boundary

必须写清：

- `support only; not evidence`
- `generated background only; not official UI`
- `conceptual metaphor; not screenshot`
- `diagram base; labels added later`
- `proof frame only; real screenshot inserted by HyperFrames`

### 12.13 Negative Prompt

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

### 12.14 Regeneration Criteria

出现这些情况必须重生成：

- 看起来像通用科技壁纸。
- 有文字、伪 UI、乱码、假 logo。
- 没有清晰证明区、字幕区或标题区。
- 背景线条碰到字幕、标题、CTA 或证据文本。
- 和本期主题无关，只是好看。
- 画面太暗、太糊、太满、太像模板。
- 生成图被误用成证据。

### 12.15 AI 科技背景专用公式

科技感、AI 感背景不是把机器人、电路板、代码、HUD 全塞进画面，而是用抽象智能元素、空间层次、发光材质、未来配色和留白构图建立高级氛围。

通用公式：

```text
使用场景 + 核心视觉主体 + 2-4 个 AI 元素 + 空间环境 + 材质质感
+ 色彩方案 + 光影效果 + 构图要求 + 画面风格 + 清晰度。
```

AI 元素池，选择 2-4 个即可，不要全用：

- 人工智能神经网络
- 数据节点
- 发光粒子
- 流动数据
- 数字脉冲
- 算法轨迹
- 抽象大脑轮廓
- 信息矩阵
- 全息界面氛围
- 量子网络
- 数字波纹
- 智能核心

科技材质池：

- 半透明玻璃
- 液态金属
- 磨砂金属
- 全息材质
- 晶体结构
- 光纤质感
- 透明亚克力
- 微粒子材质
- 镜面反射
- 细腻网格

光影池：

- 柔和霓虹光
- 体积光
- 边缘轮廓光
- 微弱环境光
- 光线穿透
- 粒子辉光
- 渐变光晕
- 电影级照明
- 低对比柔光
- 高对比戏剧光

推荐配色：

- 深色高端科技：深海蓝、靛蓝、紫罗兰、青蓝色光芒。
- 清洁型企业 AI：白色、银灰色、冰蓝色、浅青色。
- 未来赛博科技：黑色、霓虹蓝、品红色、电光紫，必须克制使用。
- 高级暖色 AI：深黑色、香槟金、琥珀橙、暖白色光。

高级控制词：

- 克制的科技感
- 高级企业视觉
- 极简未来主义
- 精密而有秩序
- 细腻微观结构
- 柔和渐变
- 干净的空间层次
- 不过度装饰
- 低饱和配色
- 真实材质反射

这些词只能作为质感补充，不能单独当 prompt 主体。必须同时写清构图、主体位置、留白区域、材质、光线、色彩角色和负面词。

负面提示词：

```text
文字，字母，数字，水印，品牌标志，人物，机器人，手，
杂乱构图，元素过多，过度曝光，颜色刺眼，低清晰度，
模糊，噪点，廉价霓虹效果，卡通风格，游戏界面，
不规则线条，重复图案，过度锐化，复杂 HUD，堆满电路板，
大量代码，骨架框架，占位卡槽，未被前景使用的流程线框。
```

万能模板：

```text
用于[官网首屏 / PPT 封面 / 发布会大屏 / 视频背景]的高端 AI 科技背景，
以[抽象神经网络 / 智能核心 / 数据流 / 数字波纹]为主要视觉元素，
结合[发光粒子、透明曲面、数据节点]，
采用[深蓝紫 / 白色冰蓝 / 黑金]配色，
具有[玻璃、液态金属、全息]质感，
[柔和体积光、边缘光、粒子辉光]，
整体风格极简、克制、专业、未来，
主体位于[左侧 / 右侧 / 中央]，另一侧留出大面积干净空间，
电影级光影，精细空间层次，超高清，[16:9 / 21:9 / 9:16]，
无人物，无文字，无标志，无水印。
```

可直接使用的背景方向：

- 高端 AI 官网背景：抽象神经网络和数据节点悬浮在深邃空间，细腻发光粒子沿弧形轨迹流动，半透明玻璃和液态金属质感，深蓝到紫色渐变，柔和青色轮廓光，主体集中右侧，左侧大面积干净留白，无文字无标志。
- 简洁白色 AI 背景：抽象数据波纹和透明神经网络结构，半透明玻璃曲面、冰晶粒子、浅蓝细光线，白色银灰空间，大量留白，轻盈、理性、可信赖，无文字。
- 深色神经网络背景：庞大抽象神经网络悬浮黑蓝空间，微小数据节点由细腻发光线连接，蓝紫能量缓慢流动，轻微粒子雾和体积光，边缘渐暗，无人物无文字。
- AI 数据流背景：细腻光线和数字粒子向远方汇聚形成信息隧道，深蓝空间配青紫光，中心偏右构图，左侧保留标题区域，干净有序，不过度复杂。
- AI 智能核心背景：悬浮半透明球形智能核心，内部是神经网络、数据节点和旋转光环，玻璃与液态金属质感，蓝紫能量缓慢流动，深色极简空间，对称构图，无文字。

### 12.16 AI 背景 15 风格随机池

每日 AI 视频背景默认从 `references/ai_background_random_style_pool.md` 的 15 个风格里随机选择 1 个，并在 `visual_style_decision.json`、`background_prompt_pack.md`、`asset_manifest.json` 记录：

- `background_style_pool_id`
- `background_style_name`
- `background_style_selection_method`

15 个可选风格：

- `BG_STYLE_01`: 量子环形反应堆
- `BG_STYLE_02`: 芯片峡谷超级计算机
- `BG_STYLE_03`: 全息数字孪生都市
- `BG_STYLE_04`: 生物神经森林
- `BG_STYLE_05`: 晶体张量矩阵
- `BG_STYLE_06`: 黑金机械量子引擎
- `BG_STYLE_07`: 银白光子实验室
- `BG_STYLE_08`: 等离子数据风暴
- `BG_STYLE_09`: 翡翠量子隧道
- `BG_STYLE_10`: 群体智能轨道网络
- `BG_STYLE_11`: AI宇宙意识网络
- `BG_STYLE_12`: AI机械文明巨构
- `BG_STYLE_13`: 星球环形AI计算都市
- `BG_STYLE_14`: 黑金AI恒星引擎
- `BG_STYLE_15`: AI机械天空之城

随机池里的原始风格可以高密度、满版、复杂，但视频安全改写必须保留前景可读性：标题区、字幕区、证据卡区域要通过景深、雾化、暗化、低对比、柔光留出干净阅读面。`无空白区域` 只能理解为“不做廉价空白壁纸”，不能理解为“不给字幕和前景留安全区”。

### 12.17 企业级 AI 计算控制台视觉系统

当视频需要整体呈现科技感时，必须读取 `references/enterprise_ai_control_console_visual_system.md`，并把科技感落实到前景组件、字幕、转场和音效，而不是只换一张科技背景。

核心规则：

- 每条视频只选定一个主背景风格，不能每个镜头随机切换不同美术方向。
- 选定风格后，整条视频继承同一套配色、光源方向、材质、界面语言、转场语言和 SFX 气质。
- 前景内容使用企业级 AI 控制台语言：深色玻璃数据面板、精密细边框、低强度内发光、节点式信息层级、局部扫描线和模块锁定反馈。
- 复杂背景上出现文字或内容面板时，必须对组件下方背景做局部压暗、局部模糊、降饱和和柔和羽化。
- 不靠大量英文状态词制造科技感。英文标签只能少量作为前景 HTML/CSS 点缀，不得伪装成官方系统或终端证明。
- 官方截图内部保持原始颜色、比例和清晰度；扫描、锁定、发光只能作用在截图外框。
- 不同内容必须使用不同组件形态：开场标题是系统启动模块，证据是数据档案框，步骤是模块化数据节点，对比是双通道分析面板，清单和结论是节点连接结构。
- 动效只使用五类主动作：`Scan`、`Assemble`、`Lock`、`Focus`、`Converge`。一个镜头同时显著动作不超过两个。
- 字幕关键词命中时只做一次轻微亮度提升或 1.02-1.04 倍缩放，不能持续闪烁、逐字弹跳或同时发光缩放。

简化总描述：

```text
本视频采用企业级人工智能计算控制台视觉系统。
背景来自一个固定的高端 AI 科技空间风格，并贯穿整条视频。
前景采用深色玻璃数据面板、精密细边框、低强度内发光、节点式信息层级、
局部扫描线、模块锁定反馈和局部可读性遮罩。
标题、证据、步骤、对比、清单、结论分别使用不同科技组件形态。
动效只表达扫描、加载、锁定、聚焦和汇聚，不做游戏 HUD，不做普通 PPT。
```

## 13. 常用图片 Prompt 模板

### 13.1 背景板

```text
Create a 16:9 premium editorial background plate for a Chinese AI explainer about [topic].
Visual thesis: [topic-specific metaphor].
Background style pool selection: [BG_STYLE_01-BG_STYLE_15 name from references/ai_background_random_style_pool.md, selected once and recorded].
Topic binding: [specific tool/source/workflow].
Information job: create premium atmosphere and clean negative space for foreground proof cards, captions, and source overlays.
Background role: text-free, skeleton-free generated support atmosphere, never official proof.
Composition: wide horizontal frame, calm negative space, quiet title zone, lower-third caption-safe band, no visible placeholder layout.
Foreground: soft light spill, shallow shadow anchors, subtle material edges, no readable fake text, no blank panels.
Midground: topic metaphor through haze, light bands, blurred architecture, material depth, or restrained bokeh; no source wall skeleton.
Background: matte graphite or warm editorial depth, realistic falloff, controlled vignette, restrained negative space.
Camera/lens: 35mm or 50mm straight-on editorial wide shot.
Lighting: gallery-grade softbox key light, restrained rim light, ambient falloff, realistic contact shadows.
Material/texture: smoked-glass haze, brushed graphite, matte mineral surface, fine film grain.
Color hierarchy: charcoal or warm neutral base, ivory text-safe zones, one accent color for focus.
Motion usage: slow 100%-103% push-in, subtle parallax, gentle light drift; proof cards and captions animate above it.
Avoid: fake UI, pseudo text, neon grid, random particles, white lines crossing captions, clutter, skeleton stage, unused rails, placeholder cards.
```

### 13.2 封面 / Hero Poster

AI 知识类发布封面优先使用 `references/fixed_ai_cover_background_rotation.json` 的 10 套双比例纯背景；封面标题由可控图层添加，并在合成前进入本地文字合规。只有需要定制海报级封面时，才使用下面的生成式 hero poster 提示词。即使定制，文字仍由可控图层添加，不把伪中文或不可编辑文字烘焙进图片。

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

### 13.3 图解底板

```text
Create a clean 16:9 diagram base for an AI workflow explainer.
Diagram idea: [pipeline / comparison / risk matrix / checklist].
Do not generate readable text. Use blank nodes, rails, cards, and placeholders only.
Composition: large shapes, clear left-to-right flow, lower-third caption safe.
Motion usage: nodes light up one by one in HyperFrames; labels added later.
Avoid: pseudo labels, dense lines, random icons, tiny text, fake logos.
```

### 13.4 转场板

```text
Create a 16:9 transition plate from [scene A] to [scene B].
Continuity anchor: [same cursor / source tag / rail / chapter marker] remains visible.
Composition: old idea recedes while new proof area opens.
Motion plan: old panel remains 8-14 frames while new panel slides over it.
Avoid: full-screen flash, unrelated new background, hard reset, random wipe.
```

## 14. 动态效果描述词

### 14.1 Motion Brief 字段

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

### 14.2 Motion Purpose

- `reveal`: 让一个新信息出现。
- `verify`: 让证据进入并锁定。
- `compare`: 左右/前后对比。
- `warn`: 风险边界、错误提示、敏感点。
- `connect`: 节点串联、流程传递。
- `summarize`: 模板、清单、结论稳定收束。

### 14.3 Motion Actors

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

### 14.4 入口动效

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

### 14.5 镜头运动

- `slow 100% to 103% push-in`
- `subtle parallax`
- `foreground stable, background moves quietly`
- `static hold for readability`
- `tracking only when following a workflow rail`
- `no rotation`
- `no page shaking`
- `no random drift`
- `no whole screenshot movement while reading`

### 14.6 转场 Recipe

- `source_focus_lens_reveal`: 来源截图裁切进入、镜头聚焦、citation callout 出现。
- `citation_rail_wipe`: 来源/日期/信号卡稳定落位，细轨道从左到右擦入。
- `comparison_split_handoff`: 错/对两侧面板从两边进入，风险 chip 依次出现。
- `operation_node_relay`: 流程节点依次点亮，光标/packet 沿轨道传递。
- `terminal_scan_proof_tray`: 终端或代码输出扫描出现，证据托盘从下方滑入。
- `template_lift_settle`: 清单行逐个抬起，最后进入稳定可读状态。
- `final_controlled_zoom`: 只在最终 CTA/模板上做一次克制推进。

45-75 秒 AI 视频至少要用 5 种，不允许全片只有同一种 fade 或 slide。

当用户要求类似剪映高级收费效果的质感时，转场不能只靠一条光线、一次模糊或一张页面滑动。应在同一视觉世界内使用不同的物理机制：

- `lens_aperture_refract`: 玻璃镜头折射，旧画面收进镜片，新画面从光学孔径中打开。
- `liquid_metal_sweep`: 液态金属带斜向扫切，边缘带柔和折射和金属高光。
- `magnetic_rail_handoff`: 数据包沿轨道传递，把下一组节点或操作舱牵引入场。
- `prism_scan_shutter`: 多层半透明棱镜快门穿过画面，用于进入证明或结果场景。
- `quantum_core_converge`: 画面信息向中央智能核心汇聚，再从核心脉冲打开结论。
- `depth_lens_pass`: 景深镜片从前景掠过，旧画面压暗，新画面从焦点后方浮现。

这些转场要有信息目的：对比交接、流程传递、证明验证、结果展开或结论汇聚。禁止把高级转场理解为闪白、抖动、强 glitch、随机光线、全屏爆光、重复同一条光轨。

### 14.7 字幕/关键词动效

- `keyword highlight only`
- `subtle scale-pop max 1.08x for 0.25s`
- `caption fades in over 160ms`
- `caption remains in stable lower third`
- `no every-word bouncing`
- `no long typewriter effect`
- `caption style changes by scene type`
- `caption never overlaps proof panel`

### 14.8 Glow / Audio Reactive / SFX

- `ambient glow opacity 8%-18%`
- `text reactive scale 3%-5%`
- `background glow 10%-15%`
- `one soft tick when card locks`
- `marker sweep sound below narration`
- `soft thump for card settle`
- `no whoosh spam`
- `clean narration remains continuous; no background audio by default`
- `transition SFX only; not full narration`
- `root-level SFX bed with cue sheet`

### 14.9 Negative Motion

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

### 14.10 金属科技动态组件升级规则

当用户指出画面像 PPT、只有文字框、缺少质感、缺少设计感或缺少动态效果时，不能继续沿用静态卡片路线。必须把证明卡、步骤卡、模板卡降级为内容草图，并在 HyperFrames/Remotion 中重建为可动的金属信息装置。

每个发布级科技镜头必须同时写清以下五层：

- `material layer`: brushed black titanium, champagne micro-bevel, smoked glass depth, crystal edge refraction, fine film grain, contact shadow.
- `structure layer`: rail, tray, hinge, aperture, node, clamp, divider spine, focus lens, verification seal, or output slot.
- `motion layer`: which physical part moves, which data element appears, what locks, what remains still for reading.
- `readability layer`: local background quieting, text-safe zone, subtitle rail protection, focus dimming, phone-size contrast.
- `quality gate`: still frame must look like an designed object, not a rectangle with text on a background.

Prompt language must describe concrete production design, not only mood words. Use phrasing like:

```text
foreground content is mounted inside a brushed black titanium proof tray;
champagne micro-beveled rails catch a narrow upper-left key light;
smoked-glass inner plate creates depth behind readable Chinese text;
an ice-cyan verification node travels along the rail, stops, then emits one restrained lock pulse;
surrounding engine detail is locally damped under the active text area;
the proof plate holds still for reading after the motion finishes.
```

For foreground proof and tutorial visuals, avoid prompts or storyboard language that only says:

- `draw a tech card`
- `add a futuristic frame`
- `高级科技背景加文字`
- `glass card with text`
- `PPT panel`
- `rectangle module`
- `cool HUD`

If a support image was produced by local PIL/canvas as a flat card, it may only be used as:

- content source
- text layout draft
- fallback reference
- proof text audit artifact

It may not be used as the final visible component unless a later HyperFrames/Remotion layer adds real depth, metal material, component-specific motion, local readability treatment, and shot-level QA screenshots.

## 15. 当前实际项目里的常用组合

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

## 16. 我看到的当前问题

1. 最近项目的 `background_prompt_pack.md` 字段是完整的，但记录显示 ImageGen 返回的是内联图，没有稳定保存到 workspace 的本地文件路径。以后生成图必须补强“图片文件可追溯路径 + asset_manifest 记录 + 样帧验收”。
2. 实际 storyboard 里部分 motion 仍然偏模板化，例如大量使用 `blur crossfade`、`smooth push slide`、`foreground panel fade-up`。这能跑通，但高级感不够稳定；后续应按每个镜头的信息目的强制换 recipe。
3. 图片描述词已经避免了“高级科技感”这类空词，但还要继续加强“每张图的 topic binding”，否则会变成好看的通用背景。
4. 动态效果不能只写给 HyperFrames 看，还要能让人验收：哪个元素动、为什么动、何时动、停在哪里读，必须写清楚。
5. 生成图不能承担证据功能。真实证据必须来自截图、网页、终端、文件、QA 报告或可验证来源。
6. 如果前景只有圆角框、细边线、文字和简单淡入，就按 PPT 风险处理；必须返工为动态金属组件或艺术化真实信息装置。

## 17. 快速验收清单

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
