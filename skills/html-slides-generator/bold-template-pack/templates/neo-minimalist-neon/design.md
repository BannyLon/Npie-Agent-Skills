# 新派极简霓虹黄 — Design System

## Font Import
```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Inter:wght@300;400&family=Noto+Sans+SC:wght@400;700&display=swap');
```

## CSS Custom Properties
```css
#stage {
  --viewport-bg: #faf8f2;
  --stage-bg: #faf8f2;
  --color-bg: #faf8f2;
  --color-text: #111111;
  --color-accent: #e6ff00;
  --color-muted: #999999;
  --font-heading: "DM Sans", "Noto Sans SC", sans-serif;
  --font-body: "Inter", "Noto Sans SC", sans-serif;
  --font-mono: "JetBrains Mono", monospace;
  --slide-padding: 140px 160px;
  --transition-speed: 0.4s;
  --nav-bg: rgba(0, 0, 0, 0.04);
  --nav-border: rgba(0, 0, 0, 0.1);
  --nav-color: #111111;
  --nav-hover-bg: rgba(230, 255, 0, 0.3);
  --indicator-color: rgba(0, 0, 0, 0.3);
  --accent-size: 80px;
}
```

## Typography Scale
| Level | Size | Weight | Letter Spacing | Line Height |
|-------|------|--------|----------------|-------------|
| h1 hero | 96px | 700 | -0.03em | 1.05 |
| h1 | 64px | 700 | -0.02em | 1.1 |
| h2 | 40px | 500 | -0.01em | 1.2 |
| body | 28px | 300 | 0.02em | 1.7 |
| small | 16px | 400 | 0.08em | 1.4 |

## Layout Rules
- Extreme minimalism: massive whitespace, one accent element per slide
- Cover: title top-left in a sea of off-white, one neon yellow circle (80px) bottom-right
- Content: headline + subtext + ONE accent mark
- Padding 140px 160px — more breathing room than any other template
- No grids, no cards, no borders — everything floats in space

## Decorative Elements
- **唯一的霓虹黄元素** — 每页只能有其中一个:
  - 圆形: `width: var(--accent-size); height: var(--accent-size); border-radius: 50%; background: var(--color-accent)`
  - 粗线: `width: 200px; height: 6px; background: var(--color-accent)`
  - 荧光笔高亮: `background: linear-gradient(transparent 60%, var(--color-accent) 60%); display: inline` (用于高亮关键词)
- **除此之外什么都没有**: 没有阴影、没有边框、没有渐变、没有第二个颜色

## Animation
- accent-pop-then-text: accent element appears first (0.3s scale 0→1.15→1), then text fades in (delay 0.2s after)
- Pattern: A (fade + slide-up, 0.6s) for text after accent
- Accent: `transform: scale(0); transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)` → `scale(1)`

## Special Slide Types
- **封面**: 左上 96px 粗体标题 + 右下 80px 霓虹黄圆，其余全部留白
- **目录**: 3 个序号 + 章节名，当前章节序号为霓虹黄圆，其余为浅灰
- **内容页 (演讲型)**: 标题 + 一行正文 + 一个霓虹黄下划线 (200px wide) 在标题下
- **内容页 (阅读型)**: 标题 + 正文，关键词用霓虹黄荧光笔高亮
- **数据页**: 大号数字黑色，单位小字灰色，一个霓虹黄 accent 圆在旁边
- **总结**: 居中大字 + 一个霓虹黄点，如句号
