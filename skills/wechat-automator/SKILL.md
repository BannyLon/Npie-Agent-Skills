---
name: wechat-automator
description: 一站式内容资产化引擎：默认对内容进行深度优化（契合公众号阅读场景），精排版渲染，一键上传草稿箱。当用户提到"推文"、"公众号"、"排版"、"发布"、"草稿"、或任何将内容转化为公众号图文的意图时，必须调用此技能。
version: 2.0.0
author: 嗯哌AI (NpieAI)
---

# 微信公众号内容资产化引擎 (WeChat Automator)

## 一句话定义

**把短期流量（视频/笔记/碎片资料），转化为长期内容复利（可搜索、可收藏、可反复阅读的图文资产）。**

---

## 触发条件 (Trigger Rules)

以下任一条件满足时，**必须**激活此技能：

1. **关键词触发**：用户消息包含以下任一关键词组合：
   - 「推文」「公众号」「排版」「发布」「草稿」「群发」「图文」
   - 「wechat」「weixin」「mp.weixin」
   - 「视频脚本」+「转/整理/发/变成」→公众号意涵
   - 「笔记」+「排版/发布/推文」
2. **文件引用触发**：用户引用了 `.md` / `.writings.md` / `.txt` 文件，并提到「发」「传」「推送」「转成图文」等动作词。
3. **路径指令触发**：
   - `wechat-automator:full(file_path)` — 完整链路：输入→草稿箱
   - `wechat-automator:format(file_path)` — 仅排版预览，不上传
   - `wechat-automator:upload_cover(path)` — 仅上传封面图
4. **上下文推断触发**：刚完成 oral-stylizer 处理，用户自然过渡到排版发布。

**🔴 强制规则：一旦触发，必须用 `Skill` 工具加载本 skill，并严格按照 skill 内定义的五阶段流水线执行。严禁绕过 skill 自行编写脚本、手写 HTML、或直接用 `requests` 调 API。**

**反触发**：纯技术咨询（「公众号 API 怎么调」）不激活，用通用知识回答。

---

## 默认行为与内容优化豁免

### 核心原则：默认深度优化，显式声明豁免

**默认行为**：对用户提供的任何内容，自动执行阶段 ①②（内容脱水 + 结构重组），使内容契合微信公众号读者的阅读习惯——包括但不限于：重构开头钩子、调整段落节奏、优化小标题、强化结尾 CTA。

**豁免规则**：仅当用户消息中**明确包含**以下任一关键词组合时，才跳过阶段 ①② 的内容修改，严格保留原文：

| 豁免关键词 | 示例 |
|-----------|------|
| 「不要修改内容」「不做任何修改」「不要改动」 | 「排版发公众号，**不要改动**原文任何一个字」 |
| 「严格按原文」「原封不动」「一字不改」 | 「**严格按原文**排版，发布到草稿箱」 |
| 「不增不减」「保留原文」「直接排版」 | 「**不增不减**，直接排版」 |
| 「仅排版」「只排版」「纯排版」 | 「**仅排版**，不需优化内容」 |

**注意**：豁免的是阶段 ①② 的**内容改写**，阶段 ③④ 的视觉增强和排版渲染始终执行。即使用户要求「不修改内容」，仍然要执行：卡片化、金句模块提取、数据可视化、配色排版。

### 判断流程

```
用户请求 → 引用的文件是 .html？
  ├─ 是 → 兼容性扫描：有 <style>？有 <div>？有 class？
  │        ├─ 全部干净 → 直达 ⑤ 上传（跳过 ①②③④）
  │        └─ 有问题   → 告知用户问题数量，询问是否自动修复后再上传
  └─ 否 → 检查是否包含豁免关键词？
           ├─ 是 → 跳过 ①②，进入 ③ 视觉增强 → ④ 排版渲染 → ⑤ 上传
           └─ 否 → 执行阶段 ①② → 🔴 暂停，输出预览给用户确认
                     ├─ 用户确认 → 继续 ③ 视觉增强 → ④ 排版渲染 → ⑤ 上传
                     └─ 用户要求修改 → 修改后再次预览，直到确认
```

**🔴 阶段 ①② 确认门禁（强制）**：执行完内容脱水 + 结构重组后，**必须暂停**，将优化后的 Markdown 内容输出给用户预览，等待用户明确确认（「确认」「可以」「继续」等）后，才能继续执行阶段 ③④⑤。禁止跳过此门禁直接完成全流程。

**HTML 兼容性扫描标准**（干净 HTML 的定义）：
- 无 `<style>` 标签
- 无 `class` 属性
- 无 `<div>` 元素
- 无可检测的 `linear-gradient`

四条全部满足 → 直达 ⑤。任一不满足 → 告知用户「这个 HTML 有 X 个 div / Y 个 style 标签，微信会丢格式，要我先修复吗？」

---

## 工作流总览（v2.0）

```
三阶段管线：
┌──────────┐    ┌──────────────────────────────────────┐    ┌──────────┐
│ ⓪ 内容优化 │ → │ ① 排版渲染                                 │ → │ ② 一键发布 │
│ 脱水+去AI │    │ 预处理→类型判定→推荐+预览→结构+渲染          │    │ 草稿箱    │
│ 🔴暂停确认 │    │ 🔴暂停确认类型  🔴暂停选择排版             │    │ 自动完成  │
└──────────┘    └──────────────────────────────────────┘    └──────────┘

详细流程：
  输入内容
    ↓
  ⓪.1 内容脱水（去冗余/提论点/压密度）
  ⓪.2 结构重组（钩子开头+正文骨架+CTA结尾）
  ⓪.3 去AI味（humanizer-zh 审阅）
    ↓
  🔴 暂停 → 输出优化后内容 → 等待用户确认
    ↓
  ①.0 智能预处理（章节编号+英文标签+关键词识别+目录提取+引言高亮+署名+签名占位）
    ↓
  ①.1 🔴 文章类型判定 → 列出 7 种类型 → 暂停，等用户确认（可覆盖）
    ↓
  ①.2 🔴 排版推荐 + 12 套预览 → 暂停，等用户选择排版方案
    ↓
  ①.3 生成 class-based HTML（融入预处理 + 选定布局专属结构 + v2.0 组件配方）
  ①.4 build_inline.py --theme <选定> → inline HTML + <span leaf=""> 包裹 + validate 校验
    ↓
  ② upload.py → 上传头图+封面 → 创建草稿
    ↓
  ✅ 草稿 media_id → 用户去后台预览群发
```

### 确认门禁（三处强制暂停）

| # | 位置 | 等什么 | 用户可回复 |
|---|------|--------|-----------|
| 🔴 1 | 阶段⓪ 结束 | 确认优化后的内容 | 「确认」/ 修改意见 |
| 🔴 2 | 阶段①.1 结束 | **确认文章类型**（AI 判定 + 列出全部 7 种供选） | 「确认」/ 类型名 / 序号 |
| 🔴 3 | 阶段①.2 结束 | **选择排版方案**（12 套预览对比） | 预设名 / 自由组合 / 自定义色 / 「用推荐的」 |

> ⚠️ **①.1 和 ①.2 不可合并。** 必须先确认类型，再基于类型推荐排版。跳过类型确认直接推荐 = 跳步。

### 豁免规则

- 用户说「不要修改内容」「一字不改」「仅排版」→ 跳过 ⓪，直接进入 ①
- 用户引用的文件是干净 HTML → 跳过 ⓪①，直达 ②

---

## 排版设计哲学（v1.8.0）

> 本节是阶段① 所有排版决策的理论基础。

### 三层视觉层级体系

公众号文章是**扫描式阅读**——读者不会逐字读，而是用眼睛扫。好的排版为读者建立一条视觉动线：先看什么、再看什么、略过什么。

| 层级 | 作用 | 频率 | 手段（按所选主题色自适应） |
|------|------|------|------|
| **锚点层** 🔴 | 最强锚点：产品名/步骤/CTA/核心金句，读者扫到的第一眼 | 全文 ≤ 5 处 | `.anchor-bold` 主色加粗、`.anchor-block` 深色底白字、`.golden-quote` 金句模块 |
| **标记层** 🟡 | 正文关键词下划线，让读者快速抓取每段重点 | 每段 1-3 处，高频 | `.kw-underline` 主题色底划线（**默认标记手段**）、`.highlight-marker` 荧光笔（偶尔长句） |
| **容器层** ⚪ | 引用块、概念标签、提示框、卡片——结构化信息块 | 按需，点缀 ≤3 种/篇 | `blockquote` 引用、`.highlight-box` 强调块、`.tip-box`/`.warn-box` 提示框、`.card-item` 卡片 |

