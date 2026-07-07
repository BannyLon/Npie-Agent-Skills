#!/usr/bin/env python3
"""
阶段④ 排版渲染：class-based HTML → inline style HTML
v1.9.0: <span leaf=""> 自动包裹（微信防样式剥离）
v1.8.0: 三层视觉层级 CSS 类 + 文章类型判定
v1.5.0: 5套真正异构排版系统 — 每套有独立的组件库、HTML结构、视觉语言

Layouts: classic | cardflow | editorial | guide | letter | workshop
Palettes: teal-gold | navy-coral | forest-amber | plum-sage | slate-rose
Presets: teal/navy/forest/plum/slate/amber (向后兼容)

铁律 2/3/4/5/7/13 贯穿始终。
"""
import sys, os, re
from html.parser import HTMLParser

# ══════════════════════════════════════════════════════════
# 配色方案 (5 套多对比色，16 token/套)
# ══════════════════════════════════════════════════════════

PALETTES = {
    "teal-gold":   {"name":"青蓝金","desc":"冷青蓝×暖琥珀金","primary":"#0d7377","contrast":"#c8940a","bg_light":"#e8f4f8","bg_warm":"#fef8f0","bg_dark":"#0a4d50","bg_dark_alt":"#3d2e00","text_on_dark":"#e8f4f8","text_dark":"#1a1a1a","text_body":"#3f3f3f","text_muted":"#8a9aaa","border":"#e0e7ef","border_light":"#dce3ea","card_bg":"#fafbfc","code_bg":"#f9f2f4","code_color":"#c7254e","white":"#ffffff","body_bg":"#f5f5f5","warn_bg":"#fff8f0","warn_border":"#e8a838","tip_bg":"#f0faf6","tip_border":"#4aaf87",},
    "navy-coral":  {"name":"深蓝珊瑚","desc":"深海蓝×暖珊瑚红","primary":"#2c3e6b","contrast":"#d4685c","bg_light":"#edf0f7","bg_warm":"#fdf5f4","bg_dark":"#1a2747","bg_dark_alt":"#5c1e19","text_on_dark":"#edf0f7","text_dark":"#1a1a1a","text_body":"#3f3f3f","text_muted":"#8a8f9a","border":"#dde1ed","border_light":"#d5dae5","card_bg":"#fafbfd","code_bg":"#fdf2f2","code_color":"#c0392b","white":"#ffffff","body_bg":"#f5f5f5","warn_bg":"#fff5f4","warn_border":"#e87060","tip_bg":"#f0f4fa","tip_border":"#5a7db8",},
    "forest-amber":{"name":"森语琥珀","desc":"深林绿×暖琥珀","primary":"#2d6a4f","contrast":"#d4923a","bg_light":"#e8f5ee","bg_warm":"#fef9f2","bg_dark":"#1a4230","bg_dark_alt":"#4a2d0a","text_on_dark":"#e8f5ee","text_dark":"#1a1a1a","text_body":"#3f3f3f","text_muted":"#8a9a90","border":"#d5e8dc","border_light":"#c8ddd0","card_bg":"#fafcfa","code_bg":"#f2f9f4","code_color":"#1e7a42","white":"#ffffff","body_bg":"#f5f5f5","warn_bg":"#fff9f0","warn_border":"#e0a040","tip_bg":"#f0f8f4","tip_border":"#5aaf80",},
    "plum-sage":   {"name":"梅紫灰绿","desc":"梅子紫×灰鼠尾草绿","primary":"#7c3a8c","contrast":"#6b8b7a","bg_light":"#f5edf8","bg_warm":"#f2f7f4","bg_dark":"#3d1a46","bg_dark_alt":"#2d4035","text_on_dark":"#f5edf8","text_dark":"#1a1a1a","text_body":"#3f3f3f","text_muted":"#9a8f9e","border":"#e5dded","border_light":"#dcd0e5","card_bg":"#faf9fb","code_bg":"#f8f2f9","code_color":"#8b3a7c","white":"#ffffff","body_bg":"#f5f5f5","warn_bg":"#faf2f8","warn_border":"#b060a0","tip_bg":"#f2f8f4","tip_border":"#78a888",},
    "slate-rose":  {"name":"岩灰玫瑰","desc":"都市岩灰×干枯玫瑰","primary":"#4a5568","contrast":"#c57080","bg_light":"#f0f2f5","bg_warm":"#fdf6f7","bg_dark":"#2d3545","bg_dark_alt":"#5c3038","text_on_dark":"#f0f2f5","text_dark":"#1a1a1a","text_body":"#3f3f3f","text_muted":"#8a8f98","border":"#e2e5ea","border_light":"#d5d9df","card_bg":"#fafbfc","code_bg":"#fdf5f6","code_color":"#b85060","white":"#ffffff","body_bg":"#f5f5f5","warn_bg":"#fdf6f6","warn_border":"#d08890","tip_bg":"#f2f4f6","tip_border":"#8090a0",},
    # v2.0: 新增配色方案
    "emerald":     {"name":"摸鱼绿","desc":"翡翠绿×暖黄高亮，杂志卡片风","primary":"#059669","contrast":"#FDE68A","bg_light":"#ECFDF5","bg_warm":"#FFFBEB","bg_dark":"#064E3B","bg_dark_alt":"#3d2e00","text_on_dark":"#ECFDF5","text_dark":"#111827","text_body":"#374151","text_muted":"#6B7280","border":"#D1D5DB","border_light":"#E5E7EB","card_bg":"#F9FAFB","code_bg":"#F3F4F6","code_color":"#059669","white":"#ffffff","body_bg":"#f5f5f5","warn_bg":"#FFFBEB","warn_border":"#FDE68A","tip_bg":"#F0FDF4","tip_border":"#34D399",},
    "crimson":     {"name":"红白编辑","desc":"正红点睛×克制白底，经典编辑风","primary":"#DC2626","contrast":"#991B1B","bg_light":"#FEF2F2","bg_warm":"#FFF5F5","bg_dark":"#7F1D1D","bg_dark_alt":"#991B1B","text_on_dark":"#FEF2F2","text_dark":"#1C1917","text_body":"#374151","text_muted":"#9CA3AF","border":"#E5E7EB","border_light":"#FEE2E2","card_bg":"#FEF2F2","code_bg":"#F3F4F6","code_color":"#DC2626","white":"#ffffff","body_bg":"#f5f5f5","warn_bg":"#FEF2F2","warn_border":"#FCA5A5","tip_bg":"#FEF2F2","tip_border":"#DC2626",},
    "graphite":    {"name":"素砚","desc":"全灰阶×极致克制，素净如砚","primary":"#52525B","contrast":"#F97316","bg_light":"#FAFAFA","bg_warm":"#F4F4F5","bg_dark":"#27272A","bg_dark_alt":"#18181B","text_on_dark":"#FAFAFA","text_dark":"#27272A","text_body":"#52525B","text_muted":"#A1A1AA","border":"#E4E4E7","border_light":"#F4F4F5","card_bg":"#FAFAFA","code_bg":"#F4F4F5","code_color":"#52525B","white":"#ffffff","body_bg":"#f5f5f5","warn_bg":"#FAFAFA","warn_border":"#D4D4D8","tip_bg":"#FAFAFA","tip_border":"#A1A1AA",},
    "zen":         {"name":"虚白","desc":"虚室生白×大呼吸感，极简深度随笔","primary":"#4A5D52","contrast":"#8B9D83","bg_light":"#F5F7F5","bg_warm":"#F8FAF8","bg_dark":"#2D3A32","bg_dark_alt":"#1A2420","text_on_dark":"#F5F7F5","text_dark":"#2B2B2B","text_body":"#525252","text_muted":"#A3A3A3","border":"#E8E8E8","border_light":"#EEF3F0","card_bg":"#F8FAF8","code_bg":"#F5F7F5","code_color":"#4A5D52","white":"#ffffff","body_bg":"#f5f5f5","warn_bg":"#F7F5F5","warn_border":"#C8B8B0","tip_bg":"#F5F7F5","tip_border":"#8B9D83",},
    "ticket":      {"name":"票根","desc":"票据隐喻×硬阴影×撕票虚线","primary":"#059669","contrast":"#EAB308","bg_light":"#F0FDF4","bg_warm":"#FFFEF8","bg_dark":"#064E3B","bg_dark_alt":"#1A1A1A","text_on_dark":"#F0FDF4","text_dark":"#1A1A1A","text_body":"#555555","text_muted":"#888888","border":"#D1D5DB","border_light":"#A7F3D0","card_bg":"#FFFEF8","code_bg":"#F3F4F6","code_color":"#1F2937","white":"#FFFEF8","body_bg":"#f5f5f5","warn_bg":"#FFFBEB","warn_border":"#EAB308","tip_bg":"#F0FDF4","tip_border":"#34D399",},
    "olive":       {"name":"墨帖","desc":"墨色深底×暖橙点睛，内刊编辑质感","primary":"#1E1F23","contrast":"#ED7B2F","bg_light":"#EEEFE9","bg_warm":"#FDFDF8","bg_dark":"#1E1F23","bg_dark_alt":"#3D2E00","text_on_dark":"#FDFDF8","text_dark":"#23251D","text_body":"#4D4F46","text_muted":"#9EA096","border":"#BFC1B7","border_light":"#E5E7E0","card_bg":"#FDFDF8","code_bg":"#F3F3F2","code_color":"#ED7B2F","white":"#FDFDF8","body_bg":"#f5f5f5","warn_bg":"#FDF6F0","warn_border":"#ED7B2F40","tip_bg":"#EEEFE9","tip_border":"#1E1F23",},
}

# ══════════════════════════════════════════════════════════
# 5 套异构排版系统
# ══════════════════════════════════════════════════════════

