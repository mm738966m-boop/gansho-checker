# -*- coding: utf-8 -*-
# 記事md → ブランドHTML 変換ビルダー
# 図解・ヒーロー画像は svg_lib.py（同じディレクトリに必須）
import re, os, html, datetime
import svg_lib

BASE = "https://akapen-lab.com/"
SRC = "/Users/morikawa/Desktop/AIチェッカー/24h-engine/seo/"

ARTICLES = [
    ("記事1本文.md", "gansho-ai-kakikata.html"),
    ("記事2本文.md", "shibouriyusho-chatgpt-bareru.html"),
    ("記事3本文.md", "shougakkoujuken-gansho-reibun.html"),
    ("記事4本文.md", "gansho-aippoi-naoshikata.html"),
    ("記事5本文.md", "chugakujuken-shibouriyusho-kakikata.html"),
    ("記事6本文.md", "shibouriyusho-ai-tsukaikata.html"),
    ("記事7本文.md", "gansho-shibouriyusho-chigai.html"),
    ("記事8本文.md", "shougakkoujuken-mensetsu-gansho-icchi.html"),
    ("記事9本文.md", "shibouriyusho-chushouteki-naoshikata.html"),
    ("記事10本文.md", "ao-nyushi-shibouriyusho-ai.html"),
    ("記事11本文.md", "sougougata-katsudouhoukokusho.html"),
    ("記事12本文.md", "gansho-katei-kyouiku-houshin.html"),
    ("記事13本文.md", "setsumeikai-ikenakatta-shibouriyusho.html"),
]

# 公開日（記事ごとに固定）。ここに無いスラッグはビルド当日の日付になる。
PUBDATES = {
    "gansho-ai-kakikata.html": "2026-08-28",
    "shibouriyusho-chatgpt-bareru.html": "2026-08-28",
    "shougakkoujuken-gansho-reibun.html": "2026-08-28",
    "gansho-aippoi-naoshikata.html": "2026-08-28",
    "chugakujuken-shibouriyusho-kakikata.html": "2026-08-29",
    "shibouriyusho-ai-tsukaikata.html": "2026-08-29",
    "gansho-shibouriyusho-chigai.html": "2026-08-29",
    "shougakkoujuken-mensetsu-gansho-icchi.html": "2026-08-29",
    "shibouriyusho-chushouteki-naoshikata.html": "2026-08-29",
    "ao-nyushi-shibouriyusho-ai.html": "2026-08-29",
    "sougougata-katsudouhoukokusho.html": "2026-08-30",
    "gansho-katei-kyouiku-houshin.html": "2026-08-30",
    "setsumeikai-ikenakatta-shibouriyusho.html": "2026-09-01",
}


# トピッククラスタ：ハブページと「あわせて読みたい」の厳選に使う。
# 記事は複数クラスタに属してよい。未公開スラッグを書いてもよい（公開分だけ拾われる）。
CLUSTERS = {
    "guide-shougakkoujuken.html": {
        "title": "小学校受験の願書ガイド",
        "desc": "小学校受験の願書・面接準備の記事をまとめました。例文の作り方から提出前の確認まで。",
        "slugs": ["shougakkoujuken-gansho-reibun.html", "shougakkoujuken-mensetsu-gansho-icchi.html",
                  "gansho-katei-kyouiku-houshin.html", "gansho-shibouriyusho-chigai.html",
                  "gansho-ai-kakikata.html", "setsumeikai-ikenakatta-shibouriyusho.html"],
    },
    "guide-chugakujuken.html": {
        "title": "中学受験の志望理由書ガイド",
        "desc": "中学受験の志望理由書の記事をまとめました。構成の型・字数配分・直し方まで。",
        "slugs": ["chugakujuken-shibouriyusho-kakikata.html", "shibouriyusho-chushouteki-naoshikata.html",
                  "gansho-katei-kyouiku-houshin.html", "gansho-shibouriyusho-chigai.html",
                  "shibouriyusho-ai-tsukaikata.html", "setsumeikai-ikenakatta-shibouriyusho.html"],
    },
    "guide-sougougata.html": {
        "title": "総合型選抜・推薦ガイド",
        "desc": "総合型選抜（AO）・推薦入試の書類の記事をまとめました。志望理由書・活動報告書・面接まで。",
        "slugs": ["ao-nyushi-shibouriyusho-ai.html", "sougougata-katsudouhoukokusho.html",
                  "shibouriyusho-chatgpt-bareru.html"],
    },
    "guide-ai-kihon.html": {
        "title": "願書×AIの基本ガイド",
        "desc": "AIと願書・志望理由書の付き合い方の記事をまとめました。使い方の線引きから直し方まで。",
        "slugs": ["gansho-ai-kakikata.html", "shibouriyusho-ai-tsukaikata.html",
                  "gansho-aippoi-naoshikata.html", "shibouriyusho-chatgpt-bareru.html",
                  "shibouriyusho-chushouteki-naoshikata.html"],
    },
}

