# 浅绿白卡 — Design System

## Font Import
```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Inter:wght@300;400;600&family=Noto+Sans+SC:wght@400;700&display=swap');
```

## CSS Custom Properties
```css
#stage {
  --viewport-bg: #f5faf0;
  --stage-bg: #f5faf0;
  --color-bg: #f5faf0;
  --color-text: #2c3e1a;
  --color-accent: #9ccb54;
  --color-accent2: #6da832;
  --color-muted: #8a9e7a;
  --color-card-bg: #ffffff;
  --color-card-shadow: rgba(156, 203, 84, 0.15);
  --font-heading: "DM Sans", "Noto Sans SC", sans-serif;
  --font-body: "Inter", "Noto Sans SC", sans-serif;
  --font-mono: "JetBrains Mono", monospace;
  --slide-padding: 100px 120px;
  --transition-speed: 0.5s;
  --nav-bg: rgba(156, 203, 84, 0.1);
  --nav-border: rgba(156, 203, 84, 0.25);
  --nav-color: #2c3e1a;
  --nav-hover-bg: rgba(156, 203, 84, 0.2);
  --indicator-color: rgba(44, 62, 26, 0.4);
  --card-radius: 24px;
  --card-padding: 48px;
}
```

## Typography Scale
| Level | Size | Weight | Letter Spacing | Line Height |
|-------|------|--------|----------------|-------------|
| h1 hero | 72px | 700 | -0.02em | 1.1 |
| h1 | 56px | 700 | -0.01em | 1.2 |
| h2 | 40px | 500 | 0em | 1.3 |
| h3 | 28px | 500 | 0em | 1.4 |
| body | 24px | 400 | 0.01em | 1.6 |
| small | 16px | 400 | 0.03em | 1.4 |

## Layout Rules
- Card grid system: `display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 32px`
- Each card: `background: var(--color-card-bg); border-radius: var(--card-radius); padding: var(--card-padding); box-shadow: 0 4px 24px var(--color-card-shadow)`
- Cover: single large centered card (800×400px)
- Content: 1-3 cards per slide
- Green accent bar: 120px wide, 4px tall, `background: var(--color-accent)`, at top-left of each card

## Decorative Elements
- **白卡片**: the core element — always #ffffff with green-tinted shadow
- **绿色 accent bar**: `width: 120px; height: 4px; background: var(--color-accent); border-radius: 2px` at the top of key cards
- **背景光晕**: `radial-gradient(ellipse at 70% 20%, rgba(156,203,84,0.08), transparent 50%)` on `#stage` background
- **绿色图标/数字**: accent-colored large numbers (64px+, font-weight 700)

## Animation
- Pattern: C (scale + fade, 0.92→1 + opacity, 0.5s ease-out)
- Stagger: 100ms increments
- Cards rise with slight scale, green accent bar extends first
- Background glow pulses subtly on slide transition

## Special Slide Types
- **封面**: 居中大白卡片 (900×500px) + 标题 + 绿色 accent bar + 副标题
- **目录**: 3 张卡片水平排列，每张卡片顶部绿色圆点 + 章节名
- **内容页 (演讲型)**: 一张大卡片居中，绿色 accent bar 在顶部，1-2 句话
- **内容页 (阅读型)**: 左右两张卡片，左边正文右边要点/列表
- **数据页**: 3-4 张小卡片网格，每张显示一个绿色大数字 + 标签
- **总结**: 3 张卡片水平排列，每张一个 takeaway，绿色勾号
