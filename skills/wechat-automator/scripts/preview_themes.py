#!/usr/bin/env python3
"""
阶段④ 主题预览生成器 (v2.0)
每套布局渲染专属结构化样本，展示布局×配色的完整差异

用法:
  python3 scripts/preview_themes.py output/article-class-html.html [--open]
"""
import sys, os, re, webbrowser

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SKILL_ROOT)

from scripts.build_inline import (
    LAYOUTS, PALETTES, PRESETS, build_styles, build_nested_overrides,
    InlineStyleConverter, recommend, CONTENT_TYPE_NAMES,
)

# ══════════════════════════════════════════════════════════
# v2.0: 每套布局的结构化样本 —— 同一段内容，不同的 HTML 骨架
# ══════════════════════════════════════════════════════════

def _sample(layout_key, html):
    """返回 (layout_key, html_snippet)"""
    return (layout_key, html)

# 共用内容:
#   标题: 文字的力量
#   正文: 莉泽尔在地下室里给躲藏的犹太人朗读。防空洞里所有人蜷缩着等炸弹落下，她打开一本书，声音压过了爆炸声。
#   金句: 文字不是武器。但有时候，它是防空洞里唯一的光。

LAYOUT_SAMPLES = {
    "classic": _sample("classic",
        '<h2><span class="chapter-num">01</span> 文字的力量</h2>'
        '<p>莉泽尔在地下室里给躲藏的犹太人<span class="kw-underline">朗读</span>。防空洞里所有人蜷缩着等炸弹落下，她打开一本书，<span class="kw-underline">声音压过了爆炸声</span>。</p>'
        '<blockquote class="golden-quote"><p>文字不是武器。但有时候，它是防空洞里唯一的光。</p></blockquote>'
        '<section class="card-item"><p>📌 两个被战争碾碎的人，用文字<span class="kw-underline">交换氧气</span>。</p></section>'
        '<section class="highlight-box"><p>马克斯后来也写字——他有一本漆成白色的书，满脑袋的奇思妙想。</p></section>'
    ),
    "cardflow": _sample("cardflow",
        '<section class="section-card">'
        '<h2><span class="chapter-num">01</span> 文字的力量</h2>'
        '<section class="section-card-body">'
        '<p>莉泽尔在地下室里给躲藏的犹太人<span class="kw-underline">朗读</span>。防空洞里所有人蜷缩着等炸弹落下。</p>'
        '<section class="info-card"><p>📌 <span class="kw-underline">声音压过了爆炸声</span>——周围的人停下了发抖。</p></section>'
        '<blockquote class="golden-quote"><p>文字不是武器。但有时候，它是防空洞里唯一的光。</p></blockquote>'
        '</section></section>'
    ),
    "editorial": _sample("editorial",
        '<p class="lead">她打开一本书，开始念——</p>'
        '<h2><span class="chapter-num">01</span> <span class="chapter-en">WORDS</span> 文字的力量</h2>'
        '<p>莉泽尔在地下室里给躲藏的犹太人<span class="kw-underline">朗读</span>。防空洞里所有人蜷缩着等炸弹落下，<span class="kw-underline">声音压过了爆炸声</span>，周围的人停下了发抖。</p>'
        '<blockquote class="golden-quote"><p>文字不是武器。但有时候，它是防空洞里唯一的光。</p></blockquote>'
    ),
    "guide": _sample("guide",
        '<h2><span class="chapter-num">01</span> 文字的力量</h2>'
        '<section class="step-block">'
        '<span class="step-num">1</span><span class="step-title">找到避难所</span>'
        '<p class="step-body">莉泽尔在地下室里给躲藏的犹太人<span class="kw-underline">朗读</span>。</p>'
        '</section>'
        '<section class="step-block">'
        '<span class="step-num">2</span><span class="step-title">打开一本书</span>'
        '<p class="step-body">防空洞里所有人蜷缩着等炸弹落下，她开始念。</p>'
        '</section>'
        '<section class="tip-box"><p>💡 <span class="kw-underline">声音压过了爆炸声</span></p></section>'
        '<section class="warn-box"><p>⚠️ 沉默不是安全——沉默是一个洞穴，我们在其中避难却无法平安无事。</p></section>'
        '<blockquote class="golden-quote"><p>文字不是武器。但有时候，它是防空洞里唯一的光。</p></blockquote>'
    ),
    "letter": _sample("letter",
        '<p class="dateline">2026.07.07</p>'
        '<p class="greeting">她打开一本书，开始念。防空洞里所有人蜷缩着等炸弹落下——</p>'
        '<h2><span class="chapter-num">01</span> 文字的力量</h2>'
        '<p>莉泽尔在地下室里给躲藏的犹太人<span class="kw-underline">朗读</span>。<span class="kw-underline">声音压过了爆炸声</span>，周围的人停下了发抖。两个被战争碾碎的人，用文字交换氧气。</p>'
        '<blockquote class="golden-quote"><p>文字不是武器。但有时候，它是防空洞里唯一的光。</p></blockquote>'
    ),
    "workshop": _sample("workshop",
        '<h2><span class="chapter-num">01</span> <span class="chapter-en">WORDS</span> 文字的力量</h2>'
        '<p>莉泽尔在地下室里给躲藏的犹太人<span class="kw-underline">朗读</span>。防空洞里所有人蜷缩着等炸弹落下，<span class="kw-underline">声音压过了爆炸声</span>。</p>'
        '<section class="prompt-card">'
        '<p class="prompt-card-header">📋 核心 Prompt</p>'
        '<p class="prompt-card-body">文字不是武器。但有时候，它是防空洞里唯一的光。</p>'
        '</section>'
        '<p><span class="tool-badge">朗读</span><span class="tool-badge">文字</span><span class="tool-badge">避难所</span></p>'
        '<section class="workflow-step"><span class="wf-step-num">1</span> 找到地下室<span class="kw-underline">避难所</span></section>'
        '<section class="workflow-step"><span class="wf-step-num">2</span> 打开一本书开始<span class="kw-underline">朗读</span></section>'
    ),
    "moyu": _sample("moyu",
        '<section class="cover-card">'
        '<span class="cover-tag">📖 读书札记</span>'
        '<p class="cover-title">文字的力量</p>'
        '<p class="cover-subtitle">防空洞里的朗读声，压过了炸弹的爆炸</p>'
        '</section>'
        '<h2><span class="chapter-num">01</span> <span class="chapter-en">WORDS</span> 文字的力量</h2>'
        '<p><span class="tag-step">STEP 01</span> 莉泽尔在地下室里给躲藏的犹太人<span class="kw-underline">朗读</span>。</p>'
        '<blockquote class="golden-quote"><p>文字不是武器。但有时候，它是防空洞里唯一的光。</p></blockquote>'
        '<section class="card-item"><p>🔖 两个被战争碾碎的人，用<span class="kw-underline">文字交换氧气</span>。</p></section>'
        '<section class="flow-row">'
        '<section class="flow-active"><p class="flow-active-text">朗读</p><p class="flow-active-sub">声音压过爆炸</p></section>'
        '<span class="flow-arrow">→</span>'
        '<section class="flow-inactive"><p class="flow-inactive-text">安静</p><p class="flow-inactive-sub">周围的人停下发抖</p></section>'
        '<span class="flow-arrow">→</span>'
        '<section class="flow-inactive"><p class="flow-inactive-text">交换</p><p class="flow-inactive-sub">文字变成氧气</p></section>'
        '</section>'
    ),
    "red-editorial": _sample("red-editorial",
        '<section class="intro-card">'
        '<p class="intro-quote-mark">"</p>'
        '<p><span class="intro-highlight">文字</span>不是武器。但有时候，它是<span class="intro-highlight">防空洞里唯一的光</span>。</p>'
        '</section>'
        '<h2><span class="chapter-num">01</span> <span class="chapter-en">WORDS</span> 文字的力量</h2>'
        '<p>莉泽尔在地下室里给躲藏的犹太人<span class="kw-underline">朗读</span>。防空洞里所有人蜷缩着等炸弹落下，<span class="kw-underline">声音压过了爆炸声</span>。</p>'
        '<blockquote class="golden-quote"><p>两个被战争碾碎的人，用文字交换氧气。</p></blockquote>'
        '<section class="info-note"><p>📌 《偷书贼》以死神视角讲述，全篇充满诗意的残酷——"任何事物的美都源于它们终将消失"。</p></section>'
        '<section class="end-divider"><section class="end-line"><span class="end-line-l"></span><span class="end-label">END</span><span class="end-line-r"></span></section></section>'
    ),
    "graphite": _sample("graphite",
        '<p class="meta-tag">ESSAY · 读书札记</p>'
        '<h2><span class="chapter-num">01</span> 文字的力量</h2>'
        '<p>莉泽尔在地下室里给躲藏的犹太人<span class="kw-underline">朗读</span>。防空洞里所有人蜷缩着等炸弹落下，她打开一本书，<span class="kw-underline">声音压过了爆炸声</span>。</p>'
        '<blockquote class="golden-quote"><p>文字不是武器。但有时候，它是防空洞里唯一的光。</p></blockquote>'
        '<p>两个被战争碾碎的人，用文字<span class="kw-underline">交换氧气</span>。</p>'
    ),
    "zen": _sample("zen",
        '<p class="meta-tag">E S S A Y</p>'
        '<h2><span class="chapter-num">01</span> 文字的力量</h2>'
        '<p>莉泽尔在地下室里给躲藏的犹太人朗读。防空洞里所有人蜷缩着等炸弹落下，她打开一本书，声音压过了爆炸声。</p>'
        '<blockquote class="golden-quote"><p>文字不是武器。<br>但有时候，它是防空洞里唯一的光。</p></blockquote>'
        '<p>两个被战争碾碎的人，用文字<span class="kw-underline">交换氧气</span>。</p>'
    ),
    "ticket": _sample("ticket",
        '<p class="meta-tag">★★★★★ · 必读</p>'
        '<h2><span class="chapter-num">01</span> <span class="chapter-en">WORDS</span> 文字的力量</h2>'
        '<p>莉泽尔在地下室里给躲藏的犹太人<span class="kw-underline">朗读</span>。防空洞里所有人蜷缩着等炸弹落下，她打开一本书，<span class="kw-underline">声音压过了爆炸声</span>。</p>'
        '<blockquote class="golden-quote"><p>文字不是武器。但有时候，它是防空洞里唯一的光。</p></blockquote>'
        '<section class="card-item"><p>🔖 两个被战争碾碎的人，用<span class="kw-underline">文字交换氧气</span>。</p></section>'
    ),
    "olive": _sample("olive",
        '<p class="meta-tag">EDITORIAL · 内刊手记</p>'
        '<h2><span class="chapter-num">01</span> <span class="chapter-en">WORDS</span> 文字的力量</h2>'
        '<p><span class="tag-skill">核心概念</span> 莉泽尔在地下室里给躲藏的犹太人<span class="kw-underline">朗读</span>。防空洞里所有人蜷缩着等炸弹落下。</p>'
        '<blockquote class="golden-quote"><p>文字不是武器。但有时候，它是防空洞里唯一的光。</p></blockquote>'
        '<section class="tl-row">'
        '<section class="tl-dot"><section class="tl-dot-circle"></section><section class="tl-dot-line"></section></section>'
        '<section class="tl-body"><p class="tl-title">第一章 · 偷书</p><p class="tl-text">弟弟的葬礼上捡起《掘墓人手册》</p></section>'
        '</section>'
        '<section class="tl-row">'
        '<section class="tl-dot"><section class="tl-dot-circle"></section></section>'
        '<section class="tl-body"><p class="tl-title">第四章 · 朗读</p><p class="tl-text">防空洞里声音压过爆炸声</p></section>'
        '</section>'
    ),
}


