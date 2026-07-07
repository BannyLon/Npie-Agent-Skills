# wechat-automator v2.0

> 一站式微信公众号内容资产化引擎 — 把短期流量转化为长期内容复利。
>
> 🧑‍🎨 设计者：**嗯哌AI (NpieAI)**

`wechat-automator` 是一个 Claude Code Skill，将**内容深度优化**、**精排版渲染**、**一键推送草稿箱**整合为一条三阶段自动化流水线。说一句「发公众号」，从 Markdown 到草稿箱全部搞定。

---

## 效果预览

![12 套排版主题效果预览](img/Layout_style.png)

---

## 它能做什么

```
你给一个文件 + 说一句「发公众号」
         ↓
  ⓪ 内容优化：脱水 + 结构重组 + 去 AI 味 → 🔴 你确认
  ① 排版渲染：预处理 → 类型判定 → 12 套预览对比 → 🔴 你确认类型 → 🔴 你选排版
  ② 一键发布：上传头图+封面 → 创建草稿
         ↓
  打开公众号后台 → 预览 → 群发 ✅
```

**核心差异化**：不是换颜色的排版工具。v2.0 拥有 **12 套异构排版系统**，每套都有独立的 HTML 骨架、组件库和视觉语言——同一篇文章用书信流和票据风排出来，是两种完全不同的阅读体验。

---

## 12 套精选排版主题

| 预设 | 布局 | 配色 | 适用场景 |
|------|------|------|---------|
| `teal` 青蓝经典 | classic 经典左线 | teal-gold 青蓝金 | 通用深度分析、工具盘点——左粗线分区清晰，百搭款 |
| `navy` 深蓝杂志 | editorial 杂志流 | navy-coral 深蓝珊瑚 | 商业评论、行业分析、数据报告——大标题+装饰线，专业感 |
| `forest` 森语手册 | guide 手册流 | forest-amber 森语琥珀 | 教程指南、操作步骤——编号步骤+提示框+对比 |
| `plum` 梅紫卡片 | cardflow 卡片流 | plum-sage 梅紫灰绿 | 产品介绍、工具清单——每段独立成卡，模块化可扫描 |
| `slate` 岩灰书信 | letter 书信流 | slate-rose 岩灰玫瑰 | 个人随笔、读书感悟、生活故事——极简亲密对话感 |
| `amber` 暖金工坊 | workshop 极客流 | forest-amber 森语琥珀 | 技术编程、AI 实战——深色实验台+Prompt 卡+工具徽章 |
| `moyu` 摸鱼杂志 | moyu 摸鱼杂志 | emerald 摸鱼绿 | 教程测评、工具盘点——翠绿卡片+黄色高亮+虚线引用，杂志快讯感 |
| `ruby` 红白编辑 | red-editorial 红白编辑 | crimson 红白编辑 | 观点分析、读书感悟、人物特稿——正红点睛+戏剧引言卡，经典编辑风 |
| `graph` 素砚 | graphite 素砚 | graphite 素砚 | 设计评论、科技观点、高端品牌——全灰阶+1px 细线，极致克制理性 |
| `zen` 虚白 | zen 虚白 | zen 虚白 | 深度随笔、读书笔记、禅意思考——虚室生白+大呼吸感，极简留白 |
| `ticket` 票根 | ticket 票根 | ticket 票根 | 工具对比、创意测评——票据隐喻+硬阴影+撕票虚线，仪式感满分 |
| `olive` 墨帖 | olive 墨帖 | olive 墨帖 | 案例复盘、深度评测、内刊手记——墨色深底+暖橙点睛，编辑质感 |

### 按场景速查

| 你的内容类型 | 推荐预设 |
|-------------|---------|
| 📖 读书笔记/个人感悟 | `slate` 岩灰书信 · `zen` 虚白 · `ruby` 红白编辑 |
| 📊 商业分析/行业评论 | `navy` 深蓝杂志 · `graph` 素砚 |
| 📝 教程/操作指南 | `forest` 森语手册 · `amber` 暖金工坊 · `moyu` 摸鱼杂志 |
| 🛠️ 工具盘点/产品介绍 | `plum` 梅紫卡片 · `moyu` 摸鱼杂志 · `ticket` 票根 |
| 💡 深度观点/评论 | `teal` 青蓝经典 · `ruby` 红白编辑 · `olive` 墨帖 |
| 🔬 案例复盘/项目总结 | `olive` 墨帖 · `forest` 森语手册 · `amber` 暖金工坊 |
| 🎨 设计/科技/高端品牌 | `graph` 素砚 · `navy` 深蓝杂志 |

