# 新 Brutalist 粉红鼠尾草 — Design System

## Font Import
```css
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:wght@400;700&family=Noto+Sans+SC:wght@400;700&display=swap');
```

## CSS Custom Properties
```css
#stage {
  --viewport-bg: #fff5f5;
  --stage-bg: #fff5f5;
  --color-bg: #fff5f5;
  --color-text: #2c2c3a;
  --color-accent: #ff6b8a;
  --color-accent2: #7a9a7a;
  --color-accent3: #fff8e8;
  --color-border: #2c2c3a;
  --color-shadow: rgba(44, 44, 58, 0.8);
  --font-heading: "Bebas Neue", "Noto Sans SC", sans-serif;
  --font-body: "Space Mono", "Noto Sans SC", monospace;
  --font-mono: "Space Mono", monospace;
  --slide-padding: 60px 80px;
  --transition-speed: 0.35s;
  --nav-bg: rgba(255, 107, 138, 0.15);
  --nav-border: #2c2c3a;
  --nav-color: #2c2c3a;
  --nav-hover-bg: rgba(255, 107, 138, 0.3);
  --indicator-color: rgba(44, 44, 58, 0.5);
  --border-width: 3px;
  --shadow-offset: 8px;
  --radius: 0px;
}
```

## Typography Scale
| Level | Size | Weight | Letter Spacing | Line Height |
|-------|------|--------|----------------|-------------|
| h1 hero | 120px | 400 | -0.02em | 0.95 |
| h1 | 80px | 400 | -0.01em | 1.0 |
| h2 | 48px | 400 | 0em | 1.1 |
| body | 22px | 400 | 0em | 1.6 |
| small | 14px | 400 | 0.05em | 1.4 |

## Layout Rules
- Asymmetric color block grid — no traditional columns
- Elements can overflow canvas edges intentionally
- Color blocks: large rectangles with hard borders and offset shadows
- Text often overlays color blocks
- Maximum 3-4 blocks per slide, each 300-600px wide
- NO border-radius anywhere — `--radius: 0px` is the rule
- `box-shadow: var(--shadow-offset) var(--shadow-offset) 0 var(--color-shadow)` on all blocks

## Decorative Elements
- **粗黑边框**: `border: var(--border-width) solid var(--color-border)` on every block, card, button
- **偏移阴影**: `box-shadow: var(--shadow-offset) var(--shadow-offset) 0 var(--color-shadow)` — no blur, hard edge
- **大色块碰撞**: pink blocks beside sage blocks beside bone blocks — colors abut directly with 3px black borders between
- **hover 阴影偏移变化**: on interactive elements, shadow moves from 8px→4px on hover (not used in slides but noted for consistency)

## Animation
- block-bounce-in: `transform: scale(0); transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)` → `scale(1)`
- Color blocks pop in with elastic overshoot
- Text on blocks: fade-up after block lands (delay 0.15s)
- Fastest stagger of all templates: 60ms

## Special Slide Types
- **封面**: 大粉红色块 (1200×500px) 居中偏上 + Bebas Neue 标题叠在色块上 (白色文字) + 鼠尾草色块在右下角
- **目录**: 3 个带偏移阴影的色块水平排列 (粉红/鼠尾草/骨白)，每个内含章节标题
- **内容页 (演讲型)**: 左侧大色块 + 右侧骨白色块叠放，Bebas Neue 标题
- **内容页 (阅读型)**: 上方色块标题 + 下方 Space Mono 正文 (黑色边框围住整个内容区)
- **数据页**: 色块的高度 = 数据值 (bar chart 用色块天然实现)，数字用 Bebas Neue 超大
- **总结**: 3 个堆叠色块 + 1 个 CTA 按钮 (黑边框 + 偏移阴影)
