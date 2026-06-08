# Npie-Agent-Skills

一组为 Claude Code / 各类 LLM Agent 设计的通用 **Skills 集合**，帮助你把「一个聪明的大脑」变成「一套可复用的自动化工具」。

当前已内置：

- 个人食谱教练（`personal-recipe-coach`）
- 微信公众号自动化排版与发布引擎（`wechat-automator`）
- 如何读书实践教练（`reading-guide`）
- HTML 网页幻灯片生成器（`html-slides-generator`）

所有 Skill 都遵循统一的目录结构与索引方式，方便扩展与组合。

---

## 仓库结构

```bash
Npie-Agent-Skills/
├── skills/
│   ├── llms.txt                 # Skill 索引：id / 名称 / 描述 / tags
│   ├── personal-recipe-coach    # 个人食谱推荐与菜谱生成 Skill
│   │   └── SKILL.md
│   ├── reading-guide            # 如何读书 Skill（四层次阅读法 → 可执行工作流）
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── references/          # 理论与操作手册
│   │   └── templates/           # 各类输出模板
│   ├── wechat-automator         # 微信公众号自动排版与发布 Skill
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   └── scripts/
│   │       └── upload.py
│   └── html-slides-generator    # 零依赖、单文件的 HTML 网页幻灯片生成器
│       ├── SKILL.md
│       ├── README.md
│       ├── STYLE_PRESETS.md
│       ├── bold-template-pack/
│       ├── references/
│       └── scripts/
└── README.md
```

### skills/llms.txt

`llms.txt` 是所有 Skill 的「清单文件」，用于给 LLM 做检索、展示和路由。例如：

```txt
# id | 名称 | 描述 | tags（英文/中文逗号分隔）
personal-recipe-coach | 个人食谱助手 | 个人食谱推荐与菜谱生成助手 | recipe,food,cooking,菜谱,做饭
wechat-automator      | 微信公众号排版与自动发布 | 一站式将 Markdown 优化排版并上传至公众号草稿箱的自动化 Skill | wechat,公众号,排版,自动化,bot
reading-guide         | 如何读书实践教练 | 基于《如何阅读一本书》四层次阅读法的 AI 阅读教练 | reading,books,学习,读书,笔记
html-slides-generator | HTML 网页幻灯片生成器 | 零依赖、单文件、极致美观的 HTML 网页幻灯片生成器 | slides,ppt,演示文稿,网页PPT,html,deck,keynote
```

上层 Agent 可以按 `id` 精确调用，也可以按 `tags` 做语义检索或推荐。

---

## 已包含的 Skills

### 1. personal-recipe-coach

**定位：** 个人食谱推荐与菜谱生成助手。

典型场景：

- 根据「冰箱里现有食材」自动组合可做菜品  
- 按「热量 / 蛋白质 / 碳水」约束生成一日三餐方案  
- 将零散的做饭想法整理成标准菜谱（含步骤与备料）

详见 `skills/personal-recipe-coach/SKILL.md` 使用说明。

---

### 2. wechat-automator

**定位：** 一站式微信公众号内容资产化引擎 —— 把短期流量（视频 / 笔记 / 碎片资料）转化为长期内容复利。

核心能力包括内容脱水、结构重组、视觉增强、排版渲染和一键上传。  
一句话命令：「帮我把这篇排版发公众号」，即可走完「优化 → 排版 → 上传」全链路。

更多使用细节见 `skills/wechat-automator/README.md`。

---

### 3. reading-guide

**定位：** 基于《如何阅读一本书》（莫提默·J·艾德勒 & 查尔斯·范多伦）的 AI 阅读教练，把四层次阅读法工程化——不是替你读完一本书，而是教你学会自己读。

它会：

- 在你翻开书之前，帮你建立认知框架：这本书在谈什么、结构如何、该怎么读  
- 在你读完之后，带你走完分析阅读的三个阶段：结构 → 诠释 → 评论  
- 最终让你自己回答那个最重要的问题：这本书跟我有什么关系