### 克制原则

1. **锚点不滥用**：到处加粗等于没有重点。红/蓝/绿加粗只在全文 ≤5 处最关键的位置
2. **标记不遗漏**：每段正文必须主动标记 1-3 个关键词（4-15 字短语），即使原文没有任何加粗也要主动加下划线——这是本 skill 的**核心特色**，也是最高频的标记手段
3. **容器不混搭**：一篇只用所选布局的组件，不跨布局借组件；点缀组件种类 ≤3
4. **下划线是主角**：`.kw-underline` 是全文出现最多的样式，比加粗更轻、比无色更突出，是扫描阅读的最佳标记
5. **颜色克制**：主色用于锚点层和标记层的关键位置，正文大面积保持中性灰；对比色/警告色只在需要读者停顿的地方出现

### 智能主动标记（AI 做的事，不等用户写标记）

不等用户在 Markdown 里写好 `**加粗**` 和 `==高亮==`，AI 主动分析内容，替读者标记重点。 阶段① 执行时，AI 必须完成以下 7 项智能处理：

1. **章节自动编号**：按 `##` 出现顺序分配 01/02/03…，末章若为结语/总结类用 `∞`
2. **英文标签生成**：据中文章节标题生成英文标签（教程→TUTORIAL、总结→SUMMARY、思考→THOUGHTS…）
3. **正文关键词下划线**：对**每个正文段落**主动找出 1-3 个最重要的短语标记 `.kw-underline`
4. **引言金句高亮**：识别开头引言中的核心词，用 `.intro-highlight` 或 `.anchor-block` 标记
5. **目录/看点提取**：从所有 `##` 取前 3 个作为导读要点
6. **引言卡署名**：按文章作者/主题确定，未知则省略不写
7. **尾部签名区占位**：默认 `{{作者名}}` / `{{简介}}`，用户提供则填入

### 文章类型 → 组件配方

先判定文章类型，再按类型选择排版系统。同类文章用同一套组件组合，保证排版气质稳定。

| 文章类型 | 判据 | 推荐排版系统 | 核心组件 | 点缀组件 |
|---------|------|------------|---------|---------|
| 教程/操作指南 | 步骤、命令、配置词多 | `forest` 手册流 / `amber` 极客流 | `.step-block` + 代码块 + `.ordered-list` | `.tip-box` / `.warn-box` |
| 盘点/工具清单 | 并列条目、推荐、工具词多 | `plum` 卡片流 / `teal` 经典左线 | `.card-item` + `.tool-badge` + 胶囊列表 | 表格 / 数据卡 |
| 观点/深度分析 | 分析、逻辑、判断词多 | `navy` 杂志流 / `teal` 经典左线 | 正文段 + `.golden-quote` + `.highlight-box` | `.kw-underline` 高频 / 居中金句 |
| 访谈/人物特稿 | 采访、引语、人物叙事多 | `navy` 杂志流 / `slate` 书信流 | 正文段 + blockquote 引语 + timeline | `.golden-quote` / 居中金句 |
| 数据复盘/报告 | 数字、统计、对比词多 | `navy` 杂志流 / `teal` 经典左线 | 数据卡 + 表格 + `.ordered-list` | `.anchor-bold` 关键数字 |
| 生活/情感随笔 | 我、感觉、日常词多 | `slate` 书信流 / `plum` 卡片流 | 正文段 + 居中金句 + 轻量引用 | `.kw-underline` 少量 |
| 案例实战 | 案例、项目、踩坑词多 | `amber` 极客流 / `forest` 手册流 | case-label + `.step-block` | `.warn-box` / `.prompt-card` |

---

## 阶段 ⓪：内容优化（Content Optimization）

**目标**：输入内容 → 深度优化 → 去 AI 味 → 用户确认。

### ⓪.1 内容脱水

1. **去冗余**：删除重复论述、口语填充句
2. **提论点**：每段提炼 1 句可独立传播的核心观点
3. **压密度**：信息密度提升 30-50%
4. **保人味**：保留作者标志性表达（Banny 的「Vibe Coding」「Agentic Workflow」等）

### ⓪.2 结构重组

- **钩子开头**：提取最反直觉的 1 句话前置，或用 2-3 句制造信息落差
- **正文架构**：根据内容类型选择骨架（教程→问题原理步骤/观点→现象分析本质/案例→背景决策方法论/清单→总览逐条展开）
- **H2 控制**：3-5 个板块，标题要具体（「问题是什么」而非「关于 XX 的讨论」）
- **CTA 结尾**：给读者一个具体的下一步

### ⓪.3 去 AI 味

调用 `humanizer-zh` 审阅优化后的全文，去除 AI 写作特征（夸大的象征意义、宣传性语言、三段式法则、AI 词汇等）。

### ⓪.4 确认输出

**🔴 必须暂停**。将优化后的 Markdown 内容输出给用户预览，等待明确确认后才能继续。

---

## 阶段 ①：排版渲染（Layout & Rendering）v2.0

**目标**：智能预处理 → 🔴 文章类型判定确认 → 🔴 排版推荐+预览+选择 → 生成 HTML → 渲染。

```
①.0 智能预处理（AI 强制执行）
  ↓
①.1 文章类型判定 → 🔴 暂停：用户确认类型（可覆盖）
  ↓
①.2 排版系统推荐 + 生成预览网页 → 🔴 暂停：用户选择排版方案
  ↓
①.3 生成 class-based HTML（融入预处理 + 选定布局的专属结构 + 组件配方）
  ↓
①.4 build_inline.py 渲染 → validate 校验
```

> ⚠️ **关键顺序铁律**：必须先确认文章类型，再推荐排版系统。类型决定推荐方向，跳过类型确认直接推荐 = 跳步，禁止。

### ①.0 智能预处理（v1.8.0 🔴 AI 强制执行）

**在生成任何 HTML 之前**，AI 必须对优化后的 Markdown 执行以下 7 项智能处理。核心理念：不等用户写标记，AI 主动替读者做信息导航。

#### ①.0.1 章节自动编号

按 `##` 出现顺序分配：`01` `02` `03` …。末章若标题含「总结/结语/写在最后/尾声」等词，编号用 `∞`，PART 改为 `LAST`。

- 编号不与原文标题冲突，作为章节视觉锚点
- 中间章节不跳号、不用 `∞`

#### ①.0.2 英文标签生成

为每个 `##` 章节生成英文副标签（`.chapter-en` 类），用于章节标题区的装饰：

| 中文关键词 | 英文标签 | 中文关键词 | 英文标签 |
|-----------|---------|-----------|---------|
| 教程/步骤/操作/实战/指南 | TUTORIAL | 盘点/清单/工具/推荐 | TOOLS |
| 分析/观点/评论/深度/解读 | ANALYSIS | 案例/复盘/项目/经验 | CASE STUDY |
| 总结/结语/写在最后/尾声 | EPILOGUE | 思考/反思/感悟 | THOUGHTS |
| 问题/挑战/困境/难点 | PROBLEM | 方法/方案/策略/框架 | METHOD |
| 背景/现状/趋势/格局 | CONTEXT | 数据/指标/统计 | DATA |
| 原理/机制/本质/底层 | PRINCIPLE | 展望/未来/预测 | OUTLOOK |

无明确对应时，取章节核心名词的英文翻译（≤12 字符）。

#### ①.0.3 正文关键词下划线 🔴 核心特色

对**每个正文段落**（`<p>` 元素），AI 主动识别 1-3 个最重要的短语（4-15 字），用 `.kw-underline` 类标记。

- **优先标**：核心观点、结论判断、关键数据、专有名词、产品名
- **不标**：过渡句、废话、整段内容
- **整段无要点时可跳过**
- **即使原文没有任何 `**加粗**` 标记，也要主动加下划线**——这是本 skill 出现频率最高的标记