---

## 快速开始

### 安装

```bash
cp -r wechat-automator/ ~/.claude/skills/wechat-automator/
```

### 可选：设置凭据环境变量

```bash
export WEIXIN_APPID="你的公众号 AppID"
export WEIXIN_APPSECRET="你的公众号 AppSecret"
```

凭据获取：公众号后台 → 开发 → 基本配置。不设环境变量也可以，用到时 Claude 会问你。

### 准备封面和头图

将你的品牌封面图和头图放入 `img/` 目录：

```
img/
├── cover.png         # 推文封面（1080×1080px，1:1）
└── header_image.png  # 正文顶部头图（宽度 677px）
```

两个文件都会被自动上传到微信 CDN 并注入正文。如果缺失，封面会自动生成品牌纯色图 fallback。

### 触发方式

说人话就行：

| 你说的话 | 效果 |
|----------|------|
| 「帮我把这篇排版发公众号」 | 完整三阶段：优化 → 排版 → 上传 |
| 「这个脚本转成推文」 | 同上 |
| 「排版看看效果，先不发」 | 仅排版预览，输出 HTML 文件 |
| 「严格按原文排版发草稿箱」 | 跳过内容修改，仅排版上传 |
| 「用暖色系排版发公众号」 | 自动匹配主题 |

### 豁免内容修改

用以下关键词跳过优化阶段（排版仍执行）：

`一字不改` `原封不动` `严格按原文` `不要修改内容` `仅排版` `只排版` `纯排版`

---

## 三阶段工作流

### ⓪ 内容优化（可豁免）

1. **脱水**：去冗余、提论点、压密度（信息密度 +30-50%）
2. **重组**：钩子开头 + 正文骨架 + CTA 结尾
3. **去 AI 味**：调用 humanizer-zh 审阅

🔴 优化完成后暂停，等你确认内容。

### ① 排版渲染（始终执行）

```
①.0 智能预处理（章节编号+英文标签+关键词标记+目录提取+引言高亮+署名）
  ↓
①.1 🔴 文章类型判定（AI 判定 + 列出 7 种类型供选择）→ 等你确认
  ↓
①.2 🔴 排版推荐 + 12 套预览对比（浏览器四栏对比）→ 等你选择
  ↓
①.3 生成 class-based HTML（选定布局专属结构 + v2.0 组件配方）
  ↓
①.4 build_inline.py 渲染（<span leaf=""> 自动包裹 + 强制校验）
```

### ② 一键发布（按需执行）

`upload.py` 自动完成：上传头图到 CDN → 注入正文顶部 → 底部留白 → 上传封面 → 创建草稿 → 返回 media_id。

---

## v2.0 核心特性

### 三层视觉层级

| 层级 | 手段 | 频率 |
|------|------|------|
| 🔴 锚点层 | `.anchor-bold` 主色加粗 `.anchor-block` 主色底白字 | 全文 ≤5 处 |
| 🟡 标记层 | `.kw-underline` 主题色下划线（默认） `.highlight-marker` 荧光笔 | 每段 1-3 处 |
| ⚪ 容器层 | `.golden-quote` 金句 `.flow-row` 流程卡 `.tl-row` 时间线 `.cover-card` 封面卡 | 点缀 ≤3 种/篇 |

### 智能主动标记

AI 不等用户写标记，主动为文章做信息导航：
- 章节自动编号（01/02/03…∞）
- 英文标签生成（WORDS/MORALITY/SILENCE…）
- 每段关键词下划线标记
- 引言金句高亮
- 目录看点提取（前 3 章）

### v2.0 通用组件库

| 组件 | 用途 |
|------|------|
| `.tag-step` `.tag-case` `.tag-skill` | 内容类型标签 |
| `.flow-row` `.flow-active` `.flow-inactive` | 三步流程卡片 |
| `.tl-row` `.tl-dot-circle` `.tl-dot-line` | 时间线 |
| `.end-divider` | END 章节分割线 |
| `.cover-card` `.cover-tag` `.cover-title` | 文章封面卡 |
| `.info-note` | 信息旁注 |
| `.pill-capsule` | 胶囊列表 |
| `.cta-triple` `.cta-action` | CTA 三连互动区 |

