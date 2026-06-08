# 毛玻璃科技 — Design System

## Font Import
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=DM+Sans:wght@400;500;700&family=Noto+Sans+SC:wght@400;700&display=swap');
```

## CSS Custom Properties
```css
#stage {
  --viewport-bg: #f0f4f8;
  --stage-bg: #f0f4f8;
  --color-bg: #f0f4f8;
  --color-text: #1a1a2e;
  --color-accent: #4a9eff;
  --color-accent2: #7b5cff;
  --color-muted: #8a8fa0;
  --color-glass-bg: rgba(255, 255, 255, 0.25);
  --color-glass-border: rgba(255, 255, 255, 0.4);
  --color-glass-shadow: rgba(0, 0, 0, 0.06);
  --glass-blur: 20px;
  --font-heading: "Inter", "Noto Sans SC", sans-serif;
  --font-body: "DM Sans", "Noto Sans SC", sans-serif;
  --font-mono: "JetBrains Mono", monospace;
  --slide-padding: 100px 120px;
  --transition-speed: 0.5s;
  --nav-bg: rgba(74, 158, 255, 0.08);
  --nav-border: rgba(74, 158, 255, 0.2);
  --nav-color: #1a1a2e;
  --nav-hover-bg: rgba(74, 158, 255, 0.2);
  --indicator-color: rgba(26, 26, 46, 0.4);
  --radius-sm: 12px;
  --radius-md: 16px;
  --radius-lg: 24px;
}
```

## Typography Scale
| Level | Size | Weight | Letter Spacing | Line Height |
|-------|------|--------|----------------|-------------|
| h1 hero | 80px | 700 | -0.02em | 1.1 |
| h1 | 56px | 600 | -0.01em | 1.2 |
| h2 | 40px | 600 | 0em | 1.3 |
| h3 | 28px | 500 | 0em | 1.4 |
| body | 26px | 400 | 0.01em | 1.6 |
| small | 18px | 400 | 0.02em | 1.4 |

## Layout Rules
- Layered card system: cards with varying glass depth (blur amounts)
- Cover: large glass hero card centered, floating orbs behind
- Content: grid of glass cards, 2-3 per slide
- Each card: `background: var(--color-glass-bg); backdrop-filter: blur(var(--glass-blur)); border: 1px solid var(--color-glass-border); border-radius: var(--radius-lg); box-shadow: 0 8px 32px var(--color-glass-shadow)`
- Cards can overlap slightly for depth effect

## Decorative Elements
- **光晕球体**: `<div>` with `border-radius: 50%; background: radial-gradient(circle at 40% 40%, var(--color-accent), transparent 70%); opacity: 0.3; position: absolute; width: 400px; height: 400px; filter: blur(60px); pointer-events: none`
- **毛玻璃面板**: the core element — everything sits on glass. Multiple layers with different blur amounts (10px, 20px, 30px) for depth hierarchy
- **微妙的渐变边框**: `border: 1px solid transparent; background: linear-gradient(white, white) padding-box, linear-gradient(135deg, rgba(74,158,255,0.3), rgba(123,92,255,0.3)) border-box`

## Animation
- Pattern: C (scale + fade, 0.92→1 + opacity 0→1, 0.5s cubic-bezier(0.16,1,0.3,1))
- Stagger: 100ms increments
- Cards rise and scale in sequence
- Glow orbs: subtle float animation (translateY ±10px, 6s ease-in-out infinite)

## Special Slide Types
- **封面**: 居中大玻璃卡片 (800×500px) + 标题/副标题 + 3 个光晕球体在背景漂浮
- **目录**: 3-4 张玻璃卡片水平排列，每张一个章节
- **内容页 (演讲型)**: 单张大玻璃卡片居中，1-2 句话
- **内容页 (阅读型)**: 左侧大卡片 (文字) + 右侧小卡片堆叠 (要点)
- **数据页**: 玻璃卡片网格，每张显示一个指标 (大数字 + 标签)
- **总结**: 水平排列 3 张玻璃卡片，每张一个 takeaway
