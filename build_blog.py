# -*- coding: utf-8 -*-
# 記事md → ブランドHTML 変換ビルダー
import re, os, html, datetime

BASE = "https://akapen-lab.com/"
SRC = "/Users/morikawa/Desktop/AIチェッカー/24h-engine/seo/"

ARTICLES = [
    ("記事1本文.md", "gansho-ai-kakikata.html"),
    ("記事2本文.md", "shibouriyusho-chatgpt-bareru.html"),
    ("記事3本文.md", "shougakkoujuken-gansho-reibun.html"),
    ("記事4本文.md", "gansho-aippoi-naoshikata.html"),
]

# 公開日（記事ごとに固定）。ここに無いスラッグはビルド当日の日付になる。
PUBDATES = {
    "gansho-ai-kakikata.html": "2026-08-28",
    "shibouriyusho-chatgpt-bareru.html": "2026-08-28",
    "shougakkoujuken-gansho-reibun.html": "2026-08-28",
    "gansho-aippoi-naoshikata.html": "2026-08-28",
}

CSS = """
  :root { --paper:#FAF7F1; --paper-line:#EAE3D5; --card:#FFFFFF; --ink:#2B2926; --ink-soft:#6E6960;
    --redpen:#C73E3A; --redpen-soft:#F6E3E2; --green:#4A7C59; --green-soft:#E4EEE7;
    --serif:"Shippori Mincho",serif; --sans:"Zen Kaku Gothic New",sans-serif; }
  * { box-sizing:border-box; } html,body { margin:0; padding:0; }
  body { background:var(--paper);
    background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 31px,var(--paper-line) 31px,var(--paper-line) 32px);
    color:var(--ink); font-family:var(--sans); line-height:2.0; }
  .wrap { max-width:680px; margin:0 auto; padding:36px 20px 90px; }
  .sitebar { font-size:13px; margin-bottom:26px; display:flex; gap:14px; flex-wrap:wrap; align-items:center; }
  .sitebar .logo { font-family:var(--serif); font-weight:700; color:var(--redpen); font-size:16px; text-decoration:none; }
  .sitebar a { color:var(--ink-soft); text-decoration:none; }
  .sitebar a:hover { color:var(--redpen); }
  h1 { font-family:var(--serif); font-weight:700; font-size:clamp(23px,4.4vw,30px); line-height:1.6; margin:0 0 10px; }
  .meta { font-size:12px; color:var(--ink-soft); margin-bottom:26px; }
  h2 { font-family:var(--serif); font-size:20px; font-weight:700; margin:42px 0 14px; padding-left:12px; border-left:4px solid var(--redpen); line-height:1.6; }
  p { margin:14px 0; font-size:15px; }
  table { border-collapse:collapse; width:100%; font-size:13.5px; background:var(--card); margin:16px 0; }
  th,td { border:1px solid var(--paper-line); padding:9px 12px; text-align:left; }
  th { font-family:var(--serif); background:#F5F0E6; }
  .tablewrap { overflow-x:auto; }
  ul,ol { padding-left:1.5em; } li { margin:6px 0; font-size:15px; }
  .cta { background:var(--card); border:1.5px solid var(--redpen); border-radius:8px; padding:20px 22px; margin:28px 0; }
  .cta .t { font-family:var(--serif); font-weight:700; font-size:16px; margin-bottom:6px; }
  .cta p { font-size:13.5px; color:var(--ink-soft); margin:0 0 14px; }
  .cta a.btn { display:inline-block; background:var(--redpen); color:#fff; text-decoration:none;
    font-family:var(--serif); font-weight:600; font-size:14px; padding:10px 20px; border-radius:6px; margin:0 8px 8px 0; }
  .cta a.btn.sub { background:#fff; color:var(--redpen); border:1.5px solid var(--redpen); }
  .related { margin-top:48px; }
  .related h3 { font-family:var(--serif); font-size:16px; border-left:4px solid var(--redpen); padding-left:10px; }
  .related a { display:block; color:var(--ink); text-decoration:none; background:var(--card);
    border:1px solid var(--paper-line); border-radius:6px; padding:12px 16px; margin:10px 0; font-size:14px; }
  .related a:hover { border-color:var(--redpen); }
  footer { margin-top:52px; padding-top:16px; border-top:1px solid var(--paper-line); font-size:12px; color:var(--ink-soft); line-height:2; }
  .tana-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:12px; }
  .tana-card { display:block; background:var(--card); border:1px solid var(--paper-line); border-radius:6px; padding:15px 17px; text-decoration:none; color:var(--ink); }
  .tana-card:hover { border-color:var(--redpen); }
  .tana-card .t { font-family:var(--serif); font-weight:700; font-size:14.5px; margin-bottom:6px; }
  .tana-card p { font-size:12.5px; color:var(--ink-soft); margin:0 0 8px; line-height:1.8; }
  .tana-card .go { font-family:var(--serif); font-size:13px; color:var(--redpen); font-weight:600; }
"""