#### ①.0.4 引言金句高亮

识别文章开头引言（`> 引用` 块或首段金句）中的核心关键词，用 `.intro-highlight`（主色底白字）或 `.anchor-bold`（主色加粗）标记。引言卡中最多 2 处高亮。

#### ①.0.5 目录/看点提取

从所有 `##` 章节标题中精选 **前 3 个**作为导读看点（非完整章节目录），生成 `.toc-card` 容器。章节多于 3 个时挑最重要的 3 个，不要硬塞。

#### ①.0.6 引言卡署名

按文章实际作者或主题确定引言卡署名：
- 文章有明确作者 → 写「—— 作者名」
- 无明确作者但主题明确 → 可用与主题相关的简短落款
- 完全未知 → 省略署名行，不留空

**不要固定写任何默认人名。**

#### ①.0.7 尾部签名区占位

在文末 CTA 之前生成签名段落，**默认用占位符**，让用户替换成自己的署名：

- 用户在请求/偏好里给了署名或简介 → 直接填入
- 没给 → 保留 `{{作者名}}` / `{{一句话简介}}` 占位，交付时提示用户替换
- 原文末尾已有作者签名段 → 直接沿用原文，不替换成占位
- **签名区有且仅有末尾一处**

---

### ①.1 🔴 第一步：文章类型判定（先确认类型，不推荐排版）

> ⚠️ **这一步只做类型判定，不推荐排版系统。排版推荐在 ①.2 用户确认类型之后。**

1. 阅读优化后的文章，理解内容类型、情感基调、目标读者
2. 调用 `detect_content_type()` 判定文章类型
3. **列出全部 7 种类型供用户选择**，标注 AI 判定的推荐项：

```
📝 AI 判定文章类型：**{类型名}**（置信度：{高/中/低}）

你也可以选择其他类型（不同类型的推荐结果不同）：

| 序号 | 文章类型 | 适合场景 |
|------|---------|---------|
| 1 | 生活/情感随笔 ⭐ 推荐 | 读书感悟、个人叙事、情感表达 |
| 2 | 观点/深度分析 | 论证推演、逻辑分析、评论 |
| 3 | 访谈/人物特稿 | 引语多、人物叙事多 |
| 4 | 案例实战 | 项目复盘、踩坑经验 |
| 5 | 盘点/工具清单 | 并列条目、推荐合集 |
| 6 | 教程/操作指南 | 步骤、命令、操作流程 |
| 7 | 数据复盘/报告 | 数字统计、对比分析 |
```

**🔴 必须暂停等待用户确认**。用户可回复：
- 「确认」/「用推荐的」→ 使用 AI 判定类型
- 序号或类型名 → 更换为用户指定的类型
- 自定义描述 → 按用户描述调整

**用户确认类型后，才进入 ①.2。**

---

### ①.2 🔴 第二步：排版系统推荐 + 预览对比

> ⚠️ **用户确认文章类型后执行。** AI 先生成一个临时 class-based HTML（用于文本提取，任意布局即可），然后运行 preview_themes.py。

1. 调用 `recommend()` 做关键词匹配 + 文章类型加权，得出 12 套预设的分数排名
2. 向用户说明推荐结果：

```
📊 排版系统推荐（基于类型：{类型名}）：

| 排名 | 预设 | 布局 × 配色 | 得分 | 来源 |
|------|------|------------|------|------|
| ⭐ 1 | slate 岩灰书信 | 书信流 × 岩灰玫瑰 | 20 分 | 原有 |
| 2 | ruby 红白编辑 | 红白编辑 × 红白配色 | 7 分 | v2.0 新增 |
| ...
```

3. 生成临时 class HTML → 运行 `preview_themes.py` 生成预览页：

```bash
python3 scripts/preview_themes.py output/article-class-html.html --open
```

**v2.0 预览页特性**：
- 12 套布局 × 各自专属 HTML 结构样本（不是同一段 HTML 换皮肤）
- 四栏 grid 布局，响应式（>1200px 四栏 → >900px 三栏 → >560px 两栏 → 手机一栏）
- 每张卡片标注：📐 布局名 + 🎨 配色名 + 🏷️ 适用文章类型
- 推荐项 ⭐ 金色边框高亮
- 每张卡片展示该布局的专属组件（封面卡/流程卡/时间线/END 分割线/引言卡等）

**🔴 必须暂停等待用户选择**。用户可回复：
- 预设名：`slate` `ruby` `zen` `moyu` `olive` `ticket` `graph` `teal` `navy` `forest` `plum` `amber`
- 自由组合：`zen:slate-rose` `moyu:emerald`（布局:配色）
- 自定义颜色：`#e63946`（默认 classic 布局，自动推导配色）
- 「用推荐的」→ 分数最高项

---

### ①.3 生成 class-based HTML（融入智能预处理 + 选定布局专属结构）

**在运行 build_inline.py 之前**，AI 用选定布局的专属结构生成 class-based HTML。必须满足：

1. **结构骨架**：使用选定布局的专属 HTML 模板（参见 4.3 章节「各布局推荐组件配方」表）
2. **章节**：`.chapter-num` / `.chapter-num-final` 编号 + `.chapter-en` 英文标签
3. **正文**：每段 `.kw-underline` 标记 1-3 个关键词
4. **锚点**：`.anchor-bold` 或 `.anchor-block` 全文 ≤5 处
5. **引言**：`.intro-highlight` 高亮核心词（如有引言卡）
6. **目录**：`.toc-card` + `.toc-num` + `.toc-item`（≥3 章节时）
7. **签名**：末尾 `.sig-placeholder` 占位（或用户提供的署名）
8. **容器组件**：按「各布局推荐组件配方」表使用，点缀 ≤3 种
9. **通用组件**（v2.0）：`.tag-step`/`.tag-case`/`.tag-skill` 内容标签、`.flow-row` 流程卡、`.tl-row` 时间线、`.end-divider` END 分割线、`.cover-card` 封面卡、`.info-note` 信息旁注等——按需选用
10. **头图**：class-based HTML 中**不写头图 `<img>`**（由 upload.py 自动注入）

### ①.4 渲染

```bash
python3 scripts/build_inline.py output/article-class-html.html output/article-inline.html --theme <选定>
```

`build_inline.py` 自动完成：
- class → inline style 转换
- `<span leaf="">` 包裹所有文本节点（v1.9.0）
- `validate_output()` 强制校验

### ①.5 排版质量检查（v2.0 更新）

- [ ] 全文无 `<style>`、`class=`、`<div>`、`linear-gradient`、`letter-spacing`
- [ ] **🔴 全文文本已由 `build_inline.py` 自动包裹 `<span leaf="">`（v1.9.0 自动执行，`validate_output` 强制校验，不可跳过）**
- [ ] 正文行高 ≥ 1.8，字号 ≥ 15px
- [ ] **🔴 每段正文含 1-3 个 `.kw-underline` 关键词下划线**
- [ ] **🔴 章节编号连续（01/02/03…∞），不跳号**
- [ ] **🔴 `.anchor-bold` / `.anchor-block` 全文 ≤ 5 处**
- [ ] H2 视觉层级正确，英文标签已生成
- [ ] 关键观点用金句/强调模块包裹
- [ ] CTA 后有底部留白（≥32px）
- [ ] 颜色来自配色色板，全文主色一致
- [ ] **🔴 签名区仅末尾一处，默认占位或用户提供**
- [ ] 头图位和配图位已标记（由 upload.py 阶段②自动注入）
- [ ] v2.0 通用组件按布局配方使用，点缀种类 ≤3

---

## 微信排版技术规范（Typography & Rendering Reference）

**目标**：无论选择哪套排版系统，最终输出都遵循以下技术规范。

### 4.1 🔴 微信 CSS 核心规则：禁止 `<style>` + 禁止 `<div>`

**两项关键发现**（基于生产环境实测验证）：

| 规则 | 后果 | 解决方案 |
|------|------|---------|
| `<style>` 标签 | ❌ 微信**完全删除** | 所有样式写入 `style=""` 内联属性 |
| `class` 属性 | ❌ 微信**完全剥离** | 不依赖 class 选择器 |
| `<div>` 元素 | ❌ 微信**全部转为裸 `<p>`**，丢失所有样式 | **零 div**：用 `<section>`/`<p>`/`<blockquote>`/`<table>` 替代 |
| `linear-gradient` | ❌ 微信删除 | 用纯色 `background-color` 替代 |

