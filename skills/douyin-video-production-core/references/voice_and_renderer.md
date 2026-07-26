# 声音与渲染

## 提供商预检

生产前执行：

```bash
python3 scripts/preflight_providers.py --project <project>
```

预检只报告能力是否存在，不输出密钥内容。缺少 Remotion、FFmpeg、旁白提供商或必要项目文件时停止渲染。

## 声音路由

生成完整旁白前先锁定 `script.voice_lock`。声音不确定时只做短试听；记录 provider、voice id、人物感、rate、pitch 和确认来源。用户改变性别、音色、语速或音高后，旧旁白、字幕时间和依赖时长的 storyboard 都失效。

1. 已配置 `ELEVENLABS_API_KEY` 和 voice id：优先 ElevenLabs，生成连续旁白后调用 Forced Alignment。
2. 未配置 ElevenLabs：允许显式选择 `edge-tts`，保留 voice、rate、pitch 和边界字幕报告。
3. 用户提供人声：使用 `existing`，保留来源与转写/对齐方式。

生成命令：

```bash
python3 scripts/generate_voiceover.py \
  --script <project>/script.json \
  --out-audio <project>/public/audio/narration.mp3 \
  --out-captions <project>/public/data/captions.json \
  --out-report <project>/voiceover_report.json \
  --provider auto
```

任何回退都写入报告，不得静默替换。

## 渲染分工

- Remotion：唯一最终时间轴，负责画面、连续旁白、字幕、音效和最终 MP4。
- HyperFrames：仅在局部 HTML/GSAP/Lottie 动画确有优势时输出素材，再由 Remotion 引用。
- FFmpeg：探测、独立裁切、混流和技术 QA，不承担创意时间轴。

Remotion 动画只使用 frame 驱动的 `useCurrentFrame()`、`interpolate()`、`Sequence` 等确定性机制；禁止依赖 CSS animation 或 transition。

`storyboard.json.render_plan.canonical_renderer` 必须为 `remotion`。局部渲染器不能改变旁白、字幕和最终时长。
