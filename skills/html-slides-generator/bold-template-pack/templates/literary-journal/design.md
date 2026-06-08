# 高级文学杂志 — Design System

## Font Import
```css
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Libre+Baskerville:ital@0;1&family=Noto+Serif+SC:wght@400;500;700&display=swap');
```

## CSS Custom Properties
```css
#stage {
  --viewport-bg: #faf8f5;
  --stage-bg: #faf8f5;
  --color-bg: #faf8f5;
  --color-text: #1a1a1a;
  --color-accent: #c12530;
  --color-muted: #999590;
  --color-divider: #e0dcd5;
  --color-warm-gray: #f0ece6;
  --font-heading: "Cormorant Garamond", "Noto Serif SC", serif;
  --font-body: "Libre Baskerville", "Noto Serif SC", serif;
  --font-mono: "JetBrains Mono", monospace;
  --slide-padding: 160px 200px;
  --transition-speed: 0.8s;
  --nav-bg: rgba(193, 37, 48, 0.06);
  --nav-border: rgba(193, 37, 48, 0.15);
  --nav-color: #1a1a1a;
  --nav-hover-bg: rgba(193, 37, 48, 0.12);
  --indicator-color: rgba(26, 26, 26, 0.35);
  --content-max-width: 960px;
}
```

## Typography Scale
| Level | Size | Weight | Letter Spacing | Line Height |
|-------|------|--------|----------------|-------------|
| h1 hero | 88px | 600 | -0.01em | 1.1 |
| h1 | 64px | 600 | 0em | 1.15 |
| h2 | 40px | 500 | 0em | 1.3 |
| h3 | 28px | 500 | 0.04em | 1.4 |
| body | 26px | 400 | 0em | 1.75 |
| small | 16px | 400 | 0.1em | 1.4 |

## Layout Rules
- Book-proportion layout: content area max-width 960px centered on 1920px canvas
- Extra-wide padding (160px 200px) creates vast margins
- Cover: title centered vertically and horizontally
- Content: narrow centered column, like a book page
- Double-line header: `border-top: 3px double var(--color-accent)` at the top of each content slide
- Roman numeral page numbers in footer, small and centered

## Decorative Elements
- **双线标头**: `border-top: 3px double var(--color-accent); width: 200px` centered at top of content slides
- **首字下沉**: `p:first-of-type::first-letter { font-size: 3.5em; float: left; line-height: 0.8; padding-right: 8px; font-family: var(--font-heading); color: var(--color-accent); }`
- **细灰分隔线**: `border-bottom: 0.5px solid var(--color-divider); width: 100px`
- **章节罗马数字**: `font-family: var(--font-heading); font-size: 18px; color: var(--color-accent); letter-spacing: 0.2em`

## Animation
- Pattern: D (slow academic fade, 0.9s ease-out, translateY 16px→0)
- Stagger: 150ms increments (slowest stagger of all templates)
- Double-line header fades in first, then content
- No bouncy or playful easing — everything is dignified ease-out

## Special Slide Types
- **封面**: 标题居中 (80px, 600 weight) + 副标题下方 (28px, italic, muted) + 底部作者/日期 (16px, small caps)
- **目录**: 罗马数字序号 + 章节名 (italic)，细灰线分隔每个条目
- **内容页 (演讲型)**: 双线标头 + 标题 (64px) + 一行引言 (28px italic)
- **内容页 (阅读型)**: 双线标头 + 标题 + 正文段 (首字下沉) + 段落间距 32px
- **引用页**: 居中大号 italic 引用 (48px) + 出处小字下方 + 两侧巨大留白
- **总结**: 居中标题 + 3 个编号要点 + 底部编辑部红细线