**唯一可靠的样式方式：`style=""` 内联属性 + 零 div + 语义化 HTML 元素。**

### 4.2 微信排版硬约束

- ❌ 禁止 `<style>` 标签（微信直接删除）
- ❌ 禁止 `<div>` 元素（微信转为裸 `<p>`，样式全部丢失）
- ❌ 禁止 `class` 属性（微信直接删除）
- ❌ 禁止外部 CSS 文件、外部字体、JavaScript
- ❌ 禁止 `position: fixed/absolute/sticky`
- ❌ 禁止 `flex` 和 `grid` 布局（微信会剥离）
- ❌ 禁止 `linear-gradient`（微信会删除，改用纯色 `background-color`）
- ❌ 禁止 `<iframe>`、`<form>`、`<input>`
- ⚠️ **`<blockquote>` 有隐性 300 字限制**：微信编辑器对单次引用内容超过 300 字会自动插入「引用字数:XX/300」警告。超过 300 字的引用内容（如 Prompt 全文、长文摘录等）必须改用 `<section>` + `border-left` 样式替代
- ✅ **所有样式写在每个元素的 `style=""` 属性中**
- ✅ **用语义元素替代 div**：`<section>` 做容器、`<blockquote>` 做强调块（≤300字）、`<section>` + 左边框做超长引用（>300字）、`<table>` 做数据对比、`<p>` 做卡片
- ✅ 布局基于 `block`/`inline-block`/`table` + `margin`/`padding`
- ✅ 背景色使用纯色（`background-color`），禁用渐变
- ✅ 图片 src 必须是微信 CDN URL（`mmbiz.qpic.cn` 域名）
- ✅ 容器最大宽度 `677px`

**Div → 语义元素映射表（关键！所有 `<div>` 必须转换）：**

| 原始 div 用途 | 替换元素 | 示例 |
|-------------|---------|------|
| 页面容器 | `<section style="...">` | `<section style="margin:0;padding:0 16px 0;...">` |
| 元信息标签 | `<span style="display:inline-block;...">` 包在 `<p>` 中 | `<p style="text-align:center;"><span style="...">深度解析</span></p>` |
| 开篇大数字 | `<p>` + `<strong>` | `<p style="text-align:center;"><strong style="font-size:56px;">9,500 ★</strong></p>` |
| 金句模块 | `<blockquote style="...">`（不设左边框） | `<blockquote style="background-color:#d4edf5;border-radius:12px;text-align:center;">` |
| 强调模块 | `<blockquote style="...">`（带完整边框） | `<blockquote style="background-color:#f7fafc;border:1px solid #e0e7ef;">` |
| 卡片列表 wrapper | 直接删除，子项用 `<p>` | |
| 卡片项 | `<p style="...">`（带背景+边框+圆角） | `<p style="background-color:#fafbfc;border:1px solid #e8ecf1;border-radius:8px;">` |
| 数据双栏 | `<table>` + `<td style="width:50%">` | |
| CTA 底部 | `<blockquote style="...">`（不设左边框） | `<blockquote style="margin-top:44px;background-color:#d4edf5;border-radius:14px;">` |
| 编辑注记 | `<p style="...">`（左侧灰色细线） | `<p style="border-left:2px solid #dce3ea;color:#8a9aaa;font-style:italic;">` |
| 超长引用（>300字） | `<section style="...">`（左边框 + 略小字号，视觉等效 blockquote 但不触发微信 300 字限制） | `<section style="border-left:3px solid #0d7377;margin:16px 0;padding:4px 0 4px 18px;"><p style="font-size:14px;color:#4a5a6a;">...</p></section>` |

### 4.3 6 套异构排版系统（v1.8.0）

每套排版系统拥有**独立的组件库、HTML 结构和视觉语言**，不是同一骨架换 CSS。

#### 排版系统一览

| 系统 | 设计理念 | H2 特征 | 独有组件 | 适用文章类型 |
|------|---------|---------|---------|------------|
| `classic` 经典左线 | 左粗线分区，结构清晰 | 左蓝条+浅底 | `.golden-quote` `.card-item` `.highlight-box` | 观点分析、工具盘点 |
| `cardflow` 卡片流 | 每段独立成卡，模块化 | 深色顶栏（卡片标题） | `.section-card` `.info-card` `.data-badge` | 产品介绍、工具清单 |
| `editorial` 杂志流 | 大标题+引题+戏剧化引用 | 居中+上下装饰线 | `.lead` `.ornament-divider` `.image-frame` | 商业评论、人物访谈 |
| `guide` 手册流 | 步骤编号+提示框+对比 | 最大号无装饰 | `.step-num` `.tip-box` `.warn-box` | 教程指南、案例实战 |
| `letter` 书信流 | 日期+问候+署名，极简 | 只比正文略大 | `.dateline` `.greeting` `.sign-off` `.postscript` | 个人随笔、生活感悟 |
| `workshop` 极客流 | 深色实验台+Prompt卡+工具徽章 | 深底白字，等宽感 | `.prompt-card` `.tool-badge` `.workflow-step` | 技术编程、AI 实战 |
| `moyu` 摸鱼杂志 | 翠绿卡片+黄色高亮+虚线引用 | 大号绿字+深色标题 | `.cover-card` `.pill-capsule` `.flow-row` | 教程测评、工具盘点 |
| `red-editorial` 红白编辑 | 正红点睛+克制白底+戏剧引言卡 | 红底编号+底部红色实线 | `.intro-card` `.intro-quote-mark` `.end-divider` | 观点分析、读书感悟 |
| `graphite` 素砚 | 全灰阶+1px细线，极致克制 | 无底色大留白 | `.golden-quote`（上下细线） `.highlight-box` | 设计评论、科技观点 |
| `zen` 虚白 | 虚室生白+大呼吸感，极简 | 衬线体+64px 章间距 | `.golden-quote`（无线框） `.card-item`（底部分割线） | 深度随笔、读书笔记 |
| `ticket` 票根 | 票据隐喻+硬阴影+撕票虚线 | 虚线上下边框 | `.golden-quote`（硬阴影） `.card-item`（硬阴影） | 工具对比、创意测评 |
| `olive` 墨帖 | 墨色深底+暖橙点睛，编辑质感 | 深色底栏+6px 小圆角 | `.golden-quote`（橙左边条） `.tl-row` `.highlight-box` | 案例复盘、深度评测 |

#### 12 套预设主题组合（v2.0）

| 预设名 | 布局 | 配色 | 适用内容 | 适用文章类型 |
|--------|------|------|---------|------------|
| `teal` | classic 经典左线 | teal-gold 青蓝金 | 通用深度分析 | `opinion` `list` `tutorial` |
| `navy` | editorial 杂志流 | navy-coral 深蓝珊瑚 | 商业/行业评论 | `opinion` `interview` `data` |
| `forest` | guide 手册流 | forest-amber 森语琥珀 | 教程/操作指南 | `tutorial` `case` |
| `plum` | cardflow 卡片流 | plum-sage 梅紫灰绿 | 产品/工具介绍 | `list` `personal` `case` |
| `slate` | letter 书信流 | slate-rose 岩灰玫瑰 | 个人随笔/故事 | `personal` `interview` |
| `amber` | workshop 极客流 | forest-amber 森语琥珀 | 技术/AI/编程 | `tutorial` `case` `list` |
| `moyu` | moyu 摸鱼杂志 | emerald 摸鱼绿 | 教程测评/工具盘点 | `tutorial` `list` `case` `opinion` |
| `ruby` | red-editorial 红白编辑 | crimson 红白编辑 | 观点分析/读书感悟 | `opinion` `personal` `interview` |
| `graph` | graphite 素砚 | graphite 素砚 | 设计/科技/高端品牌 | `opinion` `data` `case` |
| `zen` | zen 虚白 | zen 虚白 | 深度随笔/读书笔记 | `personal` `opinion` `interview` |
| `ticket` | ticket 票根 | ticket 票根 | 工具对比/创意测评 | `list` `case` `tutorial` |
| `olive` | olive 墨帖 | olive 墨帖 | 案例复盘/深度评测 | `case` `opinion` `tutorial` |

