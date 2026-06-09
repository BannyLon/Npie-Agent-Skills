#!/usr/bin/env python3
"""Generate WeChat-safe HTML from markdown and upload to draft box."""

import json
import struct
import sys
import zlib
import os

import requests

# ============================================================
# Configuration
# ============================================================
APPID = "wxfe5a95a913482f81"
APPSECRET = "3b4a0d4ec3bd74257ae9e81a534c721a"

MARKDOWN_FILE = os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/嗯哌-知识库/Script/开源三个skill-公众号推文-final.md"
)
HTML_OUTPUT = os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/嗯哌-知识库/Script/开源三个skill-公众号推文-formatted.html"
)
PAYLOAD_FILE = "/tmp/wechat_payload.json"
COVER_FILE = "/tmp/cover.png"

TITLE = "我把三个「吃饭的家伙」开源了——每个都是被现实反复毒打出来的"
AUTHOR = "嗯哌"
DIGEST = "分享我最近开源的三个Claude Code Skill：公众号排版引擎、AI阅读教练、网页幻灯片生成器，每个都是被真实业务需求磨出来的。"

# ============================================================
# Inline Style Constants (zero div, zero class, all inline)
# ============================================================

BODY_STYLE = (
    "background-color:#f5f5f5;"
    "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC',"
    "'Hiragino Sans GB','Microsoft YaHei','Helvetica Neue',sans-serif;"
    "color:#3f3f3f;-webkit-font-smoothing:antialiased;margin:0;padding:0;"
)

WRAPPER_STYLE = (
    "max-width:677px;margin:0 auto;padding:32px 20px 48px;background-color:#ffffff;"
)

H2_STYLE = (
    "margin:44px 0 22px;padding:14px 18px;font-size:19px;font-weight:700;"
    "line-height:1.5;color:#1a1a1a;background-color:#e8f4f8;"
    "border-left:4px solid #0d7377;border-radius:0 6px 6px 0;"
)

H3_STYLE = (
    "margin:34px 0 16px;padding:0 0 12px;font-size:17px;font-weight:700;"
    "color:#2c3e50;border-bottom:2px solid #e0e7ef;line-height:1.5;"
)

P_STYLE = (
    "margin:0 0 16px;font-size:15px;line-height:1.9;color:#3f3f3f;text-align:justify;"
)

P_CENTER_STYLE = (
    "margin:0 0 16px;font-size:15px;line-height:1.9;color:#3f3f3f;text-align:center;"
)

STRONG_STYLE = "color:#212121;font-weight:700;"

BLOCKQUOTE_STYLE = (
    "margin:20px 0;padding:18px 20px 18px 22px;background-color:#f7fafc;"
    "border-left:3px solid #0d7377;border-radius:0 8px 8px 0;"
    "color:#4a5a6a;font-size:14px;line-height:1.8;"
)

BLOCKQUOTE_P_STYLE = (
    "margin:0 0 8px;font-size:14px;line-height:1.8;color:#4a5a6a;text-align:justify;"
)

CODE_STYLE = (
    "padding:2px 6px;font-family:'SF Mono','Menlo','Monaco','Courier New',monospace;"
    "font-size:13px;color:#c7254e;background-color:#f9f2f4;border-radius:3px;"
)

PRE_STYLE = (
    "margin:18px 0;padding:18px 20px;background-color:#282c34;color:#abb2bf;"
    "border-radius:8px;overflow-x:auto;font-size:13px;line-height:1.8;"
)

PRE_CODE_STYLE = "font-size:13px;line-height:1.8;"

GOLDEN_QUOTE_STYLE = (
    "margin:30px 0;padding:26px 28px;background-color:#d4edf5;border-radius:12px;"
    "text-align:center;font-size:17px;font-weight:700;line-height:1.9;color:#0d7377;"
)

GOLDEN_QUOTE_P_STYLE = (
    "margin:0;font-size:17px;font-weight:700;line-height:1.9;color:#0d7377;text-align:center;"
)

HIGHLIGHT_BOX_STYLE = (
    "margin:24px 0;padding:20px 22px;background-color:#f7fafc;border-radius:10px;"
    "border:1px solid #e0e7ef;font-size:15px;line-height:1.9;color:#2c3e50;"
)

