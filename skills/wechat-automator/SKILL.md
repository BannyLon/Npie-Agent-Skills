---
name: wechat-automator
description: 一站式内容资产化引擎：默认对内容进行深度优化（契合公众号阅读场景），精排版渲染，一键上传草稿箱。当用户提到"推文"、"公众号"、"排版"、"发布"、"草稿"、或任何将内容转化为公众号图文的意图时，必须调用此技能。
version: 1.1.0
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
           └─ 否 → 完整五阶段：① → ② → ③ → ④ → ⑤
```

**HTML 兼容性扫描标准**（干净 HTML 的定义）：
- 无 `<style>` 标签
- 无 `class` 属性
- 无 `<div>` 元素
- 无可检测的 `linear-gradient`

四条全部满足 → 直达 ⑤。任一不满足 → 告知用户「这个 HTML 有 X 个 div / Y 个 style 标签，微信会丢格式，要我先修复吗？」

---

## 核心链路（三阶段用户视角 / 五阶段内部流水线）

```
用户视角（三阶段）：
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  ① 深度优化   │ ──→ │  ② 精排版渲染  │ ──→ │  ③ 一键发布   │
│  (默认执行)   │     │  (始终执行)   │     │  草稿箱      │
│  跳过:豁免词  │     │  跳过:干净HTML│     │              │
└──────────────┘     └──────────────┘     └──────────────┘
  ≡ 阶段①②             ≡ 阶段③④             ≡ 阶段⑤