#### 🆕 v1.8.0 智能标记 CSS 类（全布局通用）

以下新增类在所有 6 套布局中可用，由 AI 在阶段①.0 智能预处理时主动标记，build_inline.py 自动转换为 inline style：

| CSS 类 | 层级 | 用途 | 频率 |
|--------|------|------|------|
| `.kw-underline` | 🟡 标记层 | 主题色下划线——关键词标记的**默认手段** | 每段 1-3 处 |
| `.kw-underline-warn` | 🟡 标记层 | 对比色下划线——对比/否定专用 | 偶尔 |
| `.highlight-marker` | 🟡 标记层 | 荧光笔效果——偶尔长句强调 | 偶尔 |
| `.anchor-bold` | 🔴 锚点层 | 主色加粗——最强强调 | 全文 ≤5 处 |
| `.anchor-block` | 🔴 锚点层 | 主色底白字标签——视觉锚点 | 全文 ≤3 处 |
| `.intro-highlight` | 🔴 锚点层 | 引言核心词高亮——开场焦点 | 引言内 ≤2 处 |
| `.chapter-num` | ⚪ 结构层 | 章节大号编号（01/02…） | 每章 1 处 |
| `.chapter-num-final` | ⚪ 结构层 | 结语编号变体（∞） | 末章 1 处 |
| `.chapter-en` | ⚪ 结构层 | 英文章节副标签 | 每章 1 处 |
| `.toc-card` / `.toc-num` / `.toc-item` | ⚪ 容器层 | 目录/看点卡片 | ≥3 章时 1 组 |
| `.sig-placeholder` | ⚪ 结构层 | 签名区占位 | 文末 1 处 |

#### 🆕 v2.0 通用组件库（跨布局可用）

| CSS 类 | 类别 | 用途 | 适用布局 |
|--------|------|------|---------|
| `.tag-step` `.tag-case` `.tag-skill` | 内容标签 | STEP/CASE/SKILL 编号标签 | guide, moyu, olive, workshop |
| `.flow-row` `.flow-active` `.flow-inactive` `.flow-arrow` | 流程卡片 | 3 步横排流程展示 | moyu, guide, workshop |
| `.tl-row` `.tl-dot-circle` `.tl-dot-line` `.tl-body` | 时间线 | 递进/经历脉络 | olive, editorial, red-editorial |
| `.end-divider` `.end-line-l` `.end-line-r` `.end-label` | END 分割 | 章节结束标记 | red-editorial, editorial, letter |
| `.pill-capsule` | 胶囊列表 | 行内圆角标签 | moyu, classic, cardflow |
| `.cover-card` `.cover-tag` `.cover-title` `.cover-subtitle` | 封面卡 | 文章开篇封面 | moyu, red-editorial, olive |
| `.info-note` | 信息旁注 | 左竖条提示/名词解释 | red-editorial, classic, editorial |
| `.cta-triple` `.cta-action` `.cta-icon-box` | CTA 三连 | 点赞/在看/转发三连区 | 所有布局（文末） |

#### 各布局推荐组件配方

| 布局 | 常用组件 | 点缀组件 |
|------|---------|---------|
| classic 经典左线 | `.golden-quote` `.highlight-box` `.card-item` | `.info-note` `.pill-capsule` |
| cardflow 卡片流 | `.section-card` `.info-card` `.data-badge` | `.golden-quote` |
| editorial 杂志流 | `.lead` `.golden-quote` `.ornament-divider` | `.end-divider` `.tl-row` |
| guide 手册流 | `.step-block` `.tip-box` `.warn-box` | `.tag-step` `.flow-row` |
| letter 书信流 | `.dateline` `.greeting` `.sign-off` | `.end-divider` |
| workshop 极客流 | `.prompt-card` `.tool-badge` `.workflow-step` | `.tag-skill` `.flow-row` |
| moyu 摸鱼杂志 | `.cover-card` `.golden-quote` `.card-item` | `.flow-row` `.pill-capsule` `.tag-step` |
| red-editorial 红白编辑 | `.intro-card` `.golden-quote` `.end-divider` | `.info-note` `.tl-row` |
| graphite 素砚 | `.golden-quote` `.highlight-box` | `.cover-card` |
| zen 虚白 | `.golden-quote`（无线框居中） `.card-item`（底部分割线） | 几乎不加装饰 |
| ticket 票根 | `.golden-quote`（硬阴影） `.card-item`（硬阴影） | `.cover-card` `.meta-tag` |
| olive 墨帖 | `.golden-quote`（橙左边条） `.highlight-box` | `.tl-row` `.tag-skill` `.info-note` |

#### 使用方式

```bash
# 预设组合
python3 scripts/build_inline.py in.html out.html --theme navy

# 显式指定布局和配色
python3 scripts/build_inline.py in.html out.html --layout workshop --palette teal-gold

# 自定义主色（默认 classic 布局，自动推导配色）
python3 scripts/build_inline.py in.html out.html --theme "#e63946"
```

---

### 4.3.5 主题推荐与可视化预览（v1.8.0）🔴 强制交互节点

在运行 `build_inline.py` 之前，**必须**执行以下交互流程：

#### 步骤 A：文章类型判定 + 自动推荐

调用 `detect_content_type(text)` → `recommend(text)` 分析文章文本。`recommend()` 返回：

```python
{
    "presets": [("forest", {...}, 16), ("amber", {...}, 13), ...],  # 降序排列
    "content_type": "tutorial",          # 文章类型 ID
    "content_type_name": "教程/操作指南",  # 中文名
    "content_type_confidence": "high",    # high/medium/low
    "secondary_type": "case",             # 次类型（可能为 None）
}
```

推荐逻辑：关键词匹配分 + 文章类型加权（高置信度 +3 分，中 +1 分），确保同类型文章推荐稳定。

#### 步骤 B：生成可视化预览网页

```bash
python3 scripts/preview_themes.py output/article-class-html.html --open
```

#### 步骤 C：用户选择

预览页打开后，**必须暂停等待用户选择**。用户可回复：
- 预设名：`navy`、`amber`、`forest`、`teal`、`plum`、`slate`
- 自由组合：`classic:teal-gold` `workshop:navy-coral`
- 自定义颜色：`#e63946`
- 「用推荐的」→ 使用得分最高的预设

#### 步骤 D：进入 build_inline.py

用户确认后，将选定主题传入：
```bash
python3 scripts/build_inline.py output/article-class-html.html output/article-inline.html --theme <选定主题>
```

---

### 4.4 嵌套上下文特殊处理

某些元素在特定父容器内需要覆盖默认样式：

| 父容器 | 子元素 | 特殊处理 |
|--------|--------|---------|
| `<blockquote>` | `<p>` | `color:#4a5a6a;font-size:14px;`（覆盖默认 p 的 `color:#3f3f3f`） |
| `<pre>` | `<code>` | 去掉 `background-color` 和 `color`（继承 pre 的深色主题） |
| `.golden-quote` | `<p>` | `color:#0d7377;font-weight:700;text-align:center;` |
| `.highlight-box` | `<strong>` | `color:#0d7377;`（覆盖默认 strong 的 `color:#212121`） |
| `.cta-footer` | `<p>` | `color:#0d7377;font-weight:500;text-align:center;font-size:14px;` |

### 4.5 HTML 生成流程

**Step 0**：主题推荐与预览（v1.3.0 🔴 强制交互）
- 用 `recommend_theme()` 分析文章内容 → 自动推荐最匹配的主题
- 运行 `preview_themes.py --open` → 在浏览器中并排展示 5 套主题的实际渲染效果
- **暂停等待用户选择**（主题名 / 自定义颜色 / 「用推荐的」）
- 将选定 `--theme <name|#RRGGBB>` 传给 `build_inline.py`

