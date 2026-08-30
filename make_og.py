# -*- coding: utf-8 -*-
"""記事ごとのOGP画像(1200x630)を og/slug.png に生成。
ヒーローSVG＋タイトル＋ブランド名を紙背景に組んで headless Chrome で撮影。"""
import io, os, re, subprocess, tempfile, html
import svg_lib
from build_blog import ARTICLES, SRC

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PAGE = """<meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@600;700&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap">
<style>
html,body{margin:0;padding:0}
.og{width:1200px;height:630px;background:#FAF7F1;position:relative;overflow:hidden;
  background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 39px,#EAE3D5 39px,#EAE3D5 40px);
  font-family:'Zen Kaku Gothic New',sans-serif}
.hero{position:absolute;left:80px;right:80px;top:56px}
.hero svg{width:100%%;height:auto;display:block;border-radius:14px}
.title{position:absolute;left:80px;right:80px;top:388px;font-family:'Shippori Mincho',serif;
  font-weight:700;font-size:46px;line-height:1.5;color:#2B2926;letter-spacing:.01em}
.brand{position:absolute;left:80px;bottom:44px;font-family:'Shippori Mincho',serif;
  font-weight:700;font-size:26px;color:#C73E3A}
.free{position:absolute;right:80px;bottom:44px;font-size:20px;color:#6E6960}
.bar{position:absolute;left:0;top:0;bottom:0;width:14px;background:#C73E3A}
</style>
<div class="og"><div class="bar"></div>
<div class="hero">%(hero)s</div>
<div class="title">%(title)s</div>
<div class="brand">✍ 赤ペン願書ラボ</div>
<div class="free">無料でセルフチェックできます</div>
</div>"""

os.makedirs("og", exist_ok=True)
made = 0
for src, slug in ARTICLES:
    hero_fn = svg_lib.HEROES.get(slug)
    if not hero_fn:
        print("skip (heroなし)", slug); continue
    raw = io.open(SRC + src, encoding="utf-8").read()
    title = re.match(r"#\s*(.+)", raw).group(1).strip()
    # タイトルが長い場合は少し縮める
    size = 46 if len(title) <= 24 else (40 if len(title) <= 30 else 36)
    page = PAGE % {"hero": hero_fn(), "title": html.escape(title)}
    page = page.replace("font-size:46px", "font-size:%dpx" % size)
    tmp = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8")
    tmp.write(page); tmp.close()
    out = "og/" + slug.replace(".html", ".png")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", "--window-size=1200,630",
        "--virtual-time-budget=4000", "--screenshot=" + out, "file://" + tmp.name],
        capture_output=True)
    os.unlink(tmp.name)
    print("og:", out, os.path.getsize(out), "bytes")
    made += 1
print("done", made)