内部五阶段流水线：
┌─────────────────────────────────────────────────────────────┐
│  输入源                     输出                              │
│  ┌──────────┐              ┌──────────┐                     │
│  │ 视频脚本  │              │          │                     │
│  │ 知识笔记  │──→ 五阶段 ──→│ 公众号草稿 │                     │
│  │ 碎片资料  │   流水线     │ (精排版)  │                     │
│  └──────────┘              └──────────┘                     │
│                                                             │
│  ① 内容脱水 ──→ ② 结构重组 ──→ ③ 视觉增强 ──→ ④ 排版渲染 ──→ ⑤ 上传 │
└─────────────────────────────────────────────────────────────┘
```

---

## 阶段 ①：内容脱水（Information Distillation）

**目标**：无论输入是什么形态（视频脚本/口述稿/笔记/资料堆），先提炼出可传播的核心信息骨架。

### 输入源识别

| 输入类型 | 典型特征 | 处理策略 |
|----------|----------|----------|
| **视频脚本** | 口语化、线性叙事、有"你看"/"咱们来看"等镜头语 | 剥离镜头指令，提取论述主线 |
| **口述/碎碎念** | 跳跃、重复、有"就是说""然后""嗯"等口语助词 | 先调 `oral-stylizer` 做结构化 |
| **知识笔记** | 已有一定结构，但信息密度不均 | 直接进入脱水 |
| **资料整理** | 多来源拼合，风格不统一 | 统一视角+去重，再进入脱水 |

### 脱水操作

1. **去冗余**：删除重复论述、口头禅、填充性句子（"大家都知道""这里我想说的是"）。
2. **提论点**：将散落的叙述收敛为可独立传播的**核心观点句**——每段内容必须能提炼出 1 句可以直接被引用的主干观点。
3. **压密度**：合并相似论述，用更精炼的表达覆盖原文。目标：**信息密度提升 30-50%**。
4. **保人味**：脱水不是脱口感。保留作者的标志性表达方式和态度。如果是 Banny 的内容，保留「Vibe Coding」「Agentic Workflow」等命名习惯。

### 脱水完成标志

- [ ] 每条核心观点可以用一句话复述
- [ ] 没有出现两次以上的相同论述
- [ ] 每段长度适合手机阅读（≤ 4 句）
- [ ] 保留了原文的标志性语言风格

---

## 阶段 ②：结构重组（Structural Recomposition）

**目标**：将脱水的线性内容，重构成适合图文阅读的**层级化结构**。这一步的本质是完成「视频线性叙事 → 图文空间结构」的翻译。

### 重组策略

#### 开头钩子（Hook）
- 从正文中提取最反直觉/最引发共鸣的 1 句话，前置为开篇钩子
- 或用 2-3 句短句制造信息落差——「你以前以为 X，其实 Y」
- 末尾用一句自然过渡连接正文

#### 正文架构（Body）
根据内容类型选择一种骨架：

| 内容类型 | 推荐结构 | 适用场景 |
|----------|----------|----------|
| **教程/指南** | 问题→原理→步骤→验证→总结 | 工具教学、操作流程 |
| **观点/评论** | 现象→分析→本质→行动建议 | 行业洞察、趋势判断 |
| **案例/复盘** | 背景→关键决策→结果→可复用方法论 | 项目复盘、经验分享 |
| **清单/合集** | 总览→逐条展开（每条约等长）→最佳组合 | 资源推荐、工具清单 |

#### 小标题原则
- H2：大板块之间的分界，数量控制在 3-5 个
- H3：H2 内部子观点展开，仅当 H2 下内容超过 3 段时才使用
- 小标题格式：「问题是什么」而非「关于 XX 的讨论」——要具体，不要虚

#### 结尾行动召唤（CTA）
- 引导关注（公众号场景）或引导看原视频（视频号场景）
- 不是客套话，要给读者一个**具体的下一步**

### 重组完成标志

- [ ] 文章有一个 2-3 句的钩子开头
- [ ] H2 在 3-5 个之间，每个 H2 下的段落数均衡
- [ ] 手机屏幕（约 375×667px）滚动 2-3 屏内有一个视觉节奏变化
- [ ] 结尾有明确的行动召唤

---

## 阶段 ③：视觉增强（Visual Enhancement）

**目标**：在纯文字基础上，自动标记和生成配图位——示意图、截图位、信息卡片——使文章「图文并茂」，而不是一面文字墙。

这是本 Skill 区别于普通排版工具的**关键差异化能力**。

### 3.1 配图触发点检测

扫描经过阶段 ①② 处理后的结构化内容，自动识别以下**配图触发点**，并按需插入对应元素：

| 触发场景 | 插入元素 | 标记语法 | 渲染效果 |
|----------|----------|----------|----------|
| **关键概念定义** | 概念卡片 | `> 💡 概念：xxx` | `.highlight-box` 渲染 |
| **步骤流程** | 流程卡片 | `1. 步骤一\n2. 步骤二` | `.card-list` 渲染（每步一张卡片） |
| **数据/对比** | 表格或对比卡 | Markdown 表格 | 响应式表格样式 |
| **截图演示** | 截图占位 | `> 📸 截图位：描述所需截图内容` | 虚线边框占位区 + 截图说明文字 |
| **架构/关系图** | 示意图占位 | `> 📊 示意图：描述图表内容` | 虚线边框占位区 + 图表说明文字 |
| **重点结论** | 金句模块 | `> ✨ 金句：xxx` | `.highlight-box` + 加大字号渲染 |
| **工具/资源推荐** | 资源卡片 | `- [ ] 资源名：说明` | `.card-list` 渲染 |

### 3.2 截图占位符自动生成

对于视频脚本来源的内容，**自动推断**哪些位置需要截取视频画面并生成占位说明：

1. **界面操作步骤**：每个"点击/打开/选择/输入"类描述 → 标记 `> 📸 截图位：XX 界面操作截图`
2. **效果对比**：「之前 vs 之后」「优化前 vs 优化后」→ 标记 `> 📸 截图位：前后对比拼接图`
3. **工具界面**：首次提到某个工具名 → 标记 `> 📸 截图位：XX 工具主界面`
4. **数据结果**：任何涉及数字指标的结论 → 标记 `> 📸 截图位：结果数据面板`

### 3.3 信息卡片自动生成

以下类型的内容**强制使用信息卡片**渲染（不经过用户确认）：

- **工具推荐列表**：每款工具 → 1 张 `.card-item`
- **步骤指南**：每个步骤 → 1 张 `.card-item`
- **核心观点清单**：每条观点 → 1 张 `.card-item`
- **注意事项/避坑清单**：每条 → 1 张 `.card-item`

卡片内部结构：`<strong>标题</strong>` + 1-2 句说明文字。

### 3.4 视觉节奏控制

- 纯文字段落连续不超过 **3 段**，之间必须有视觉元素（图片/卡片/分隔线/引用块）
- 全文至少包含 **2 个**配图位（截图或示意图）
- 每个 H2 板块内至少有 **1 个**视觉断点

---

## 阶段 ④：排版渲染（Typography & Rendering）

**目标**：将结构化内容注入品牌 CSS 模板，输出可直接用于公众号的完整 HTML。

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
- ✅ **所有样式写在每个元素的 `style=""` 属性中**
- ✅ **用语义元素替代 div**：`<section>` 做容器、`<blockquote>` 做强调块、`<table>` 做数据对比、`<p>` 做卡片
- ✅ 布局基于 `block`/`inline-block`/`table` + `margin`/`padding`
- ✅ 背景色使用纯色（`background-color`），禁用渐变
- ✅ 图片 src 必须是微信 CDN URL（`mmbiz.qpic.cn` 域名）
- ✅ 容器最大宽度 `677px`

**Div → 语义元素映射表（关键！所有 `<div>` 必须转换）：**

| 原始 div 用途 | 替换元素 | 示例 |
|-------------|---------|------|
| 页面容器 | `<section style="...">` | `<section style="max-width:677px;margin:0 auto;...">` |
| 元信息标签 | `<span style="display:inline-block;...">` 包在 `<p>` 中 | `<p style="text-align:center;"><span style="...">深度解析</span></p>` |
| 开篇大数字 | `<p>` + `<strong>` | `<p style="text-align:center;"><strong style="font-size:56px;">9,500 ★</strong></p>` |
| 金句模块 | `<blockquote style="...">`（不设左边框） | `<blockquote style="background-color:#d4edf5;border-radius:12px;text-align:center;">` |
| 强调模块 | `<blockquote style="...">`（带完整边框） | `<blockquote style="background-color:#f7fafc;border:1px solid #e0e7ef;">` |
| 卡片列表 wrapper | 直接删除，子项用 `<p>` | |
| 卡片项 | `<p style="...">`（带背景+边框+圆角） | `<p style="background-color:#fafbfc;border:1px solid #e8ecf1;border-radius:8px;">` |
| 数据双栏 | `<table>` + `<td style="width:50%">` | |
| CTA 底部 | `<blockquote style="...">`（不设左边框） | `<blockquote style="margin-top:44px;background-color:#d4edf5;border-radius:14px;">` |
| 编辑注记 | `<p style="...">`（左侧灰色细线） | `<p style="border-left:2px solid #dce3ea;color:#8a9aaa;font-style:italic;">` |

### 4.3 品牌 Inline Style 映射表

每个 HTML 元素直接注入内联样式。以下为完整的元素→样式映射：

```python
# 核心元素 inline style 定义
WEIXIN_STYLES = {
    # 容器
    "#article-wrapper": "max-width:677px;margin:0 auto;padding:32px 20px 48px;background-color:#ffffff;",
    "body": "background-color:#f5f5f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei','Helvetica Neue',sans-serif;color:#3f3f3f;-webkit-font-smoothing:antialiased;margin:0;padding:0;",
    
    # 顶部元信息
    ".article-meta": "margin-bottom:28px;padding-bottom:24px;border-bottom:1px solid #e8ecf1;text-align:center;",
    ".meta-tag": "display:inline-block;padding:4px 14px;font-size:12px;font-weight:600;color:#0d7377;background-color:#e8f4f8;border-radius:20px;margin-bottom:14px;",
    ".meta-desc": "font-size:14px;color:#8a9aaa;line-height:1.8;",
    
    # 开篇大数字冲击
    ".hero-block": "margin:0 0 36px;text-align:center;",
    ".hero-number": "font-size:56px;font-weight:900;color:#0d7377;line-height:1;margin-bottom:4px;",
    ".hero-label": "font-size:13px;color:#8a9aaa;",
    
    # H2：品牌特征块标题（纯色背景代替渐变）
    "h2": "margin:44px 0 22px;padding:14px 18px;font-size:19px;font-weight:700;line-height:1.5;color:#1a1a1a;background-color:#e8f4f8;border-left:4px solid #0d7377;border-radius:0 6px 6px 0;",
    
    # H3：加粗 + 底部细线
    "h3": "margin:34px 0 16px;padding:0 0 12px;font-size:17px;font-weight:700;color:#2c3e50;border-bottom:2px solid #e0e7ef;line-height:1.5;",
    
    # 正文段落
    "p": "margin:0 0 16px;font-size:15px;line-height:1.9;color:#3f3f3f;text-align:justify;",
    
    # 强调
    "strong,b": "color:#212121;font-weight:700;",
    
    # 分隔线
    "hr": "margin:36px 0;border:none;height:1px;background-color:#dce3ea;",
    
    # 引用块
    "blockquote": "margin:20px 0;padding:18px 20px 18px 22px;background-color:#f7fafc;border-left:3px solid #0d7377;border-radius:0 8px 8px 0;color:#4a5a6a;font-size:14px;line-height:1.8;",
    # blockquote 内 p 标签特殊处理（覆盖默认 p 样式）
    "blockquote p": "margin:0 0 8px;font-size:14px;line-height:1.8;color:#4a5a6a;text-align:justify;",
    
    # 行内代码
    "code": "padding:2px 6px;font-family:'SF Mono','Menlo','Monaco','Courier New',monospace;font-size:13px;color:#c7254e;background-color:#f9f2f4;border-radius:3px;",
    
    # 代码块
    "pre": "margin:18px 0;padding:18px 20px;background-color:#282c34;color:#abb2bf;border-radius:8px;overflow-x:auto;font-size:13px;line-height:1.8;",
    "pre code": "font-size:13px;line-height:1.8;",  # 继承 pre，不设背景
    
    # 卡片列表
    ".card-list": "margin:16px 0 24px;padding:0;",
    ".card-item": "margin-bottom:10px;padding:15px 18px;background-color:#fafbfc;border:1px solid #e8ecf1;border-radius:8px;font-size:14px;line-height:1.8;color:#3f3f3f;",
    
    # 重点强调模块
    ".highlight-box": "margin:24px 0;padding:20px 22px;background-color:#f7fafc;border-radius:10px;border:1px solid #e0e7ef;font-size:15px;line-height:1.9;color:#2c3e50;",
    ".highlight-box strong": "color:#0d7377;font-weight:700;",
    
    # 金句模块（纯色背景代替渐变）
    ".golden-quote": "margin:30px 0;padding:26px 28px;background-color:#d4edf5;border-radius:12px;text-align:center;font-size:17px;font-weight:700;line-height:1.9;color:#0d7377;",
    
    # 数据对比双栏（inline-block 布局，微信安全）
    ".data-row": "width:100%;margin:20px 0;",
    ".data-col": "display:inline-block;width:47%;vertical-align:top;text-align:center;padding:18px 12px;background-color:#fafcfd;border:1px solid #e8ecf1;border-radius:10px;margin-right:3%;",
    ".data-num": "font-size:28px;font-weight:900;color:#0d7377;line-height:1.2;",
    ".data-label": "font-size:12px;color:#8a9aaa;margin-top:6px;",
    
    # 编辑注记
    ".editor-note": "margin:14px 0;padding:8px 14px;font-size:13px;color:#8a9aaa;font-style:italic;border-left:2px solid #dce3ea;",
    
    # 表格
    "table": "width:100%;margin:20px 0;border-collapse:collapse;font-size:13px;line-height:1.7;",
    "th": "padding:12px 14px;background-color:#e8f4f8;color:#1a1a1a;font-weight:700;text-align:left;border:1px solid #dce3ea;",
    "td": "padding:12px 14px;border:1px solid #e8ecf1;color:#3f3f3f;",
    
    # 结尾 CTA（纯色背景代替渐变）
    ".cta-footer": "margin-top:44px;padding:28px 24px;background-color:#d4edf5;border-radius:14px;text-align:center;",
    ".cta-title": "font-size:17px;font-weight:700;color:#0d7377;margin-bottom:8px;",
}
```

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

**Step 1**：生成 class-based HTML（便于结构可读性）
```html
<blockquote class="golden-quote"><p>万物皆可蒸馏</p></blockquote>
```
⚠️ 必须使用语义元素（`<p>`, `<blockquote>`, `<h2>`, `<h3>`, `<pre>`, `<code>`, `<hr>`, `<strong>`），严禁 `<div>`。

⚠️ `<code>` 内如需展示 HTML 标签（如 `<style>`），必须写 `&lt;style&gt;`，不要写裸 `<style>`。

**Step 2**：用 Python `html.parser` 将 class 映射转换为 inline style
```python
# 🔴 关键：必须设置 convert_charrefs=False
# 否则 HTMLParser 会把 &lt; &gt; 转成 < >，导致 <code> 内的标签被当作真标签吃掉内容
parser = HTMLParser(convert_charrefs=False)

