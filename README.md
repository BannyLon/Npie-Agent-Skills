# Npie-Agent-Skills

一组为 Claude Code / 各类 LLM Agent 设计的通用 **Skills 集合**，帮助你把「一个聪明的大脑」变成「一套可复用的自动化工具」。

当前已内置：

- 个人食谱教练（`personal-recipe-coach`）
- 微信公众号自动化排版与发布引擎（`wechat-automator`）

所有 Skill 都遵循统一的目录结构与索引方式，方便扩展与组合。

---

## 仓库结构

```text
Npie-Agent-Skills/
├── skills/
│   ├── llms.txt              # Skill 索引：id / 名称 / 描述 / tags
│   └── wechat-automator/     # 微信公众号自动排版与发布 Skill
│       ├── SKILL.md
│       ├── README.md
│       └── scripts/
│           └── upload.py
└── personal-recipe-coach/    # 个人食谱推荐与菜谱生成 Skill
    └── SKILL.md
```

### skills/llms.txt

`llms.txt` 是所有 Skill 的「清单文件」，用于给 LLM 做检索、展示和路由。例如：

```text
# id | 名称 | 描述 | tags（英文/中文逗号分隔）
personal-recipe-coach | 个人食谱助手 | 个人食谱推荐与菜谱生成助手 | recipe,food,cooking,菜谱,做饭
wechat-automator      | 微信公众号排版与自动发布 | 一站式将 Markdown 优化排版并上传至公众号草稿箱的自动化 Skill | wechat,公众号,排版,自动化,bot
```

上层 Agent 可以按 `id` 精确调用，也可以按 `tags` 做语义检索或推荐。

---

## 已包含的 Skills

### 1. personal-recipe-coach

**定位：** 个人食谱推荐与菜谱生成助手。  
**场景示例：**

- 根据「冰箱里现有食材」自动组合可做菜品
- 按「热量 / 蛋白质 / 碳水」约束生成一日三餐方案
- 将零散的做饭想法整理成标准菜谱（含步骤与备料）

详见该目录下的 `SKILL.md` 使用说明。

---

### 2. wechat-automator

**定位：** 一站式微信公众号内容资产化引擎 —— 把短期流量（视频 / 笔记 / 碎片资料）转化为长期内容复利。

**核心能力：**

1. 内容脱水：去掉口语填充、重复表述，提炼核心观点  
2. 结构重组：重构钩子开头、正文骨架与结尾 CTA  
3. 视觉增强：自动插入概念卡片、流程卡片、数据表格、金句模块、截图位等  
4. 排版渲染：基于微信富文本编辑器限制，生成「零 div + 全 inline style」的安全 HTML  
5. 一键上传：自动生成封面，上传素材库并创建公众号草稿

一句话命令：「帮我把这篇排版发公众号」，即可走完「优化 → 排版 → 上传」全链路。  
更多使用细节见 `skills/wechat-automator/README.md`。

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
   cp -r skills/wechat-automator ~/.claude/skills/wechat-automator
   ```

3. 根据各 Skill 的 `SKILL.md` / `README.md` 配置环境变量、依赖等。

---

## 规划与贡献

后续计划补充更多面向个人效率与内容工作的通用 Skill，例如：

- 文本口述整理 / 笔记结构化
- 长文去 AI 味 + 风格统一
- 其他常见工具链（Notion / 飞书 / 邮件等）的轻量自动化

欢迎：

- Fork 本仓库，按同样结构增加你自己的 Skill
- 提交 PR：补充文档、改进现有逻辑或添加新的自动化模块
- 在 Issue 中讨论 Skill 设计和组合方式

---

## 许可证

本仓库采用 MIT 许可证。你可以在遵守协议的前提下自由使用、修改和分发。