**Step 1**：生成 class-based HTML（便于结构可读性）
```html
<blockquote class="golden-quote"><p>万物皆可蒸馏</p></blockquote>
```
⚠️ 必须使用语义元素（`<p>`, `<blockquote>`, `<h2>`, `<h3>`, `<section>`, `<code>`, `<hr>`, `<strong>`），严禁 `<div>`。**🔴 禁止 `<pre>` 标签**（微信不支持，换行全部丢失，参见铁律 7）。格式化文本用 `<section>` + `white-space:pre-wrap` + `<br>` 替代。

⚠️ `<code>` 内如需展示 HTML 标签（如 `<style>`），必须写 `&lt;style&gt;`，不要写裸 `<style>`。

⚠️ **头图（v1.3.0）**：class-based HTML 中**不要写头图 `<img>`**。头图由 `upload.py` 自动上传 `img/header_image.png` 并在阶段⑤注入正文顶部。

**Step 2**：用 `build_inline.py` 将 class 映射转换为 inline style（v1.9.0：自动包裹 `<span leaf="">`）
```bash
python3 scripts/build_inline.py output/article-class-html.html output/article-inline.html --theme teal
```
```python
# 🔴 关键：必须设置 convert_charrefs=False
# 否则 HTMLParser 会把 &lt; &gt; 转成 < >，导致 <code> 内的标签被当作真标签吃掉内容
parser = HTMLParser(convert_charrefs=False)
# 移除所有 class 属性，注入对应的 style 属性（颜色来自主题色板）
# 🆕 v1.9.0：同时自动为所有文本节点包裹 <span leaf="">，防微信剥离样式
```
⚠️ AI 在生成 class-based HTML 时**不需要手写 `<span leaf="">`**——`build_inline.py` 的 `InlineStyleConverter.handle_data()` 自动完成包裹，`validate_output()` 强制校验。

**Step 3**：后处理嵌套上下文冲突（blockquote p、pre code、golden-quote p、cta-footer p 等）
⚠️ 嵌套覆盖必须追踪父级 class 名，不能只追踪 tag 名。例如 `golden-quote` 下的 `<p>` 和普通 `blockquote` 下的 `<p>` 需要不同的覆盖样式。

**Step 4**：输出纯 body 片段 HTML（仅 inner content，不含 `<html>`, `<head>`, `<body>` 标签），所有样式通过 `style=""` 内联，全文无 `<style>` 标签、无 `class` 属性、无 `<div>` 元素。

**Step 5**（v1.3.0）：运行 `upload.py` 完成头图注入 + 底部留白 + 封面上传 + 草稿创建
```bash
python3 scripts/upload.py --token TOKEN --html output/article-inline.html --title "标题" --author "嗯哌" --digest "摘要"
```
upload.py 自动执行：上传 `img/header_image.png` → 注入 `<img>` 到正文顶部 → 底部注入留白 `<p>` → 上传 `img/cover.png` 做封面 → 创建草稿

### 4.6 排版质量检查清单

- [ ] 全文无 `<style>` 标签
- [ ] 全文无 `class` 属性
- [ ] 所有元素样式通过 `style=""` 内联
- [ ] 全文无 `linear-gradient`（已替换为纯色 `background-color`）
- [ ] 全文无 `letter-spacing`
- [ ] 正文行高 ≥ `1.8`，字号 ≥ 15px
- [ ] 在 375px 宽视口下无横向滚动
- [ ] H2 ≤ 19px，视觉层级正确（H2 > H3 > 正文 > 辅助文字）
- [ ] 关键观点使用金句模块或强调模块包裹
- [ ] 文章底部有 CTA 模块
- [ ] CTA 之后有底部留白（≥32px 空行，便于追加底部信息）
- [ ] blockquote / golden-quote / cta-footer 内子元素样式已做嵌套覆盖
- [ ] class-based HTML 中不含头图 `<img>`（由 upload.py 阶段⑤自动注入）
- [ ] 颜色来自主题色板，全文主色一致（v1.3.0）

---

## 阶段 ②：一键发布（Publish）

**目标**：排版完成 → 推送到公众号草稿箱，用户打开后台即可预览和群发。

### 5.1 凭据获取

按以下顺序查找微信 API 凭据：

1. **环境变量**：`WEIXIN_APPID` / `WEIXIN_APPSECRET` 或 `WECHAT_APPID` / `WECHAT_APPSECRET`
2. **会话上下文**：如果用户在本轮对话中已提供过，直接复用（不在日志中明文输出）
3. **主动询问**：以上均未找到时，向用户询问 AppID 和 AppSecret。提示路径：公众号后台 → 开发 → 基本配置

凭据仅在当前会话内存缓存，不写入任何文件。

### 5.2 获取 Access Token

```
GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
```
- 有效期 7200 秒，会话内存缓存复用
- 失败重试 1 次，仍失败则中止并报告错误

### 5.3 封面处理

**`thumb_media_id` 为必填字段**。封面图获取 / 生成优先级：

1. **`img/cover.png`**（v1.3.0 默认）：skill 根目录下预置封面图，直接上传到微信素材库
2. 用户显式指定的图片路径/URL → 上传到微信素材库
3. 文章内第一张 `<img>` 的 src（需已是 `mmbiz.qpic.cn` URL）
4. **自动生成封面图**（fallback）：用 Python 内置库生成品牌色纯色 PNG，1080×1080px → 上传
5. 以上均失败 → 报告错误，不上传空封面

本地上传封面：
```
POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=ACCESS_TOKEN&type=image
```
成功返回 `media_id` 和微信 CDN URL（`mmbiz.qpic.cn`）。将 URL 回填到正文 `<img>` 标签中。

**头图自动注入**（v1.3.0）：`upload.py` 会自动上传 `img/header_image.png` 到微信素材库，获取 CDN URL，并注入到正文 HTML 最顶部。class-based HTML 中**不需要**手写头图 `<img>`。

**封面自动生成代码模板**：
```python
import struct, zlib

def create_cover_png(w=1080, h=1080):
    """生成品牌色纯色 PNG"""
    def chunk(ctype, data):
        c = ctype + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        return struct.pack('>I', len(data)) + c + crc
    
    ihdr_data = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    ihdr = chunk(b'IHDR', ihdr_data)
    
    raw = b''
    for y in range(h):
        raw += b'\x00'
        for x in range(w):
            raw += struct.pack('BBB', 13, 115, 119)  # #0d7377
    
    idat = chunk(b'IDAT', zlib.compress(raw))
    iend = chunk(b'IEND', b'')
    
    return b'\x89PNG\r\n\x1a\n' + ihdr + idat + iend
```

**封面裁剪提示**：微信在星标/常读用户侧展示 2.35:1 宽图，普通用户展示 1:1 方图。核心信息必须放在图片中央 1:1 区域内。

### 5.4 创建草稿

使用 `upload.py` 一键完成：头图上传注入 → 底部留白 → 封面上传 → 创建草稿。

```bash
python3 scripts/upload.py \
  --token ACCESS_TOKEN \
  --html output/article-inline.html \
  --title "文章标题（≤64字）" \
  --author "嗯哌" \
  --digest "摘要（≤120字）"
```

`upload.py` 内部流程：

**步骤 0**：去除 `<section>` 外层容器 → 让内容直接填满微信文章区宽度（v1.7.0）

**步骤 1**：上传 `img/header_image.png` → 获取微信 CDN URL → 注入 `<img>` 到正文最前面

**步骤 2**：追加底部留白 `<p style="margin:0;padding:0;height:0;"><br></p>` 到正文最后

**步骤 3**：上传 `img/cover.png` → 获取 `thumb_media_id`（若不存在则自动生成品牌色封面 fallback）

**步骤 4**：构建 payload → 🔴 铁律1 序列化 → 创建草稿

```python
# 🔴 关键：必须 ensure_ascii=False，否则中文变 \uXXXX → 微信编辑器显示乱码
# 🔴 必须用 data= 传 UTF-8 字节，不能用 json= 参数
payload_json = json.dumps(payload, ensure_ascii=False)
resp = requests.post(
    f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}",
    data=payload_json.encode("utf-8"),
    headers={"Content-Type": "application/json; charset=utf-8"},
    timeout=60,
)
```

关键约束：
- `title` ≤ 64 字，超长自动截断末尾加 `…`
- `content` 中的 HTML 已由 `upload.py` 自动注入头图和底部留白
- `thumb_media_id` 为**必填项**——`upload.py` 自动从 `img/cover.png` 获取