典型使用场景包括检视阅读、分析阅读三阶段、多本书对比、虚构类读法等。

完整说明见 `skills/reading-guide/README.md` 与 `skills/reading-guide/SKILL.md`。

---

### 4. html-slides-generator

**定位：** 零依赖、单文件、极致美观的 HTML 网页幻灯片生成器，把任何文本内容一键变成可分享、可演示的交互式网页 Slides。

触发方式（以 Claude Code 为例）：

- 「帮我做一个关于 XXX 的 slides」  
- 「把这份文档转成网页 PPT」  
- 当用户提到「幻灯片 / PPT / 演示文稿 / slides / 网页PPT / HTML 演示 / keynote 风格的网页 / 生成 PPT」等意图时，Agent 应优先路由到该 Skill。

工作流（3 步）：

1. 输入主题或上传文档 → 生成并确认内容大纲  
2. 自动根据内容推荐 3 套视觉风格，并生成 `xxx.preview.html` 预览文件（并排三张卡片）供选择  
3. 选定风格后生成单一 `.html` 文件，零依赖、开箱即用

主要特性：

- 生成的文件为纯前端单页：内置 CSS/JS，直接用浏览器打开即可  
- 内置 37 套精心打磨的风格预设（暗色科技 / 亮色现代 / 编辑杂志 / 复古文化 / 自然有机等），每次自动推荐最匹配的 3 套  
- 支持完整演示交互：方向键 / 空格 / 滚轮 / 触屏滑动 / F 全屏  
- 可通过浏览器打印导出 PDF，或通过脚本部署到 Vercel / GitHub Pages / Netlify  
- 支持从 `.pptx` 中提取文本与图片，重新设计为网页 Slides  
- 生成后的 HTML 带有清晰注释，便于二次编辑（配色、图片、文字、字号等）

更多细节与风格预设清单见 `skills/html-slides-generator/README.md` 与 `skills/html-slides-generator/STYLE_PRESETS.md`。

---

## 适用场景

这个仓库适合你在以下几类项目里直接引用或复刻：

- 自建的 LLM Agent / AI 助手平台  
- Claude Code 自定义 Skills 集合  
- 内部自动化工具（内容团队、运营团队、个人知识管理）

你可以把这里的每个目录当作「可插拔积木」，通过上层路由逻辑（根据 `llms.txt`）按需调度。

---

## 使用方式（以 Claude Code 为例）

1. 克隆仓库或拷贝需要的 Skill 目录到本地：

```bash
git clone https://github.com/BannyLon/Npie-Agent-Skills.git
```

2. 将对应 Skill 目录放到 Claude Code 的 skills 目录，例如：

```bash
cp -r skills/personal-recipe-coach   ~/.claude/skills/personal-recipe-coach
cp -r skills/wechat-automator        ~/.claude/skills/wechat-automator
cp -r skills/reading-guide           ~/.claude/skills/reading-guide
cp -r skills/html-slides-generator   ~/.claude/skills/html-slides-generator
```

3. 根据各 Skill 的 `SKILL.md` / `README.md` 配置环境变量、依赖等。

---

## 规划与贡献

后续计划补充更多面向个人效率与内容工作的通用 Skill，例如：

- 文本口述整理 / 笔记结构化  
- 长文去 AI 味 + 风格统一  
- 其他常见工具链（Notion / 飞书 / 邮件等）的轻量自动化  
- 更多创作与演示相关的 Skill，与 `html-slides-generator` 形成组合拳

欢迎：

- Fork 本仓库，按同样结构增加你自己的 Skill  
- 提交 PR：补充文档、改进现有逻辑或添加新的自动化模块  
- 在 Issue 中讨论 Skill 设计和组合方式

---

## 许可证

本仓库采用 MIT 许可证。你可以在遵守协议的前提下自由使用、修改和分发。