def _common_styles(p, lname):
    """所有布局共享的基础样式"""
    styles = {
        "#article-wrapper": f"margin:0;padding:0 16px 0;background-color:{p['white']};",
        "body": f"background-color:{p['body_bg']};font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei','Helvetica Neue',sans-serif;color:{p['text_body']};-webkit-font-smoothing:antialiased;margin:0;padding:0;",
        ".header-image": "display:block;width:100%;max-width:100%;margin:0 0 28px;border-radius:0;",
        "p": f"margin:0 0 16px;font-size:15px;line-height:1.9;color:{p['text_body']};text-align:justify;",
        "strong": f"color:{p['text_dark']};font-weight:700;",
        "b": f"color:{p['text_dark']};font-weight:700;",
        "code": f"padding:2px 6px;font-family:'SF Mono','Menlo','Monaco','Courier New',monospace;font-size:13px;color:{p['code_color']};background-color:{p['code_bg']};border-radius:3px;",
        "pre": "margin:18px 0;padding:18px 20px;background-color:#282c34;color:#abb2bf;border-radius:8px;overflow-x:auto;font-size:13px;line-height:1.8;",
        ".code-block": "white-space:pre-wrap;font-family:'SF Mono','Menlo','Monaco','Courier New',monospace;margin:16px 0;padding:18px 20px;border-radius:8px;font-size:13px;line-height:1.7;",
        ".code-block-dark": "white-space:pre-wrap;font-family:monospace;margin:16px 0;padding:18px 20px;border-radius:8px;font-size:13px;line-height:1.7;background-color:#282c34;color:#abb2bf;",
        ".code-block-scroll": "white-space:pre-wrap;font-family:monospace;margin:16px 0;padding:18px 20px;border-radius:8px;font-size:13px;line-height:1.7;max-height:520px;overflow-y:auto;-webkit-overflow-scrolling:touch;",
        ".editor-note": f"margin:14px 0;padding:8px 14px;font-size:13px;color:{p['text_muted']};font-style:italic;border-left:2px solid {p['border_light']};",
        "table": "width:100%;margin:20px 0;border-collapse:collapse;font-size:13px;line-height:1.7;",
        "td": f"padding:12px 14px;border:1px solid {p['border']};color:{p['text_body']};",
        ".footer-spacer": "margin:0;padding:0;height:0;",
        ".illustration": "margin:28px 0;text-align:center;",
        ".illustration img": "display:block;width:100%;max-width:100%;border-radius:6px;",
    }
    # ── v1.8.0 三层视觉层级 CSS 类 ──
    # 标记层：关键词下划线（主题色半透明底划线，每段 1-3 处，最常用）
    styles[".kw-underline"] = f"border-bottom:2px solid {p['primary']}40;font-weight:600;"
    # 锚点层：最强强调（全文 ≤5 处，产品名/核心结论/CTA）
    styles[".anchor-bold"] = f"color:{p['primary']};font-weight:800;"
    # 锚点层：深色底白字强调块
    styles[".anchor-block"] = f"display:inline-block;background:{p['primary']};color:{p['white']};padding:1px 8px;border-radius:4px;font-weight:700;"
    # 英文章节副标签
    styles[".chapter-en"] = f"font-size:10px;font-weight:700;color:{p['text_muted']};letter-spacing:2px;"
    # 章节大号编号
    styles[".chapter-num"] = f"font-size:28px;font-weight:900;color:{p['primary']};line-height:1;letter-spacing:-2px;"
    # 结语编号变体
    styles[".chapter-num-final"] = f"font-size:28px;font-weight:900;color:{p['primary']};line-height:1;"
    # 目录/看点容器
    styles[".toc-card"] = f"margin:0 0 24px;padding:18px 20px;background:{p['bg_light']};border-radius:10px;border:1px solid {p['border_light']};"
    styles[".toc-item"] = f"margin-bottom:8px;font-size:14px;line-height:1.7;color:{p['text_body']};"
    styles[".toc-num"] = f"display:inline-block;width:22px;height:22px;line-height:22px;text-align:center;font-size:11px;font-weight:800;color:{p['white']};background:{p['primary']};border-radius:4px;margin-right:8px;"
    styles[".toc-label"] = f"font-size:12px;color:{p['text_muted']};margin-bottom:10px;letter-spacing:1px;font-weight:600;"
    # 引言卡关键词高亮
    styles[".intro-highlight"] = f"background:{p['primary']};color:{p['white']};padding:1px 6px;border-radius:3px;font-weight:700;"
    # 引言卡署名
    styles[".intro-byline"] = f"font-size:12px;color:{p['text_muted']};margin-top:8px;text-align:right;"
    # 签名区占位
    styles[".sig-placeholder"] = f"color:{p['text_muted']};font-style:italic;"
    # 荧光笔效果（偶尔用于长句强调，标记层补充手段）
    styles[".highlight-marker"] = f"background:{p['primary']}12;font-weight:600;padding:0 2px;border-radius:2px;"
    # 红色下划线变体（对比/否定专用）
    styles[".kw-underline-warn"] = f"border-bottom:2px solid {p['contrast']}60;font-weight:600;"
    # ── v2.0 通用组件库（所有布局可用）──
    # 内容标签：STEP / CASE / SKILL / TOOL
    styles[".tag-step"] = f"display:inline-block;background:{p['bg_dark']};color:{p['text_on_dark']};font-size:10px;font-weight:700;padding:2px 8px;border-radius:12px;margin-right:6px;"
    styles[".tag-case"] = f"display:inline-block;background:{p['border_light']};color:{p['text_muted']};font-size:10px;font-weight:700;padding:2px 8px;border-radius:12px;margin-right:6px;"
    styles[".tag-skill"] = f"display:inline-block;background:{p['primary']};color:{p['white']};font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;margin-right:6px;"
    # 流程卡片（3 步横排）
    styles[".flow-row"] = f"display:flex;align-items:stretch;justify-content:center;gap:6px;margin:0 0 20px;padding:14px;background:{p['card_bg']};border-radius:10px;border:1px solid {p['border_light']};"
    styles[".flow-active"] = f"flex:1;text-align:center;padding:10px 8px;background:{p['primary']};border-radius:6px;"
    styles[".flow-inactive"] = f"flex:1;text-align:center;padding:10px 8px;background:{p['white']};border:1px solid {p['border']};border-radius:6px;"
    styles[".flow-active-text"] = f"font-size:12px;font-weight:800;color:{p['white']};margin:0 0 2px;"
    styles[".flow-active-sub"] = f"font-size:9px;color:{p['white']}cc;margin:0;line-height:1.4;"
    styles[".flow-inactive-text"] = f"font-size:12px;font-weight:800;color:{p['text_dark']};margin:0 0 2px;"
    styles[".flow-inactive-sub"] = f"font-size:9px;color:{p['text_muted']};margin:0;line-height:1.4;"
    styles[".flow-arrow"] = "display:flex;align-items:center;color:#D1D5DB;font-size:14px;padding:0 4px;"
    # 时间线
    styles[".tl-row"] = "display:flex;margin-bottom:20px;"
    styles[".tl-dot"] = f"display:flex;flex-direction:column;align-items:center;margin-right:14px;flex-shrink:0;"
    styles[".tl-dot-circle"] = f"width:12px;height:12px;border-radius:50%;border:3px solid {p['primary']};background:{p['white']};margin-top:3px;"
    styles[".tl-dot-line"] = f"width:2px;background:{p['border_light']};flex:1;margin-top:4px;min-height:36px;"
    styles[".tl-body"] = "flex:1;padding-bottom:8px;"
    styles[".tl-title"] = f"font-size:14px;font-weight:800;color:{p['text_dark']};margin:0 0 4px;"
    styles[".tl-text"] = f"font-size:13px;color:{p['text_body']};margin:0;line-height:1.7;"
    # END 分割线
    styles[".end-divider"] = f"margin:40px 0 32px;text-align:center;"
    styles[".end-line"] = f"display:flex;align-items:center;justify-content:center;"
    styles[".end-line-l"] = f"height:1px;width:50px;background:{p['border_light']};margin-right:12px;"
    styles[".end-line-r"] = f"height:1px;width:50px;background:{p['border_light']};margin-left:12px;"
    styles[".end-label"] = f"font-size:11px;color:{p['primary']};font-weight:700;"
    # 胶囊列表
    styles[".pill-capsule"] = f"display:inline-block;margin:0 5px 5px 0;padding:3px 10px;font-size:12px;font-weight:700;color:{p['primary']};background:{p['primary']}08;border-radius:999px;"
    # 封面/引言增强
    styles[".cover-card"] = f"margin:0 0 28px;padding:24px 20px;background:{p['white']};border-radius:12px;border:1px solid {p['border_light']};"
    styles[".cover-tag"] = f"display:inline-block;font-size:10px;font-weight:700;color:{p['primary']};margin-bottom:14px;"
    styles[".cover-title"] = f"font-size:20px;font-weight:900;color:{p['text_dark']};margin:0 0 8px;line-height:1.2;"
    styles[".cover-subtitle"] = f"font-size:13px;color:{p['text_muted']};margin:0;line-height:1.6;"
    # 三连 CTA 区
    styles[".cta-triple"] = f"display:flex;justify-content:center;gap:20px;margin:16px 0;"
    styles[".cta-action"] = f"text-align:center;color:{p['text_muted']};"
    styles[".cta-icon-box"] = f"width:36px;height:36px;display:flex;align-items:center;justify-content:center;margin:0 auto 4px;background:{p['white']};border-radius:10px;border:1px solid {p['border_light']};"
    styles[".cta-icon-label"] = "font-size:10px;font-weight:600;"
    # 信息卡（带图标的小提示）
    styles[".info-note"] = f"margin:14px 0;padding:10px 14px;background:{p['tip_bg']};border-left:3px solid {p['tip_border']};border-radius:0 6px 6px 0;font-size:13px;color:{p['text_body']};line-height:1.7;"
    return styles