BRAIN = "https://brain-market.com/u/fulfull/a/b3UTMzYjMgoTZsNWa0JXY"
TANA = ('<h2>この先の一歩に</h2><div class="tana-grid">'
  '<a class="tana-card" href="' + BASE + '"><div class="t">無料チェッカー</div><p>願書・志望理由書のAIっぽさを赤ペン診断。</p><span class="go">試してみる →</span></a>'
  '<a class="tana-card" href="' + BRAIN + '"><div class="t">フル版パスコード（¥1,980）</div><p>すべての指摘と言い換え例、全文書き直し指示文の完全版。</p><span class="go">Brainで見る →</span></a>'
  '<a class="tana-card" href="https://utage-system.com/p/xBWncXOH1VaH?ref=akapen"><div class="t">教育費と新NISAの無料勉強会</div><p>受験の先にある教育費の計画を、オンラインで。</p><span class="go">詳しく見る →</span></a>'
  '<a class="tana-card" href="https://mm738966m-boop.github.io/yumekane-salon/?ref=akapen"><div class="t">ユメカネサロン（無料）</div><p>お金の話を気軽にできる、無料のオンラインの町。</p><span class="go">のぞいてみる →</span></a>'
  '</div><p style="font-size:11px;color:var(--ink-soft);margin-top:8px">※ 勉強会・サロンは、提携先fulfullの運営です。</p>')

CTA = ('<div class="cta"><div class="t">自分の文章のAIっぽさを、無料でチェックできます</div>'
  '<p>貼り付けるだけで、AIにありがちな表現に赤い波線が入ります。<br>登録不要・何度でも無料です。</p>'
  '<a class="btn" href="' + BASE + '">願書AI感チェッカーを開く（無料）</a>'
  '<a class="btn sub" href="' + BASE + 'ao.html">総合型選抜・推薦の方はこちら</a></div>')

SITEBAR = ('<div class="sitebar"><a class="logo" href="' + BASE + 'blog/">✍ 赤ペン願書ラボ</a>'
  '<a href="' + BASE + '">無料チェッカー</a><a href="' + BASE + 'ao.html">総合型選抜版</a>'
  '<a href="' + BASE + 'blog/">読みもの一覧</a></div>')

FOOTER = ('<footer>本記事は一般的な情報提供であり、合格・合否を保証するものではありません。<br>'
  '出願先の学校・大学が生成AIの使用について規定を設けている場合は、必ずそちらに従ってください。<br>'
  '運営：赤ペン願書ラボ</footer>')

def md_to_html(body, others):
    lines = body.split("\n")
    out, para, table, ul = [], [], [], []
    def flush_para():
        if para:
            out.append("<p>" + "<br>".join(html.escape(x) for x in para) + "</p>")
            para.clear()
    def flush_table():
        if table:
            rows = [r.strip().strip("|").split("|") for r in table]
            rows = [r for r in rows if not all(re.match(r"^[\s:-]*$", c) for c in r)]
            t = "<div class=\"tablewrap\"><table>"
            for i, r in enumerate(rows):
                tag = "th" if i == 0 else "td"
                t += "<tr>" + "".join("<%s>%s</%s>" % (tag, html.escape(c.strip()), tag) for c in r) + "</tr>"
            t += "</table></div>"
            out.append(t)
            table.clear()
    def flush_ul():
        if ul:
            out.append("<ul>" + "".join("<li>%s</li>" % html.escape(x) for x in ul) + "</ul>")
            ul.clear()
    for ln in lines:
        s = ln.strip()
        if s == "{CTA}":
            flush_para(); flush_table(); flush_ul(); out.append(CTA); continue
        if s.startswith("## "):
            flush_para(); flush_table(); flush_ul()
            out.append("<h2>" + html.escape(s[3:]) + "</h2>"); continue
        if s.startswith("|"):
            flush_para(); flush_ul(); table.append(s); continue
        if s.startswith("- ") or s.startswith("・"):
            flush_para(); flush_table(); ul.append(s.lstrip("-・ ")); continue
        if s == "":
            flush_para(); flush_table(); flush_ul(); continue
        para.append(s)
    flush_para(); flush_table(); flush_ul()
    h = "\n".join(out)
    h = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", h)
    rel = "".join('<a href="%s">%s</a>' % (u, html.escape(t)) for t, u in others)
    return h + '<div class="related"><h3>あわせて読みたい</h3>' + rel + "</div>"

