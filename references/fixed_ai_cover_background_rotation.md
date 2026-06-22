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
- 标题样式按 `accent_rgb` 自动生成局部高光、压印描边和阅读遮罩；不使用旧卡片、旧编号、旧固定文字。

## 第一帧要求

- 合成后的封面必须写成 `internal/first_frame_cover.png` 和 `internal/cover.png`。
- 第一帧封面默认只占第 0 帧，30fps 约 `0.033s`。
- `internal/actual_frame_000_cover.png` 必须匹配封面。
- `internal/actual_frame_001_after_cover.png` 必须已经回到正片。

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