# ── 1. CLASSIC 经典左线 ──
def _classic(p):
    s = {}
    s[".article-meta"] = f"margin-bottom:28px;padding-bottom:24px;border-bottom:1px solid {p['border']};text-align:center;"
    s[".meta-tag"] = f"display:inline-block;padding:4px 14px;font-size:12px;font-weight:600;color:{p['primary']};background-color:{p['bg_light']};border-radius:20px;margin-bottom:14px;"
    s[".meta-desc"] = f"font-size:14px;color:{p['text_muted']};line-height:1.8;"
    s[".hero-block"] = "margin:0 0 36px;text-align:center;"
    s[".hero-number"] = f"font-size:56px;font-weight:900;color:{p['primary']};line-height:1;margin-bottom:4px;"
    s[".hero-label"] = f"font-size:13px;color:{p['text_muted']};"
    s["h2"] = f"margin:44px 0 22px;padding:14px 18px;font-size:19px;font-weight:700;line-height:1.5;color:{p['text_dark']};background-color:{p['bg_light']};border-left:4px solid {p['primary']};border-radius:0 6px 6px 0;"
    s["h3"] = f"margin:34px 0 16px;padding:0 0 12px;font-size:17px;font-weight:700;color:{p['primary']};border-bottom:2px solid {p['border']};line-height:1.5;"
    s["blockquote"] = f"margin:20px 0;padding:18px 20px 18px 22px;background-color:{p['card_bg']};border-left:3px solid {p['primary']};border-radius:0 8px 8px 0;color:{p['text_muted']};font-size:14px;line-height:1.8;"
    s[".golden-quote"] = f"margin:30px 0;padding:26px 28px;background-color:{p['bg_light']};border-radius:12px;text-align:center;font-size:17px;font-weight:700;line-height:1.9;color:{p['primary']};"
    s[".highlight-box"] = f"margin:24px 0;padding:20px 22px;background-color:{p['bg_warm']};border-radius:10px;border:1px solid {p['border']};font-size:15px;line-height:1.9;color:{p['primary']};"
    s[".card-item"] = f"margin-bottom:10px;padding:15px 18px;background-color:{p['card_bg']};border:1px solid {p['border']};border-radius:8px;font-size:14px;line-height:1.8;color:{p['text_body']};"
    s[".cta-footer"] = f"margin-top:44px;margin-bottom:0;padding:28px 24px;background-color:{p['bg_light']};border-radius:14px;text-align:center;"
    s[".cta-title"] = f"font-size:17px;font-weight:700;color:{p['primary']};margin-bottom:8px;"
    s["th"] = f"padding:12px 14px;background-color:{p['bg_light']};color:{p['text_dark']};font-weight:700;text-align:left;border:1px solid {p['border_light']};"
    s["hr"] = f"margin:36px 0;border:none;height:1px;background-color:{p['border_light']};"
    s[".data-num"] = f"font-size:28px;font-weight:900;color:{p['primary']};line-height:1.2;"
    s[".data-row"] = "width:100%;margin:20px 0;"
    s[".data-col"] = f"display:inline-block;width:47%;vertical-align:top;text-align:center;padding:18px 12px;background-color:{p['card_bg']};border:1px solid {p['border']};border-radius:10px;margin-right:3%;"
    s[".data-label"] = f"font-size:12px;color:{p['text_muted']};margin-top:6px;"
    return s

# ── 2. CARDFLOW 卡片流 ──
def _cardflow(p):
    s = {}
    s[".article-meta"] = f"margin-bottom:32px;text-align:center;"
    s[".meta-tag"] = f"display:inline-block;padding:5px 18px;font-size:11px;font-weight:700;color:{p['white']};background-color:{p['primary']};border-radius:3px;margin-bottom:10px;"
    s[".meta-desc"] = f"font-size:14px;color:{p['text_muted']};line-height:1.8;"
    s["h2"] = f"margin:0;padding:14px 20px;font-size:17px;font-weight:700;line-height:1.4;color:{p['white']};background-color:{p['primary']};border-radius:10px 10px 0 0;"
    s["h3"] = f"margin:24px 0 10px;padding:0;font-size:15px;font-weight:700;color:{p['text_dark']};line-height:1.6;border:none;"
    # 卡片容器：包裹 H2 + 内容
    s[".section-card"] = f"margin:0 0 28px;padding:0;background-color:{p['white']};border:1px solid {p['border']};border-radius:10px;overflow:hidden;"
    s[".section-card-body"] = f"padding:4px 20px 18px;"
    # info-card：独立信息卡片
    s[".info-card"] = f"margin:0 0 12px;padding:14px 16px;background-color:{p['card_bg']};border-left:4px solid {p['contrast']};border-radius:0 6px 6px 0;font-size:14px;line-height:1.8;color:{p['text_body']};"
    s[".info-card strong"] = f"color:{p['primary']};font-weight:700;"
    # 数据徽章
    s[".data-badge"] = f"display:inline-block;margin:4px 6px 4px 0;padding:6px 14px;background-color:{p['bg_light']};color:{p['primary']};font-size:13px;font-weight:700;border-radius:20px;"
    s["blockquote"] = f"margin:16px 0;padding:14px 18px;background-color:{p['bg_warm']};border:none;border-radius:8px;color:{p['text_body']};font-size:14px;line-height:1.8;"
    s[".golden-quote"] = f"margin:0 0 20px;padding:20px 24px;background-color:{p['bg_light']};border-radius:0 0 10px 10px;text-align:center;font-size:16px;font-weight:700;line-height:1.8;color:{p['primary']};"
    s[".highlight-box"] = f"margin:16px 0;padding:16px 20px;background-color:{p['bg_warm']};border-radius:8px;font-size:14px;line-height:1.8;color:{p['text_dark']};border-left:3px solid {p['contrast']};"
    s[".card-item"] = f"margin-bottom:8px;padding:12px 16px;background-color:{p['card_bg']};border:1px solid {p['border']};border-radius:6px;font-size:14px;line-height:1.7;color:{p['text_body']};"
    s[".cta-footer"] = f"margin-top:44px;margin-bottom:0;padding:24px 20px;background-color:{p['primary']};border-radius:10px;text-align:center;"
    s[".cta-title"] = f"font-size:16px;font-weight:700;color:{p['white']};margin-bottom:6px;"
    s["th"] = f"padding:12px 14px;background-color:{p['primary']};color:{p['white']};font-weight:700;text-align:left;border:none;"
    s["hr"] = f"margin:32px 0;border:none;height:1px;background-color:{p['border_light']};"
    s[".data-num"] = f"font-size:30px;font-weight:900;color:{p['contrast']};line-height:1.1;"
    s[".data-row"] = "width:100%;margin:20px 0;"
    s[".data-col"] = f"display:inline-block;width:47%;vertical-align:top;text-align:center;padding:16px 10px;background-color:{p['card_bg']};border:1px solid {p['border']};border-radius:8px;margin-right:3%;"
    s[".data-label"] = f"font-size:12px;color:{p['text_muted']};margin-top:6px;"
    return s

# ── 3. EDITORIAL 杂志流 ──
def _editorial(p):
    s = {}
    s[".article-meta"] = f"margin-bottom:32px;text-align:center;"
    s[".meta-tag"] = f"display:inline-block;padding:2px 0;font-size:11px;font-weight:600;color:{p['text_muted']};border-bottom:2px solid {p['primary']};margin-bottom:10px;"
    s[".meta-desc"] = f"font-size:15px;color:{p['text_muted']};line-height:1.8;font-style:italic;"
    # 引题段落
    s[".lead"] = f"margin:0 0 24px;font-size:17px;line-height:2.0;color:{p['text_muted']};text-align:center;font-weight:400;"
    s["h2"] = f"margin:56px 0 20px;padding:20px 0;text-align:center;font-size:20px;font-weight:800;line-height:1.4;color:{p['text_dark']};border-top:3px solid {p['primary']};border-bottom:1px solid {p['border_light']};background-color:transparent;"
    s["h3"] = f"margin:36px 0 14px;padding:0;font-size:16px;font-weight:700;color:{p['text_dark']};line-height:1.6;border:none;"
    # 装饰分隔线
    s[".ornament-divider"] = f"margin:40px auto;border:none;height:3px;background-color:{p['primary']};width:60px;"
    # 引用（戏剧化居中）
    s["blockquote"] = f"margin:36px 0;padding:18px 20px;text-align:center;font-size:20px;font-weight:600;line-height:1.9;color:{p['primary']};background-color:transparent;border:none;"
    s[".golden-quote"] = f"margin:40px 0;padding:32px 28px;background-color:{p['bg_light']};text-align:center;font-size:18px;font-weight:700;line-height:2.0;color:{p['primary']};border-top:2px solid {p['contrast']};border-bottom:2px solid {p['contrast']};"
    s[".highlight-box"] = f"margin:24px 0;padding:20px 24px;background-color:{p['bg_warm']};font-size:15px;line-height:2.0;color:{p['text_dark']};border-left:4px solid {p['contrast']};"
    s[".card-item"] = f"margin-bottom:14px;padding:18px 22px;background-color:{p['white']};border-top:3px solid {p['primary']};border-bottom:1px solid {p['border']};font-size:14px;line-height:1.8;color:{p['text_body']};"
    # 署名式 CTA
    s[".cta-footer"] = f"margin-top:52px;margin-bottom:0;padding:0;text-align:center;background-color:transparent;border:none;"
    s[".cta-title"] = f"font-size:15px;font-weight:600;color:{p['text_muted']};margin-bottom:6px;font-style:italic;"
    s["th"] = f"padding:14px 16px;background-color:{p['primary']};color:{p['white']};font-weight:700;text-align:left;border:none;"
    s["hr"] = f"margin:40px auto;border:none;height:3px;background-color:{p['primary']};width:60px;"
    s[".data-num"] = f"font-size:34px;font-weight:900;color:{p['primary']};line-height:1.1;"
    s[".data-row"] = "width:100%;margin:20px 0;"
    s[".data-col"] = f"display:inline-block;width:47%;vertical-align:top;text-align:center;padding:18px 12px;background-color:{p['card_bg']};border:1px solid {p['border']};border-radius:10px;margin-right:3%;"
    s[".data-label"] = f"font-size:12px;color:{p['text_muted']};margin-top:6px;"
    # 图片框
    s[".image-frame"] = f"margin:28px 0;padding:0;border:1px solid {p['border']};border-radius:4px;overflow:hidden;"
    s[".image-caption"] = f"margin:4px 0 20px;font-size:12px;color:{p['text_muted']};text-align:center;font-style:italic;"
    return s

