# 固定 AI 封面纯背景轮换规则

本规则用于 AI 知识类视频第一帧和发布封面。封面底图只来自固定纯背景库，公开标题文字由运行时后期图层合成。

## 固定素材

- 素材目录：`assets/ai_cover_backgrounds_fixed_v2/`
- 轮换清单：`references/fixed_ai_cover_background_rotation.json`
- 默认轮换状态：`outputs/.ai_cover_background_rotation_state.json`

## 选择规则

- 先按视频尺寸选池，不跨比例随机。
- `1920x1080` / `16:9` 使用 `16x9` 背景。
- `1080x1920` / `9:16` 使用 `9x16` 背景。
- 每个比例池按 `T01 -> T02 -> ... -> T10 -> T01` 顺序轮换。
- 选择报告必须记录 `template_id`、`template_path`、`template_aspect`、`recommended_text_safe_rect_px`、`accent_rgb`、`selection_method=sequential_by_size_pool` 和 `frame_grab_used=false`。

## 文字规则

- 背景图本身必须是纯背景，`background_contains_text=false`。
- 封面标题文字必须在文案阶段生成，并写入 `internal/publish_cover_text.txt`。
- `internal/publish_cover_text.txt` 必须和发布标题、发布文案、话题、字幕、画面文字一起进入本地合规检查；文字有改动必须重新检查。
- 封面合成时，标题只能放入 manifest 的 `recommended_text_safe_rect_px`。该字段是 `[x1, y1, x2, y2]`，不是 `[x, y, width, height]`。
- 16:9 横版封面用于抖音时，主文字必须同时满足“完整横版可读”和“中间 9:16 裁切预览可读”。横版背景仍保持完整 16:9，但公开封面文字要落在 `douyin_center_text_safe_rect_px` 内，默认中间裁切区为 `douyin_center_crop_rect_px`。
- 封面文字不是发布标题的全文复刻。发布标题可以较长，封面文字必须改写成短主题：主标题建议 8-14 个中文字符，最多 18 字；副标题建议 6-12 字。超出时改写或拆成两行，不通过缩小字号硬塞。
- 每次生成 16:9 封面时，必须同时输出 `internal/cover_publish_douyin_center_crop.png` 作为抖音中间裁切预览图；这张图里主标题、副标题不能被裁掉。
- 标题样式按 `accent_rgb` 自动生成局部高光、压印描边和阅读遮罩；不使用旧卡片、旧编号、旧固定文字。

## 第一帧要求

- 合成后的封面必须写成 `internal/first_frame_cover.png` 和 `internal/cover.png`。
- 横版项目还必须写成 `internal/cover_publish_horizontal.png`、`internal/cover_publish_vertical.png` 和 `internal/cover_publish_douyin_center_crop.png`。其中 `cover_publish_douyin_center_crop.png` 是抖音中间默认预览检查图，不是替代原始 16:9 首帧。
- 第一帧封面默认只占第 0 帧，30fps 约 `0.033s`。
- `internal/actual_frame_000_cover.png` 必须匹配封面。
- `internal/actual_frame_001_after_cover.png` 必须已经回到正片。

## 发布前硬门

`internal/publish_cover_report.json` 必须记录：

- `cover_layout.text_bbox_px`
- `cover_layout.recommended_text_safe_rect_px`
- `cover_layout.douyin_center_crop_rect_px`
- `checks.cover_text_fit_safe_rect=true`
- `checks.primary_text_inside_douyin_center_crop=true`
- `checks.douyin_center_crop_preview_generated=true`
- `checks.compact_cover_text_used=true`

任何一项失败，都不能进入 `pre_publish_gate`、上传或发布。

## 推荐命令

```bash
python3 scripts/select_fixed_cover_template.py \
  --project outputs/demo \
  --video-width 1920 \
  --video-height 1080 \
  --require-checked-cover-text
```

如果需要临时覆盖封面文字：

```bash
python3 scripts/select_fixed_cover_template.py \
  --project outputs/demo \
  --video-width 1920 \
  --video-height 1080 \
  --cover-text "主标题|副标题" \
  --require-checked-cover-text
```
