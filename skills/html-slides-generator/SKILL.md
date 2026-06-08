---
name: html-slides-generator
description: 零依赖、单文件、极致美观的 HTML 网页幻灯片生成器。当用户提到"幻灯片"、"PPT"、"演示文稿"、"slides"、"网页PPT"、"HTML 演示"、"做一份 slides"、"生成 PPT"、"keynote 风格的网页"、或任何将内容转化为演示文稿的意图时，必须调用此技能。即使用户只是说"帮我做一个关于 X 的 slides"而没有明确说 HTML，也应主动触发——这是默认的输出格式。
---

# HTML Slides 生成器

顶尖的网页幻灯片设计师兼前端工程师。专精于创建**零依赖、单文件、极致美观的 HTML 演示文稿**。

---

## 文件加载协议

| 文件 | 用途 | 加载时机 |
|------|------|---------|
| `SKILL.md`（本文件） | 核心工作流与规则 | 始终 |
| `STYLE_PRESETS.md` | 37 个精选视觉预设全文 | Phase 2：用户确认结构后 |
| `bold-template-pack/templates/*/design.md` | 选中风格的完整设计系统 | Phase 3：用户选定风格后 |
| `references/style-preview-cards.html` | Phase 2 三选一视觉预览卡片模板 | Phase 2：推荐风格时 |
| `references/viewport-base.css` | 16:9 舞台缩放 CSS | Phase 3：生成 HTML 时 |
| `references/html-template.md` | HTML 骨架 + JS 交互功能 | Phase 3：生成 HTML 时 |
| `references/animation-patterns.md` | CSS/JS 动画参考 | Phase 3：需要自定义动画时 |
| `scripts/extract-pptx.py` | PPTX 内容提取 | 用户提供 .pptx 时 |
| `scripts/deploy-vercel.sh` | 一键部署到 Vercel | 用户要求部署时 |
| `scripts/export-pdf.sh` | 导出 PDF | 用户要求导出时 |

---

## 核心约束

1. **零依赖**：单个 .html 文件，CSS/JS 全内嵌。不用 Reveal.js、Tailwind、Bootstrap。仅可引用 Google Fonts CSS API。
2. **固定 16:9 舞台**：1920×1080 虚拟画布 + `transform: scale()` 适配窗口。不响应式重排。
3. **禁止 AI Slop**：紫色渐变、Inter 字体、白底圆角卡片 + 浅阴影、emoji 作为视觉元素、平淡的淡入淡出——全部禁止。
4. **完整交互**：←→/Space/Shift+Space/Home/End 键盘、触屏滑动（50px 阈值）、鼠标滚轮（800ms debounce）、进度条、页码显示、`prefers-reduced-motion` 支持、F 键全屏。

---

## Phase 1：内容理解与结构规划

### Step 1.1 判断输入类型

- **用户直接提供文件**（.md / .doc / .pptx / .txt）：直接解析文件内容，进入 Step 1.2。
- **用户用自然语言描述主题**（"帮我做一个关于 X 的 slides"）：**先询问**用户是否有相关的文字资料、大纲、笔记或文档可以上传。如果有，等用户上传后再继续。如果没有，基于用户的口述内容继续。

### Step 1.2 理解内容
通读所有材料，抓住核心主题、论点、数据、故事线。

### Step 1.3 整理结构
将内容组织为 PPT 逻辑结构：
```
封面 → 目录/议程 → 内容页 ×N（每页 1-3 核心点）
→ 数据/视觉页 → 总结 → 致谢/Q&A
```

### Step 1.4 确认参数
若用户未明确，必须询问：
- **用途**：演讲辅助（低密度，每页 15-40 字）还是阅读型（高密度，每页 40-100 字）？
- **时长/页数**：预估页数？
- **风格偏好**：有品牌色吗？有厌恶的风格吗？
- **图片**：用户提供图片？

### Step 1.5 输出大纲并等待确认
用简洁的文本展示结构（每页标题 + 1-2 句要点），等待用户确认后再进入 Phase 2。如果用户说"直接出"或"不用确认"，则跳过确认直接进入 Phase 2。

---

## Phase 2：视觉风格推荐（文本 + 视觉预览卡）

### Step 2.1 读取预设库
读取 `STYLE_PRESETS.md`，了解全部 37 个可用视觉预设。

### Step 2.2 筛选 3 个候选
基于**内容主题和场景**，从 37 个预设中精选 **3 个最契合的**。选择原则：
- 分别来自暗色/亮色/暖色三个维度（让用户感受真正的设计广度）
- 覆盖不同排版哲学（衬线 vs 无衬线、极简 vs 装饰）
- 匹配内容的行业属性（科技→暗黑科技未来、学术→安静学术蓝金、创意→新 Brutalist，等等）

### Step 2.3 文本推荐格式
**只输出文字描述，不生成任何 HTML 代码**。每个推荐包含：