# ── 4. GUIDE 手册流 ──
def _guide(p):
    s = {}
    s[".article-meta"] = f"margin-bottom:28px;text-align:left;padding-bottom:20px;border-bottom:2px solid {p['primary']};"
    s[".meta-tag"] = f"display:inline-block;padding:3px 12px;font-size:11px;font-weight:700;color:{p['white']};background-color:{p['primary']};border-radius:3px;margin-bottom:10px;"
    s[".meta-desc"] = f"font-size:14px;color:{p['text_muted']};line-height:1.8;"
    s["h2"] = f"margin:44px 0 20px;padding:0;font-size:22px;font-weight:800;line-height:1.3;color:{p['text_dark']};background-color:transparent;border:none;"
    s["h3"] = f"margin:32px 0 14px;padding:0;font-size:17px;font-weight:700;color:{p['primary']};line-height:1.5;border:none;"
    # 步骤块
    s[".step-block"] = f"margin:0 0 24px;padding:0;"
    s[".step-num"] = f"display:inline-block;width:32px;height:32px;line-height:32px;text-align:center;font-size:16px;font-weight:800;color:{p['white']};background-color:{p['primary']};border-radius:50%;margin-bottom:8px;"
    s[".step-title"] = f"display:inline;margin-left:8px;font-size:17px;font-weight:700;color:{p['text_dark']};vertical-align:middle;"
    s[".step-body"] = f"margin:8px 0 0 40px;font-size:15px;line-height:1.9;color:{p['text_body']};"
    # 提示框 - 两种
    s[".tip-box"] = f"margin:18px 0;padding:14px 18px;background-color:{p['tip_bg']};border-left:4px solid {p['tip_border']};border-radius:0 6px 6px 0;font-size:14px;line-height:1.8;color:{p['text_body']};"
    s[".tip-box strong"] = f"color:{p['primary']};font-weight:700;"
    s[".warn-box"] = f"margin:18px 0;padding:14px 18px;background-color:{p['warn_bg']};border-left:4px solid {p['warn_border']};border-radius:0 6px 6px 0;font-size:14px;line-height:1.8;color:{p['text_body']};"
    s[".warn-box strong"] = f"color:{p['contrast']};font-weight:700;"
    # 清单项
    s[".checklist-item"] = f"margin-bottom:8px;padding:10px 14px;font-size:14px;line-height:1.7;color:{p['text_body']};background-color:{p['card_bg']};border-radius:6px;"
    # 前后对比
    s[".before-after"] = "width:100%;margin:20px 0;"
    s[".ba-col"] = f"display:inline-block;width:47%;vertical-align:top;padding:14px;margin-right:3%;background-color:{p['card_bg']};border-radius:8px;"
    s[".ba-label"] = f"font-size:12px;font-weight:700;color:{p['text_muted']};margin-bottom:6px;"
    s[".ba-text"] = f"font-size:14px;line-height:1.8;color:{p['text_body']};"
    # 引用
    s["blockquote"] = f"margin:16px 0;padding:12px 16px;background-color:{p['bg_warm']};border:none;border-radius:6px;color:{p['text_body']};font-size:14px;line-height:1.7;"
    s[".golden-quote"] = f"margin:28px 0;padding:22px 24px;background-color:{p['bg_dark']};border-radius:8px;text-align:center;font-size:16px;font-weight:700;line-height:1.8;color:{p['text_on_dark']};"
    s[".highlight-box"] = f"margin:20px 0;padding:16px 20px;background-color:{p['bg_warm']};border-radius:8px;font-size:14px;line-height:1.8;color:{p['text_dark']};"
    s[".card-item"] = f"margin-bottom:8px;padding:12px 16px;background-color:{p['card_bg']};border:1px solid {p['border']};border-radius:6px;font-size:14px;line-height:1.7;color:{p['text_body']};"
    s[".cta-footer"] = f"margin-top:44px;margin-bottom:0;padding:24px 20px;background-color:{p['bg_light']};border-radius:10px;text-align:center;"
    s[".cta-title"] = f"font-size:16px;font-weight:700;color:{p['primary']};margin-bottom:6px;"
    s["th"] = f"padding:10px 14px;background-color:{p['bg_dark']};color:{p['text_on_dark']};font-weight:700;text-align:left;border:none;"
    s["hr"] = f"margin:32px 0;border:none;height:2px;background-color:{p['primary']};"
    s[".data-num"] = f"font-size:32px;font-weight:900;color:{p['primary']};line-height:1.1;"
    s[".data-row"] = "width:100%;margin:20px 0;"
    s[".data-col"] = f"display:inline-block;width:47%;vertical-align:top;text-align:center;padding:18px 12px;background-color:{p['card_bg']};border:1px solid {p['border']};border-radius:10px;margin-right:3%;"
    s[".data-label"] = f"font-size:12px;color:{p['text_muted']};margin-top:6px;"
    return s

# ── 5. LETTER 书信流 ──
def _letter(p):
    s = {}
    # 无 meta-tag/meta-desc，走书信格式
    s[".dateline"] = f"margin:0 0 28px;font-size:13px;color:{p['text_muted']};text-align:right;"
    s[".greeting"] = f"margin:0 0 24px;font-size:16px;color:{p['text_dark']};font-weight:500;line-height:1.8;"
    s[".letter-body"] = f"margin:0 0 16px;font-size:15px;line-height:2.0;color:{p['text_body']};text-align:justify;"
    # H2 在书信中极克制，只比正文略大
    s["h2"] = f"margin:40px 0 14px;padding:0;font-size:18px;font-weight:700;line-height:1.6;color:{p['text_dark']};background-color:transparent;border:none;"
    s["h3"] = f"margin:28px 0 10px;padding:0;font-size:15px;font-weight:600;color:{p['text_muted']};line-height:1.6;border:none;font-style:italic;"
    # 轻引用
    s["blockquote"] = f"margin:18px 0;padding:0 0 0 16px;font-size:14px;line-height:1.8;color:{p['text_muted']};background-color:transparent;border:none;border-left:2px solid {p['border_light']};font-style:italic;"
    # 书信中"金句"就是加大加粗的一段话，无底无边框
    s[".golden-quote"] = f"margin:28px 0;padding:0;text-align:center;font-size:18px;font-weight:600;line-height:2.0;color:{p['primary']};background-color:transparent;border:none;"
    s[".highlight-box"] = f"margin:20px 0;padding:0 0 0 14px;font-size:14px;line-height:1.9;color:{p['text_dark']};background-color:transparent;border:none;border-left:2px solid {p['contrast']};"
    s[".card-item"] = f"margin-bottom:12px;padding:0 0 10px;font-size:14px;line-height:1.8;color:{p['text_body']};background-color:transparent;border:none;border-bottom:1px solid {p['border_light']};"
    # 署名区
    s[".sign-off"] = f"margin:36px 0 12px;font-size:15px;color:{p['text_muted']};text-align:right;font-style:italic;"
    s[".signature"] = f"margin:0 0 8px;font-size:16px;font-weight:600;color:{p['text_dark']};text-align:right;"
    s[".postscript"] = f"margin:24px 0 0;padding:14px 0 0;font-size:13px;color:{p['text_muted']};line-height:1.8;border-top:1px solid {p['border_light']};font-style:italic;"
    # CTA 极克制
    s[".cta-footer"] = f"margin-top:48px;margin-bottom:0;padding:20px 0 0;text-align:center;background-color:transparent;border:none;border-top:1px solid {p['border_light']};"
    s[".cta-title"] = f"font-size:14px;font-weight:500;color:{p['primary']};margin-bottom:6px;"
    # 元信息简化
    s[".article-meta"] = f"margin-bottom:24px;text-align:right;"
    s[".meta-tag"] = f"font-size:11px;color:{p['text_muted']};font-style:italic;background:none;border:none;padding:0;display:inline;"
    s[".meta-desc"] = f"font-size:13px;color:{p['text_muted']};line-height:1.6;display:none;"
    s["th"] = f"padding:10px 12px;font-weight:600;color:{p['text_dark']};text-align:left;border:none;border-bottom:1px solid {p['border_light']};background-color:transparent;"
    s["hr"] = f"margin:32px auto;border:none;height:1px;background-color:{p['border_light']};width:40%;"
    s[".data-num"] = f"font-size:24px;font-weight:700;color:{p['text_dark']};line-height:1.2;"
    s[".data-row"] = "width:100%;margin:16px 0;"
    s[".data-col"] = f"display:inline-block;width:47%;vertical-align:top;text-align:center;padding:14px 10px;margin-right:3%;"
    s[".data-label"] = f"font-size:11px;color:{p['text_muted']};margin-top:4px;"
    return s

# ── 6. WORKSHOP 极客流 ──
def _workshop(p):
    s = {}
    s[".article-meta"] = f"margin-bottom:28px;padding-bottom:20px;border-bottom:2px solid {p['primary']};text-align:left;"
    s[".meta-tag"] = f"display:inline-block;padding:3px 10px;font-size:11px;font-weight:700;color:{p['white']};background-color:{p['primary']};border-radius:3px;margin-bottom:8px;"
    s[".meta-desc"] = f"font-size:14px;color:{p['text_muted']};line-height:1.8;"
    # H2: 实验笔记风格 — 深底+等宽感
    s["h2"] = f"margin:44px 0 20px;padding:12px 18px;font-size:18px;font-weight:700;line-height:1.4;color:{p['text_on_dark']};background-color:{p['bg_dark']};border:none;border-radius:4px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;"
    s["h3"] = f"margin:32px 0 12px;padding:0 0 0 12px;font-size:16px;font-weight:700;color:{p['text_dark']};line-height:1.5;border:none;border-left:3px solid {p['primary']};"
    # 引用块：终端风格
    s["blockquote"] = f"margin:18px 0;padding:16px 20px;background-color:{p['bg_dark']};color:{p['text_on_dark']};font-size:14px;line-height:1.8;border:none;border-radius:6px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;"
    # Prompt 模板卡
    s[".prompt-card"] = f"margin:20px 0;padding:0;background-color:{p['white']};border:2px solid {p['primary']};border-radius:8px;overflow:hidden;"
    s[".prompt-card-header"] = f"margin:0;padding:10px 16px;font-size:12px;font-weight:700;color:{p['white']};background-color:{p['primary']};"
    s[".prompt-card-body"] = f"margin:0;padding:16px 18px;font-size:14px;line-height:1.8;color:{p['text_body']};white-space:pre-wrap;font-family:'SF Mono','Menlo','Monaco','Courier New',monospace;"
    # 工具徽章
    s[".tool-badge"] = f"display:inline-block;margin:2px 4px 2px 0;padding:3px 10px;font-size:12px;font-weight:600;color:{p['primary']};background-color:{p['bg_light']};border:1px solid {p['primary']};border-radius:4px;"
    # 工作流步骤
    s[".workflow-step"] = f"margin:0 0 20px;padding:0 0 0 24px;border-left:2px dashed {p['border']};position:relative;"
    s[".wf-step-num"] = f"display:inline-block;width:24px;height:24px;line-height:24px;text-align:center;font-size:13px;font-weight:800;color:{p['white']};background-color:{p['primary']};border-radius:3px;margin-bottom:6px;"
    # 金句：实验结果风
    s[".golden-quote"] = f"margin:30px 0;padding:22px 24px;background-color:{p['bg_dark']};border-radius:6px;text-align:center;font-size:16px;font-weight:700;line-height:1.8;color:{p['contrast']};"
    s[".highlight-box"] = f"margin:20px 0;padding:16px 20px;background-color:{p['bg_warm']};border-radius:6px;font-size:14px;line-height:1.8;color:{p['text_dark']};border-left:3px solid {p['contrast']};"
    s[".card-item"] = f"margin-bottom:8px;padding:12px 16px;background-color:{p['card_bg']};border:1px solid {p['border']};border-radius:4px;font-size:14px;line-height:1.7;color:{p['text_body']};"
    s[".card-item strong"] = f"color:{p['primary']};font-weight:700;"
    s[".tip-box"] = f"margin:18px 0;padding:14px 18px;background-color:{p['tip_bg']};border-left:4px solid {p['tip_border']};border-radius:0 6px 6px 0;font-size:14px;line-height:1.8;color:{p['text_body']};"
    s[".warn-box"] = f"margin:18px 0;padding:14px 18px;background-color:{p['warn_bg']};border-left:4px solid {p['warn_border']};border-radius:0 6px 6px 0;font-size:14px;line-height:1.8;color:{p['text_body']};"
    s[".cta-footer"] = f"margin-top:44px;margin-bottom:0;padding:24px 20px;background-color:{p['bg_dark']};border-radius:8px;text-align:center;"
    s[".cta-title"] = f"font-size:16px;font-weight:700;color:{p['text_on_dark']};margin-bottom:6px;"
    s["th"] = f"padding:12px 14px;background-color:{p['bg_dark']};color:{p['text_on_dark']};font-weight:700;text-align:left;border:none;"
    s["hr"] = f"margin:32px 0;border:none;height:2px;background-color:{p['primary']};"
    s[".data-num"] = f"font-size:30px;font-weight:900;color:{p['contrast']};line-height:1.1;"
    s[".data-row"] = "width:100%;margin:20px 0;"
    s[".data-col"] = f"display:inline-block;width:47%;vertical-align:top;text-align:center;padding:16px 10px;background-color:{p['card_bg']};border:1px solid {p['border']};border-radius:8px;margin-right:3%;"
    s[".data-label"] = f"font-size:12px;color:{p['text_muted']};margin-top:6px;"
    return s

