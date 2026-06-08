# 动画模式参考

Phase 3 生成最终 HTML 时，根据模板的 `animation` 字段选择对应的动画模式。

---

## 核心 Reveal 动画

### A. Fade + Slide Up（默认通用）
适用：大多数内容页，优雅不突兀

```css
.reveal {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide.active .reveal { opacity: 1; transform: translateY(0); }

/* Staggered delays */
.slide .reveal:nth-child(1) { transition-delay: 0.10s; }
.slide .reveal:nth-child(2) { transition-delay: 0.18s; }
.slide .reveal:nth-child(3) { transition-delay: 0.26s; }
.slide .reveal:nth-child(4) { transition-delay: 0.34s; }
.slide .reveal:nth-child(5) { transition-delay: 0.42s; }
.slide .reveal:nth-child(6) { transition-delay: 0.50s; }
.slide .reveal:nth-child(7) { transition-delay: 0.58s; }
.slide .reveal:nth-child(8) { transition-delay: 0.66s; }
```

### B. Scale + Fade（图片/卡片专用）
适用：卡片、图片、数据面板

```css
.reveal {
  opacity: 0;
  transform: scale(0.92);
  transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide.active .reveal { opacity: 1; transform: scale(1); }
```

### C. Clip-path Reveal（戏剧化）
适用：大标题、视觉冲击页

```css
.reveal {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 0.65s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide.active .reveal { clip-path: inset(0 0 0 0); }
```

### D. 极慢学术淡入
适用：安静学术风格、文学杂志风格

```css
.reveal {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.9s ease-out,
              transform 0.9s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide .reveal:nth-child(1) { transition-delay: 0.15s; }
.slide .reveal:nth-child(2) { transition-delay: 0.30s; }
.slide .reveal:nth-child(3) { transition-delay: 0.45s; }
.slide .reveal:nth-child(4) { transition-delay: 0.60s; }
.slide .reveal:nth-child(5) { transition-delay: 0.75s; }
```

---

## 装饰元素动画

### 霓虹描边延伸
```css
.neon-line {
  width: 0;
  transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide.active .neon-line { width: 100%; }
```

### 下划线从左到右展开
```css
.underline-reveal {
  background: linear-gradient(to right, var(--color-accent), var(--color-accent)) no-repeat left bottom;
  background-size: 0 2px;
  transition: background-size 0.6s ease-out;
}
.slide.active .underline-reveal { background-size: 100% 2px; }
```

### 色块弹入（Brutalist 专用）
```css
.color-block {
  transform: scale(0);
  transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.slide.active .color-block { transform: scale(1); }
```

### 几何形状旋转缩放（Bauhaus 专用）
```css
.geo-shape {
  opacity: 0;
  transform: rotate(-30deg) scale(0.6);
  transition: opacity 0.5s ease-out,
              transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide.active .geo-shape { opacity: 1; transform: rotate(0deg) scale(1); }
```

### 光晕呼吸
```css
.glow-orb {
  animation: breathe 4s ease-in-out infinite;
}
@keyframes breathe {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.05); }
}
```

### 像素打字效果
```css
.pixel-type {
  overflow: hidden;
  white-space: nowrap;
  width: 0;
  animation: typewriter 1.5s steps(20) forwards;
}
@keyframes typewriter { to { width: 100%; } }
```

---

## 翻页过渡模式

```css
/* Crossfade（默认） */
.slide { opacity: 0; transition: opacity 0.5s ease-out; }
.slide.active { opacity: 1; }

/* Slide Horizontal（叙事型） */
.slide { transform: translateX(100%); transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1); }
.slide.active { transform: translateX(0); }

/* Scale Fade（演讲型） */
.slide { opacity: 0; transform: scale(1.05); transition: all 0.6s ease-out; }
.slide.active { opacity: 1; transform: scale(1); }
```

---

## Reduced Motion 覆盖

```css
@media (prefers-reduced-motion: reduce) {
  .reveal, .slide { transition: none !important; animation: none !important; }
  .reveal { opacity: 1 !important; transform: none !important; clip-path: none !important; }
  .neon-line, .underline-reveal { transition: none !important; }
  .neon-line { width: 100% !important; }
  .underline-reveal { background-size: 100% 2px !important; }
}
```