HIGHLIGHT_BOX_STRONG_STYLE = "color:#0d7377;font-weight:700;"

CTA_FOOTER_STYLE = (
    "margin-top:44px;padding:28px 24px;background-color:#d4edf5;border-radius:14px;"
    "text-align:center;"
)

CTA_P_STYLE = (
    "margin:0 0 8px;font-size:15px;font-weight:500;line-height:1.9;"
    "color:#0d7377;text-align:center;"
)

CTA_STRONG_STYLE = "color:#0d7377;font-weight:700;font-size:16px;"

HR_STYLE = "margin:36px 0;border:none;height:1px;background-color:#dce3ea;"

EDITOR_NOTE_STYLE = (
    "margin:14px 0;padding:8px 14px;font-size:13px;color:#8a9aaa;"
    "font-style:italic;border-left:2px solid #dce3ea;"
)

TABLE_STYLE = (
    "width:100%;margin:20px 0;border-collapse:collapse;font-size:13px;line-height:1.7;"
)

TH_STYLE = (
    "padding:12px 14px;background-color:#e8f4f8;color:#1a1a1a;"
    "font-weight:700;text-align:left;border:1px solid #dce3ea;"
)

TD_STYLE = "padding:12px 14px;border:1px solid #e8ecf1;color:#3f3f3f;"

CARD_ITEM_STYLE = (
    "margin-bottom:10px;padding:15px 18px;background-color:#fafbfc;"
    "border:1px solid #e8ecf1;border-radius:8px;font-size:14px;line-height:1.8;color:#3f3f3f;"
)

# ============================================================
# Helper Functions
# ============================================================

def tag(tag_name, style, content="", void=False):
    """Build an HTML element with inline style, zero class."""
    if void:
        return f"<{tag_name} style=\"{style}\" />"
    return f"<{tag_name} style=\"{style}\">{content}</{tag_name}>"

def p(text, center=False):
    """Paragraph with inline style."""
    s = P_CENTER_STYLE if center else P_STYLE
    # Process inline formatting
    text = process_inline(text)
    return tag("p", s, text)

def process_inline(text):
    """Process inline markdown: **bold**, `code`."""
    import re
    # bold
    text = re.sub(
        r'\*\*(.+?)\*\*',
        lambda m: f'<strong style="{STRONG_STYLE}">{m.group(1)}</strong>',
        text
    )
    # inline code
    text = re.sub(
        r'`([^`]+)`',
        lambda m: f'<code style="{CODE_STYLE}">{m.group(1)}</code>',
        text
    )
    # arrow →
    text = text.replace(' → ', ' → ')
    # emoji
    text = text.replace('✅', '✅')
    text = text.replace('⭐', '⭐')
    text = text.replace('🖼', '🖼')
    text = text.replace('📇', '📇')
    text = text.replace('🧠', '🧠')
    text = text.replace('📋', '📋')
    text = text.replace('📚', '📚')
    text = text.replace('🔔', '🔔')
    text = text.replace('❤️', '❤️')
    return text

def heading2(text):
    return tag("h2", H2_STYLE, text)

def heading3(text):
    return tag("h3", H3_STYLE, text)

def hr():
    return tag("hr", HR_STYLE, "", void=True)

def blockquote(text):
    lines = text.strip().split('\n')
    content = ''.join(
        f'<p style="{BLOCKQUOTE_P_STYLE}">{process_inline(l.strip())}</p>'
        for l in lines if l.strip()
    )
    return tag("blockquote", BLOCKQUOTE_STYLE, content)

def golden_quote(text):
    return tag("blockquote", GOLDEN_QUOTE_STYLE,
               f'<p style="{GOLDEN_QUOTE_P_STYLE}">{process_inline(text)}</p>')

def highlight_box(content):
    return tag("blockquote", HIGHLIGHT_BOX_STYLE, content)

def cta_footer(text):
    lines = text.strip().split('\n')
    content = ''.join(
        f'<p style="{CTA_P_STYLE}">{process_inline(l.strip())}</p>'
        for l in lines if l.strip()
    )
    return tag("blockquote", CTA_FOOTER_STYLE, content)