def render_sample(layout_key, preset_key):
    """用指定布局的专属样本 × 指定预设的配色，返回 inline HTML"""
    preset = PRESETS[preset_key]
    palette = PALETTES[preset["palette"]]
    # 🔴 关键：用布局专属样本，而不是预设的布局
    # 这样每张卡片展示的是该布局的结构特征
    if layout_key not in LAYOUT_SAMPLES:
        return "<p>样本缺失</p>"
    sample_html = LAYOUT_SAMPLES[layout_key][1]
    styles = build_styles(layout_key, palette)
    nested = build_nested_overrides(layout_key, palette)
    wrapped = f'<section style="margin:0;padding:0 12px 0;background-color:#ffffff;">{sample_html}</section>'
    converter = InlineStyleConverter(styles, nested)
    converter.feed(wrapped)
    result = converter.get_result()
    result = re.sub(r'letter-spacing:[^;"]*;?', '', result)
    return result


def generate_preview_page(result, article_title=""):
    """v2.0: 每张卡片 = 该布局的专属结构样本 × 该预设的配色"""
    ranked = result["presets"]
    content_type_name = result.get("content_type_name", "")
    content_type_conf = result.get("content_type_confidence", "")

    # 预渲染所有卡片
    renders = {}
    for preset_key, preset in PRESETS.items():
        layout_key = preset["layout"]
        renders[preset_key] = render_sample(layout_key, preset_key)

    recommended_keys = {ranked[0][0], ranked[1][0]} if len(ranked) >= 2 else {ranked[0][0]}

    cards_html = ""
    for preset_key, preset in PRESETS.items():
        layout_key = preset["layout"]
        layout = LAYOUTS.get(layout_key, {"name": layout_key, "desc": ""})
        palette = PALETTES[preset["palette"]]
        is_rec = preset_key in recommended_keys
        badge = '<span class="badge">⭐ 推荐</span>' if is_rec else ""

        swatch_html = f'''
            <div class="dual-swatch">
                <span class="swatch-p" style="background-color:{palette['primary']};"></span>
                <span class="swatch-c" style="background-color:{palette['contrast']};"></span>
            </div>'''

        content_types = preset.get("content_types", [])
        ct_tags = " ".join(f'<span class="ct-tag">{CONTENT_TYPE_NAMES.get(ct, ct)}</span>' for ct in content_types[:2])

        cards_html += f'''
        <div class="theme-card{' recommended' if is_rec else ''}">
            <div class="card-header">
                {swatch_html}
                <div class="card-meta">
                    <span class="theme-name">{preset['name']}</span>
                    {badge}
                </div>
                <div class="theme-spec">
                    <span class="spec-layout">📐 {layout['name']}</span>
                    <span class="spec-palette">🎨 {palette['name']}</span>
                </div>
                <div class="theme-desc">{layout['desc']} · {palette['desc']}</div>
                <div class="theme-ct">{ct_tags}</div>
            </div>
            <div class="card-preview">{renders[preset_key]}</div>
        </div>'''

    legend_items = ""
    for key, preset, score in ranked:
        palette = PALETTES[preset["palette"]]
        layout_key = preset["layout"]
        layout = LAYOUTS.get(layout_key, {"name": layout_key, "desc": ""})
        bar_w = min(score * 8, 120)
        legend_items += f'''
        <div class="legend-item">
            <span class="legend-swatch" style="background-color:{palette['primary']};"></span>
            <span class="legend-name">{preset['name']}</span>
            <span class="legend-detail">({layout['name']} × {palette['name']})</span>
            <span class="legend-bar"><span style="display:inline-block;width:{bar_w}px;height:8px;background-color:{palette['primary']};border-radius:4px;"></span></span>
            <span class="legend-score">{score} 分</span>
        </div>'''

    title_display = article_title or "文章预览"
    ct_info = f'<span class="ct-badge">{content_type_name}</span> <span class="ct-conf">置信度: {content_type_conf}</span>' if content_type_name else ""

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>排版风格预览 — {title_display}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: -apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;
    background: #1a1d23; color: #e0e0e0; padding: 32px 24px 64px;
  }}
  .page-header {{ max-width: 1600px; margin: 0 auto 40px; text-align: center; }}
  .page-header h1 {{ font-size: 28px; font-weight: 800; color: #fff; margin-bottom: 8px; }}
  .page-header .subtitle {{ font-size: 14px; color: #8a8f9a; }}
  .ct-info {{ margin-top: 8px; }}
  .ct-badge {{ display: inline-block; padding: 2px 10px; background: #3a7bd5; color: #fff; font-size: 12px; font-weight: 600; border-radius: 4px; }}
  .ct-conf {{ font-size: 12px; color: #6a6f7a; margin-left: 6px; }}

  .legend {{ max-width: 900px; margin: 0 auto 40px; padding: 20px 28px; background: #252830; border-radius: 12px; }}
  .legend-title {{ font-size: 13px; font-weight: 700; color: #8a8f9a; margin-bottom: 14px; }}
  .legend-item {{ display: flex; align-items: center; gap: 10px; margin-bottom: 8px; font-size: 13px; }}
  .legend-swatch {{ width: 14px; height: 14px; border-radius: 4px; flex-shrink: 0; }}
  .legend-name {{ width: 90px; flex-shrink: 0; color: #ccc; font-weight: 600; }}
  .legend-detail {{ width: 170px; flex-shrink: 0; color: #6a6f7a; font-size: 12px; }}
  .legend-bar {{ flex-shrink: 0; }}
  .legend-score {{ color: #8a8f9a; font-weight: 600; }}

  .theme-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; max-width: 1600px; margin: 0 auto; }}
  .theme-card {{ background: #252830; border-radius: 14px; overflow: hidden; border: 2px solid #333840; transition: border-color .2s; }}
  .theme-card.recommended {{ border-color: #f0b90b; box-shadow: 0 0 24px rgba(240,185,11,.12); }}
  .card-header {{ padding: 16px 18px 12px; border-bottom: 1px solid #333840; }}
  .dual-swatch {{ display: inline-block; vertical-align: middle; margin-right: 10px; }}
  .swatch-p {{ display: inline-block; width: 24px; height: 24px; border-radius: 6px 0 0 6px; }}
  .swatch-c {{ display: inline-block; width: 24px; height: 24px; border-radius: 0 6px 6px 0; }}
  .card-meta {{ display: inline-block; vertical-align: middle; }}
  .theme-name {{ font-size: 16px; font-weight: 700; color: #fff; }}
  .badge {{ display: inline-block; margin-left: 8px; padding: 2px 8px; background: #f0b90b; color: #1a1d23; font-size: 11px; font-weight: 700; border-radius: 4px; vertical-align: middle; }}
  .theme-spec {{ margin-top: 6px; display: flex; gap: 14px; }}
  .spec-layout, .spec-palette {{ font-size: 12px; color: #8a8f9a; }}
  .theme-desc {{ margin-top: 4px; font-size: 12px; color: #6a6f7a; line-height: 1.5; }}
  .theme-ct {{ margin-top: 5px; }}
  .ct-tag {{ display: inline-block; margin-right: 4px; padding: 1px 6px; font-size: 10px; color: #6a6f7a; background: #333840; border-radius: 3px; }}
  .card-preview {{ padding: 4px 0 0; max-height: 420px; overflow-y: auto; -webkit-overflow-scrolling: touch; }}
  .card-preview section {{ margin: 0 !important; }}

  .action-bar {{ max-width: 1600px; margin: 40px auto 0; text-align: center; padding: 24px; background: #252830; border-radius: 12px; }}
  .action-bar p {{ font-size: 14px; color: #8a8f9a; line-height: 1.8; }}
  .action-bar code {{ background: #333840; color: #f0b90b; padding: 2px 8px; border-radius: 4px; font-size: 13px; }}
  .action-bar .mix-note {{ font-size: 12px; color: #555a63; margin-top: 10px; }}

  @media (max-width: 1200px) {{ .theme-grid {{ grid-template-columns: repeat(3, 1fr); }} }}
  @media (max-width: 900px)  {{ .theme-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
  @media (max-width: 560px)  {{
    body {{ padding: 16px 8px 32px; }}
    .theme-grid {{ grid-template-columns: 1fr; gap: 16px; }}
    .legend-detail {{ display: none; }}
  }}
</style>
</head>
<body>

<div class="page-header">
  <h1>🎨 排版风格预览</h1>
  <p class="subtitle">{title_display}</p>
  <div class="ct-info">{ct_info}</div>
</div>

<div class="legend">
  <div class="legend-title">📊 内容匹配度 — 每张卡片展示该布局的专属结构样本</div>
  {legend_items}
</div>

<div class="theme-grid">{cards_html}</div>

<div class="action-bar">
  <p>👆 每张卡片 = 一套 <strong>布局结构</strong>（📐） × <strong>配色方案</strong>（🎨）</p>
  <p>不同布局的 HTML 骨架不同 —— 不是换颜色，是换结构</p>
  <p>选定后回复预设名：<code>slate</code> <code>ruby</code> <code>zen</code> <code>moyu</code> <code>olive</code> <code>ticket</code> <code>graph</code> …</p>
  <p>或自由组合：<code>moyu:emerald</code> <code>zen:slate-rose</code></p>
</div>

</body>
</html>'''


def main():
    args = sys.argv[1:]
    input_file = "output/article-class-html.html"
    do_open = False
    for a in args:
        if a == "--open": do_open = True
        elif not a.startswith("--"): input_file = a

    html_path = os.path.join(SKILL_ROOT, input_file) if not os.path.isabs(input_file) else input_file
    if not os.path.exists(html_path):
        print(f"❌ 文件不存在: {html_path}"); sys.exit(1)

    with open(html_path, "r", encoding="utf-8") as f:
        full_html = f.read()

    text = re.sub(r'<[^>]+>', '', full_html)
    text = re.sub(r'\s+', ' ', text)

    title = ""
    m = re.search(r'class="meta-desc"[^>]*>([^<]+)', full_html)
    if m: title = m.group(1).strip()

    result = recommend(text)
    ranked = result["presets"]
    content_type_name = result.get("content_type_name", "")
    content_type_conf = result.get("content_type_confidence", "")

    print("📊 内容匹配分析:")
    print(f"   📝 文章类型: {content_type_name}（置信度: {content_type_conf}）")
    for key, preset, score in ranked:
        layout_key = preset["layout"]
        layout = LAYOUTS.get(layout_key, {"name": layout_key, "desc": ""})
        palette = PALETTES[preset["palette"]]
        marker = " ⭐" if score == ranked[0][1] else ""
        ct = ", ".join(CONTENT_TYPE_NAMES.get(c, c) for c in preset.get("content_types", [])[:2])
        print(f"   {preset['name']:8s} | 📐{layout['name']:6s} × 🎨{palette['name']:6s} | {score:2d} 分 | 🏷️ {ct}{marker}")

    print(f"\n🔧 渲染 12 套布局专属样本...")
    preview_html = generate_preview_page(result, title)
    out_path = os.path.join(SKILL_ROOT, "output", "theme-preview.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(preview_html)

    print(f"✅ 预览页已生成: {out_path}")
    print(f"   大小: {len(preview_html)} 字符 | 每张卡片展示该布局的独特结构")

    if do_open:
        webbrowser.open("file://" + out_path)
        print("🌐 已在浏览器中打开")


if __name__ == "__main__":
    main()