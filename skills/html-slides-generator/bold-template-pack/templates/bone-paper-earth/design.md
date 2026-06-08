# 骨纸大地 — Design System

## Font Import
```css
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Jost:wght@300;400;500&family=Noto+Serif+SC:wght@400;500;700&display=swap');
```

## CSS Custom Properties
```css
#stage {
  --viewport-bg: #e8dcc8;
  --stage-bg: #e8dcc8;
  --color-bg: #e8dcc8;
  --color-text: #2c2416;
  --color-accent: #5c4033;
  --color-accent2: #3a5a3a;
  --color-accent3: #d4a853;
  --color-accent4: #c4a882;
  --color-accent5: #8b7355;
  --color-muted: #a09080;
  --font-heading: "Cormorant Garamond", "Noto Serif SC", serif;
  --font-body: "Jost", "Noto Serif SC", sans-serif;
  --font-mono: "JetBrains Mono", monospace;
  --slide-padding: 90px 120px;
  --transition-speed: 0.6s;
  --nav-bg: rgba(92, 64, 51, 0.08);
  --nav-border: rgba(92, 64, 51, 0.2);
  --nav-color: #2c2416;
  --nav-hover-bg: rgba(212, 168, 83, 0.2);
  --indicator-color: rgba(44, 36, 22, 0.4);
  --strata-line-height: 2px;
  --strata-count: 6;
}
```

## Typography Scale
| Level | Size | Weight | Letter Spacing | Line Height |
|-------|------|--------|----------------|-------------|
| h1 hero | 80px | 600 | 0em | 1.1 |
| h1 | 56px | 600 | 0.01em | 1.15 |
| h2 | 40px | 500 | 0.02em | 1.3 |
| h3 | 28px | 500 | 0.04em | 1.4 |
| body | 24px | 300 | 0.02em | 1.65 |
| small | 16px | 400 | 0.1em | 1.4 |

## Layout Rules
- Horizontal strata (layers): the canvas is divided by colored horizontal lines
- Content sits between strata lines
- Heading zone (top 30%): title + decorative lines above and below
- Content zone (70%): text/visuals below the heading strata
- Six colors used exclusively as line colors — never all at once, 2-3 per slide

## Decorative Elements
- **分层地质线条**: multiple `<div>` elements styled as horizontal lines: `height: var(--strata-line-height); background: var(--color-accent); width: 300px` each in different earth tones, stacked with 8px gaps
- **模板切割标题**: `h1 { background: linear-gradient(90deg, var(--color-accent), var(--color-accent3)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }` — looks like stencil-cut letters filled with earth gradient
- **测量标记**: small tick marks (16px tall, 1px wide) at the ends of strata lines, like architectural blueprint marks
- **骨纸纹理**: `background-image: url("data:image/svg+xml,...")` subtle noise overlay at 3% opacity for paper texture

## Animation
- strata-line-extend: horizontal lines extend from width 0→300px, sequential with 100ms delay per line
- Pattern: A (fade + slide-up, 0.6s) for content after lines complete
- Lines: `transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1)`
- Overall feel: like unrolling a geological core sample

## Special Slide Types
- **封面**: 标题用模板切割效果 + 6 条地层线从顶部依次向下排列 (暗棕 → 中棕 → 橄榄绿 → 沙金 → 牛皮 → 暗金)
- **目录**: 每行前后有测量标记 + 细地层线，形成"标本标签"感
- **内容页 (演讲型)**: 顶部 3 条地层线 + 大标题 + 一句话
- **内容页 (阅读型)**: 左侧地层线竖线 (vertical strata) + 右侧内容，考古田野笔记风格
- **数据页**: 水平条形图用地层线样式 (不同颜色、不同宽度)
- **总结**: 6 条地层线从上到下排列 (全六色) + 中心标题