def pre_block(text):
    # Escape HTML
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    code_tag = tag("code", PRE_CODE_STYLE, text)
    return tag("pre", PRE_STYLE, code_tag)

def editor_note(text):
    return tag("p", EDITOR_NOTE_STYLE, process_inline(text))

def card_item(text):
    return tag("p", CARD_ITEM_STYLE, process_inline(text))

# ============================================================
# Article HTML Generation
# ============================================================

def generate_html():
    """Generate WeChat-safe HTML from the article markdown."""

    # Read the markdown file
    with open(MARKDOWN_FILE, "r", encoding="utf-8") as f:
        md = f.read()

    parts = []

    # ---------- TOP EMPTY LINE (user requirement) ----------
    parts.append('<p style="margin:0 0 16px;font-size:15px;line-height:1.9;color:#3f3f3f;"><br></p>')

    # ---------- TITLE (H2-style hero) ----------
    parts.append(heading2("我把三个「吃饭的家伙」开源了——每个都是被现实反复毒打出来的"))

    # ---------- 先说点背景 ----------
    parts.append(p("给你们看下我的 GitHub。目前两个项目库，其中一个已经 2.6K stars。"))
    parts.append(p("自从有了 Claude Code、Codex 这种 coding agent，我做东西的速度直接起飞。Dify 工作流、各种 skills、轻量小应用，一个接一个往外丢。GitHub 对我来说早就不只是放代码的地方了，它更像是一种对外的表达——我把想法和审美，用 coding agent 沉淀成产品或者 skill，然后丢上去。"))
    parts.append(p("有人直接拿去用，有人在 issues 里提需求，有人提 PR 跟我一起打磨。这些反馈又会反过来推着我把东西做得更完整。"))
    parts.append(p("说句实话，有 coding agent 加持之后，GitHub 越来越像一个「互动型博客」。跟你会不会写代码关系不大了。代码 AI 能写，项目文件能一键上传。我们真正需要花力气的，是产品逻辑和体验本身：决定做什么，做完怎么分发，怎么吸引对的人，怎么让他们理解这个东西的价值。"))
    parts.append(editor_note("如果你现在还不太会用 GitHub，我频道里有一期非常详细的教学，三个平台都有，自己去翻。"))
    parts.append(p("好，回到正题。今天想跟你分享我最近开源的三个 Claude Code Skill。"))

    # ---------- 这三个 Skill 是什么来头？ ----------
    parts.append(heading2("这三个 Skill 是什么来头？"))
    parts.append(p("先交个底：这三个 skill，不是我「为了开源而开源」随手做的玩具。是我自己有业务需求，被现实反复毒打，一步步从工作流里拆出来、磨出来的东西。我自己每天都在用。"))

    # Three skill intros as cards
    parts.append(card_item('<strong style="color:#0d7377;font-weight:700;">第一个，给内容创作者的一站式公众号引擎：wechat-automator。</strong><br>'
        '你只需要把一段 Markdown 或者任意原始内容丢给它，说一句「帮我排版发公众号」。'
        '它就自动帮你走完内容提炼、结构重组、视觉增强、排版渲染，最后直接上传到你的公众号草稿箱。'
        '你唯一要做的事，就是打开后台，审一眼，点发布。'))
    parts.append(card_item('<strong style="color:#0d7377;font-weight:700;">第二个，AI 阅读教练：reading-guide。</strong><br>'
        '它把《如何阅读一本书》里那套四层次阅读法，变成了随时可以召唤的工作流。'
        '翻书之前先帮你搭认知框架：这本书在讲什么、结构怎么拆、你该怎么读。'
        '读完之后再一步步带着你做结构分析、诠释、评论。逼你讲清楚三件事——'
        '作者想说什么，你同不同意，这本书跟你现在的生活和工作到底有什么关系。'))
    parts.append(card_item('<strong style="color:#0d7377;font-weight:700;">第三个，我日常演讲最常用的：html-slides-generator。</strong><br>'
        '任何一段文字，一键变网页幻灯片。不用 PowerPoint，不用纠结模板。'
        '一个 HTML 文件丢进浏览器，键盘一按，现场开讲。还能直接打印成 PDF，或者一条命令部署到 Vercel。'))

    parts.append(hr())
    parts.append(p("下面一个一个细说。", center=True))
    parts.append(hr())

    # ========== wechat-automator ==========
    parts.append(heading2("wechat-automator：从「写完」到「发布」，一步到位"))
    parts.append(p("做过公众号的人都懂这个痛：写完文章只是第一步。排版、调格式、做封面、传素材、推草稿，每一步都在磨你的耐心。"))
    parts.append(p("wechat-automator 做的事很简单：把这一整条链路压成一句话。"))

    parts.append(heading3("它到底做了什么？"))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">内容脱水。</strong> '
        '把你的口播稿、笔记、碎片素材里那些口语填充、重复论述、镜头语言全剥离，'
        '收敛成干净的核心观点。信息密度能提升 30% 到 50%，但你的表达风格它不动。'
        '这点我很在意——排版可以优化，味道不能丢。'))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">结构重组。</strong> '
        '线性内容重构为适合手机阅读的层级：钩子开头先制造信息落差，'
        '正文按教程/观点/案例/清单四种骨架来撑住，结尾给读者一个具体的行动指引。'
        '不是随便分段，是按阅读节奏来。'))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">视觉增强。</strong> '
        '这个最狠。它会自动识别哪些地方该配什么元素：关键概念给概念卡片，'
        '步骤流程给流程卡片，数据对比给响应式表格，重点结论给金句模块，'
        '工具推荐给资源卡片，界面操作标截图位。出来的不是一面文字墙，是有呼吸感的杂志级排版。'))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">排版渲染。</strong> '
        '基于微信生产环境实测的硬约束来渲染：零 <code style="' + CODE_STYLE + '">&lt;style&gt;</code> 标签、'
        '零 <code style="' + CODE_STYLE + '">class</code>、'
        '零 <code style="' + CODE_STYLE + '">&lt;div&gt;</code>，'
        '全 <code style="' + CODE_STYLE + '">style=""</code> 内联。'
        '微信会把这些全干掉，这些坑我都替你踩过了。'))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">一键上传。</strong> '
        '自动生成品牌色封面 → 上传素材库 → 创建草稿 → 返回 media_id。打开后台就能预览群发。'))

    parts.append(heading3("怎么用？"))
    parts.append(p("说人话就行，不需要精确指令："))

    parts.append(card_item('<strong>「帮我把这篇排版发公众号」</strong> → 全链路'))
    parts.append(card_item('<strong>「排版看看效果，先不发」</strong> → 仅预览'))
    parts.append(card_item('<strong>「仅排版，不需优化内容」</strong> → 跳过修改，只排版上传'))

    parts.append(p("不想让 AI 动你的原文？说一句「一字不改」，视觉增强和排版照样执行，内容原封不动。"))

    parts.append(heading3("安全"))
    parts.append(p("API 凭据只从环境变量或会话内存拿，不写磁盘。会话结束自动丢弃。上传完自动清理临时文件。凭据在日志里不出现明文。你的 AppID 和 AppSecret 不会被存在任何地方。"))

    parts.append(hr())

    # ========== reading-guide ==========
    parts.append(heading2("reading-guide：不是替你读书，是教你学会自己读"))

    parts.append(p("这个 skill 的定位，我直接引用 README 里的一句话："))

    parts.append(golden_quote("如果用户拿着报告就可以说「我懂了，不用读了」——那这个 skill 就失败了。"
        "它的成功是：你读完报告后更想读这本书，而且知道该怎么读。"))

    parts.append(p("市面上太多 AI 工具在帮你「读完」一本书。reading-guide 不干这事。"
        "它只做一件事：把莫提默·J·艾德勒《如何阅读一本书》里那套四层次阅读法，"
        "变成你随时可以召唤的 AI 阅读教练。"))

    parts.append(heading3("理论基础"))
    parts.append(p("这个 skill 是对《如何阅读一本书》的完整工程化实现。里面塞了："))

    parts.append(card_item('<strong>四个阅读层次：</strong>基础 → 检视 → 分析 → 主题'))
    parts.append(card_item('<strong>四个基本问题：</strong>这本书在谈什么？细节怎么说的？有道理吗？跟我有什么关系？'))
    parts.append(card_item('<strong>分析阅读 15 条规则：</strong>三阶段严格递进（结构 → 诠释 → 评论），不可以跳'))
    parts.append(card_item('<strong>6 类书的不同读法：</strong>实用型、想象文学、历史、科学、哲学、社会科学，各走各的路径'))
    parts.append(card_item('<strong>书的金字塔：</strong>帮你判断一本书在第几层。99.9% 的书只需要扫读，不到 100 本值得一生反复读'))

    parts.append(heading3("我最喜欢的一条铁律"))
    parts.append(p("在你真正理解之前，不准说「我同意」或「我不同意」。"))

    parts.append(highlight_box(
        '<strong style="' + HIGHLIGHT_BOX_STRONG_STYLE + '">在你真正理解之前，不准说「我同意」或「我不同意」。</strong>'
    ))
    parts.append(p("这可能是整个 skill 最值钱的部分。它在逼你做一个负责任的读者，而不是翻两页就急着发表意见。"))

    parts.append(heading3("几个典型场景"))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">想读一本书，不知道怎么下手。</strong>'))
    parts.append(p("你跟它说「我想读《思考，快与慢》，怎么读？」它搜索目录和热门划线，判断类型，"
        "产出一份 ≤400 字的检视报告。里面有核心问题、架构质量、论证可信度、难度评估，"
        "最后给你一个初步印象：精读还是跳读。但最终判断它不替你做，它会停下来问你。"))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">读完了，想消化。</strong>'))
    parts.append(p("你说「刚读完《也许你该找个人聊聊》，帮我整理。」它启动分析阅读三阶段："
        "结构 → 诠释 → 评论。每个阶段末尾都会停一下，引导你做出自己的判断。"
        "最后甩给你三个问题，不是它替你回答的那种，是你必须自己想的那种。"))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">几本书里不知道选哪本。</strong>'))
    parts.append(p("把《原子习惯》《掌控习惯》《微习惯》丢进去，它出一张对比表，"
        "告诉你每个维度上哪本更强，然后说「如果只能读一本，选这个」。但最终你选哪本，它不替你做主。"))

    parts.append(heading3("不用微信读书也能用"))
    parts.append(p("没有微信读书完全没关系。给一个书名就行，skill 会通过 Web 搜索获取公开信息。"
        "微信读书只是一个可选的数据增强：如果你在用，它可以拉取你自己的划线和笔记做个性化分析。"))

    parts.append(heading3("输出长什么样"))
    parts.append(p("每份报告四件套：快照卡片、思维导图（文字大纲 + Mermaid 可选增强）、"
        "行动清单、延伸阅读。默认交付 Markdown，存完后会提示你可以生成 HTML 视觉版。"
        "5 种风格可选，从学术严谨到暗夜影院全都有。"))

    parts.append(hr())

    # ========== html-slides-generator ==========
    parts.append(heading2("html-slides-generator：文字一键变演示，我每天在用"))
    parts.append(p("这个是我使用频率最高的一个。任何需要演示、汇报、分享的场合，"
        "我不再打开 PowerPoint。直接把文字给它，一个 HTML 文件就出来了。"))

    parts.append(heading3("三个让我离不开的点"))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">零依赖。</strong> '
        '单个 HTML 文件，所有 CSS/JS 全内嵌。不需要 npm install，不需要任何框架。'
        '一个浏览器就能跑。发给别人，双击就打开。这一点在临开会前五分钟要改 slides 的时候，你会懂的。'))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">37 个内嵌视觉预设。</strong> '
        '从暗黑科技未来到骨纸大地，从新 Brutalist 到日本卡带包装。'
        '每次自动推荐 3 个最契合内容的，还会生成一张视觉预览 HTML 让你直观对比。'
        '不用靠文字脑补配色，打开预览一看，三张卡片并排，哪个好看一目了然。'))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">16:9 固定画布，全交互。</strong> '
        '1920×1080 虚拟舞台，自动缩放适配任何屏幕。键盘/鼠标/触屏全支持，'
        'F 键全屏演示，方向键翻页。跟 Keynote 的体验差不多。'))

    parts.append(heading3("三步出片"))
    parts.append(card_item('<strong>1.</strong> 你说主题（或丢给它一个文件），它出大纲，你确认'))
    parts.append(card_item('<strong>2.</strong> 它推 3 个视觉风格并生成预览 HTML，你选 1 个'))
    parts.append(card_item('<strong>3.</strong> 吐出一个完整 HTML 文件，完事'))

    parts.append(heading3("还能干什么"))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">PPTX 转换。</strong> '
        '直接把 .pptx 文件丢给它，自动提取文本和图片，用你选的风格重新设计。'
        '以前存的那些丑陋 PPT 瞬间有救了。'))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">持续迭代。</strong> '
        '生成后随时改：「把第 3 页改成两列」「整体暗一点」「标题换衬线体」。'
        '每次都输出完整新文件，不是 diff，你可以随时保存使用。'))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">分享方便。</strong> '
        '一个 .html 文件发过去，对方双击就能看。浏览器 Ctrl+P 直接导出 PDF，'
        '或者跑一条命令部署到 Vercel。'))

    parts.append(p('<strong style="color:#0d7377;font-weight:700;">手动微调。</strong> '
        '文件里带清晰注释，搜 STYLE: 改配色，搜 IMG: 换图片，不用读懂全部代码。'
        '我不是前端出身，这个设计救了我很多次。'))

    parts.append(hr())

    # ========== 三个 Skill 串起来 ==========
    parts.append(heading2("这三个串起来是什么体验？"))
    parts.append(p("说实话，这三个 skill 之间是有配合的："))

    parts.append(pre_block(
        "口述碎碎念 → oral-stylizer → wechat-automator → humanizer-zh → 公众号草稿箱\n"
        "读书笔记 → reading-guide → html-slides-generator → 网页幻灯片 / PDF\n"
        "任意想法 → html-slides-generator → 一键部署 → 链接丢给别人"
    ))

    parts.append(p("内容从生产到发布到演示，被串成了一个完整的闭环。"))
    parts.append(p("我想做的东西就是这个方向：不是一堆散装的工具，而是它们之间能接起来，"
        "覆盖一个人从思考到输出的完整工作流。"))

    parts.append(hr())

    # ========== 接下来 ==========
    parts.append(heading2("接下来"))
    parts.append(p("这三个 skill 只是起点。后面我还会继续开源更多：口述内容整理与笔记结构化、"
        "长文去 AI 味和风格统一、跟 Obsidian/飞书/微信/邮箱打通的小型自动化链路。"))
    parts.append(p("如果你也在用 Claude Code，在搭自己的 LLM Agent，与其每次从零开始写 prompt、"
        "拼工作流，不如直接从这些在真实业务场景里打磨过的 skill 开始。"
        "拿去直接用，或者 Fork 一份，按同样的结构改成你自己的版本。"))

    # CTA Footer
    parts.append(cta_footer(
        "仓库链接我放在评论区了。\n"
        "点进去逛逛，说不定刚好补上你工作流里缺的那一块拼图。\n"
        "点个 Star ⭐，我们 GitHub 见。"
    ))

    # ---------- BOTTOM EMPTY LINE (user requirement) ----------
    parts.append('<p style="margin:0 0 16px;font-size:15px;line-height:1.9;color:#3f3f3f;"><br></p>')

    # ========== Assemble full HTML ==========
    body_content = '\n'.join(parts)

    full_html = f"""\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>{TITLE}</title>
</head>
<body style="{BODY_STYLE}">
<section style="{WRAPPER_STYLE}">
{body_content}
</section>
</body>
</html>"""

    # Validate: no <style> tags, no class=, no <div>
    errors = []
    if '<style' in full_html:
        errors.append("Found <style> tag")
    if 'class=' in full_html:
        errors.append("Found class= attribute")
    if '<div' in full_html:
        errors.append("Found <div> element")
    if 'linear-gradient' in full_html:
        errors.append("Found linear-gradient")

    if errors:
        print("❌ WeChat compatibility errors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("✅ WeChat compatibility check passed: zero <style>, zero class, zero <div>")

    # Save
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"✅ HTML saved to: {HTML_OUTPUT}")
    print(f"   File size: {len(full_html):,} bytes")

    return full_html


