# 温暖奶油锈红俱乐部 — Design System

## Font Import
```css
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,400;1,9..144,500&family=Jost:wght@400;500;700&family=Noto+Serif+SC:wght@400;500;700&display=swap');
```

## CSS Custom Properties
```css
#stage {
  --viewport-bg: #faf3e8;
  --stage-bg: #faf3e8;
  --color-bg: #faf3e8;
  --color-text: #3d2b1a;
  --color-accent: #b8451e;
  --color-accent2: #e8d5c0;
  --color-muted: #a09080;
  --font-heading: "Fraunces", "Noto Serif SC", serif;
  --font-body: "Jost", "Noto Serif SC", sans-serif;
  --font-mono: "JetBrains Mono", monospace;
  --slide-padding: 120px 140px;
  --transition-speed: 0.55s;
  --nav-bg: rgba(184, 69, 30, 0.06);
  --nav-border: rgba(184, 69, 30, 0.2);
  --nav-color: #3d2b1a;
  --nav-hover-bg: rgba(184, 69, 30, 0.15);
  --indicator-color: rgba(61, 43, 26, 0.35);
  --pill-radius: 50px;
  --pill-border: 2px;
  --accent-bar-width: 160px;
  --accent-bar-height: 3px;
}
```

## Typography Scale
| Level | Size | Weight | Letter Spacing | Line Height |
|-------|------|--------|----------------|-------------|
| h1 hero | 96px | 400 italic | -0.02em | 1.05 |
| h1 | 64px | 400 italic | -0.01em | 1.1 |
| h2 | 40px | 500 | 0em | 1.2 |
| h3 | 24px | 500 | 0.06em | 1.3 |
| body | 24px | 400 | 0.01em | 1.65 |
| small | 14px | 400 | 0.12em | 1.4 |

## Layout Rules
- Classic left-aligned with rust accent: everything flush-left
- Rust accent bar (160×3px) at top-left of each content slide, 20px from top edge
- Content area: 70% width, left-aligned
- Right 30%: warm sand accent zone, may contain subtle decoration or remain empty
- Very restrained — only 4 colors total including background

## Decorative Elements
- **锈红 accent bar**: `position: absolute; top: 80px; left: 140px; width: var(--accent-bar-width); height: var(--accent-bar-height); background: var(--color-accent)` — on every content slide
- **药丸形轮廓按钮**: `display: inline-block; padding: 14px 40px; border: var(--pill-border) solid var(--color-accent); border-radius: var(--pill-radius); color: var(--color-accent); font-family: var(--font-body); font-weight: 500; font-size: 20px; text-transform: uppercase; letter-spacing: 0.08em; background: transparent` — used for CTAs on summary slide
- **斜体 Fraunces**: `font-style: italic` on all headings, with `letter-spacing: -0.02em` for elegance
- **暖沙辅助区**: subtle `var(--color-accent2)` tinted zone on the right third, `opacity: 0.3`

## Animation
- Pattern: A (fade + slide-up, 0.6s cubic-bezier(0.16,1,0.3,1))
- Accent bar extends first (width 0→160px, 0.5s), then content fades in
- Stagger: 100ms increments
- Pill buttons: extend from left on summary slide (0→auto width, 0.6s)
- Overall feel: smooth, deliberate, premium — no bouncing

## Special Slide Types
- **封面**: 大 italic Fraunces 标题 (96px) 左对齐 + 锈红 accent bar + 副标题/日期小号 Jost uppercase
- **目录**: 序号 (muted, small) + 章节名 (Fraunces italic)，锈红 accent bar 在第一个条目上方
- **内容页 (演讲型)**: accent bar + 大 italic 标题 + 一行正文
- **内容页 (阅读型)**: accent bar + 标题 + 正文段 + 暖沙色辅助区放要点
- **数据页**: 数字用 Fraunces italic 大号 (72px, accent 色) + Jost uppercase 标签
- **总结**: 居中 italic 标题 + 3 个水平排列的药丸按钮 (内含 takeaway) + 底部锈红 accent bar