# 移除所有 class 属性，注入对应的 style 属性
```

**Step 3**：后处理嵌套上下文冲突（blockquote p、pre code、golden-quote p、cta-footer p 等）
⚠️ 嵌套覆盖必须追踪父级 class 名，不能只追踪 tag 名。例如 `golden-quote` 下的 `<p>` 和普通 `blockquote` 下的 `<p>` 需要不同的覆盖样式。

**Step 4**：输出纯 body 片段 HTML（仅 inner content，不含 `<html>`, `<head>`, `<body>` 标签），所有样式通过 `style=""` 内联，全文无 `<style>` 标签、无 `class` 属性、无 `<div>` 元素。

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
- [ ] blockquote / golden-quote / cta-footer 内子元素样式已做嵌套覆盖

---

## 阶段 ⑤：一键上传（One-Click Upload）

**目标**：将排版完成的 HTML 推送到公众号草稿箱，用户打开后台即可预览和群发。

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

1. 用户显式指定的图片路径/URL → 上传到微信素材库
2. 文章内第一张 `<img>` 的 src（需已是 `mmbiz.qpic.cn` URL）
3. **自动生成封面图**：用 Python 内置库生成品牌色（#0d7377）纯色 PNG，1080×1080px → 上传
4. 以上均失败 → 报告错误，不上传空封面

本地上传封面：
```
POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=ACCESS_TOKEN&type=image
```
成功返回 `media_id` 和微信 CDN URL（`mmbiz.qpic.cn`）。将 URL 回填到正文 `<img>` 标签中。

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

**步骤 1**：用 Python 构建 JSON payload（避免 curl 直接拼接长 HTML 的转义问题）：

```python
import json

