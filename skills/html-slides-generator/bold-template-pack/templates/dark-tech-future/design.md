# 暗黑科技未来 — Design System

## Font Import
```css
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;700&family=Noto+Sans+SC:wght@400;700&display=swap');
```

## CSS Custom Properties
```css
#stage {
  --viewport-bg: #0d0d0f;
  --stage-bg: #0d0d0f;
  --color-bg: #0d0d0f;
  --color-text: #e0e0e0;
  --color-accent: #00f0ff;
  --color-accent2: #7b3fff;
  --color-muted: #666677;
  --color-panel: #1a1a2e;
  --color-border: rgba(0, 240, 255, 0.15);
  --font-heading: "Space Grotesk", "Noto Sans SC", sans-serif;
  --font-body: "Inter", "Noto Sans SC", sans-serif;
  --font-mono: "JetBrains Mono", monospace;
  --slide-padding: 100px 120px;
  --transition-speed: 0.5s;
  --nav-bg: rgba(0, 240, 255, 0.06);
  --nav-border: rgba(0, 240, 255, 0.2);
  --nav-color: #e0e0e0;
  --nav-hover-bg: rgba(0, 240, 255, 0.15);
  --indicator-color: rgba(255,255,255,0.4);
  --glow-color: rgba(0, 240, 255, 0.08);
  --grid-color: rgba(255,255,255,0.03);
}
```

## Typography Scale
| Level | Size | Weight | Letter Spacing | Line Height |
|-------|------|--------|----------------|-------------|
| h1 hero | 96px | 700 | -0.02em | 1.1 |
| h1 | 72px | 600 | -0.01em | 1.15 |
| h2 | 48px | 500 | 0em | 1.3 |
| h3 | 32px | 500 | 0em | 1.4 |
| body | 28px | 300 | 0.01em | 1.6 |
| mono/code | 24px | 400 | 0em | 1.5 |
| small | 18px | 400 | 0.05em | 1.4 |

## Layout Rules
- 1920×1080 画布，padding 100px 120px
- 居中对称为主；封面标题垂直水平居中
- 数据/对比页用三列网格：`grid-template-columns: repeat(3, 1fr); gap: 40px`
- 左侧 accent bar 宽 4px，位于内容区最左
- 底部 HUD 信息栏 80px 高，背景 `var(--color-panel)`

## Decorative Elements
- **霓虹描边**: `border: 1px solid var(--color-border)` + `box-shadow: 0 0 20px var(--glow-color)`
- **网格背景**: `background-image: repeating-linear-gradient(0deg, var(--grid-color), var(--grid-color) 1px, transparent 1px, transparent 20px), repeating-linear-gradient(90deg, var(--grid-color), var(--grid-color) 1px, transparent 1px, transparent 20px)`
- **HUD 分隔线**: `border-bottom: 1px solid var(--color-border)` + 两侧小菱形 `::before/::after` (8px rotated 45deg squares)
- **发光数字**: `color: var(--color-accent); text-shadow: 0 0 20px var(--glow-color)`

## Animation
- Pattern: A (fade + slide-up), 0.6s cubic-bezier(0.16, 1, 0.3, 1)
- Stagger: 80ms increments (nth-child 1-8)
- Neon lines: width 0→100%, 0.8s ease-out
- Cover title: clip-path reveal from center

## Special Slide Types
- **封面**: 标题居中 + 霓虹线在标题下方从左到右延伸 + 底部副标题/日期
- **目录**: 左侧序号 (mono, accent 色) + 右侧章节名，3 行垂直排列，间距 40px
- **内容页 (演讲型)**: 大标题 (72px) + 1-2 行正文 (28px) + 霓虹 accent bar 在左
- **内容页 (阅读型)**: 标题 (48px) + 正文段 (24px) + 列表，accent 色 bullet
- **数据页**: 三列，每列顶部大号 mono 数字 (64px, accent 色) + 底部说明文字
- **总结**: 3 个 key takeaways 水平排列，每个有圆形序号 (accent 边框) + 文字
