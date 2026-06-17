# Learning Bank

Use this file to preserve lessons that should influence future AI-circle Douyin videos.

Two entry types are allowed:

- Post-publish review: performance and audience feedback after a published video.
- Production postmortem: QA, visual-review, user-feedback, and director-decision lessons before or after publishing.

## Format

Append one dated entry per published video:

```markdown
## 2026-06-13 video-id

- Topic:
- Format:
- Hook type:
- 24h metrics:
- Comment insights:
- What worked:
- What to fix:
- Next video ideas:
```

Append one production postmortem entry when a video reveals workflow or quality problems:

```markdown
## production-postmortem topic

- Project:
- QA status:
- Decision summary:
- User feedback:
- Observations:
- What worked:
- What to fix:
- Bottlenecks:
- Reusable lessons:
- Next run decisions:
- Proposed rule changes:
- Human approval required:
```

## Rules

- Do not treat one video as proof of a universal rule.
- Prefer concrete observations: retention, saves, comments, shares, and repeated audience questions.
- Feed repeated lessons back into topic selection, hook choice, proof visuals, and HyperFrames components.
- Use `production_postmortem.json` as soft learning input before the next video.
- Do not let the skill rewrite hard rules automatically; proposed rule changes require user approval.
- Run `scripts/score_topic.py --learning-bank references/learning_bank.md` or `scripts/apply_learning_bank.py` so repeated lessons create visible `learning_bank_adjustment` entries in topic candidates.

## 2026-06-14 codex-three-skill-reference-study

- Topic: 三个 Codex 神级 Skill 参考视频学习。
- Format: 16:9 Codex Skill/plugin 教程，约 77 秒，三段式工具证明。
- Hook type: 高手不会告诉你的信息差 + 结果/段位承诺。
- What worked:
  - 先给 Skill 名字前后的结果感，再展示真实入口、GitHub/官网、安装或搜索页面。
  - 每个 Skill 都有证据链：入口/来源、一次可见操作、生成结果、观众为什么要保存。
  - 视觉不是靠页面晃动，而是靠多张证据图、结果图、卡片和真实 UI 轮换。
  - `Remotion`、`HyperFrames`、`ImageGen` 可以作为制作栈分工，而不是三个孤立名词。
- What to fix:
  - 不能只按参考的主题做一套原创黑板页；必须学习它的证明顺序和真实产出展示。
  - 不要用单张图片承载多个步骤；拆成多图、多场景或逐步 reveal。
  - 不要用加速口播压内容；正常语速，超长就加场景。
- Next video ideas:
  - 用 ImageGen 做视觉资产、Remotion 做组件动画、HyperFrames 做最终成片的端到端示范。
  - 做一版三 Skill 对照：每个 Skill 展示入口、操作、结果和适用场景。
