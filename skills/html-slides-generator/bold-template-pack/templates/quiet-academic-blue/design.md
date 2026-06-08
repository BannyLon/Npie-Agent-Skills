# 安静学术蓝金 — Design System

## Font Import
```css
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Libre+Baskerville:ital@0;1&family=Noto+Serif+SC:wght@400;500;700&display=swap');
```

## CSS Custom Properties
```css
#stage {
  --viewport-bg: #0a1628;
  --stage-bg: #0a1628;
  --color-bg: #0a1628;
  --color-text: #f5d47a;
  --color-accent: #f5d47a;
  --color-accent2: #8a9bb5;
  --color-accent3: #e8dcc8;
  --color-muted: #5a6a85;
  --font-heading: "Cormorant Garamond", "Noto Serif SC", serif;
  --font-body: "Libre Baskerville", "Noto Serif SC", serif;
  --font-mono: "JetBrains Mono", monospace;
  --slide-padding: 140px 180px;
  --transition-speed: 0.9s;
  --nav-bg: rgba(245, 212, 122, 0.06);
  --nav-border: rgba(245, 212, 122, 0.15);
  --nav-color: rgba(245, 212, 122, 0.7);
  --nav-hover-bg: rgba(245, 212, 122, 0.15);
  --indicator-color: rgba(245, 212, 122, 0.35);
  --glow-subtle: 0 0 30px rgba(245, 212, 122, 0.08);
  --content-width: 65%;
}
```

## Typography Scale
| Level | Size | Weight | Letter Spacing | Line Height |
|-------|------|--------|----------------|-------------|
| h1 hero | 88px | 500 italic | -0.01em | 1.1 |
| h1 | 64px | 500 italic | 0em | 1.15 |
| h2 | 40px | 500 italic | 0em | 1.3 |
| body | 24px | 400 | 0.01em | 1.7 |
| small (small caps) | 16px | 400 | 0.15em | 1.4 |

## Layout Rules
- Classic centered: content area 65% width, centered
- Generous dark negative space (35% of canvas is empty dark blue)
- Gold accent bar (1px, 200px wide) at top-center of each content slide
- Cover: everything centered, title with subtle gold glow
- All elements centered unless specifically noted

## Decorative Elements
- **暖金微发光**: `text-shadow: var(--glow-subtle)` on major headings — very subtle, not neon
- **细金线分隔**: `border-bottom: 1px solid rgba(245, 212, 122, 0.3); width: 200px; margin: 0 auto`
- **罗马数字页码**: footer centered, `font-family: var(--font-heading); font-size: 14px; color: rgba(245,212,122,0.3)`
- **章节标签 (small caps)**: `font-size: 14px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--color-accent2)` — dusty blue small caps above title

## Animation
- Pattern: golden-fade (opacity 0→1 over 1s, ease-out, no transform — pure fade from darkness)
- Stagger: 150ms increments
- Feels like text emerging from a dark library — slow, dignified, no motion except light

## Special Slide Types
- **封面**: 标题居中 (88px italic) + 金线分隔下方 + 副标题/演讲者/日期小字
- **目录**: 罗马数字 + 章节名 (gold italic)，dusty blue 细线分隔
- **内容页 (演讲型)**: small caps 标签 + 大 italic 标题 + 一句话 (gold)
- **内容页 (阅读型)**: 标题 + 正文 (dusty blue 文字色，或 gold 用于强调) + 金线分隔段落
- **引用页**: 居中 italic 大字 + 出处，全在金色中
- **总结**: 居中标题 + 3 个要点 (带 gold bullet 圆点) + 底部金线
