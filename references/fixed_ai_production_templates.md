# AI 视频固定生产模板系统

本文件把可固定的高成本设计决策收敛成五类模板库：背景板、转场与音效、前景组件、男声混音、封面纯背景。它们的目标不是让所有视频长得一样，而是减少每次临场重新设计造成的 token 浪费、质量波动和风格冲突。

## 执行顺序

1. 完成选题和导演分类，生成 `director_selection.json` 与 `style_recipe.json`。
2. 运行 `scripts/select_fixed_ai_templates.py`。
3. 写出 `internal/fixed_template_selection.json`。
4. 后续 `visual_style_plan.json`、`background_prompt_pack.md`、HyperFrames 组件、转场、SFX 和混音必须继承这个选择报告。

## 固定模板库

- 背景板：`references/fixed_ai_background_template_rotation.json`
- 转场/SFX：`references/fixed_ai_transition_sfx_packs.json`
- 前景组件：`references/fixed_ai_component_template_packs.json`
- 男声混音：`references/fixed_ai_voice_mix_profiles.json`
- 封面纯背景：`references/fixed_ai_cover_background_rotation.json`
- 背景成图：`assets/ai_background_templates_fixed/`

## 固定与随机的边界

- 封面底图固定为纯背景真实图片资产，按视频比例和尺寸池顺序轮换；公开封面标题由运行时后期图层合成，并必须进入本地合规检查。
- 背景板固定为真实图片资产池，按主题方案、尺寸和轮换状态选择；描述词只用于维护或重做资产，不能在每条视频里临时随机重画背景。
- `internal/fixed_template_selection.json` 必须写出 `background_template.fixed_asset_path`，HyperFrames 必须使用这个固定资产作为底层背景。
- 转场和 SFX 固定为 pack，每条视频选一个主 pack，最多一个辅助 pack，不允许每个场景临时换一种廉价特效。
- 前景组件固定为 pack，但组件内的文字、截图和证明内容必须按当期选题变化。
- 男声混音固定 profile，默认厚实男讲师；不要只拉高最终 MP4 音量来解决声音薄。

## 推荐命令

```bash
python3 scripts/generate_fixed_ai_background_assets.py \
  --out-dir assets/ai_background_templates_fixed \
  --manifest-out assets/ai_background_templates_fixed/asset_manifest.json

python3 scripts/select_fixed_ai_templates.py \
  --project outputs/demo \
  --director-selection outputs/demo/internal/director_selection.json \
  --style-recipe outputs/demo/internal/style_recipe.json \
  --video-width 1920 \
  --video-height 1080
```