```
### 推荐 A：[风格名称]
**氛围**：一句话描述
**配色**：`bg` | `text` | `accent` — 简短色值
**字体**：Heading / Body
**为什么适合**：1 句话解释与该主题的契合点

### 推荐 B：[风格名称]
...

### 推荐 C：[风格名称]
...
```

### Step 2.4 告知预设总量
推荐末尾必须注明：
> 以上从内嵌的 37 个视觉预设中精选。不满意可以说"换一批"查看更多，或者直接描述你想要的风格（如"深色背景 + 金色衬线字体"），我为你定制。

### Step 2.5 风格兜底
- 用户说"换一批"→ 从剩余预设中再选 3 个，确保与上一批不重复。
- 用户描述自定义风格 → 跳过预设库，直接按描述生成设计系统。
- 用户说"都不满意，我要 XXX"→ 按 XXX 描述生成。

### Step 2.6 生成视觉预览卡 HTML

文本推荐完成后，**必须**生成一份视觉预览 HTML 文件，让用户可以直观对比三个风格的配色、字体与幻灯片实际呈现效果。

1. 读取 `references/style-preview-cards.html`，获取预览卡片模板结构。
2. 将三款推荐风格的参数填入模板（`{{STYLE_A/B/C_*}}` 占位符）。
3. 保存到输出目录下，文件名为 `<原文件名>.preview.html`（如 `proposal.preview.html`）。
4. 告知用户打开此文件查看三款风格的视觉预览。

**预览卡片数据来源**：
- 如果该风格在 `bold-template-pack/templates/<id>/` 下有 `design.md`，从中提取精确的配色、字体参数。
- 如果没有对应模板（仅存在于 `STYLE_PRESETS.md` 中），则根据预设描述自行构建参数。

**Google Fonts 加载**：合并三个风格所需的所有字体 URL，去除重复后写入 `{{GOOGLE_FONTS_IMPORT}}`。中文字体一律使用 `Noto Serif SC` 或 `Noto Sans SC`（无需从 Google Fonts 加载，系统自带）。

**微型预览区的设计原则**：
- 背景使用该风格的 `bg` 色
- 文字色使用该风格的 `text`/`ink` 色
- 标题字号 22px，正文字号 14px
- 展示该风格的 accent 线、accent 标签等签名元素
- 示例标题用中文（8-12 字），示例正文用中文（15-25 字），示例标签用 2-4 字中文

**仅生成预览 HTML 文件。不要在此阶段生成完整的幻灯片 HTML。**

---

## Phase 3：生成最终完整 PPT

用户选定风格后，进入生成。

### Step 3.1 读取设计系统
读取对应模板的 `design.md`（或根据用户自定义风格自行构建设计系统）。

### Step 3.2 读取技术参考
读取 `references/viewport-base.css` + `references/html-template.md`。如需特殊动画则读取 `references/animation-patterns.md`。

### Step 3.3 生成完整 HTML
输出**单个完整 .html 文件**（用 ```html 包裹）。

**设计系统一致性**：
- CSS 自定义属性集中管理（`--color-bg`、`--color-text`、`--color-accent`、`--font-heading` 等，写在 `#stage` 上）
- 同章节幻灯片有视觉延续（如相同的 accent bar 位置和颜色）

**动画规范**：
- 每页进入时元素逐个 reveal（stagger 60-100ms）
- 默认 `opacity + translateY(20px→0)`，0.6s cubic-bezier(0.16,1,0.3,1)
- `prefers-reduced-motion: reduce` → 瞬间完成

**内容密度参考**：
| 类型 | 标题字号 | 正文字号 | 每页字数 |
|------|---------|---------|---------|
| 演讲型 | 64-96px | 28-36px | 15-40 字 |
| 阅读型 | 48-72px | 22-30px | 40-100 字 |

### Step 3.4 交付说明
在 HTML 末尾以注释形式附上使用说明（翻页/全屏/导出 PDF/部署/修改配色）。

---

## 后续能力

### PowerPoint 转换
用户提供 `.pptx` → 运行 `python scripts/extract-pptx.py <file>` 提取文本+图片 → 用选定风格重新设计。

### 持续迭代
用户可要求修改（"第 3 页改两列"、"色调更暗"）→ 输出**完整新 HTML**（不输出 diff）。

### 部署与分享
- **Vercel**：`bash scripts/deploy-vercel.sh <file.html>`
- **PDF**：`bash scripts/export-pdf.sh <file.html>`
- **GitHub Pages**：推送 `index.html` 到 `gh-pages` 分支

---

## 代码质量标准

1. **CSS 变量集中**：所有颜色/字号/间距在 `#stage` 上定义
2. **语义化**：`<section class="slide">` 每页，`<h1>-<h3>` `<p>` `<ul>` 内容
3. **JS 健壮**：边界条件（首页不能后退、末页不能前进）、debounce 滚轮
4. **注释关键点**：`/* STYLE: 配色 */` `<!-- IMG: 占位 -->` 方便手动修改
5. **体积控制**：纯文本 ≤30KB，含图片 base64 ≤500KB
