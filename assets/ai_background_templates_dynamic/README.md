# AI 动态背景资产池

本目录保存 AI 知识视频默认使用的动态背景模板。

规则：

- 每个动态背景由 `assets/ai_background_templates_fixed_archive/` 中对应的归档静态源图生成，保持同一视觉家族。
- 默认渲染资产是 `.mp4` 动态循环背景；对应 `.poster.png` 用于预览、抽帧和回退说明。
- 原静态 `.png` 背景只保存在 archive 中作为重新生成动态资产的源素材，不作为正式视频 fallback。
- 背景本身不包含文字、数字、字母、人物、品牌标志或水印。
- 标题、字幕、证明截图、标签和任何可读信息只能由 HyperFrames / HTML / CSS 前景层渲染。
- 前景内容默认使用超薄透明玻璃模块，避免遮住动态背景。

生成命令：

```bash
python3 scripts/generate_dynamic_ai_background_assets.py \
  --fixed-manifest assets/ai_background_templates_fixed_archive/asset_manifest.json \
  --out-dir assets/ai_background_templates_dynamic \
  --manifest-out assets/ai_background_templates_dynamic/dynamic_asset_manifest.json \
  --force
```

说明：生成器会输出 10 个动态 MP4、10 个 poster、`dynamic_asset_manifest.json` 和 `dynamic_background_contact_sheet.jpg`。
