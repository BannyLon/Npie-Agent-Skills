# 像素霓虹街机 — Design System

## Font Import
```css
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Fira+Code:wght@400;700&family=Noto+Sans+SC:wght@400;700&display=swap');
```

## CSS Custom Properties
```css
#stage {
  --viewport-bg: #0a0e27;
  --stage-bg: #0a0e27;
  --color-bg: #0a0e27;
  --color-text: #e8e0ff;
  --color-accent: #ff00ff;
  --color-accent2: #00ffff;
  --color-accent3: #ffff00;
  --color-muted: #5a5a8a;
  --color-panel: #1a1a3e;
  --font-heading: "Press Start 2P", "Noto Sans SC", cursive;
  --font-body: "Fira Code", "Noto Sans SC", monospace;
  --font-mono: "Fira Code", monospace;
  --slide-padding: 80px 100px;
  --transition-speed: 0.4s;
  --nav-bg: rgba(255, 0, 255, 0.1);
  --nav-border: rgba(255, 0, 255, 0.3);
  --nav-color: #ff00ff;
  --nav-hover-bg: rgba(255, 0, 255, 0.25);
  --indicator-color: rgba(0, 255, 255, 0.6);
  --glow-strong: 0 0 15px;
  --scanline-opacity: 0.04;
}
```

## Typography Scale
| Level | Size | Weight | Letter Spacing | Line Height |
|-------|------|--------|----------------|-------------|
| h1 hero | 64px | 400 | 0em | 1.5 |
| h1 | 48px | 400 | 0em | 1.5 |
| h2 | 32px | 400 | 0em | 1.5 |
| body | 22px | 400 | 0em | 1.8 |
| small | 16px | 400 | 0.05em | 1.5 |

## Layout Rules
- 1920×1080 canvas, padding 80px 100px
- HUD/game UI style: center-heavy composition
- Bottom info bar: 60px, full-width, `var(--color-panel)` background
- Title centered in upper 60% of canvas
- Data displayed in pixel "windows" with 4px solid neon borders

## Decorative Elements
- **像素网格背景**: `background-size: 8px 8px; background-image: radial-gradient(circle, rgba(255,0,255,0.1) 1px, transparent 1px)`
- **霓虹发光**: `text-shadow: var(--glow-strong) var(--color-accent)` for magenta, similar for cyan
- **扫描线**: `::after` pseudo-element with `repeating-linear-gradient(0deg, rgba(0,0,0,var(--scanline-opacity)), transparent 2px)` covering full canvas, `pointer-events: none`
- **像素故障装饰**: `clip-path: polygon(0 0, 100% 0, 100% 85%, 95% 85%, 95% 90%, 90% 90%, 90% 100%, 0 100%)` for stair-step edges

## Animation
- Pattern: pixel-typewriter (keyframes: width 0→100% with steps())
- Cover: title types out character by character over 1.5s
- Neon elements: opacity pulse 2s infinite
- Content pages: fade-up with slight glitch (translateX -3px→3px→0, 100ms)

## Special Slide Types
- **封面**: 大标题居中 + 像素边框围住标题 + 底部扫描线效果
- **目录**: 像素风格菜单列表，每项前有 `>` 光标提示符闪烁
- **内容页 (演讲型)**: 标题在像素框内 + 关键词霓虹高亮
- **内容页 (阅读型)**: 左侧像素装饰条 + 右侧文字
- **数据页**: 大号像素数字 (accent 色) + 像素进度条
- **总结**: "GAME OVER" 风格居中大字 + 闪烁 "CONTINUE?" 提示