# ── 7. MOYU 摸鱼绿杂志风 ──
def _moyu(p):
    """摸鱼绿杂志卡片风：翠绿主色+黄色高亮+卡片丰富+虚线引用"""
    s = {}
    s[".article-meta"] = f"margin-bottom:28px;text-align:center;"
    s[".meta-tag"] = f"display:inline-block;padding:4px 16px;font-size:11px;font-weight:700;color:{p['white']};background-color:{p['primary']};border-radius:20px;margin-bottom:10px;"
    s[".meta-desc"] = f"font-size:14px;color:{p['text_muted']};line-height:1.8;"
    # H2: 大号绿色数字+深色标题
    s["h2"] = f"margin:48px 0 24px;padding:0;font-size:19px;font-weight:800;line-height:1.4;color:{p['text_dark']};background-color:transparent;border:none;"
    s["h3"] = f"margin:28px 0 12px;padding:0;font-size:15px;font-weight:700;color:{p['text_dark']};line-height:1.5;border:none;"
    # 引用：灰色虚线框（摸鱼绿签名风格）
    s["blockquote"] = f"margin:16px 0 24px;padding:14px 18px;background:{p['card_bg']};border:1px dashed {p['border']};border-radius:8px;color:{p['text_body']};font-size:14px;line-height:1.8;"
    # 金句：绿色虚线卡片+黄色下划线高亮
    s[".golden-quote"] = f"margin:28px 0;padding:18px 20px;background:{p['white']};border:1px dashed {p['bg_light']};border-radius:8px;text-align:center;font-size:16px;font-weight:700;line-height:1.9;color:{p['primary']};"
    # 强调块：浅绿底+绿色左边条
    s[".highlight-box"] = f"margin:24px 0;padding:16px 20px;background:{p['bg_light']};border-radius:8px;border:1px solid {p['tip_border']}40;font-size:15px;line-height:1.9;color:{p['text_dark']};"
    # 卡片项：白色卡片+绿色阴影
    s[".card-item"] = f"margin-bottom:8px;padding:14px 18px;background:{p['white']};border:1px solid {p['border_light']};border-radius:10px;font-size:14px;line-height:1.8;color:{p['text_body']};box-shadow:0 2px 8px {p['primary']}08;"
    # CTA：浅绿底圆角
    s[".cta-footer"] = f"margin-top:44px;margin-bottom:0;padding:24px 20px;background:{p['bg_light']};border-radius:12px;text-align:center;border:1px solid {p['border_light']};"
    s[".cta-title"] = f"font-size:16px;font-weight:700;color:{p['primary']};margin-bottom:8px;"
    s["th"] = f"padding:10px 14px;background:{p['primary']};color:{p['white']};font-weight:700;text-align:left;border:none;"
    s["hr"] = f"margin:32px 0;border:none;height:1px;background:{p['border_light']};"
    s[".data-num"] = f"font-size:30px;font-weight:900;color:{p['primary']};line-height:1.1;"
    s[".data-row"] = "width:100%;margin:20px 0;"
    s[".data-col"] = f"display:inline-block;width:47%;vertical-align:top;text-align:center;padding:18px 12px;background:{p['bg_light']};border:1px solid {p['border_light']};border-radius:12px;margin-right:3%;"
    s[".data-label"] = f"font-size:12px;color:{p['text_muted']};margin-top:6px;"
    # 摸鱼绿专属：绿色胶囊列表
    s[".pill-item"] = f"display:inline-block;margin:0 6px 6px 0;padding:4px 12px;font-size:13px;font-weight:700;color:{p['primary']};background:{p['bg_light']};border-radius:999px;"
    # 提示框
    s[".tip-box"] = f"margin:18px 0;padding:14px 18px;background:{p['tip_bg']};border-left:4px solid {p['tip_border']};border-radius:0 8px 8px 0;font-size:14px;line-height:1.8;color:{p['text_body']};"
    s[".warn-box"] = f"margin:18px 0;padding:14px 18px;background:{p['warn_bg']};border:1px solid {p['warn_border']};border-radius:10px;font-size:14px;line-height:1.8;color:{p['text_dark']};font-weight:600;"
    return s

# ── 8. RED-EDITORIAL 红白编辑风 ──
def _red_editorial(p):
    """红白编辑风：正红点睛×克制白底×戏剧引言卡"""
    s = {}
    s[".article-meta"] = f"margin-bottom:32px;text-align:center;"
    s[".meta-tag"] = f"display:inline-block;padding:2px 0;font-size:11px;font-weight:600;color:{p['text_muted']};border-bottom:2px solid {p['primary']};margin-bottom:10px;"
    s[".meta-desc"] = f"font-size:15px;color:{p['text_muted']};line-height:1.8;font-style:italic;"
    # 引言卡：白底红色光晕（摸鱼红白签名组件）
    s[".intro-card"] = f"margin:10px 0 32px;background:{p['white']};border-radius:12px;box-shadow:0 4px 24px -4px {p['primary']}25;padding:28px 24px 22px;"
    s[".intro-quote-mark"] = f"font-size:42px;color:{p['primary']};font-weight:900;margin:0;line-height:0.6;"
    # H2: 红底编号+底部红色实线
    s["h2"] = f"margin:48px 0 20px;padding:0 0 14px;font-size:19px;font-weight:800;line-height:1.4;color:{p['text_dark']};background-color:transparent;border-bottom:3px solid {p['primary']};"
    s["h3"] = f"margin:28px 0 12px;padding:0 0 0 12px;font-size:16px;font-weight:700;color:{p['text_dark']};line-height:1.5;border:none;border-left:3px solid {p['primary']};"
    # 引用：浅红底左边条（金句版）
    s["blockquote"] = f"margin:20px 0 24px;padding:16px 20px;background:{p['bg_light']};border-left:4px solid {p['primary']};border-radius:0 8px 8px 0;color:{p['text_body']};font-size:14px;line-height:1.8;"
    # 金句：粉底左竖条+深红字
    s[".golden-quote"] = f"margin:28px 0;padding:20px 22px;background:{p['bg_light']};border-radius:0 10px 10px 0;border-left:4px solid {p['primary']};font-size:16px;font-weight:800;line-height:1.9;color:{p['contrast']};"
    # 强调块：浅红底
    s[".highlight-box"] = f"margin:24px 0;padding:18px 22px;background:{p['bg_light']};border-radius:10px;border:1px solid {p['border_light']};font-size:15px;line-height:1.9;color:{p['text_dark']};"
    s[".card-item"] = f"margin-bottom:10px;padding:14px 18px;background:{p['white']};border:1px solid {p['border_light']};border-radius:8px;font-size:14px;line-height:1.8;color:{p['text_body']};"
    # CTA：浅红底
    s[".cta-footer"] = f"margin-top:44px;margin-bottom:0;padding:24px 20px;background:{p['bg_light']};border-radius:10px;text-align:center;"
    s[".cta-title"] = f"font-size:16px;font-weight:700;color:{p['primary']};margin-bottom:8px;"
    s["th"] = f"padding:10px 14px;background:{p['primary']};color:{p['white']};font-weight:700;text-align:left;border:none;"
    s["hr"] = f"margin:32px 0;border:none;height:2px;background:{p['primary']};"
    s[".data-num"] = f"font-size:30px;font-weight:900;color:{p['primary']};line-height:1.1;"
    s[".data-row"] = "width:100%;margin:20px 0;"
    s[".data-col"] = f"display:inline-block;width:47%;vertical-align:top;text-align:center;padding:18px 12px;background:{p['bg_light']};border:1px solid {p['border_light']};border-radius:10px;margin-right:3%;"
    s[".data-label"] = f"font-size:12px;color:{p['text_muted']};margin-top:6px;"
    # 红色标签胶囊
    s[".red-tag"] = f"display:inline-block;padding:2px 8px;font-size:11px;font-weight:700;color:{p['white']};background:{p['primary']};border-radius:4px;margin-right:6px;"
    # 提示/警告
    s[".tip-box"] = f"margin:18px 0;padding:14px 18px;background:{p['bg_light']};border-left:4px solid {p['primary']};border-radius:0 8px 8px 0;font-size:14px;line-height:1.8;color:{p['text_body']};"
    s[".warn-box"] = f"margin:18px 0;padding:14px 18px;background:{p['bg_light']};border-left:4px solid {p['contrast']};border-radius:0 8px 8px 0;font-size:14px;line-height:1.8;color:{p['text_dark']};"
    return s

