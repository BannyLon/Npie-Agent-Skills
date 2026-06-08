# 深夜编辑 — Design System

## Font Import
```css
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400&family=Noto+Serif+SC:wght@400;700&display=swap');
```

## CSS Custom Properties
```css
#stage {
  --viewport-bg: #0a0a0a;
  --stage-bg: #0a0a0a;
  --color-bg: #0a0a0a;
  --color-text: #fff5f0;
  --color-accent: #ff3b8b;
  --color-muted: #555555;
  --color-panel: #141414;
  --font-heading: "Instrument Serif", "Noto Serif SC", serif;
  --font-body: "Inter", "Noto Serif SC", sans-serif;
  --font-mono: "JetBrains Mono", monospace;
  --slide-padding: 120px 140px;
  --transition-speed: 0.6s;
  --nav-bg: rgba(255, 59, 139, 0.06);
  --nav-border: rgba(255, 59, 139, 0.15);
  --nav-color: rgba(255, 245, 240, 0.7);
  --nav-hover-bg: rgba(255, 59, 139, 0.15);
  --indicator-color: rgba(255, 245, 240, 0.35);
  --underline-width: 2px;
}
```

## Typography Scale
| Level | Size | Weight | Letter Spacing | Line Height |
|-------|------|--------|----------------|-------------|
| h1 hero | 120px | 400 italic | -0.02em | 1.05 |
| h1 | 80px | 400 italic | -0.01em | 1.1 |
| h2 | 48px | 400 italic | 0em | 1.2 |
| body | 28px | 300 | 0.02em | 1.7 |
| small | 16px | 400 | 0.1em | 1.4 |

## Layout Rules
- 1920×1080 canvas, padding 120px 140px (generous breathing room)
- Left-aligned content, right 1/3 intentionally empty
- Cover: title bottom-left anchored, massive negative space above
- Content: asymmetric 60/40 split — text left, image/decor right
- All text flush-left, never justified

## Decorative Elements
- **粉红下划线**: `background: linear-gradient(to right, var(--color-accent), var(--color-accent)) no-repeat left bottom; background-size: 0 var(--underline-width); transition: background-size 0.8s ease-out` — extends to 100% on slide.active
- **大段暗色留白**: intentionally empty dark space is the signature — 30-50% of each slide is empty
- **斜体标题**: `font-style: italic` on all headings — the italic is the personality
- **粉红光晕**: subtle `radial-gradient(circle at 70% 30%, rgba(255,59,139,0.04), transparent 60%)` on `.slide` background

## Animation
- Pattern: underline-extend (0.8s ease-out) + D (slow fade-up, 0.9s ease-out)
- Stagger: 120ms increments (slower, more deliberate)
- Underlines extend first, then text fades up
- Cover: massive title fades in alone over 1.2s, then underline extends

## Special Slide Types
- **封面**: 大标题 (120px italic) 在左下 + 粉红下划线从左到右 + 右下角小号副标题
- **目录**: 序号 (mono, muted) + 章节名 (italic heading)，3-4 行垂直排列，每行有粉红下划线
- **内容页 (演讲型)**: 大 italic 标题 + 一行正文，右侧全空
- **内容页 (阅读型)**: 标题 + 正文左 60%，右侧可放图片
- **图片页**: 全幅图片 dimmed + 文字叠层在左下
- **总结**: 居中 italic 大字 + 粉红下划线 + 联系方式小字