### `<span leaf="">` 自动包裹（v1.9.0）

`build_inline.py` 自动为所有文本节点包裹 `<span leaf="">`，防止微信剥离样式。`validate_output()` 强制校验，leaf 包裹为 0 时报错。

---

## 排版系统对比

同一篇文章用不同排版系统，**golden-quote（金句）** 的渲染完全不同：

| 布局 | 金句风格 |
|------|---------|
| `classic` 经典左线 | 圆角蓝底居中卡片 |
| `cardflow` 卡片流 | 卡片底部横幅 |
| `editorial` 杂志流 | 上下装饰线+大号居中 |
| `guide` 手册流 | 深色满底反白块 |
| `letter` 书信流 | 无底无边框，纯文字加大加粗 |
| `workshop` 极客流 | 深色实验台+对比色文字 |
| `moyu` 摸鱼杂志 | 绿色虚线卡片+黄色下划线 |
| `red-editorial` 红白编辑 | 粉底左竖条+深红字 |
| `graphite` 素砚 | 上下 1px 细线，无底色 |
| `zen` 虚白 | 上下细线+大呼吸感，衬线体 |
| `ticket` 票根 | 硬阴影边框，票据仪式感 |
| `olive` 墨帖 | 橙左边条+米白纸感底 |

---

## 使用方式

```bash
# 预设组合
build_inline.py in.html out.html --theme zen

# 自由混搭（12×12=144 种组合）
build_inline.py in.html out.html --layout zen --palette slate-rose

# 自定义主色（默认 classic 布局，自动推导配色）
build_inline.py in.html out.html --theme "#e63946"
```

---

## 微信兼容性

基于生产环境实测得出的硬约束：

| 规则 | 原因 |
|------|------|
| 零 `<style>` 标签 | 微信完全删除 |
| 零 `class` 属性 | 微信完全剥离 |
| 零 `<div>` 元素 | 微信转为裸 `<p>` |
| `<span leaf="">` 包裹所有文本 | 防样式剥离 |
| 纯色背景 | `linear-gradient` 会被删除 |
| 禁止 `<pre>` | 换行全部丢失 |
| `<blockquote>` ≤300 字 | 微信有隐性字数上限 |

所有约束已内建在 `build_inline.py` 的验证逻辑中，输出自动检查。

---

## 与其它 Skill 协作

```
oral-stylizer → wechat-automator → humanizer-zh
（口述整理）    （排版发布）        （去 AI 味）
```

三者都是软依赖——有则调用，无则跳过。

---

## 文件结构

```
wechat-automator/
├── SKILL.md                  # Skill 定义（三阶段流水线 + 铁律 + 技术规范）
├── README.md                 # 本文件
├── img/
│   ├── cover.png             # 推文封面
│   ├── header_image.png      # 正文头图
│   └── Layout_style.png      # 12 套主题效果预览
├── output/
│   ├── article-class-html.html   # （中间产物）class-based HTML
│   ├── article-inline.html       # （中间产物）微信兼容 inline HTML
│   └── theme-preview.html        # （生成物）12 套排版浏览器预览页
└── scripts/
    ├── build_inline.py       # 排版引擎：Layout×Palette → inline HTML + leaf 包裹
    ├── preview_themes.py     # 预览生成器：12 套布局专属结构样本对比
    └── upload.py             # 上传工具：头图+封面+草稿箱
```

---

## 版本历史

| 版本 | 关键更新 |
|------|---------|
| v2.0 | 6 套新主题（配色+布局+通用组件库）；12 套布局专属 HTML 骨架；预览页四栏对比；文章类型判定→排版推荐两阶段确认流程 |
| v1.9.0 | `<span leaf="">` 自动包裹；validate_output 强制校验 |
| v1.8.0 | 三层视觉层级体系；智能主动标记（章节编号/关键词下划线/英文标签）；文章类型判定；12 个智能标记 CSS 类 |
| v1.7.0 | 三阶段管线定型；铁律系统建立；upload.py 头图+封面上传 |
| v1.0-v1.6 | 6 套异构排版系统；5 套配色方案；class→inline 转换引擎；预览对比页 |

---

## 依赖

- Python 3.8+
- `requests`：`pip install requests`
- 一个已认证的微信公众号（AppID + AppSecret）

---

## 许可证

MIT