### 5.5 错误处理

| 错误码 | 含义 | 处理 |
|--------|------|------|
| 40001 | access_token 过期/无效 | 重新获取 token，重试 1 次 |
| 40007 | 不合法的媒体 ID | ① 检查 thumb_media_id 是否已正确上传；② 重新上传封面获取新 media_id；③ 确认上传时使用了 `type=image` 参数 |
| 40125 | 无效的 appsecret | 提示用户检查凭据，重新提供 |
| 45009 | 调用频率超限 | 等待 1 分钟后重试 |
| 50000+ | 微信服务器错误 | 等待 5 秒后重试，最多 3 次 |

### 5.6 成功响应

```json
{ "media_id": "xxx" }
```
保存 `media_id`，提示用户：**打开公众号后台 → 草稿箱 → 预览确认排版效果 → 群发**。

上传完成后，`upload.py` 自动清理临时文件，只保留 HTML 排版文件和原始 Markdown。

---

## 完整链路示例

### 示例 1：默认完整流程——优化 + 排版 + 发布

```
用户：帮我把这篇文章优化后发公众号
（附带 draft.md）

→ 阶段⓪：内容脱水 + 结构重组 + 去AI味
→ 🔴 输出优化稿 → 用户确认「可以」
→ 阶段①：analyze_content() → 推荐最佳排版系统
         preview_themes.py --open → 浏览器 6 套对比
         🔴 用户选择
         build_inline.py --theme <选定> → inline HTML
→ 阶段②：upload.py → 上传头图+封面 → 创建草稿
→ ✅ media_id 返回
```

### 示例 2：豁免优化 + 指定排版

```
用户：这篇按原文，用卡片流排版发公众号，一字不改

→ 豁免「一字不改」→ 跳过阶段⓪
→ 阶段①：用户指定「卡片流」→ build_inline.py --theme plum
→ 阶段②：upload.py → ✅
```

### 示例 3：自定义颜色

```
用户：主色用 #e63946，发公众号

→ 阶段⓪① 正常执行
→ 阶段①：build_inline.py --theme "#e63946" → 默认 classic 布局 + 自动推导配色
→ 阶段②：upload.py → ✅
```

---

## 与其它 Skill 的协作

- **oral-stylizer**：阶段⓪ 的前置处理器。口述碎碎念先调 oral-stylizer 结构化，再进入本 skill。
- **humanizer-zh**：阶段⓪.3 去 AI 味的执行引擎，直接调用审阅全文。

协作管线：`oral-stylizer → wechat-automator（⓪优化 → ①排版 → ②发布）`

### 配图扩展（预留口子）

本 skill 不内置配图生成。但 HTML 结构支持配图占位：

```html
<p class="illustration"><img src="PLACEHOLDER" alt="配图说明"></p>
```

配图准备完成后，替换 `PLACEHOLDER` 为微信 CDN URL 即可。`.illustration` 样式（居中、圆角、全宽）已在所有排版系统中内置。

未来可通过安装 `npie-illustrations` skill 实现自动配图流程（出 shot list → 生成 → 插入），两 skill 接口已预留对齐。

---

---

## 🔴 历史事故与铁律（2026-06-09 血泪教训）

以下每条都曾经导致过**批量乱码草稿**的生产事故。**违反任何一条 = 用户草稿箱被污染 = 不可接受。**

### 铁律 0：排版发布 = 必须调用本 skill

用户说「排版」「发布」「排版发布」「发公众号」「推送草稿」或任何含公众号发布意图的话 → **必须先用 `Skill` 工具加载 `wechat-automator`，然后严格按其五阶段流水线执行。** 严禁以下行为：

- ❌ 加载了 skill 但自己另写 Python 脚本绕过
- ❌ 手动拼接 HTML 直接用 `requests` 上传
- ❌ 用 `curl` 代替 skill 的 `build_and_upload.py`
- ❌ 跳过 class-based → html.parser → inline 转换管线

**skill 加载后的 `scripts/build_and_upload.py` 是唯一合法的执行入口。**

### 铁律 1：JSON 序列化必须 `ensure_ascii=False`

```python
# ❌ 错误：requests 的 json= 参数默认 ensure_ascii=True
# 中文 → \uXXXX → 微信编辑器不解码 → 草稿箱全乱码
resp = requests.post(url, json=payload)

# ✅ 正确：手动序列化，ensure_ascii=False
payload_json = json.dumps(payload, ensure_ascii=False)
resp = requests.post(url, data=payload_json.encode("utf-8"),
                     headers={"Content-Type": "application/json; charset=utf-8"})
```

**根因**：`requests.post(json=payload)` 内部调用 `json.dumps(payload)`，默认 `ensure_ascii=True`，所有非 ASCII 字符（中文）被转义为 `\uXXXX`。微信 API 虽接受请求并返回成功，但草稿编辑器**不解码**这些转义序列，直接显示为 `我把...`。

### 铁律 2：HTMLParser 必须 `convert_charrefs=False`

```python
# ❌ 错误：默认 convert_charrefs=True
# &lt;style&gt; → <style>（真标签）→ 微信/浏览器吃掉后续内容
parser = HTMLParser()  # 默认 convert_charrefs=True

# ✅ 正确
parser = HTMLParser(convert_charrefs=False)
# &lt;style&gt; 保持为实体引用 → handle_entityref('lt') → 正确输出 &lt;
```

**根因**：Python `HTMLParser` 默认 `convert_charrefs=True`，将 `&lt;` `&gt;` 等命名实体转为对应字符 `<` `>`。如果 `<code>&lt;style&gt;</code>` 被转为 `<code><style></code>`，`<style>` 被当作真标签，导致后面内容全部丢失。

### 铁律 3：只传 body 片段，不传完整 HTML 文档

```python
# ❌ 错误：传完整 HTML 文档给 content 字段
content = "<!DOCTYPE html><html><head>...</head><body>...</body></html>"

# ✅ 正确：只传 body 内部纯内容片段
# content = "<p>...</p><h2>...</h2><blockquote>...</blockquote>"
# 不含 <html>, <head>, <body>, <section> 外层包裹
```

**根因**：微信草稿 API 的 `content` 字段期望的是文章内文 HTML 片段，不是完整网页文档。传入 `<!DOCTYPE>` / `<html>` / `<head>` 标签会导致编辑器解析异常。

### 铁律 4：嵌套覆盖必须追踪父级 class

```python
# ❌ 错误：只追踪 tag 名，无法区分子元素的父容器类型
tag_stack = ["blockquote"]  # 丢失 class 信息
# golden-quote 下的 <p> 和 cta-footer 下的 <p> 都用了 blockquote p 样式

# ✅ 正确：追踪 (tag, class) 元组
tag_stack = [("blockquote", "golden-quote")]
# 先查 (class, tag) → (golden-quote, p) → 正确样式
# 再查 (tag, tag)   → (blockquote, p)    → 兜底样式
```

### 铁律 6：超长引用（>300 字）禁用 `<blockquote>`，改用 `<section>` + 左边框

```html
<!-- ❌ 错误：Prompt 全文等超长内容（>300字）包在 <blockquote> 中
     微信编辑器自动插入警告：「引用字数:1119/300(单次引用不得超过300字)」 -->
<blockquote>
  <p>你现在是我的Obsidian知识库资深架构师和重构专家...</p>
  <p>审查重点（必须覆盖）...</p>
  <!-- ...1100+ 字内容 -->
</blockquote>

<!-- ✅ 正确：用 <section> + border-left 替代，视觉等效但无字数警告 -->
<section style="border-left:3px solid #0d7377;margin:16px 0;padding:4px 0 4px 18px;">
  <p style="font-size:14px;color:#4a5a6a;">你现在是我的Obsidian知识库资深架构师和重构专家...</p>
  <p style="font-size:14px;color:#4a5a6a;">审查重点（必须覆盖）...</p>
</section>
```

**根因**：微信编辑器对 `<blockquote>` 元素有隐性 300 字上限检测。超过 300 字的单次引用会被自动插入警告文字，破坏排版。`<section>` 不受此限制，配合 `border-left` 样式可实现相同的视觉效果。