# ============================================================
# WeChat API Upload
# ============================================================

def get_access_token():
    """Get WeChat access token."""
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": APPID,
        "secret": APPSECRET,
    }
    resp = requests.get(url, params=params, timeout=30)
    data = resp.json()
    if "access_token" in data:
        print(f"✅ Access token obtained (expires in {data.get('expires_in', '?')}s)")
        return data["access_token"]
    else:
        print(f"❌ Failed to get access token: {data}")
        sys.exit(1)


def create_cover_png(w=1080, h=1080):
    """Generate brand-color solid PNG."""
    def chunk(ctype, data):
        c = ctype + data
        crc_val = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        return struct.pack('>I', len(data)) + c + crc_val

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


def upload_cover(access_token):
    """Upload cover image to WeChat material library."""
    png_data = create_cover_png()
    with open(COVER_FILE, "wb") as f:
        f.write(png_data)
    print(f"✅ Cover PNG generated: {COVER_FILE} ({len(png_data):,} bytes)")

    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material"
    params = {"access_token": access_token, "type": "image"}
    with open(COVER_FILE, "rb") as f:
        files = {"media": ("cover.png", f, "image/png")}
        resp = requests.post(url, params=params, files=files, timeout=60)
    data = resp.json()
    if "media_id" in data:
        print(f"✅ Cover uploaded, media_id: {data['media_id']}")
        print(f"   URL: {data.get('url', 'N/A')}")
        return data["media_id"]
    else:
        print(f"❌ Cover upload failed: {data}")
        sys.exit(1)


