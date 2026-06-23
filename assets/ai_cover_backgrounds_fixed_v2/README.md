# AI 封面纯背景固定库 v2

这里保存 AI 知识类视频发布封面和第一帧使用的固定纯背景图。

- 每套背景有 `16x9` 和 `9x16` 两个比例，最终按视频尺寸匹配使用。
- 背景图本身不包含公开文字，`background_contains_text=false`。
- 轮换规则见 `references/fixed_ai_cover_background_rotation.md`。
- 机器可读清单见 `references/fixed_ai_cover_background_rotation.json`。
- 运行时封面标题由 `scripts/select_fixed_cover_template.py` 写入 `internal/publish_cover_text.txt` 并渲染到安全文字区域。
- 16x9 横版封面用于抖音时，主标题和副标题必须落在中间 9:16 裁切也可见的安全区；脚本会同时输出 `internal/cover_publish_douyin_center_crop.png` 作为预览证据。
- 封面标题、发布标题、发布文案、话题、字幕和画面文字必须一起完成本地合规检查；文字有改动必须重检。
