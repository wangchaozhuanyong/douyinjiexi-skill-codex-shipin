# AI 静态背景归档源

本目录保存旧版静态 PNG 背景。

用途：

- 作为 `assets/ai_background_templates_dynamic/` 动态 MP4 的历史源素材。
- 作为重新生成动态背景时的输入资产。
- 不作为正式视频默认背景。
- 不作为 `scripts/select_fixed_ai_templates.py` 的 fallback。

默认视频生产链只使用动态 MP4：

```text
references/fixed_ai_background_template_rotation.json
-> assets/ai_background_templates_dynamic/*.mp4
-> background_template.render_asset_path
```

重新生成动态背景：

```bash
python3 scripts/generate_dynamic_ai_background_assets.py \
  --fixed-manifest assets/ai_background_templates_fixed_archive/asset_manifest.json \
  --out-dir assets/ai_background_templates_dynamic \
  --manifest-out assets/ai_background_templates_dynamic/dynamic_asset_manifest.json \
  --force
```