# ── 9. GRAPHITE 石墨极简 ──
def _graphite(p):
    s = {}
    s[".article-meta"] = f"margin-bottom:36px;text-align:center;"
    s[".meta-tag"] = f"display:inline-block;padding:0 0 4px;font-size:11px;font-weight:600;color:{p['text_muted']};border-bottom:1px solid {p['primary']};margin-bottom:10px;"
    s[".meta-desc"] = f"font-size:14px;color:{p['text_muted']};line-height:1.8;"
    s["h2"] = f"margin:56px 0 20px;padding:0;font-size:18px;font-weight:700;line-height:1.4;color:{p['text_dark']};background-color:transparent;border:none;"
    s["h3"] = f"margin:36px 0 12px;padding:0;font-size:15px;font-weight:600;color:{p['text_dark']};line-height:1.5;border:none;"
    s["blockquote"] = f"margin:20px 0 24px;padding:16px 20px;background:{p['bg_light']};border-left:2px solid {p['primary']};border-radius:0 4px 4px 0;color:{p['text_body']};font-size:14px;line-height:1.8;"
    s[".golden-quote"] = f"margin:32px 0;padding:20px 0;text-align:center;font-size:16px;font-weight:600;line-height:1.9;color:{p['text_dark']};background-color:transparent;border:none;border-top:1px solid {p['border']};border-bottom:1px solid {p['border']};"
    s[".highlight-box"] = f"margin:24px 0;padding:18px 22px;background:{p['bg_light']};border:1px solid {p['border']};border-radius:6px;font-size:15px;line-height:1.9;color:{p['text_dark']};"
    s[".card-item"] = f"margin-bottom:10px;padding:14px 18px;background:{p['white']};border:1px solid {p['border']};border-radius:4px;font-size:14px;line-height:1.8;color:{p['text_body']};"
    s[".cta-footer"] = f"margin-top:56px;margin-bottom:0;padding:20px 0;text-align:center;background-color:transparent;border:none;border-top:1px solid {p['border']};"
    s[".cta-title"] = f"font-size:15px;font-weight:600;color:{p['primary']};margin-bottom:6px;"
    s["th"] = f"padding:10px 14px;font-weight:600;color:{p['text_dark']};text-align:left;border:none;border-bottom:1px solid {p['border']};background-color:transparent;"
    s["hr"] = f"margin:40px 0;border:none;height:1px;background:{p['border']};"
    return s

# ── 10. ZEN 留白禅意 ──
def _zen(p):
    s = {}
    s[".article-meta"] = f"margin-bottom:40px;text-align:center;"
    s[".meta-tag"] = f"font-size:11px;color:{p['text_muted']};letter-spacing:3px;font-weight:400;"
    s[".meta-desc"] = f"font-size:15px;color:{p['text_muted']};line-height:2.0;"
    s["h2"] = f"margin:64px 0 22px;padding:0;font-size:20px;font-weight:600;line-height:1.5;color:{p['text_dark']};background-color:transparent;border:none;"
    s["h3"] = f"margin:40px 0 14px;padding:0 0 0 10px;font-size:15px;font-weight:600;color:{p['text_dark']};line-height:1.6;border:none;border-left:2px solid {p['primary']};"
    s["blockquote"] = f"margin:24px 0 28px;padding:0 0 0 16px;background-color:transparent;border:none;border-left:1px solid {p['border']};color:{p['text_body']};font-size:14px;line-height:2.0;font-style:italic;"
    s[".golden-quote"] = f"margin:36px 0;padding:28px 0;text-align:center;font-size:17px;font-weight:500;line-height:2.1;color:{p['text_dark']};background-color:transparent;border:none;border-top:1px solid {p['border']};border-bottom:1px solid {p['border']};"
    s[".highlight-box"] = f"margin:28px 0;padding:0;font-size:15px;line-height:2.0;color:{p['text_dark']};background-color:transparent;border:none;"
    s[".card-item"] = f"margin-bottom:12px;padding:0 0 12px;font-size:14px;line-height:1.9;color:{p['text_body']};background-color:transparent;border:none;border-bottom:1px solid {p['border']};"
    s[".cta-footer"] = f"margin-top:64px;margin-bottom:0;padding:32px 0 0;text-align:center;background-color:transparent;border:none;border-top:1px solid {p['border']};"
    s[".cta-title"] = f"font-size:14px;font-weight:400;color:{p['text_muted']};margin-bottom:10px;"
    s["th"] = f"padding:12px 16px;font-weight:500;color:{p['text_dark']};text-align:left;border:none;border-bottom:1px solid {p['border']};background-color:transparent;"
    s["hr"] = f"margin:48px auto;border:none;height:1px;background:{p['border']};width:40px;"
    return s

# ── 11. TICKET 摸鱼票据 ──
def _ticket(p):
    s = {}
    s[".article-meta"] = f"margin-bottom:32px;text-align:center;"
    s[".meta-tag"] = f"display:inline-block;padding:4px 14px;font-size:11px;font-weight:700;color:{p['white']};background:{p['primary']};border-radius:3px;margin-bottom:10px;box-shadow:2px 2px 0 {p['contrast']};"
    s[".meta-desc"] = f"font-size:14px;color:{p['text_muted']};line-height:1.8;"
    s["h2"] = f"margin:44px 0 20px;padding:10px 0;font-size:18px;font-weight:800;line-height:1.4;color:{p['text_dark']};background-color:transparent;border:none;border-top:1px dashed {p['border_light']};border-bottom:1px dashed {p['border_light']};"
    s["h3"] = f"margin:28px 0 12px;padding:0 0 0 12px;font-size:15px;font-weight:700;color:{p['text_dark']};line-height:1.5;border:none;border-left:2px dashed {p['border_light']};"
    s["blockquote"] = f"margin:16px 0 24px;padding:14px 18px;background:{p['white']};border:1px solid {p['border']};border-radius:4px;color:{p['text_body']};font-size:14px;line-height:1.8;box-shadow:4px 4px 0 {p['bg_dark_alt']};"
    s[".golden-quote"] = f"margin:28px 0;padding:18px 20px;background:{p['white']};border:2px solid {p['primary']};border-radius:4px;text-align:center;font-size:15px;font-weight:700;line-height:1.8;color:{p['primary']};box-shadow:4px 4px 0 {p['bg_dark_alt']};"
    s[".highlight-box"] = f"margin:24px 0;padding:16px 20px;background:{p['bg_light']};border:1px solid {p['border_light']};border-radius:4px;font-size:14px;line-height:1.9;color:{p['text_dark']};"
    s[".card-item"] = f"margin-bottom:10px;padding:14px 18px;background:{p['card_bg']};border:1px solid {p['border']};border-radius:4px;font-size:14px;line-height:1.8;color:{p['text_body']};box-shadow:3px 3px 0 {p['bg_dark_alt']};"
    s[".cta-footer"] = f"margin-top:44px;margin-bottom:0;padding:20px;text-align:center;background:{p['white']};border:1px solid {p['border']};border-radius:4px;box-shadow:4px 4px 0 {p['bg_dark_alt']};"
    s[".cta-title"] = f"font-size:15px;font-weight:700;color:{p['primary']};margin-bottom:8px;"
    s["th"] = f"padding:10px 14px;background:{p['primary']};color:{p['white']};font-weight:700;text-align:left;border:none;"
    s["hr"] = f"margin:32px 0;border:none;border-bottom:1px dashed {p['border_light']};background:transparent;height:0;"
    return s

# ── 12. OLIVE 橄榄手记 ──
def _olive(p):
    s = {}
    s[".article-meta"] = f"margin-bottom:28px;padding-bottom:18px;border-bottom:2px solid {p['primary']};"
    s[".meta-tag"] = f"display:inline-block;padding:2px 10px;font-size:10px;font-weight:700;color:{p['text_on_dark']};background:{p['primary']};border-radius:3px;margin-bottom:10px;"
    s[".meta-desc"] = f"font-size:14px;color:{p['text_muted']};line-height:1.8;"
    s["h2"] = f"margin:44px 0 18px;padding:8px 14px;font-size:17px;font-weight:700;line-height:1.4;color:{p['text_on_dark']};background:{p['bg_dark']};border:none;border-radius:6px;"
    s["h3"] = f"margin:28px 0 12px;padding:0 0 0 12px;font-size:15px;font-weight:700;color:{p['text_dark']};line-height:1.5;border:none;border-left:3px solid {p['contrast']};"
    s["blockquote"] = f"margin:16px 0 22px;padding:14px 18px;background:{p['bg_light']};border:1px solid {p['border']};border-radius:6px;color:{p['text_body']};font-size:14px;line-height:1.8;"
    s[".golden-quote"] = f"margin:28px 0;padding:18px 20px;background:{p['card_bg']};border-left:4px solid {p['contrast']};border-radius:0 6px 6px 0;font-size:15px;font-weight:700;line-height:1.9;color:{p['text_dark']};"
    s[".highlight-box"] = f"margin:24px 0;padding:16px 20px;background:{p['bg_warm']};border:1px solid {p['border_light']};border-radius:6px;font-size:14px;line-height:1.9;color:{p['text_dark']};"
    s[".card-item"] = f"margin-bottom:8px;padding:12px 16px;background:{p['card_bg']};border:1px solid {p['border_light']};border-radius:6px;font-size:14px;line-height:1.8;color:{p['text_body']};"
    s[".cta-footer"] = f"margin-top:44px;margin-bottom:0;padding:22px 20px;background:{p['bg_dark']};border-radius:6px;text-align:center;"
    s[".cta-title"] = f"font-size:15px;font-weight:700;color:{p['contrast']};margin-bottom:8px;"
    s["th"] = f"padding:10px 14px;background:{p['primary']};color:{p['text_on_dark']};font-weight:700;text-align:left;border:none;"
    s["hr"] = f"margin:32px 0;border:none;height:1px;background:{p['border']};"
    return s


LAYOUTS = {
    "classic":   {"name":"经典左线","desc":"左粗线+浅底分区，结构清晰，通用百搭","fn":_classic},
    "cardflow":  {"name":"卡片流","desc":"每段内容独立成卡，模块化可扫描","fn":_cardflow},
    "editorial": {"name":"杂志流","desc":"大标题+装饰线+引题段落，编辑感","fn":_editorial},
    "guide":     {"name":"手册流","desc":"步骤编号+提示框+对比，操作教学","fn":_guide},
    "letter":    {"name":"书信流","desc":"日期+问候+署名，极简亲密对话感","fn":_letter},
    "workshop":  {"name":"极客流","desc":"深色实验台+Prompt卡+工具徽章，技术感","fn":_workshop},
    "moyu":      {"name":"摸鱼杂志","desc":"翠绿卡片+黄色高亮+虚线引用，信息密度高","fn":_moyu},
    "red-editorial":{"name":"红白编辑","desc":"正红点睛+克制白底+戏剧引言卡，经典编辑感","fn":_red_editorial},
    "graphite":  {"name":"素砚","desc":"全灰阶+1px细线，素净如砚","fn":_graphite},
    "zen":       {"name":"虚白","desc":"虚室生白+大呼吸感，衬线标题","fn":_zen},
    "ticket":    {"name":"票根","desc":"票据隐喻+硬阴影+撕票虚线，仪式感","fn":_ticket},
    "olive":     {"name":"墨帖","desc":"墨色深底+暖橙点睛，内刊手帖质感","fn":_olive},
}

