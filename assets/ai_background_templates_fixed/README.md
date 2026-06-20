# AI 固定背景资产池

本目录保存 AI 知识视频固定循环使用的背景图片资产。

规则：

- 每条视频只从 `references/fixed_ai_background_template_rotation.json` 选择一个背景资产。
- 整条视频的前景组件、字幕、转场、光效和音效必须继承同一背景资产的配色、材质和空间语言。
- 背景图片本身不包含文字、数字、字母、人物、品牌标志或水印。
- 文字、截图、标题和证明内容只能由 HyperFrames / HTML / CSS 前景层渲染，并继续走本地与 Qingdou 合规检查。
- 如果后续替换为更高真实感的 ImageGen 背景，保持同名文件和 manifest 路径不变，避免影响模板轮换流程。

生成命令：

```bash
python3 scripts/generate_fixed_ai_background_assets.py \
  --out-dir assets/ai_background_templates_fixed \
  --manifest-out assets/ai_background_templates_fixed/asset_manifest.json
```

说明：默认只补缺失图片并重建 manifest，不覆盖已有高质量 ImageGen 资产；只有明确加 `--force` 才会用本地确定性方法重画背景。
