# AI 视频固定生产模板系统

本文件把可固定的高成本设计决策收敛成模板库：背景板、转场与音效、场景入场节奏、前景组件渲染包、主工程模板、男声混音、封面纯背景、候选 V3 模板、Prompt Pack 模板。它们的目标不是让所有视频长得一样，而是减少每次临场重新设计造成的 token 浪费、质量波动和风格冲突。

## 执行顺序

1. 完成选题和导演分类，生成 `director_selection.json` 与 `style_recipe.json`。
2. 运行 `scripts/select_fixed_ai_templates.py`。
3. 写出 `internal/fixed_template_selection.json`。
4. 后续 `visual_style_plan.json`、`background_prompt_pack.md`、HyperFrames 主工程、前景组件、转场、SFX 和混音必须继承这个选择报告。
5. 运行 `python3 scripts/check_premium_template_registry.py`，模板注册表未通过时不得开始临时写 `index.html`。

## 固定模板库

- 背景板选择：`references/fixed_ai_background_template_rotation.json`
- 动态背景成品：`assets/ai_background_templates_dynamic/`
- 转场/SFX：`references/fixed_ai_transition_sfx_packs.json`
- 场景/入场/主工程：`references/fixed_ai_scene_motion_templates.json`
- HyperFrames 主工程模板：`templates/hyperframes/ai_premium_main_16x9.html`
- 高级前景模块 runtime：`assets/hyperframes_components/premium_foreground_modules.js`
- 透明玻璃前景 runtime：固定模块、caption、proof frame、source card、checklist row、micro-component 必须使用 Glass Transparency v2
- 高级动效 runtime：`assets/hyperframes_components/advanced_motion_templates.js`
- 前景组件：`references/fixed_ai_component_template_packs.json`
- 男声混音：`references/fixed_ai_voice_mix_profiles.json`
- 封面纯背景：`references/fixed_ai_cover_background_rotation.json`
- 主题候选 V3：`templates/topic_candidates_v3.template.json`
- AI 热榜 TOP5：`templates/ai_hot_rank_top5.template.json`
- Prompt Pack：`templates/prompt_pack/fixed_background_visual_contract.md`
- 静态背景归档源图：`assets/ai_background_templates_fixed_archive/`

## 固定与随机的边界

- 封面底图固定为纯背景真实图片资产，按视频比例和尺寸池顺序轮换；公开封面标题由运行时后期图层合成，并必须进入本地合规检查。
- 背景板固定为真实动态资产池，按主题方案、尺寸和轮换状态选择；描述词只用于维护或重做资产，不能在每条视频里临时随机重画背景。
- `internal/fixed_template_selection.json` 必须写出 `background_template.render_asset_path`。`render_asset_path` 永远指向 `assets/ai_background_templates_dynamic/` 中的动态 MP4。
- `background_template.fixed_asset_path` 仅作为兼容旧报告字段的动态 MP4 别名，不再指向静态 PNG。
- HyperFrames 必须使用 `background_template.render_asset_path` 作为底层背景；静态 PNG 不作为 fallback。
- 前景模块必须让动态 MP4 在玻璃下方可见。禁止用实心黑卡、白板、厚 matte panel、硬矩形遮罩或 alpha `0.60+` 的安全底遮住背景；大面积背景填充必须保持 alpha `<= 0.34`。
- 转场和 SFX 固定为 pack，每条视频选一个主 pack，最多一个辅助 pack，不允许每个场景临时换一种廉价特效。
- 前景组件固定为 pack，但组件内的文字、截图和证明内容必须按当期选题变化。
- 主工程模板固定 1920×1080 画布、背景层、前景层、字幕栏、场景容器、首帧封面规则和 GSAP helper；每条视频只填场景、模块、字幕、图片和节拍点。
- 场景入场模板固定 10 套，转场模板固定 10 套；没有匹配的信息任务时直接阻塞，不降级。
- 前景信息模块第一批固定 8 个：来源证据卡、三步清单、改前改后、测试结果、结论压印、状态锁定、节点推进、指标鼓。
- 主题候选 V3 模板只能在当天热点扫描完成后填入真实来源；不能替代扫描，也不能替代最终选题判断。
- AI 热榜 TOP5 模板只能在当前 AI 热点扫描后填入 5 条真实来源排名项；不能凭感觉生成榜单，也不能替代来源、日期和打分证据。
- Prompt Pack 模板只补视觉导演合约。固定背景不在每条视频里重新生成，前景模块和文字必须按当期主题变化。
- 男声混音固定 profile，默认厚实男讲师；不要只拉高最终 MP4 音量来解决声音薄。

## 推荐命令

```bash
python3 scripts/generate_fixed_ai_background_assets.py \
  --out-dir assets/ai_background_templates_fixed_archive \
  --manifest-out assets/ai_background_templates_fixed_archive/asset_manifest.json

python3 scripts/generate_dynamic_ai_background_assets.py \
  --fixed-manifest assets/ai_background_templates_fixed_archive/asset_manifest.json \
  --out-dir assets/ai_background_templates_dynamic \
  --manifest-out assets/ai_background_templates_dynamic/dynamic_asset_manifest.json

python3 scripts/select_fixed_ai_templates.py \
  --project outputs/demo \
  --director-selection outputs/demo/internal/director_selection.json \
  --style-recipe outputs/demo/internal/style_recipe.json \
  --video-width 1920 \
  --video-height 1080

python3 scripts/check_premium_template_registry.py
```