def build():
    metas = []
    for src, slug in ARTICLES:
        raw = open(SRC + src, encoding="utf-8").read()
        m = re.match(r"#\s*(.+?)\n(?:\*{0,2}description\*{0,2}[:：]\s*(.+?)\n)?", raw)
        title = m.group(1).strip()
        desc = (m.group(2) or "").strip().strip("*")
        body = raw[m.end():]
        # 本文先頭に残った description 行を除去
        blines = body.split("\n")
        while blines and (blines[0].strip() == "" or re.match(r"^\**description\**[:：]", blines[0].strip(), re.I)):
            if re.match(r"^\**description\**[:：]", blines[0].strip(), re.I) and not desc:
                desc = re.sub(r"^\**description\**[:：]\s*", "", blines[0].strip(), flags=re.I).strip("*")
            blines.pop(0)
        body = "\n".join(blines)
        metas.append((title, desc, slug, body))
    today = datetime.date.today().isoformat()
    for i, (title, desc, slug, body) in enumerate(metas):
        pubdate = PUBDATES.get(slug, today)
        others = [(t, BASE + "blog/" + s) for j, (t, d, s, b) in enumerate(metas) if j != i]
        art = md_to_html(body, others)
        page = ("<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
          "<title>" + html.escape(title) + "｜赤ペン願書ラボ</title>\n"
          "<meta name=\"description\" content=\"" + html.escape(desc) + "\">\n"
          "<meta property=\"og:title\" content=\"" + html.escape(title) + "\">\n"
          "<meta property=\"og:description\" content=\"" + html.escape(desc) + "\">\n"
          "<meta property=\"og:image\" content=\"" + BASE + "og-oju.png\">\n"
          "<meta property=\"og:url\" content=\"" + BASE + "blog/" + slug + "\">\n"
          "<meta property=\"og:type\" content=\"article\">\n"
          "<meta name=\"twitter:card\" content=\"summary_large_image\">\n"
          "<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@600;700&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap\">\n"
          "<style>" + CSS + "</style>\n<div class=\"wrap\">" + SITEBAR
          + "<h1>" + html.escape(title) + "</h1><div class=\"meta\">" + pubdate + " ｜ 赤ペン願書ラボ</div>"
          + art + TANA + FOOTER + "</div>")
        os.makedirs("blog", exist_ok=True)
        open("blog/" + slug, "w", encoding="utf-8").write(page)
        print("built", slug, len(page))
    # 一覧
    cards = "".join('<a href="%s">%s<small>%s</small></a>' % (s, html.escape(t), html.escape(d)) for t, d, s, b in metas)
    idx = ("<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
      "<title>読みもの一覧｜赤ペン願書ラボ</title>\n"
      "<meta name=\"description\" content=\"願書・志望理由書の書き方と、AIとの上手な付き合い方のコラム集。\">\n"
      "<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@600;700&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap\">\n"
      "<style>" + CSS + " .related a small{display:block;color:var(--ink-soft);font-size:12px;margin-top:4px;font-weight:400;}"
      ".related a{font-weight:700;}</style>\n<div class=\"wrap\">" + SITEBAR
      + "<h1>読みもの一覧</h1><div class=\"meta\">願書・志望理由書の書き方と、AIとの上手な付き合い方。</div>"
      + '<div class="related">' + cards.replace("<a ", '<a class="card" ') + "</div>" + CTA + TANA + FOOTER + "</div>")
    open("blog/index.html", "w", encoding="utf-8").write(idx)
    # sitemap / robots
    urls = [BASE, BASE + "ao.html", BASE + "blog/"] + [BASE + "blog/" + s for t, d, s, b in metas]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sm += "  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n" % (u, today)
    sm += "</urlset>\n"
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    open("robots.txt", "w", encoding="utf-8").write("User-agent: *\nAllow: /\nSitemap: " + BASE + "sitemap.xml\n")
    print("index+sitemap+robots done")

if __name__ == "__main__":
    build()