**适用范围**：Prompt 全文、长文摘录、多段落引用等任何可能超过 300 字的引用内容。短引用（≤300 字）仍可正常使用 `<blockquote>`。

### 铁律 5：上传前必须验证，验证必须排除 `<code>` 和 `<pre>`

```python
# ❌ 错误：全文搜索 <style，误判 <code>&lt;style&gt;</code> 中的内容
# ❌ 错误：全文搜索 <div，误判 <code>&lt;div&gt;</code> 中的内容

# ✅ 正确：先 strip <code> 和 <pre> 块，再验证其余部分
clean = re.sub(r'<code[^>]*>.*?</code>', '', html, flags=re.DOTALL)
clean = re.sub(r'<pre[^>]*>.*?</pre>', '', clean, flags=re.DOTALL)
# 然后在 clean 上做 <style>, <div>, class= 检查
```

### 铁律 7：微信不支持 `<pre>` 标签——所有换行全部丢失，内容变成一行（2026-06-26 实战血证）

```html
<!-- ❌ 致命错误：<pre> 在微信编辑器中被吃掉所有换行符
     CLAUDE.md 的 151 行内容变成一行，目录树结构完全塌缩 -->
<pre style="...">
# My‑Viki 系统规则
## 1. 角色与总目标
- 你是 **My‑Viki 的知识架构师和维护者**。
...
</pre>
<!-- 结果：微信草稿箱里变成一行乱码 -->
```

**根因**：微信编辑器不支持 `<pre>` 标签。`<pre>` 内的换行符（`\n`）被全部忽略，所有内容挤压成一行。同时 `<pre>` 的背景色和等宽字体样式也可能被剥离。

**✅ 唯一正确的替代方案：`<section>` + `white-space:pre-wrap` + 显式 `<br>` 换行**

```python
import html as html_mod

def text_to_wechat_block(content, style_extras=""):
    """
    将多行文本转为微信兼容的格式化区块。
    三步：① HTML 转义 → ② \n → <br> → ③ 包入 <section>
    """
    escaped = html_mod.escape(content)       # 转义 < > & "
    with_br = escaped.replace('\n', '<br>')  # 换行 → 显式 <br>
    return f'<section style="white-space:pre-wrap;font-family:monospace;{style_extras}">{with_br}</section>'
```

**关键样式说明**：
| 样式属性 | 作用 | 必要性 |
|----------|------|--------|
| `white-space:pre-wrap` | 保留空格缩进，配合 `<br>` 换行 | 🔴 必须 |
| `font-family:monospace` | 等宽字体，替代 `<pre>` 的默认等宽效果 | 🟡 强烈建议 |
| `max-height:520px;overflow-y:auto` | 长内容滚动（CLAUD.md/WIKI.md 等 150+ 行文件） | 🟡 按需 |
| `-webkit-overflow-scrolling:touch` | iOS 平滑滚动 | 🟡 按需 |

**适用范围**：目录树、代码块、配置文件全文、Markdown 原文展示——任何依赖换行和空格对齐的格式化文本，一律用此方案，**禁止使用 `<pre>`**。

**禁止 `<pre>` 的唯一例外**：`build_inline.py` 的验证逻辑中，`<pre>` 仅在 `<code>` 展示 HTML 标签转义示例（如 `&lt;style&gt;`）时可用于 class-based 中间文件，但**最终输出到微信的 HTML 必须零 `<pre>`**。

### 铁律 8：每段正文必须标记 1-3 个关键词下划线（v1.8.0）

```html
<!-- ❌ 错误：整段没有任何标记，读者扫过去全是灰字，信息密度为零 -->
<p style="..."><span leaf="">前端通过自然语言描述需求，Agent 自动完成从代码生成到部署的全链路。</span></p>

<!-- ✅ 正确：AI 主动标记 1-3 个关键短语 -->
<p style="...">
  <span leaf="">前端通过</span>
  <span style="border-bottom:2px solid #0d737740;font-weight:600;"><span leaf="">自然语言描述需求</span></span>
  <span leaf="">，Agent 自动完成从</span>
  <span style="border-bottom:2px solid #0d737740;font-weight:600;"><span leaf="">代码生成到部署</span></span>
  <span leaf="">的全链路。</span>
</p>
```

**根因**：公众号是扫描式阅读。读者不会逐字读，而是用眼睛扫关键词。没有下划线标记的段落 = 读者什么都抓不住 = 跳出。`.kw-underline` 是全文出现频率最高的样式，**必须逐段落实**。

### 铁律 9：章节编号必须连续，末章结语用 ∞（v1.8.0）

```html
<!-- ❌ 错误：编号跳号（01 → 03），或中间章节用了结语编号 ∞ -->
<!-- ❌ 错误：末章是"写在最后"但编号仍是普通数字 04 -->

<!-- ✅ 正确：01 → 02 → 03 → ∞，严格连续 -->
<span class="chapter-num" leaf="">01</span>  <!-- 第一章 -->
<span class="chapter-num" leaf="">02</span>  <!-- 第二章 -->
<span class="chapter-num" leaf="">03</span>  <!-- 第三章 -->
<span class="chapter-num-final" leaf="">∞</span>  <!-- 结语章 -->
```

**根因**：章节编号是读者的空间导航。跳号会让读者困惑"我漏看了什么？"；末章不用 ∞ 区分会让结语淹没在正文中。

### 铁律 10：锚点层全文 ≤ 5 处（v1.8.0）

`.anchor-bold`（主色加粗）和 `.anchor-block`（主色底白字标签）只在全文最关键的 ≤5 处使用——产品名、核心结论、CTA 动词。**到处锚点 = 没有锚点**。正文日常强调用 `.kw-underline`（标记层），不要滥用 `.anchor-bold`。

### 铁律 11：签名区仅末尾一处，默认占位（v1.8.0）

- 签名区（「我是 {{作者名}}…」+「点赞、在看、转发」）**只在文末 CTA 之前出现一次**
- 原文末尾已有作者签名段的，直接沿用原文，不另生成
- 默认用 `{{作者名}}` / `{{一句话简介}}` 占位符——**不要写死任何人名**
- 中间章节不出现签名式段落

### 铁律 12：点缀组件种类 ≤ 3，不跨布局混用（v1.8.0）

一篇只用所选布局的组件 + 通用视觉层级类。`.tip-box` / `.warn-box` / `.prompt-card` / `.card-item` 等容器级组件，全篇点缀种类 ≤3，避免花哨。**不要从其他布局借组件**——每个布局的组件是成套设计的，混用会破坏排版气质一致性。

### 铁律 13：所有文本节点必须包裹 `<span leaf="">` ——微信防样式剥离的命门（v1.9.0）

```html
<!-- ❌ 错误：裸文本直接放在 <p> 内，微信可能剥离样式 -->
<p style="...">这是一段正文内容</p>

<!-- ✅ 正确：文本包裹在 <span leaf=""> 中 -->
<p style="..."><span leaf="">这是一段正文内容</span></p>
```

**根因**：微信公众号编辑器在处理粘贴的 HTML 时，会对没有 `<span>` 包裹的裸文本进行"样式归一化"——轻则丢失加粗/颜色，重则整段样式崩塌。`<span leaf="">` 是唯一可靠的全平台防剥离手段。

**实施方式**（v1.9.0 起自动执行）：
- `build_inline.py` 的 `InlineStyleConverter.handle_data()` 自动为所有文本节点包裹 `<span leaf="">`
- `validate_output()` 强制检查 leaf 包裹数量，为 0 时报错
- AI 在生成 class-based HTML 时**不需要**手写 `<span leaf="">`——转换管线自动补全
- **例外**：`<code>` 和 `<pre>` 内的文本保持原样（代码内容不容干扰）
- **防双重包裹**：转换器自动检测已存在的 `<span leaf="">`，不会嵌套

---

## 安全与隐私

- API 凭据（AppID / AppSecret）优先级：环境变量 → 会话上下文 → 主动询问。仅在当前会话内存缓存，不写入任何磁盘文件
- 生成的 HTML 和草稿内容保存在本地，不经过第三方服务中转
- 上传完成后自动清理临时文件（JSON payload、自动生成的封面 PNG）
- 凭据在日志和输出中不出现明文