PRESETS = {
    "teal":   {"layout":"classic","palette":"teal-gold","name":"青蓝经典","content_types":["opinion","list","tutorial"],"desc":"通用深度分析，理性中带温度"},
    "navy":   {"layout":"editorial","palette":"navy-coral","name":"深蓝杂志","content_types":["opinion","interview","data"],"desc":"商业/行业评论，专业不过分严肃"},
    "forest": {"layout":"guide","palette":"forest-amber","name":"森语手册","content_types":["tutorial","case"],"desc":"教程/操作指南，自然沉稳有生机"},
    "plum":   {"layout":"cardflow","palette":"plum-sage","name":"梅紫卡片","content_types":["list","personal","case"],"desc":"产品/工具介绍，文艺不张扬"},
    "slate":  {"layout":"letter","palette":"slate-rose","name":"岩灰书信","content_types":["personal","interview"],"desc":"个人随笔/故事，克制中带柔软"},
    "amber":  {"layout":"workshop","palette":"forest-amber","name":"暖金工坊","content_types":["tutorial","case","list"],"desc":"技术/AI/编程，极客实验台"},
    # v2.0: 新增预设
    "moyu":   {"layout":"moyu","palette":"emerald","name":"摸鱼杂志","content_types":["tutorial","list","case","opinion"],"desc":"翠绿卡片+黄色高亮，杂志快讯感"},
    "ruby":   {"layout":"red-editorial","palette":"crimson","name":"红白编辑","content_types":["opinion","personal","interview"],"desc":"正红点睛+克制白底，经典编辑风"},
    "graph":  {"layout":"graphite","palette":"graphite","name":"素砚","content_types":["opinion","data","case"],"desc":"全灰阶×极致克制，素净如砚"},
    "zen":    {"layout":"zen","palette":"zen","name":"虚白","content_types":["personal","opinion","interview"],"desc":"虚室生白×大呼吸感，极简深度随笔"},
    "ticket": {"layout":"ticket","palette":"ticket","name":"票根","content_types":["list","case","tutorial"],"desc":"票据隐喻×硬阴影，工具对比/创意测评"},
    "olive":  {"layout":"olive","palette":"olive","name":"墨帖","content_types":["case","opinion","tutorial"],"desc":"墨色深底×暖橙，内刊手帖质感"},
}


# ══════════════════════════════════════════════════════════
# 工具函数
# ══════════════════════════════════════════════════════════

def derive_palette(hex_color):
    r,g,b = int(hex_color[1:3],16),int(hex_color[3:5],16),int(hex_color[5:7],16)
    def mix(ratio):
        return f"#{int(r*ratio+255*(1-ratio)):02x}{int(g*ratio+255*(1-ratio)):02x}{int(b*ratio+255*(1-ratio)):02x}"
    def darken(ratio):
        return f"#{int(r*ratio):02x}{int(g*ratio):02x}{int(b*ratio):02x}"
    return {"name":f"自定义 {hex_color}","desc":f"从 {hex_color} 推导","primary":hex_color,"contrast":mix(0.35),"bg_light":mix(0.18),"bg_warm":mix(0.08),"bg_dark":darken(0.55),"bg_dark_alt":darken(0.35),"text_on_dark":mix(0.15),"text_dark":"#1a1a1a","text_body":"#3f3f3f","text_muted":"#8a9aaa","border":"#e0e7ef","border_light":"#dce3ea","card_bg":"#fafbfc","code_bg":"#f9f2f4","code_color":"#c7254e","white":"#ffffff","body_bg":"#f5f5f5","warn_bg":"#fff8f0","warn_border":"#e8a838","tip_bg":"#f0faf6","tip_border":"#4aaf87",}

# ── v1.8.0 文章类型判定关键词 ──
CONTENT_TYPE_KW = {
    "tutorial":   ["步骤","操作","配置","代码","命令","运行","安装","部署","教程","实战","指南","方法","技巧","实现","执行","打开","点击","输入","设置","参数"],
    "list":       ["推荐","工具","平台","产品","盘点","清单","合集","精选","资源","插件","网站","应用","软件","分别","各有","第一","第二","还有"],
    "opinion":    ["分析","深度","观点","评论","趋势","解读","思考","本质","逻辑","复盘","判断","认为","背后","意味着","真正","核心","关键"],
    "interview":  ["采访","访谈","对话","他说","提到","分享","经历","故事","创始人","团队","创业"],
    "data":       ["数据","增长","报告","统计","占比","同比","环比","指标","数字","图表","排名","对比","提升","下降","用户","市场"],
    "personal":   ["我","感觉","生活","日常","最近","记录","随笔","碎碎念","朋友","想起","记得","那天","周末","早上","晚上"],
    "case":       ["案例","实战","项目","客户","上线","结果","效果","复盘","踩坑","经验","教训","问题","解决","优化"],
}

def detect_content_type(text):
    """判定文章类型，返回 (主类型, 次类型, 置信度)"""
    scores = {}
    for ctype, kws in CONTENT_TYPE_KW.items():
        s = sum(len(re.findall(kw, text)) for kw in kws)
        # 标题权重加倍
        first_line = text.split('\n')[0] if text else ""
        s += sum(2 for kw in kws if kw in first_line)
        scores[ctype] = s
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if ranked[0][1] == 0:
        return ("opinion", "general", 0)  # 无匹配默认观点型
    primary = ranked[0][0]
    secondary = ranked[1][0] if len(ranked) > 1 and ranked[1][1] > 0 else None
    confidence = "high" if ranked[0][1] >= 5 else ("medium" if ranked[0][1] >= 2 else "low")
    return (primary, secondary, confidence)

CONTENT_TYPE_NAMES = {
    "tutorial": "教程/操作指南",
    "list": "盘点/工具清单",
    "opinion": "观点/深度分析",
    "interview": "访谈/人物特稿",
    "data": "数据复盘/报告",
    "personal": "生活/情感随笔",
    "case": "案例实战",
}

# ── v1.8.0 文章类型 → 推荐预设 ──
CONTENT_TYPE_PRESETS = {
    "tutorial":   ["forest","amber"],
    "list":       ["plum","teal"],
    "opinion":    ["navy","teal"],
    "interview":  ["navy","slate"],
    "data":       ["navy","teal"],
    "personal":   ["slate","plum"],
    "case":       ["amber","forest"],
}

def analyze_content(text):
    """v1.8.0: 返回预设分数 + 文章类型判定"""
    kw = {
        "navy":["商业","行业","市场","数据","报告","战略","投资","利润","竞争","企业","增长","收入"],
        "forest":["教程","步骤","操作","配置","代码","实战","指南","工具","方法","技巧","实现"],
        "teal":["分析","深度","观点","评论","趋势","解读","思考","本质","逻辑","复盘"],
        "plum":["产品","设计","体验","品牌","审美","创意","风格","质感","表达"],
        "slate":["我","经历","感受","故事","生活","日常","朋友","记录","随笔"],
        "amber":["Prompt","API","Agent","Workflow","模型","token","部署","自动化","编程","脚本","调试","开源","GitHub","命令行","参数"],
        # v2.0: 新增预设预设的关键词
        "moyu":["测评","清单","教程","工具","盘点","对比","实测","上手","体验","推荐","合集","卡片","信息图"],
        "ruby":["观点","深度","评论","思考","编辑","专栏","经典","解读","读书","感悟","随笔","情感","故事"],
        "graph":["设计","科技","品牌","高端","专业","极简","克制","理性","系统","架构","逻辑","本质"],
        "zen":["禅意","极简","深度","随笔","冥想","留白","沉静","读书","笔记","感悟","思考","内省"],
        "ticket":["对比","测评","工具","创意","评测","实测","横评","排名","星级","推荐","选择","指南"],
        "olive":["内刊","复盘","手记","深度","评测","案例","说明","文档","系统性","分析","报告","编辑"],
    }
    scores = {}
    for k, kws in kw.items():
        s = sum(len(re.findall(kw, text)) for kw in kws)
        fl = text.split('\n')[0] if text else ""
        s += sum(2 for kw in kws if kw in fl)
        scores[k] = s
    # 文章类型加权：按文章类型提升对应预设的分数
    ctype, _, confidence = detect_content_type(text)
    if ctype in CONTENT_TYPE_PRESETS and confidence in ("high","medium"):
        boost = 3 if confidence == "high" else 1
        for preset in CONTENT_TYPE_PRESETS[ctype]:
            if preset in scores:
                scores[preset] += boost
    return scores

def recommend(text):
    """v1.8.0: 返回预设推荐 + 文章类型判定"""
    scores = analyze_content(text)
    ctype, secondary, confidence = detect_content_type(text)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    presets = [(k, PRESETS[k], sc) for k, sc in ranked if k in PRESETS]
    return {
        "presets": presets,
        "content_type": ctype,
        "content_type_name": CONTENT_TYPE_NAMES.get(ctype, "通用"),
        "content_type_confidence": confidence,
        "secondary_type": secondary,
    }

def resolve_theme(theme_arg):
    if theme_arg is None: theme_arg = "teal"
    if theme_arg in PRESETS:
        p = PRESETS[theme_arg]
        return p["layout"], PALETTES[p["palette"]]
    if ":" in theme_arg:
        parts = theme_arg.split(":",1)
        l, pn = parts[0].strip(), parts[1].strip()
        if l in LAYOUTS and pn in PALETTES:
            return l, PALETTES[pn]
    if re.match(r'^#[0-9a-fA-F]{6}$', theme_arg):
        return "classic", derive_palette(theme_arg)
    print(f"⚠️  未知 '{theme_arg}'，回退 teal")
    return "classic", PALETTES["teal-gold"]

def build_styles(layout_name, p):
    fn = LAYOUTS[layout_name]["fn"]
    styles = _common_styles(p, layout_name)
    styles.update(fn(p))
    return styles

