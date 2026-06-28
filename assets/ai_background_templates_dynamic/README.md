# AI 动态背景资产池

本目录保存 AI 知识视频默认使用的代码驱动动态背景模板。

规则：

- 每个动态背景由 `scripts/generate_dynamic_ai_background_assets.py` 逐帧程序化生成，归档静态源图只作为视觉家族和命名参考，不参与最终像素渲染。
- 当前生成方法为 `code_driven_procedural_motion_v2`：程序化色场、透视轨道、扫描线、环形核心、粒子、节点和柔光层真正随时间运动。
- 默认渲染资产是 `.mp4` 动态循环背景；对应 `.poster.png` 用于预览、抽帧和回退说明。
- 原静态 `.png` 背景只保存在 archive 中作为视觉参考，不作为正式视频 fallback，也不作为动态背景像素来源。
- 背景本身不包含文字、数字、字母、人物、品牌标志或水印。
- 标题、字幕、证明截图、标签和任何可读信息只能由 HyperFrames / HTML / CSS 前景层渲染。
- 前景内容默认使用超薄透明玻璃模块，避免遮住动态背景。

生成命令：

```bash
python3 scripts/generate_dynamic_ai_background_assets.py \
  --fixed-manifest assets/ai_background_templates_fixed_archive/asset_manifest.json \
  --out-dir assets/ai_background_templates_dynamic \
  --manifest-out assets/ai_background_templates_dynamic/dynamic_asset_manifest.json \
  --fps 60 \
  --force
```

说明：生成器会输出 10 个动态 MP4、10 个 poster、`dynamic_asset_manifest.json` 和 `dynamic_background_contact_sheet.jpg`。
