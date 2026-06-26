# AI 静态背景旧目录

本目录不再保存默认背景图片资产。

当前默认渲染背景已经升级为 `assets/ai_background_templates_dynamic/` 中的动态 MP4。原静态 PNG 已移入 `assets/ai_background_templates_fixed_archive/`，只作为历史源素材和重新生成动态 MP4 的输入，不作为正式视频 fallback。

规则：

- 每条视频只从 `references/fixed_ai_background_template_rotation.json` 选择动态背景 MP4。
- `scripts/select_fixed_ai_templates.py` 输出的 `background_template.render_asset_path` 必须是动态 MP4。
- 静态 PNG 不参与默认渲染，也不作为 fallback。
- 文字、截图、标题和证明内容只能由 HyperFrames / HTML / CSS 前景层渲染，并继续走本地与 Qingdou 合规检查。

动态背景生成命令：

```bash
python3 scripts/generate_dynamic_ai_background_assets.py \
  --fixed-manifest assets/ai_background_templates_fixed_archive/asset_manifest.json \
  --out-dir assets/ai_background_templates_dynamic \
  --manifest-out assets/ai_background_templates_dynamic/dynamic_asset_manifest.json
```

说明：本目录保留 README 是为了阻止旧路径被误当成默认背景库。