with open("排版输出.html", "r", encoding="utf-8") as f:
    html_content = f.read()

payload = {
    "articles": [{
        "title": "文章标题（≤64字）",
        "author": "嗯哌",
        "digest": "摘要（≤120字）",
        "content": html_content,
        "thumb_media_id": "封面 media_id",
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }]
}

with open("wechat_payload.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False)
```

**步骤 2**：用 Python `requests` 发送（🔴 严禁使用 `json=` 参数，必须手动序列化）：

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
- `content` 中的 HTML 必须通过 `json.dump` 自动转义（不要手动拼接 JSON 字符串）
- `thumb_media_id` 为**必填项**——即使没有封面图，也必须自动生成并上传

**步骤 3**：上传成功后，清理临时文件（wechat_payload.json、cover.png）。

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

上传完成后，清理本地临时文件（JSON payload、自动生成的封面图），只保留 HTML 排版文件和原始 Markdown。

---

## 完整链路示例

### 示例 1：默认行为——视频脚本 → 深度优化 + 排版 + 发布

```
用户：这是我这期视频的脚本，帮我转成公众号推文
（附带 video-script.md）

→ 检查豁免关键词：未命中 → 执行完整五阶段
→ 阶段① 内容脱水：剥离镜头语言，提取论述主线，去除口语填充
→ 阶段② 结构重组：钩子开头 + 问题→原理→步骤骨架 + CTA 结尾
→ 阶段③ 视觉增强：
    - 检测到 3 个操作步骤 → 卡片化
    - 检测到工具界面引用 → 标记截图位
    - 检测到核心结论 → 金句模块
→ 阶段④ 排版渲染：注入品牌 CSS 模板，生成 HTML
→ 阶段⑤ 上传草稿箱：获取凭据 → 生成封面 → 上传素材 → 创建草稿
→ 返回草稿 media_id ✅
```

### 示例 2：豁免优化——仅排版，不改内容

```
用户：这篇按原文排版发公众号，一字不改
（附带 finished-article.md）

→ 检查豁免关键词：命中「一字不改」→ 跳过 ①②
→ 阶段③ 视觉增强：检测配图触发点，自动卡片化
→ 阶段④ 排版渲染：注入品牌 CSS 模板，生成 HTML
→ 阶段⑤ 上传草稿箱
→ 返回草稿 media_id ✅
```

### 示例 3：仅排版预览，不上传

```
用户：先排版看看效果，不上传

→ 检查豁免关键词：未命中 → 执行阶段 ①② 优化
→ 执行阶段 ③④ 排版渲染
→ 输出完整 HTML 文件（配图占位符保留，提醒用户截图后替换）
→ 提示用户可本地浏览器预览
→ 阶段⑤ 跳过
```

### 示例 4：纯排版预览 + 不修改内容

```
用户：仅排版预览，不要修改我写的内容

→ 检查豁免关键词：命中「不要修改」→ 跳过 ①②
→ 阶段③ 视觉增强 → 阶段④ 排版渲染
→ 输出 HTML，不上传
```

---

## 与其它 Skill 的协作

- **oral-stylizer**：阶段①的前置处理器。当输入为口述碎碎念时，先调 oral-stylizer 拿到结构化稿，再进入本 skill 的阶段②。
- **humanizer-zh**：阶段④之后、阶段⑤之前的可选终审。长文（3000+ 字）建议先 humanizer-zh 去 AI 味。

协作管线：`oral-stylizer → wechat-automator（五阶段）→ humanizer-zh → 上传`

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

### 铁律 5：上传前必须验证，验证必须排除 `<code>` 和 `<pre>`

```python
# ❌ 错误：全文搜索 <style，误判 <code>&lt;style&gt;</code> 中的内容
# ❌ 错误：全文搜索 <div，误判 <code>&lt;div&gt;</code> 中的内容

# ✅ 正确：先 strip <code> 和 <pre> 块，再验证其余部分
clean = re.sub(r'<code[^>]*>.*?</code>', '', html, flags=re.DOTALL)
clean = re.sub(r'<pre[^>]*>.*?</pre>', '', clean, flags=re.DOTALL)
# 然后在 clean 上做 <style>, <div>, class= 检查
```

---

## 安全与隐私

- API 凭据（AppID / AppSecret）优先级：环境变量 → 会话上下文 → 主动询问。仅在当前会话内存缓存，不写入任何磁盘文件
- 生成的 HTML 和草稿内容保存在本地，不经过第三方服务中转
- 上传完成后自动清理临时文件（JSON payload、自动生成的封面 PNG）
- 凭据在日志和输出中不出现明文