CSS = """
  :root { --paper:#FAF7F1; --paper-line:#EAE3D5; --card:#FFFFFF; --ink:#2B2926; --ink-soft:#6E6960;
    --redpen:#C73E3A; --redpen-soft:#F6E3E2; --green:#4A7C59; --green-soft:#E4EEE7;
    --serif:"Shippori Mincho",serif; --sans:"Zen Kaku Gothic New",sans-serif; }
  * { box-sizing:border-box; } html,body { margin:0; padding:0; }
  body { background:var(--paper);
    background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 31px,var(--paper-line) 31px,var(--paper-line) 32px);
    color:var(--ink); font-family:var(--sans); line-height:2.05; }
  .wrap { max-width:680px; margin:0 auto; padding:36px 20px 90px; }
  .sitebar { font-size:14px; margin-bottom:26px; display:flex; gap:14px; flex-wrap:wrap; align-items:center; }
  .sitebar .logo { font-family:var(--serif); font-weight:700; color:var(--redpen); font-size:16px; text-decoration:none; }
  .sitebar a { color:var(--ink-soft); text-decoration:none; }
  .sitebar a:hover { color:var(--redpen); }
  h1 { font-family:var(--serif); font-weight:700; font-size:clamp(25px,4.6vw,32px); line-height:1.6; margin:0 0 10px; }
  .meta { font-size:12px; color:var(--ink-soft); margin-bottom:22px; }
  h2 { font-family:var(--serif); font-size:21.5px; font-weight:700; margin:52px 0 16px; padding-left:12px; border-left:4px solid var(--redpen); line-height:1.6; scroll-margin-top:16px; }
  h2 .n { display:inline-block; font-family:var(--sans); font-size:11px; font-weight:700; color:#fff;
    background:var(--redpen); border-radius:50%; width:21px; height:21px; line-height:21px; text-align:center;
    margin-right:9px; vertical-align:3px; }
  p { margin:0 0 22px; font-size:16.5px; }
  table { border-collapse:collapse; width:100%; font-size:14.5px; background:var(--card); margin:16px 0; }
  th,td { border:1px solid var(--paper-line); padding:9px 12px; text-align:left; }
  th { font-family:var(--serif); background:#F5F0E6; }
  .tablewrap { overflow-x:auto; }
  ol { padding-left:1.5em; } li { margin:7px 0; font-size:16px; }
  ul.cl { list-style:none; padding-left:0; background:var(--card); border:1px solid var(--paper-line);
    border-radius:8px; padding:16px 20px; margin:22px 0; }
  ul.cl li { position:relative; padding-left:1.8em; line-height:1.9; }
  ul.cl li + li { margin-top:10px; padding-top:10px; border-top:1px dashed var(--paper-line); }
  ul.cl li:before { content:"✓"; position:absolute; left:0; top:0; color:var(--redpen); font-weight:700; }
  ul.cl li + li:before { top:10px; }
  .cta { background:var(--card); border:1.5px solid var(--redpen); border-radius:8px; padding:20px 22px; margin:28px 0; }
  .cta .t { font-family:var(--serif); font-weight:700; font-size:16px; margin-bottom:6px; }
  .cta p { font-size:14.5px; color:var(--ink-soft); margin:0 0 14px; }
  .cta a.btn { display:inline-block; background:var(--redpen); color:#fff; text-decoration:none;
    font-family:var(--serif); font-weight:600; font-size:15px; padding:10px 20px; border-radius:6px; margin:0 8px 8px 0; }
  .cta a.btn.sub { background:#fff; color:var(--redpen); border:1.5px solid var(--redpen); }
  .related { margin-top:48px; }
  .related h3 { font-family:var(--serif); font-size:16px; border-left:4px solid var(--redpen); padding-left:10px; }
  .related a { display:block; color:var(--ink); text-decoration:none; background:var(--card);
    border:1px solid var(--paper-line); border-radius:6px; padding:13px 17px; margin:10px 0; font-size:15px; }
  .related a:hover { border-color:var(--redpen); }
  footer { margin-top:52px; padding-top:16px; border-top:1px solid var(--paper-line); font-size:13px; color:var(--ink-soft); line-height:2; }
  .tana-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:12px; }
  .tana-card { display:block; background:var(--card); border:1px solid var(--paper-line); border-radius:6px; padding:15px 17px; text-decoration:none; color:var(--ink); }
  .tana-card:hover { border-color:var(--redpen); }
  .tana-card .t { font-family:var(--serif); font-weight:700; font-size:15.5px; margin-bottom:6px; }
  .tana-card p { font-size:13.5px; color:var(--ink-soft); margin:0 0 8px; line-height:1.8; }
  .tana-card .go { font-family:var(--serif); font-size:13px; color:var(--redpen); font-weight:600; }
  /* ── 図解・イメージ画像 ── */
  .hero { margin:0 0 24px; }
  .hero svg { width:100%; height:auto; display:block; border-radius:10px; }
  figure.fig { margin:32px 0; }
  figure.fig svg { width:100%; height:auto; display:block; background:var(--card);
    border:1px solid var(--paper-line); border-radius:9px; }
  figure.fig figcaption { font-size:13.5px; color:var(--ink-soft); line-height:1.85; margin-top:9px;
    padding-left:13px; border-left:2px solid var(--paper-line); }
  /* ── リード・目次 ── */
  .lead { background:var(--card); border-left:4px solid var(--redpen); border-radius:0 8px 8px 0;
    padding:15px 18px; margin:0 0 24px; }
  .lead .t { font-family:var(--serif); font-weight:700; font-size:13px; color:var(--redpen); margin-bottom:5px; }
  .lead p { font-size:14.5px; color:var(--ink-soft); margin:0; line-height:1.95; }
  .toc { background:var(--card); border:1px solid var(--paper-line); border-radius:8px; padding:15px 20px 17px; margin:0 0 34px; }
  .toc .th { font-family:var(--serif); font-weight:700; font-size:14.5px; margin-bottom:9px;
    display:flex; justify-content:space-between; align-items:baseline; gap:10px; }
  .toc .rt { font-family:var(--sans); font-weight:400; font-size:11.5px; color:var(--ink-soft); white-space:nowrap; }
  .toc ol { margin:0; padding-left:1.4em; }
  .toc li { font-size:14px; margin:4px 0; line-height:1.8; }
  .toc a { color:var(--ink); text-decoration:none; border-bottom:1px solid transparent; }
  .toc a:hover { color:var(--redpen); border-bottom-color:var(--redpen); }
  /* ── Before / After ── */
  .ba { margin:22px 0; display:grid; gap:11px; }
  .ba .box { border-radius:8px; padding:14px 17px; font-size:15.5px; line-height:1.95; }
  .ba .box.b { background:var(--redpen-soft); border:1px solid #EBCFCD; }
  .ba .box.a { background:var(--green-soft); border:1px solid #C9DED1; }
  .ba .lbl { display:inline-block; font-family:var(--serif); font-weight:700; font-size:11px;
    padding:2px 10px; border-radius:20px; margin-bottom:6px; letter-spacing:.04em; }
  .ba .box.b .lbl { background:var(--redpen); color:#fff; }
  .ba .box.a .lbl { background:var(--green); color:#fff; }
  .hublinks { display:flex; flex-wrap:wrap; gap:9px; margin:34px 0 6px; }
  .hublinks.top { margin:4px 0 20px; }
  .hublinks a { font-family:var(--serif); font-size:14px; font-weight:600; color:var(--redpen);
    text-decoration:none; background:var(--card); border:1px solid var(--paper-line);
    border-radius:20px; padding:7px 16px; }
  .hublinks a:hover { border-color:var(--redpen); }
  /* ── 記事一覧カード ── */
  .postcard { display:block; background:var(--card); border:1px solid var(--paper-line); border-radius:9px;
    overflow:hidden; text-decoration:none; color:var(--ink); margin:14px 0; }
  .postcard:hover { border-color:var(--redpen); }
  .postcard svg { width:100%; height:auto; display:block; border-bottom:1px solid var(--paper-line); }
  .postcard .pb { padding:14px 18px 16px; }
  .postcard .pt { font-family:var(--serif); font-weight:700; font-size:17px; line-height:1.6; }
  .postcard .pd { font-size:13.5px; color:var(--ink-soft); line-height:1.85; margin-top:6px; }
  @media (max-width:520px) {
    figure.fig { margin:24px -4px; }
    .toc .th { flex-direction:column; gap:2px; }
  }
"""