def create_draft(access_token, html_content, thumb_media_id):
    """Create a draft in WeChat draft box."""
    payload = {
        "articles": [{
            "title": TITLE,
            "author": AUTHOR,
            "digest": DIGEST,
            "content": html_content,
            "thumb_media_id": thumb_media_id,
            "need_open_comment": 1,
            "only_fans_can_comment": 0,
        }]
    }

    with open(PAYLOAD_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    print(f"✅ Payload saved: {PAYLOAD_FILE}")

    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    resp = requests.post(url, json=payload, headers=headers, timeout=60)
    data = resp.json()

    if "media_id" in data:
        print(f"✅ Draft created! media_id: {data['media_id']}")
        return data["media_id"]
    else:
        print(f"❌ Draft creation failed: {data}")
        errcode = data.get("errcode", 0)
        if errcode == 40001:
            print("   → Access token expired, retrying...")
            return None  # signal retry
        elif errcode == 40007:
            print("   → Invalid media_id. Check cover upload.")
        elif errcode == 40125:
            print("   → Invalid appsecret.")
        elif errcode == 45009:
            print("   → Rate limited. Wait and retry.")
        return None


def cleanup():
    """Remove temporary files."""
    for f in [PAYLOAD_FILE, COVER_FILE]:
        if os.path.exists(f):
            os.remove(f)
            print(f"🧹 Cleaned up: {f}")


# ============================================================
# Main
# ============================================================

def main():
    print("=" * 60)
    print("  WeChat Automator - Full Pipeline")
    print("=" * 60)

    # Step 1: Generate HTML
    print("\n📝 Stage ①-④: Generating WeChat-safe HTML...")
    html_content = generate_html()

    # Step 2: Get access token
    print("\n🔑 Stage ⑤a: Getting access token...")
    access_token = get_access_token()

    # Step 3: Upload cover
    print("\n🖼 Stage ⑤b: Generating & uploading cover...")
    thumb_media_id = upload_cover(access_token)

    # Step 4: Create draft
    print("\n📤 Stage ⑤c: Creating draft...")
    media_id = create_draft(access_token, html_content, thumb_media_id)

    if media_id is None:
        # Retry with new token
        print("\n🔄 Retrying with fresh token...")
        access_token = get_access_token()
        media_id = create_draft(access_token, html_content, thumb_media_id)

    if media_id:
        print("\n" + "=" * 60)
        print("  🎉 SUCCESS! Draft is ready.")
        print(f"  Media ID: {media_id}")
        print("  Next: 打开公众号后台 → 草稿箱 → 预览 → 群发")
        print("=" * 60)
    else:
        print("\n❌ Upload failed. Check errors above.")
        sys.exit(1)

    # Cleanup
    cleanup()
    print("\n✅ Done.")


if __name__ == "__main__":
    main()
