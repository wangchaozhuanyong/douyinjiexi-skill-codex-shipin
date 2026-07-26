# 参考视频与证据

## 可播放本体

参考研究必须先取得本地可播放视频。执行：

```bash
python3 scripts/analyze_reference.py --input <video> --out <reference_analysis.json>
python3 scripts/extract_reference_frames.py --video <video> --out-dir <frames>
```

至少检查：

- duration、aspect、fps、audio
- 前 3–5 秒
- 代表性场景和结尾
- 字幕密度、镜头节奏、首个证明时间
- 旁白、音乐与画面关系

标题、封面、URL 元数据、作者页或音乐页不能替代视频本体。

## 可学习与不可复用

可以学习信息组织、节奏、证据出现方式、字幕层级和运动语言。

不得复用原画面、人物、字幕、配音、文案、创作者身份、水印或高度相似的完整镜头顺序。

## Claim–Proof 绑定

每条事实 claim：

1. 在 `source_brief.json` 绑定 source。
2. 在 `script.json` 的 beat 中绑定 proof。
3. 在 `storyboard.json` 的同一场景显示 proof。
4. 在 `asset_manifest.json` 记录 proof 文件和来源。

官方文档、真实界面、真实操作和真实输出优先。生成图、抽象动画和装饰图只能做 support。

## 平台数据

记录采集时可见的播放、点赞、评论、收藏或分享数据，并写采集时间。无法看到时写 `not_observed`。不得由播放量推断完播率，也不得把用户口述表现改写成平台已核实数据。