BRAIN = "https://brain-market.com/u/fulfull/a/b3UTMzYjMgoTZsNWa0JXY"
BRAIN_SENSEI = "https://brain-market.com/u/fulfull/a/b3kDNzYjMgoTZsNWa0JXY"
TANA = ('<h2>この先の一歩に</h2><div class="tana-grid">'
  '<a class="tana-card" href="' + BASE + '"><div class="t">無料チェッカー</div><p>願書・志望理由書のAIっぽさを赤ペン診断。</p><span class="go">試してみる →</span></a>'
  '<a class="tana-card" href="' + BRAIN + '"><div class="t">フル版パスコード（¥1,980）</div><p>すべての指摘と言い換え例、全文書き直し指示文の完全版。</p><span class="go">Brainで見る →</span></a>'
  '<a class="tana-card" href="' + BRAIN_SENSEI + '"><div class="t">添削指導をされる先生へ（¥4,980）</div><p>生徒がAIで書いてくる時代の添削キット。質問集・文例・テンプレ30。</p><span class="go">Brainで見る →</span></a>'
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

FIG_RE = re.compile(r"^\{FIG:([A-Za-z0-9_-]+)\}$")
# 記事4の「Before：〜」形式と、記事3の「**Before例1**」＋次行以降の形式の両方を拾う
BA_INLINE_RE = re.compile(r"^(Before|After)[：:]\s*(.+)$")
BA_LABEL_RE = re.compile(r"^\*\*(Before|After)([^*]*)\*\*$")


def md_to_html(body, others):
    """記事md → HTML。見出しの一覧も返す（目次用）。"""
    lines = body.split("\n")
    out, para, table, ul, ba = [], [], [], [], []
    heads = []
    ba_label = [None]   # 「**Before例1**」形式で開いている最中のラベル

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
            out.append('<ul class="cl">' + "".join("<li>%s</li>" % html.escape(x) for x in ul) + "</ul>")
            ul.clear()

    def flush_ba():
        """Before／After の行を、ラベルごとに色分けカードへまとめる"""
        if not ba:
            return
        groups = []
        for kind, label, txt in ba:
            if groups and groups[-1][0] == label:
                groups[-1][2].append(txt)
            else:
                groups.append((label, kind, [txt]))
        h = '<div class="ba">'
        for label, kind, txts in groups:
            cls = "b" if kind == "Before" else "a"
            h += ('<div class="box %s"><span class="lbl">%s</span><br>%s</div>'
                  % (cls, html.escape(label), "<br>".join(html.escape(t) for t in txts)))
        out.append(h + "</div>")
        ba.clear()
        ba_label[0] = None

    def flush_all():
        flush_para(); flush_table(); flush_ul(); flush_ba()

    for ln in lines:
        s = ln.strip()

        if s == "":
            # 空行では Before/After のまとまりは切らない（例1・例2…を1つの塊で見せるため）
            flush_para(); flush_table(); flush_ul(); ba_label[0] = None
            continue

        if s == "{CTA}":
            flush_all(); out.append(CTA); continue

        mf = FIG_RE.match(s)
        if mf:
            flush_all()
            name = mf.group(1)
            if name in svg_lib.FIGURES:
                fn, cap = svg_lib.FIGURES[name]
                out.append('<figure class="fig">' + fn() + '<figcaption>' + html.escape(cap) + '</figcaption></figure>')
            else:
                print("  !! 未知の図解マーカー: %s" % name)
            continue

        if s.startswith("## "):
            flush_all()
            heads.append(s[3:])
            n = len(heads)
            out.append('<h2 id="s%d"><span class="n">%d</span>%s</h2>' % (n, n, html.escape(s[3:])))
            continue

        ml = BA_LABEL_RE.match(s)
        if ml:
            flush_para(); flush_table(); flush_ul()
            ba_label[0] = (ml.group(1), (ml.group(1) + ml.group(2)).strip())
            continue

        mb = BA_INLINE_RE.match(s)
        if mb:
            flush_para(); flush_table(); flush_ul()
            ba_label[0] = None
            ba.append((mb.group(1), mb.group(1), mb.group(2)))
            continue

        if ba_label[0]:
            ba.append((ba_label[0][0], ba_label[0][1], s))
            continue

        if s.startswith("|"):
            flush_para(); flush_ul(); flush_ba(); table.append(s); continue

        if s.startswith("- ") or s.startswith("・"):
            flush_para(); flush_table(); flush_ba(); ul.append(s.lstrip("-・ ")); continue

        flush_ba()
        para.append(s)

    flush_all()
    h = "\n".join(out)
    h = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", h)
    rel = "".join('<a href="%s">%s</a>' % (u, html.escape(t)) for t, u in others)
    return h + '<div class="related"><h3>あわせて読みたい</h3>' + rel + "</div>", heads


def toc_html(heads, body):
    """目次＋読了時間。見出しが3本未満なら出さない。"""
    if len(heads) < 3:
        return ""
    chars = len(re.sub(r"\s|\{[A-Z][^}]*\}", "", body))
    mins = max(1, round(chars / 500.0))
    items = "".join('<li><a href="#s%d">%s</a></li>' % (i + 1, html.escape(t)) for i, t in enumerate(heads))
    return ('<nav class="toc"><div class="th"><span>この記事の流れ</span>'
            '<span class="rt">読むのにかかる時間：約%d分</span></div><ol>%s</ol></nav>' % (mins, items))


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
    published = {s: t for t, d, s, b in metas}
    def related_for(slug):
        """同クラスタの公開記事を優先して最大3件。足りなければ他記事で補う。"""
        picks, seen = [], {slug}
        for hub, c in CLUSTERS.items():
            if slug in c["slugs"]:
                for s2 in c["slugs"]:
                    if s2 in published and s2 not in seen:
                        picks.append(s2); seen.add(s2)
        for t, d, s2, b in metas:
            if len(picks) >= 3: break
            if s2 not in seen:
                picks.append(s2); seen.add(s2)
        return [(published[s2], BASE + "blog/" + s2) for s2 in picks[:3]]
    def hubs_for(slug):
        return [(hub, c["title"]) for hub, c in CLUSTERS.items() if slug in c["slugs"]]
    for i, (title, desc, slug, body) in enumerate(metas):
        pubdate = PUBDATES.get(slug, today)
        art, heads = md_to_html(body, related_for(slug))
        hub_h = ""
        hs = hubs_for(slug)
        if hs:
            hub_h = ('<div class="hublinks">' + "".join(
                '<a href="%s">%s →</a>' % (h, html.escape(t)) for h, t in hs) + "</div>")
        art = art.replace('<div class="related">', hub_h + '<div class="related">', 1)
        hero = svg_lib.HEROES.get(slug)
        hero_h = '<div class="hero">' + hero() + "</div>" if hero else ""
        og_name = "og/" + slug.replace(".html", ".png")
        og_img = BASE + (og_name if os.path.exists(og_name) else "og-oju.png")
        import json as _json
        jsonld = ('<script type="application/ld+json">' + _json.dumps({
            "@context": "https://schema.org", "@type": "Article",
            "headline": title, "description": desc,
            "datePublished": pubdate, "dateModified": pubdate,
            "image": og_img,
            "mainEntityOfPage": BASE + "blog/" + slug,
            "author": {"@type": "Organization", "name": "赤ペン願書ラボ", "url": BASE},
            "publisher": {"@type": "Organization", "name": "赤ペン願書ラボ", "url": BASE},
        }, ensure_ascii=False) + "</script>")
        lead = ('<div class="lead"><div class="t">この記事でわかること</div><p>' + html.escape(desc) + "</p></div>") if desc else ""
        page = ("<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
          "<title>" + html.escape(title) + "｜赤ペン願書ラボ</title>\n"
          "<meta name=\"description\" content=\"" + html.escape(desc) + "\">\n"
          "<meta property=\"og:title\" content=\"" + html.escape(title) + "\">\n"
          "<meta property=\"og:description\" content=\"" + html.escape(desc) + "\">\n"
          "<meta property=\"og:image\" content=\"" + og_img + "\">\n"
          "<meta property=\"og:url\" content=\"" + BASE + "blog/" + slug + "\">\n"
          "<meta property=\"og:type\" content=\"article\">\n"
          "<meta name=\"twitter:card\" content=\"summary_large_image\">\n"
          "<link rel=\"canonical\" href=\"" + BASE + "blog/" + slug + "\">\n"
          + jsonld + "\n"
          "<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@600;700&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap\">\n"
          "<style>" + CSS + "</style>\n<div class=\"wrap\">" + SITEBAR
          + "<h1>" + html.escape(title) + "</h1><div class=\"meta\">" + pubdate + " ｜ 赤ペン願書ラボ</div>"
          + hero_h + lead + toc_html(heads, body)
          + art + TANA + FOOTER + "</div>")
        os.makedirs("blog", exist_ok=True)
        open("blog/" + slug, "w", encoding="utf-8").write(page)
        print("built", slug, len(page), "bytes /", len(heads), "見出し")
    # 一覧（各記事のイメージ画像つきカード）
    cards = ""
    for t, d, s, b in metas:
        hero = svg_lib.HEROES.get(s)
        cards += ('<a class="postcard" href="%s">%s<div class="pb"><div class="pt">%s</div><div class="pd">%s</div></div></a>'
                  % (s, hero() if hero else "", html.escape(t), html.escape(d)))
    idx = ("<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
      "<title>読みもの一覧｜赤ペン願書ラボ</title>\n"
      "<meta name=\"description\" content=\"願書・志望理由書の書き方と、AIとの上手な付き合い方のコラム集。\">\n"
      "<meta property=\"og:title\" content=\"読みもの一覧｜赤ペン願書ラボ\">\n"
      "<meta property=\"og:description\" content=\"願書・志望理由書の書き方と、AIとの上手な付き合い方のコラム集。\">\n"
      "<meta property=\"og:image\" content=\"" + BASE + "og-oju.png\">\n"
      "<meta property=\"og:url\" content=\"" + BASE + "blog/\">\n"
      "<meta name=\"twitter:card\" content=\"summary_large_image\">\n"
      "<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@600;700&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap\">\n"
      "<style>" + CSS + "</style>\n<div class=\"wrap\">" + SITEBAR
      + "<h1>読みもの一覧</h1><div class=\"meta\">願書・志望理由書の書き方と、AIとの上手な付き合い方。</div>"
      + '<div class="hublinks top">' + "".join('<a href="%s">%s →</a>' % (h, html.escape(c["title"])) for h, c in CLUSTERS.items()) + "</div>"
      + cards + CTA + TANA + FOOTER + "</div>")
    open("blog/index.html", "w", encoding="utf-8").write(idx)
    # ハブページ
    hub_slugs = []
    for hub, c in CLUSTERS.items():
        hcards = ""
        for s2 in c["slugs"]:
            if s2 not in published: continue
            t2 = published[s2]
            d2 = next(d for t, d, s3, b in metas if s3 == s2)
            hero2 = svg_lib.HEROES.get(s2)
            hcards += ('<a class="postcard" href="%s">%s<div class="pb"><div class="pt">%s</div><div class="pd">%s</div></div></a>'
                       % (s2, hero2() if hero2 else "", html.escape(t2), html.escape(d2)))
        hpage = ("<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
          "<title>" + html.escape(c["title"]) + "｜赤ペン願書ラボ</title>\n"
          "<meta name=\"description\" content=\"" + html.escape(c["desc"]) + "\">\n"
          "<meta property=\"og:title\" content=\"" + html.escape(c["title"]) + "\">\n"
          "<meta property=\"og:description\" content=\"" + html.escape(c["desc"]) + "\">\n"
          "<meta property=\"og:image\" content=\"" + BASE + "og-oju.png\">\n"
          "<meta property=\"og:url\" content=\"" + BASE + "blog/" + hub + "\">\n"
          "<link rel=\"canonical\" href=\"" + BASE + "blog/" + hub + "\">\n"
          "<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@600;700&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap\">\n"
          "<style>" + CSS + "</style>\n<div class=\"wrap\">" + SITEBAR
          + "<h1>" + html.escape(c["title"]) + "</h1><div class=\"meta\">" + html.escape(c["desc"]) + "</div>"
          + hcards + CTA + TANA + FOOTER + "</div>")
        open("blog/" + hub, "w", encoding="utf-8").write(hpage)
        hub_slugs.append(hub)
        print("built hub", hub)
    # sitemap / robots
    urls = [(BASE, today), (BASE + "ao.html", today), (BASE + "blog/", today)] + \
        [(BASE + "blog/" + h, today) for h in hub_slugs] + \
        [(BASE + "blog/" + s, PUBDATES.get(s, today)) for t, d, s, b in metas]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u, lm in urls:
        sm += "  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n" % (u, lm)
    sm += "</urlset>\n"
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    open("robots.txt", "w", encoding="utf-8").write("User-agent: *\nAllow: /\nSitemap: " + BASE + "sitemap.xml\n")
    print("index+sitemap+robots done")


if __name__ == "__main__":
    build()
