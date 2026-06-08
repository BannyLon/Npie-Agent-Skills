# 新包豪斯粉彩霓虹 — Design System

## Font Import
```css
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=DM+Sans:wght@400;500&family=Noto+Sans+SC:wght@400;700&display=swap');
```

## CSS Custom Properties
```css
#stage {
  --viewport-bg: #faf8f3;
  --stage-bg: #faf8f3;
  --color-bg: #faf8f3;
  --color-text: #1a1a1a;
  --color-accent: #ffb3ba;
  --color-accent2: #bae1ff;
  --color-accent3: #ffffba;
  --color-accent4: #baffc9;
  --color-border: #1a1a1a;
  --font-heading: "Outfit", "Noto Sans SC", sans-serif;
  --font-body: "DM Sans", "Noto Sans SC", sans-serif;
  --font-mono: "JetBrains Mono", monospace;
  --slide-padding: 80px 100px;
  --transition-speed: 0.45s;
  --nav-bg: rgba(26, 26, 26, 0.05);
  --nav-border: #1a1a1a;
  --nav-color: #1a1a1a;
  --nav-hover-bg: rgba(255, 179, 186, 0.3);
  --indicator-color: rgba(26, 26, 26, 0.4);
  --border-width: 3px;
  --shape-size: 120px;
}
```

## Typography Scale
| Level | Size | Weight | Letter Spacing | Line Height |
|-------|------|--------|----------------|-------------|
| h1 hero | 72px | 700 | -0.02em | 1.1 |
| h1 | 56px | 600 | -0.01em | 1.15 |
| h2 | 36px | 500 | 0em | 1.3 |
| body | 24px | 400 | 0.01em | 1.6 |
| small | 16px | 400 | 0.05em | 1.4 |

## Layout Rules
- Geometric partition: canvas divided by geometric shapes, not traditional grid
- Circle zones for images/icons, square zones for text, triangle accents for visual interest
- Every shape has `border: var(--border-width) solid var(--color-border)`
- Shapes use 4 pastel colors, never mixing gradients — pure flat color
- Composition feels balanced but playful — shapes rotate slightly (-5 to +5 deg)

## Decorative Elements
- **几何基本形** (all CSS-drawn):
  - 圆: `width: var(--shape-size); height: var(--shape-size); border-radius: 50%; border: var(--border-width) solid var(--color-border); background: var(--color-accent)`
  - 方: `width: var(--shape-size); height: var(--shape-size); border: var(--border-width) solid var(--color-border); background: var(--color-accent2)`
  - 三角: `width: 0; height: 0; border-left: 60px solid transparent; border-right: 60px solid transparent; border-bottom: 104px solid var(--color-accent3)` + outline via `filter: drop-shadow(3px 0 0 black) drop-shadow(-3px 0 0 black) drop-shadow(0 -3px 0 black)`
- **全黑边框**: 3px solid `#1a1a1a` everywhere — the unifying element
- **包豪斯抽象构图**: shapes overlap, intersect, and are placed asymmetrically — inspired by Kandinsky compositions

## Animation
- shape-rotate-scale: `opacity: 0; transform: rotate(-15deg) scale(0.7); transition: opacity 0.5s ease-out, transform 0.55s cubic-bezier(0.16, 1, 0.3, 1)` → `opacity: 1; transform: rotate(0deg) scale(1)`
- Each shape animates independently with 80ms stagger
- Text fades up after shapes settle

## Special Slide Types
- **封面**: 大圆 (粉红) 居中偏左 + 大方 (粉蓝) 右下 + 小三角 (粉黄) 右上 + Outfit 标题叠在上方
- **目录**: 4 个不同颜色的圆水平排列，每个内含章节序号 (数字)
- **内容页 (演讲型)**: 左侧粉蓝方框 (标题) + 右侧粉红圆 (关键词) + 文字在下方
- **内容页 (阅读型)**: 顶部扁矩形 (粉绿) 作为标题栏 + 下方正文
- **数据页**: 用不同大小的圆/方/三角表示数据量 (面积 = 数值)，包豪斯信息图
- **总结**: 四种颜色、四种形状围绕中心文字，形成包豪斯式构图
