# HTML 结构骨架 + JS 交互功能

生成最终 HTML 时使用此模板。`{{PLACEHOLDER}}` 替换为实际内容。

---

## 完整 HTML 骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
{{GOOGLE_FONTS_IMPORT}}
<style>
  /* ===== 复制 viewport-base.css 全部内容 ===== */

  /* ===== 设计系统 CSS 变量 ===== */
  /* STYLE: 修改以下变量来改变整体风格 */
  #stage {
    {{CSS_CUSTOM_PROPERTIES}}
  }

  /* ===== Reveal 动画 ===== */
  .reveal {
    opacity: 0;
    transform: translateY(24px);
    transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1),
                transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .slide.active .reveal { opacity: 1; transform: translateY(0); }

  /* Staggered delay — 最多 8 个子元素 */
  {{STAGGER_DELAYS}}

  /* ===== 每页独特样式 ===== */
  {{PER_SLIDE_STYLES}}
</style>
</head>
<body>

<div id="viewport">
  <div id="stage">
    {{ALL_SLIDES}}
  </div>
</div>

<div id="progress"></div>
<div id="page-indicator">01 / {{TOTAL}}</div>

<div id="nav-arrows">
  <button id="prev-btn" aria-label="上一页">←</button>
  <button id="next-btn" aria-label="下一页">→</button>
</div>

<script>
  // ===== 幻灯片导航引擎 =====
  (function() {
    const slides = document.querySelectorAll('.slide');
    const progress = document.getElementById('progress');
    const indicator = document.getElementById('page-indicator');
    const total = slides.length;
    let current = 0;
    let transitioning = false;

    function goTo(index) {
      if (index < 0 || index >= total || transitioning) return;
      transitioning = true;

      slides[current].classList.remove('active');
      slides[index].classList.add('active');
      current = index;

      const pct = ((current + 1) / total) * 100;
      progress.style.width = pct + '%';
      indicator.textContent =
        String(current + 1).padStart(2, '0') + ' / ' + String(total).padStart(2, '0');

      setTimeout(function() { transitioning = false; }, 500);
    }

    function next() { goTo(current + 1); }
    function prev() { goTo(current - 1); }

    // 键盘：← → Space Shift+Space Home End
    document.addEventListener('keydown', function(e) {
      if (e.key === 'ArrowRight' || e.key === ' ') {
        e.preventDefault(); next();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault(); prev();
      } else if (e.key === 'Home') {
        e.preventDefault(); goTo(0);
      } else if (e.key === 'End') {
        e.preventDefault(); goTo(total - 1);
      } else if (e.key === 'f' || e.key === 'F') {
        // 全屏切换
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().catch(function(){});
        } else {
          document.exitFullscreen();
        }
      }
    });

    // 滚轮（800ms debounce 防连跳）
    let wheelTimeout;
    document.addEventListener('wheel', function(e) {
      if (wheelTimeout) return;
      wheelTimeout = setTimeout(function() { wheelTimeout = null; }, 800);
      if (e.deltaY > 30) next();
      else if (e.deltaY < -30) prev();
    }, { passive: true });

    // 触屏滑动（50px 阈值）
    let touchStartY = 0, touchStartX = 0;
    document.addEventListener('touchstart', function(e) {
      touchStartY = e.touches[0].clientY;
      touchStartX = e.touches[0].clientX;
    }, { passive: true });

    document.addEventListener('touchend', function(e) {
      const dy = e.changedTouches[0].clientY - touchStartY;
      const dx = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(dy) > 50 && Math.abs(dy) > Math.abs(dx)) {
        if (dy > 0) next(); else prev();
      }
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) {
        if (dx < 0) next(); else prev();
      }
    });

    // 导航按钮
    document.getElementById('prev-btn').addEventListener('click', prev);
    document.getElementById('next-btn').addEventListener('click', next);

    // 16:9 缩放适配
    function resize() {
      const vp = document.getElementById('viewport');
      const scaleX = window.innerWidth / 1920;
      const scaleY = window.innerHeight / 1080;
      const scale = Math.min(scaleX, scaleY);
      vp.style.transform = 'translate(-50%, -50%) scale(' + scale + ')';
    }

    window.addEventListener('resize', resize);
    resize();

    // 初始化
    progress.style.width = (1 / total) * 100 + '%';
    indicator.textContent = '01 / ' + String(total).padStart(2, '0');

    // 已访问页面追踪（再次进入时跳过动画）
    const visited = new Set();
    visited.add(0);
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        if (mutation.target.classList.contains('active') && !visited.has(current)) {
          visited.add(current);
        }
      });
    });
    slides.forEach(function(s) {
      observer.observe(s, { attributes: true, attributeFilter: ['class'] });
    });
  })();
</script>

</body>
</html>
```

---

## 幻灯片 <section> 结构规范

```html
<!-- 封面页 -->
<section class="slide active" data-slide="0">
  <div class="reveal">主标题（h1, 超大字号）</div>
  <div class="reveal">副标题/日期/演讲者</div>
  <!-- IMG: 如需封面背景图 -->
</section>

<!-- 目录页 -->
<section class="slide" data-slide="1">
  <h2 class="reveal">目录</h2>
  <div class="reveal">01 — 章节名</div>
  <div class="reveal">02 — 章节名</div>
  <div class="reveal">03 — 章节名</div>
</section>

<!-- 内容页（演讲型，低密度） -->
<section class="slide" data-slide="2">
  <span class="reveal section-tag">01</span>
  <h2 class="reveal">核心观点</h2>
  <p class="reveal">15-40 字的精炼表达</p>
</section>

<!-- 内容页（阅读型，高密度） -->
<section class="slide" data-slide="3">
  <span class="reveal section-tag">02</span>
  <h2 class="reveal">展开论述</h2>
  <p class="reveal">段落正文，40-100 字</p>
  <ul class="reveal">
    <li>要点一</li>
    <li>要点二</li>
  </ul>
</section>

<!-- 总结页 -->
<section class="slide" data-slide="N-1">
  <h2 class="reveal">关键 Takeaways</h2>
  <div class="reveal">1. ...</div>
  <div class="reveal">2. ...</div>
</section>

<!-- 致谢/Q&A -->
<section class="slide" data-slide="N">
  <h2 class="reveal">Thank You</h2>
  <p class="reveal">联系方式 / Q&A</p>
</section>
```

---

## JS 功能清单

| 功能 | 实现方式 | 备注 |
|------|---------|------|
| 键盘翻页 | keydown 监听 ← → Space Shift+Space Home End | 阻止默认行为 |
| 全屏切换 | F 键 → `requestFullscreen()` | 需用户交互触发 |
| 滚轮翻页 | wheel 事件 + 800ms debounce | passive: true |
| 触屏滑动 | touchstart/touchend + 50px 阈值 | 支持横竖滑动 |
| 16:9 缩放 | resize 事件 → `transform: scale()` | `min(scaleX, scaleY)` |
| 进度条 | `width: (current+1)/total * 100%` | 底部 3px |
| 页码显示 | `01 / 10` 格式 | 右下角 |
| 已访问追踪 | MutationObserver + visited Set | 回访时动画跳过 |
| Reduced motion | `@media (prefers-reduced-motion: reduce)` | 关闭所有动画 |