def build_nested_overrides(layout_name, p):
    """v1.8.0: 布局特定的嵌套覆盖 + 视觉层级类嵌套处理"""
    base = {
        ("blockquote","p"): f"margin:0 0 8px;font-size:14px;line-height:1.8;color:{p['text_muted']};text-align:justify;",
        ("pre","code"): "font-size:13px;line-height:1.8;",
        ("golden-quote","p"): f"margin:0 0 8px;font-size:17px;font-weight:700;line-height:1.9;color:{p['primary']};text-align:center;",
        ("highlight-box","strong"): f"color:{p['contrast']};font-weight:700;",
        ("cta-footer","p"): f"margin:0 0 10px;font-size:14px;font-weight:500;line-height:1.8;color:{p['primary']};text-align:center;",
        ("highlight-box","p"): f"margin:0 0 8px;font-size:15px;line-height:1.9;color:{p['text_dark']};text-align:justify;",
        # v1.8.0: 关键词下划线在深色/浅色背景上的适配
        ("golden-quote","kw-underline"): f"border-bottom:2px solid {p['contrast']}60;font-weight:700;",
        ("blockquote","kw-underline"): f"border-bottom:2px solid {p['primary']}50;font-weight:600;",
        ("cta-footer","kw-underline"): f"border-bottom:2px solid {p['white']}60;font-weight:600;",
    }
    if layout_name == "cardflow":
        base[("cta-footer","p")] = f"margin:0 0 10px;font-size:14px;font-weight:500;line-height:1.8;color:{p['white']};text-align:center;"
        base[("cta-footer","kw-underline")] = f"border-bottom:2px solid {p['white']}50;font-weight:600;"
    if layout_name == "editorial":
        base[("blockquote","p")] = f"margin:0;font-size:20px;font-weight:600;line-height:1.9;color:{p['primary']};text-align:center;"
        base[("blockquote","kw-underline")] = f"border-bottom:2px solid {p['contrast']}50;font-weight:600;"
    if layout_name == "letter":
        base[("golden-quote","p")] = f"margin:0;font-size:18px;font-weight:600;line-height:2.0;color:{p['primary']};text-align:center;"
        base[("cta-footer","p")] = f"margin:0 0 8px;font-size:13px;color:{p['text_muted']};text-align:center;"
    if layout_name == "workshop":
        base[("blockquote","p")] = f"margin:0 0 8px;font-size:14px;line-height:1.8;color:{p['text_on_dark']};text-align:justify;"
        base[("cta-footer","p")] = f"margin:0 0 10px;font-size:14px;font-weight:500;line-height:1.8;color:{p['text_on_dark']};text-align:center;"
        base[("golden-quote","p")] = f"margin:0;font-size:16px;font-weight:700;line-height:1.8;color:{p['contrast']};text-align:center;"
        base[("blockquote","kw-underline")] = f"border-bottom:2px solid {p['contrast']}40;font-weight:600;"
        base[("cta-footer","kw-underline")] = f"border-bottom:2px solid {p['contrast']}50;font-weight:600;"
    # v2.0: 新增预设布局的嵌套覆盖
    if layout_name == "moyu":
        base[("golden-quote","p")] = f"margin:0;font-size:16px;font-weight:700;line-height:1.9;color:{p['primary']};text-align:center;"
        base[("blockquote","p")] = f"margin:0 0 8px;font-size:14px;line-height:1.8;color:{p['text_body']};text-align:justify;"
        base[("cta-footer","p")] = f"margin:0 0 8px;font-size:14px;line-height:1.8;color:{p['text_body']};text-align:center;"
        base[("golden-quote","kw-underline")] = f"border-bottom:2px solid {p['contrast']}80;font-weight:700;"
    if layout_name == "red-editorial":
        base[("golden-quote","p")] = f"margin:0;font-size:16px;font-weight:800;line-height:1.9;color:{p['contrast']};text-align:left;"
        base[("blockquote","p")] = f"margin:0 0 8px;font-size:14px;line-height:1.8;color:{p['text_body']};text-align:justify;"
        base[("highlight-box","p")] = f"margin:0;font-size:15px;line-height:1.9;color:{p['text_dark']};text-align:justify;"
        base[("cta-footer","p")] = f"margin:0 0 8px;font-size:14px;line-height:1.8;color:{p['text_body']};text-align:center;"
    return base


# ══════════════════════════════════════════════════════════
# InlineStyleConverter (v1.9.0: <span leaf=""> 自动包裹)
# ══════════════════════════════════════════════════════════

class InlineStyleConverter(HTMLParser):
    def __init__(self, styles, nested_overrides):
        super().__init__(convert_charrefs=False)
        self.styles = styles; self.nested_overrides = nested_overrides
        self.output = []; self.tag_stack = []
        self._void_elements = {'hr','br','img','input','meta','link'}
        self._last_container_cls = None  # 🔴 追踪上一个闭合容器元素的 class，用于兄弟间距防叠加
        self._leaf_depth = 0             # v1.9.0: 追踪 <span leaf=""> 嵌套深度，避免双重包裹
        self._code_depth = 0             # v1.9.0: 追踪 <code>/<pre> 嵌套深度，代码内容不包裹
    def _get_base_style(self, tag, cls):
        if cls:
            ck = f".{cls}"
            if ck in self.styles: return self.styles[ck]
        if tag in self.styles: return self.styles[tag]
        return None
    def _get_nested_override(self, tag):
        if not self.tag_stack: return None
        pt, pc = self.tag_stack[-1]
        if pc:
            ov = self.nested_overrides.get((pc, tag))
            if ov: return ov
        return self.nested_overrides.get((pt, tag))
    def _build_style_attr(self, tag, cls, extra_style=None):
        base = self._get_base_style(tag, cls)
        override = self._get_nested_override(tag)
        final = override or base
        if extra_style:
            final = (final.rstrip(';')+';'+extra_style) if final else extra_style
        return f' style="{final}"' if final else ""
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get('class', None)
        extra_style = attrs_dict.get('style', None)
        attr_parts = [f'{k}="{v}"' for k,v in attrs if k not in ('class','style')]
        style_str = self._build_style_attr(tag, cls, extra_style)

        # 🔴 兄弟间距防叠加：golden-quote → cta-footer 紧邻时压缩 margin-top
        if cls == 'cta-footer' and self._last_container_cls == 'golden-quote' and style_str:
            style_str = re.sub(r'margin-top:\s*\d+px', 'margin-top:12px', style_str)

        if style_str: attr_parts.append(style_str)
        attr_str = (' '+' '.join(attr_parts)) if attr_parts else ''
        self.output.append(f'<{tag}{attr_str}>')
        if tag not in self._void_elements:
            self.tag_stack.append((tag, cls))
            # v1.9.0: 追踪 leaf span 深度（避免双重包裹）
            if tag == 'span' and 'leaf' in attrs_dict:
                self._leaf_depth += 1
            # v1.9.0: 追踪 code/pre 深度（代码内容不包裹）
            if tag in ('code','pre'):
                self._code_depth += 1
    def handle_endtag(self, tag):
        self.output.append(f'</{tag}>')
        if self.tag_stack and self.tag_stack[-1][0] == tag:
            _, cls = self.tag_stack.pop()
            # 🔴 记录容器级元素的 class，供兄弟间距防叠加使用
            if tag in ('blockquote','section'):
                self._last_container_cls = cls
        # v1.9.0: 追踪 leaf/code 深度
        if tag == 'span' and self._leaf_depth > 0:
            self._leaf_depth -= 1
        if tag in ('code','pre') and self._code_depth > 0:
            self._code_depth -= 1
    def handle_data(self, data):
        """v1.9.0: 所有文本节点自动包裹 <span leaf="">，微信公众号防样式剥离"""
        stripped = data.strip()
        if not stripped:
            # 纯空白保留原样（如 <br> 前的换行符）
            self.output.append(data)
            return
        # 已在 <span leaf=""> 内 → 不双重包裹
        if self._leaf_depth > 0:
            self.output.append(data)
            return
        # 在 <code> 或 <pre> 内 → 保持原样（代码内容不容干扰）
        if self._code_depth > 0:
            self.output.append(data)
            return
        # 包裹文本：保留前后空白
        leading = data[:len(data) - len(data.lstrip())]
        trailing = data[len(data.rstrip()):]
        self.output.append(f'{leading}<span leaf="">{stripped}</span>{trailing}')
    def handle_entityref(self, name): self.output.append(f'&{name};')
    def handle_charref(self, name): self.output.append(f'&#{name};')
    def get_result(self): return ''.join(self.output)


# ══════════════════════════════════════════════════════════
# 验证 & CLI
# ══════════════════════════════════════════════════════════

def validate_output(html):
    """v1.9.0: 增加 <span leaf=""> 包裹验证"""
    clean = re.sub(r'<code[^>]*>.*?</code>','',html,flags=re.DOTALL)
    clean = re.sub(r'<pre[^>]*>.*?</pre>','',clean,flags=re.DOTALL)
    errors = []
    if re.search(r'<style[^>]*>',clean,re.IGNORECASE): errors.append("❌ <style>")
    if re.search(r'\sclass\s*=',clean): errors.append("❌ class=")
    if re.search(r'<div[\s>]',clean,re.IGNORECASE): errors.append("❌ <div>")
    if 'linear-gradient' in clean.lower(): errors.append("❌ linear-gradient")
    if 'letter-spacing' in clean.lower(): errors.append("❌ letter-spacing")
    # v1.9.0: 验证 <span leaf=""> 包裹（公众号防样式剥离的核心保障）
    leaf_count = len(re.findall(r'<span leaf="">', clean))
    if leaf_count == 0:
        errors.append("❌ 缺少 <span leaf=""> 包裹——文本将被微信剥离样式")
    if errors:
        print("\n".join(errors)); return False
    print(f"✅ 验证通过: 零 style/div/class/linear-gradient/letter-spacing | leaf 包裹 {leaf_count} 处")
    return True

def main():
    args = sys.argv[1:]
    theme_arg = "teal"; layout_arg = None; palette_arg = None
    input_file = "output/article-class-html.html"
    output_file = "output/article-inline.html"
    pos_count = 0; i = 0
    while i < len(args):
        if args[i] == "--theme" and i+1 < len(args): theme_arg = args[i+1]; i += 2
        elif args[i] == "--layout" and i+1 < len(args): layout_arg = args[i+1]; i += 2
        elif args[i] == "--palette" and i+1 < len(args): palette_arg = args[i+1]; i += 2
        elif not args[i].startswith("--"):
            if pos_count == 0: input_file = args[i]
            else: output_file = args[i]
            pos_count += 1; i += 1
        else: i += 1

    if layout_arg and palette_arg and palette_arg in PALETTES and layout_arg in LAYOUTS:
        layout_name, palette = layout_arg, PALETTES[palette_arg]
    else:
        layout_name, palette = resolve_theme(theme_arg)

    li = LAYOUTS[layout_name]
    print(f"📐 布局: {li['name']} ({li['desc']})")
    print(f"🎨 配色: {palette['name']} ({palette['desc']})")
    print(f"   主色: {palette['primary']}  |  对比色: {palette['contrast']}")

    styles = build_styles(layout_name, palette)
    nested = build_nested_overrides(layout_name, palette)

    with open(input_file,'r',encoding='utf-8') as f: html = f.read()
    converter = InlineStyleConverter(styles, nested)
    converter.feed(html)
    result = converter.get_result()
    result = re.sub(r'letter-spacing:[^;"]*;?','',result)

    with open(output_file,'w',encoding='utf-8') as f: f.write(result)
    print(f"✅ 转换完成: {input_file} → {output_file}")
    print(f"   输出大小: {len(result)} 字符")
    validate_output(result)

if __name__ == '__main__':
    main()
