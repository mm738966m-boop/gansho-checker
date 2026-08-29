# -*- coding: utf-8 -*-
"""赤ペン願書ラボ ブログ用 図解ライブラリ（インラインSVG）

写真素材ではなくSVGを使う理由：
- 匿名運営のため人物写真・ストック写真の権利/出所管理を持ち込みたくない
- 原稿用紙×赤ペンのブランド色をそのまま使え、記事ごとに絵柄が散らからない
- 1枚2〜3KBで済み、Retinaでも輪郭が潰れない
"""

PAPER = "#F6F1E7"
LINE = "#EAE3D5"
CARD = "#FFFFFF"
INK = "#2B2926"
SOFT = "#6E6960"
RED = "#C73E3A"
REDBG = "#F9EAE9"
GRN = "#4A7C59"
GRNBG = "#E9F1EC"
SERIF = "Shippori Mincho, serif"
SANS = "Zen Kaku Gothic New, sans-serif"


_GRID_N = [0]


def _grid(x, y, cols, rows, s=14):
    """原稿用紙のマス目（patternで軽量化。idはページ内で衝突しないよう連番）"""
    _GRID_N[0] += 1
    gid = "g%d" % _GRID_N[0]
    return ('<defs><pattern id="%s" width="%g" height="%g" patternUnits="userSpaceOnUse">'
            '<rect width="%g" height="%g" fill="none" stroke="%s"/></pattern></defs>'
            '<rect x="%g" y="%g" width="%g" height="%g" fill="url(#%s)"/>'
            % (gid, s, s, s, s, LINE, x, y, cols * s, rows * s, gid))


def _txt(x, y, s, size=13, fill=INK, font=SANS, anchor="start", weight="400"):
    return ('<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" text-anchor="%s" font-weight="%s">%s</text>'
            % (x, y, font, size, fill, anchor, weight, s))


def _arrow_r(x, y, w=26, color=RED):
    """右向き矢印"""
    return ('<g stroke="%s" stroke-width="2" fill="none"><path d="M%g %gh%g"/></g>'
            '<path d="M%g %gl-7-5v10z" fill="%s"/>' % (color, x, y, w - 6, x + w, y, color))


def _arrow_d(x, y, h=22, color=RED):
    """下向き矢印"""
    return ('<g stroke="%s" stroke-width="2" fill="none"><path d="M%g %gv%g"/></g>'
            '<path d="M%g %gl-5-7h10z" fill="%s"/>' % (color, x, y, h - 6, x, y + h, color))


def _pen(x, y, scale=1.0, rot=0):
    """赤ペン（斜めのペン先）"""
    return ('<g transform="translate(%g,%g) scale(%g) rotate(%g)">'
            '<rect x="0" y="0" width="10" height="62" rx="4" fill="%s"/>'
            '<rect x="0" y="0" width="10" height="16" rx="4" fill="#A82F2C"/>'
            '<path d="M0 62h10l-5 12z" fill="#E8D9C4"/>'
            '<path d="M3.4 70h3.2l-1.6 4z" fill="%s"/></g>' % (x, y, scale, rot, RED, INK))


def _wave(x, y, w, color=RED):
    """赤ペンの波線"""
    d = "M%g %g" % (x, y)
    step = 6
    n = int(w / step)
    for i in range(n):
        d += "q3 -4 6 0" if i % 2 == 0 else "q3 4 6 0"
    return '<path d="%s" fill="none" stroke="%s" stroke-width="1.6"/>' % (d, color)


def _card(x, y, w, h, fill=CARD, stroke=LINE, r=7):
    return '<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s"/>' % (x, y, w, h, r, fill, stroke)


def _svg(h, label, inner):
    return ('<svg viewBox="0 0 640 %g" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="%s">%s</svg>'
            % (h, label, inner))


# ─────────────────────────────── ヒーロー（記事冒頭のイメージ画像）

def hero_ai():
    """記事1：AIに下書きを手伝ってもらう"""
    g = '<rect width="640" height="190" rx="10" fill="%s"/>' % PAPER
    g += _card(46, 34, 178, 122)
    g += _grid(58, 46, 11, 6, 14)
    g += _wave(72, 76, 60) + _wave(72, 118, 84)
    g += _arrow_r(246, 95, 40)
    # チャットの吹き出し
    g += _card(302, 40, 190, 52, CARD, LINE)
    g += '<path d="M318 92l4 14 14-14z" fill="%s" stroke="%s"/>' % (CARD, LINE)
    g += _txt(318, 63, "たたき台を作って", 13, SOFT)
    g += _txt(318, 81, "もらえますか", 13, SOFT)
    g += _card(342, 108, 190, 52, "#EFEAF5", "#DCD3E8")
    g += _txt(358, 131, "整った文章を返します", 13, "#5B4B77")
    g += _txt(358, 149, "ただし中身は空のまま", 13, "#5B4B77")
    g += _pen(560, 44, 1.0, 12)
    return _svg(190, "原稿用紙とAIのやり取りのイメージ", g)


def hero_eye():
    """記事2：読み手が書類のどこを見ているか"""
    g = '<rect width="640" height="190" rx="10" fill="%s"/>' % PAPER
    g += _card(60, 30, 230, 130)
    g += _grid(74, 44, 14, 6, 14)
    g += _wave(88, 74, 92) + _wave(88, 116, 64)
    # めがね
    g += ('<g fill="none" stroke="%s" stroke-width="3">'
          '<circle cx="392" cy="96" r="34"/><circle cx="480" cy="96" r="34"/>'
          '<path d="M426 92q18-10 20 0"/><path d="M358 84l-26-12"/><path d="M514 84l26-12"/></g>' % INK)
    g += _txt(436, 160, "読み手は、整った文章の奥を見ている", 13, SOFT, SANS, "middle")
    return _svg(190, "願書と、それを読む人のめがねのイメージ", g)


def hero_reibun():
    """記事3：例文に赤ペンで丸をつける"""
    g = '<rect width="640" height="190" rx="10" fill="%s"/>' % PAPER
    g += _card(150, 24, 250, 142)
    g += _grid(164, 38, 15, 7, 14)
    g += '<circle cx="222" cy="66" r="26" fill="none" stroke="%s" stroke-width="2.5"/>' % RED
    g += _wave(178, 122, 116)
    g += _txt(300, 152, "◎ここが伝わる", 13, RED, SERIF, "middle", "700")
    g += _card(424, 52, 152, 86, REDBG, "#EBCFCD")
    g += _txt(440, 80, "NG例", 12, RED, SERIF, "start", "700")
    g += _txt(440, 102, "豊かな人間性を", 12, SOFT)
    g += _txt(440, 120, "育んでまいりました", 12, SOFT)
    g += _pen(84, 40, 1.0, -14)
    return _svg(190, "願書の例文に赤ペンで印をつけるイメージ", g)


def hero_fix():
    """記事4：AIっぽい文章を直す前後"""
    g = '<rect width="640" height="190" rx="10" fill="%s"/>' % PAPER
    g += _card(40, 32, 200, 126, CARD, "#EBCFCD")
    g += _txt(56, 56, "Before", 12, RED, SERIF, "start", "700")
    for i, y in enumerate((78, 98, 118, 138)):
        g += '<rect x="56" y="%g" width="%g" height="6" rx="3" fill="#E3CFCD"/>' % (y - 5, 168 if i != 3 else 96)
    g += _wave(56, 88, 150)
    g += _arrow_r(258, 95, 46)
    g += _card(322, 32, 200, 126, CARD, "#C9DED1")
    g += _txt(338, 56, "After", 12, GRN, SERIF, "start", "700")
    for i, y in enumerate((78, 98, 118, 138)):
        g += '<rect x="338" y="%g" width="%g" height="6" rx="3" fill="#CFE0D5"/>' % (y - 5, 168 if i != 3 else 120)
    g += '<circle cx="360" cy="93" r="13" fill="none" stroke="%s" stroke-width="2"/>' % GRN
    g += _pen(556, 42, 1.0, 10)
    return _svg(190, "AIっぽい文章を家庭の言葉に直す前と後のイメージ", g)


# ─────────────────────────────── 本文中の図解

def fig_signs():
    """AIっぽさの3つのクセ"""
    g = ""
    items = [
        ("抽象語", "「豊かな学び」", "どの子にも当てはまり、", "何があったか見えない"),
        ("接続詞", "「そして」「また」", "同じつなぎ方が続き、", "機械的に感じられる"),
        ("語尾", "「〜と考えております」", "熱量が均一になり、", "書き手の顔が消える"),
    ]
    for i, (t, ex, l1, l2) in enumerate(items):
        x = 16 + i * 206
        g += _card(x, 34, 190, 148, CARD, "#EBCFCD")
        g += '<rect x="%g" y="34" width="190" height="4" rx="2" fill="%s"/>' % (x, RED)
        g += _txt(x + 95, 68, t, 16, RED, SERIF, "middle", "700")
        g += _card(x + 16, 82, 158, 30, REDBG, "none", 5)
        g += _txt(x + 95, 102, ex, 12.5, INK, SANS, "middle")
        g += _txt(x + 95, 134, l1, 12, SOFT, SANS, "middle")
        g += _txt(x + 95, 152, l2, 12, SOFT, SANS, "middle")
    g += _txt(320, 20, "AIっぽさが出やすい3つのクセ", 14, INK, SERIF, "middle", "700")
    return _svg(196, "AIっぽさが出やすい3つのクセ：抽象語・接続詞・語尾", g)


def fig_scene():
    """抽象語 → 具体的な場面"""
    g = _txt(320, 20, "抽象語を、その日の場面に置き換える", 14, INK, SERIF, "middle", "700")
    g += _card(20, 36, 250, 118, REDBG, "#EBCFCD")
    g += _txt(36, 60, "抽象語のまま", 12, RED, SERIF, "start", "700")
    g += _txt(36, 88, "貴校の教育方針に", 13.5, INK)
    g += _txt(36, 110, "強く共感いたしました", 13.5, INK)
    g += _wave(36, 118, 200)
    g += _txt(36, 140, "何を見て、そう思ったのか", 11.5, SOFT)
    g += _arrow_r(284, 95, 44)
    g += _card(352, 36, 268, 118, GRNBG, "#C9DED1")
    g += _txt(368, 60, "その日の場面に置き換える", 12, GRN, SERIF, "start", "700")
    g += _txt(368, 88, "上級生が休み時間に、下級生へ", 13.5, INK)
    g += _txt(368, 110, "折り紙を教えていました", 13.5, INK)
    g += _txt(368, 140, "読み手の頭の中に、絵が浮かぶ", 11.5, SOFT)
    return _svg(168, "抽象語を具体的な場面に置き換える対比図", g)


def fig_split():
    """AIに任せる / 家庭が担う"""
    g = _txt(320, 20, "AIに任せられること、家庭にしかできないこと", 14, INK, SERIF, "middle", "700")
    left = ["文章の型を整える", "言い回しの候補を出す", "文字数を調整する", "誤字を拾う"]
    right = ["その日、何があったか", "子どもが言った言葉", "家庭が大事にしてきたこと", "説明会で感じたこと"]
    g += _card(20, 36, 290, 172, "#EFEAF5", "#DCD3E8")
    g += _txt(40, 62, "AIに任せられる", 13.5, "#5B4B77", SERIF, "start", "700")
    for i, s in enumerate(left):
        g += '<circle cx="46" cy="%g" r="3.5" fill="#8B79AE"/>' % (88 + i * 28)
        g += _txt(60, 92 + i * 28, s, 13, INK)
    g += _card(330, 36, 290, 172, GRNBG, "#C9DED1")
    g += _txt(350, 62, "家庭にしか書けない", 13.5, GRN, SERIF, "start", "700")
    for i, s in enumerate(right):
        g += '<circle cx="356" cy="%g" r="3.5" fill="%s"/>' % (88 + i * 28, GRN)
        g += _txt(370, 92 + i * 28, s, 13, INK)
    g += _txt(320, 228, "AIは素材を言葉にする道具で、素材そのものは作れない", 12, SOFT, SANS, "middle")
    return _svg(242, "AIに任せられる作業と、家庭にしか書けない内容の切り分け", g)


def fig_3step():
    """家庭の言葉に直す3ステップ"""
    g = _txt(320, 20, "AIの下書きを、家庭の言葉に戻す3ステップ", 14, INK, SERIF, "middle", "700")
    steps = [("1", "事実を足す", "日付・場所・子どもの一言"),
             ("2", "語尾をゆるめる", "普段の話し言葉に近づける"),
             ("3", "声に出す", "つかえた所が、実感の薄い所")]
    for i, (n, t, d) in enumerate(steps):
        x = 24 + i * 206
        g += _card(x, 40, 186, 106)
        g += '<circle cx="%g" cy="40" r="16" fill="%s"/>' % (x + 93, RED)
        g += _txt(x + 93, 45, n, 14, "#fff", SERIF, "middle", "700")
        g += _txt(x + 93, 88, t, 14.5, INK, SERIF, "middle", "700")
        g += _txt(x + 93, 118, d, 11.5, SOFT, SANS, "middle")
        if i < 2:
            g += _arrow_r(x + 190, 93, 22)
    return _svg(164, "AIの下書きを家庭の言葉に戻す3つのステップ", g)


def fig_blind():
    """書いた本人 vs 初めて読む人"""
    g = _txt(320, 20, "同じ一文でも、見えているものが違う", 14, INK, SERIF, "middle", "700")
    g += _card(20, 36, 600, 40, "#F3EFE5", LINE)
    g += _txt(320, 62, "「豊かな学びの環境に魅力を感じました」", 15, INK, SERIF, "middle", "700")
    g += _arrow_d(170, 84, 22) + _arrow_d(470, 84, 22)
    g += _card(20, 116, 290, 112, GRNBG, "#C9DED1")
    g += _txt(165, 142, "書いた本人に見えているもの", 12.5, GRN, SERIF, "middle", "700")
    g += _txt(165, 170, "見学した日の廊下の掲示物、", 12, INK, SANS, "middle")
    g += _txt(165, 190, "子どもが立ち止まった場面", 12, INK, SANS, "middle")
    g += _txt(165, 214, "＝頭が勝手に補ってしまう", 11, SOFT, SANS, "middle")
    g += _card(330, 116, 290, 112, REDBG, "#EBCFCD")
    g += _txt(475, 142, "初めて読む人に見えるもの", 12.5, RED, SERIF, "middle", "700")
    g += _txt(475, 178, "（何も浮かばない）", 13, SOFT, SANS, "middle")
    g += _txt(475, 214, "＝だから自分では気づけない", 11, SOFT, SANS, "middle")
    return _svg(244, "同じ一文でも書いた本人と読み手で見えているものが違うことの図", g)


def fig_loop():
    """書く→見直す→直す のループ"""
    g = _txt(320, 20, "提出までにまわしたい、小さなループ", 14, INK, SERIF, "middle", "700")
    nodes = [("書く", 108), ("見直す", 320), ("直す", 532)]
    for t, x in nodes:
        g += '<circle cx="%g" cy="100" r="46" fill="%s" stroke="%s" stroke-width="1.5"/>' % (x, CARD, LINE)
        g += _txt(x, 105, t, 15, INK, SERIF, "middle", "700")
    g += _arrow_r(160, 100, 108) + _arrow_r(372, 100, 108)
    g += ('<path d="M532 148q0 30-212 30T108 148" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="5 4"/>' % RED)
    g += '<path d="M108 148l-5 9h10z" fill="%s"/>' % RED
    g += _txt(320, 202, "2〜3か所直したら、もう一度読み返す", 12, SOFT, SANS, "middle")
    return _svg(218, "書く・見直す・直すを繰り返すループの図", g)


def fig_struct():
    """志望理由書の構成の型"""
    g = _txt(320, 20, "伝わる文章の、いちばん基本の並び", 14, INK, SERIF, "middle", "700")
    items = [("きっかけ", "見た場面から始める", REDBG, "#EBCFCD", RED),
             ("重なり", "家庭の考えとどう合うか", "#F3EFE5", LINE, INK),
             ("これから", "入学後にどう育ってほしいか", GRNBG, "#C9DED1", GRN)]
    for i, (t, d, bg, st, fg) in enumerate(items):
        x = 16 + i * 206
        g += _card(x, 40, 190, 92, bg, st)
        g += _txt(x + 95, 74, t, 15.5, fg, SERIF, "middle", "700")
        g += _txt(x + 95, 104, d, 11.5, SOFT, SANS, "middle")
        if i < 2:
            g += _arrow_r(x + 192, 86, 18)
    g += _txt(320, 156, "字数の目安は 2 : 3 : 2。真ん中がいちばん厚くなる", 12, SOFT, SANS, "middle")
    return _svg(174, "きっかけ・重なり・これからという文章構成の型", g)


def hero_chugaku():
    """記事5：説明会のメモが志望理由書になる"""
    g = '<rect width="640" height="190" rx="10" fill="%s"/>' % PAPER
    # メモ帳
    g += _card(44, 30, 186, 132)
    g += '<rect x="44" y="30" width="186" height="20" rx="7" fill="#EFEAF5"/>'
    g += _txt(64, 45, "説明会メモ", 11.5, "#5B4B77", SANS, "start", "700")
    for i, y in enumerate((72, 92, 112, 132)):
        g += '<rect x="62" y="%g" width="%g" height="5" rx="2.5" fill="#E2DBCB"/>' % (y - 4, 150 if i % 2 == 0 else 108)
    g += '<rect x="222" y="58" width="8" height="26" rx="3" fill="%s"/>' % RED
    g += '<rect x="222" y="94" width="8" height="26" rx="3" fill="%s"/>' % GRN
    g += _arrow_r(252, 95, 40)
    # 原稿用紙
    g += _card(320, 26, 206, 140)
    g += _grid(334, 40, 12, 6, 14)
    g += '<circle cx="378" cy="61" r="20" fill="none" stroke="%s" stroke-width="2.2"/>' % RED
    g += _wave(348, 116, 130)
    g += _pen(564, 40, 1.0, 12)
    return _svg(190, "説明会のメモが志望理由書の一文になるイメージ", g)


def fig_ratio():
    """字数配分の目安"""
    g = _txt(320, 20, "600字なら、このくらいの配分がめやす", 14, INK, SERIF, "middle", "700")
    x0, y0, w, h = 40, 44, 560, 46
    segs = [("きっかけ", 2, REDBG, "#EBCFCD", RED, "約170字"),
            ("重なり", 3, "#F3EFE5", LINE, INK, "約260字"),
            ("これから", 2, GRNBG, "#C9DED1", GRN, "約170字")]
    x = x0
    for name, n, bg, st, fg, chars in segs:
        sw = w * n / 7.0
        g += '<rect x="%g" y="%g" width="%g" height="%g" fill="%s" stroke="%s"/>' % (x, y0, sw, h, bg, st)
        g += _txt(x + sw / 2, y0 + 22, name, 13.5, fg, SERIF, "middle", "700")
        g += _txt(x + sw / 2, y0 + 39, chars, 11, SOFT, SANS, "middle")
        x += sw
    g += _txt(320, 118, "2 ： 3 ： 2", 15, INK, SERIF, "middle", "700")
    g += _txt(320, 142, "決まりではなく、迷ったときに当たりをつけるための目安です", 12, SOFT, SANS, "middle")
    return _svg(158, "きっかけ2・重なり3・これから2という字数配分の帯グラフ", g)


def fig_memo():
    """見学メモから一文を作る"""
    g = _txt(320, 20, "その日のメモが、そのまま一文になる", 14, INK, SERIF, "middle", "700")
    # メモ帳
    g += _card(20, 40, 236, 150)
    g += '<rect x="20" y="40" width="236" height="22" rx="7" fill="#EFEAF5"/>'
    g += _txt(38, 56, "見学のときのメモ", 11.5, "#5B4B77", SANS, "start", "700")
    memo = ["10/12 説明会", "体育館の写真の前で足が止まった", "「ここで走ってみたい」"]
    for i, t in enumerate(memo):
        g += _txt(38, 88 + i * 30, t, 12, INK)
        g += '<path d="M38 %g h180" stroke="%s" stroke-width="1"/>' % (96 + i * 30, LINE)
    g += _arrow_r(268, 112, 38)
    # 出来上がった一文
    g += _card(326, 40, 294, 150, GRNBG, "#C9DED1")
    g += _txt(344, 66, "願書の一文になる", 12, GRN, SERIF, "start", "700")
    g += _txt(344, 96, "説明会の日、子どもは体育館の", 12.5, INK)
    g += _txt(344, 116, "写真の前で足を止め、", 12.5, INK)
    g += _txt(344, 136, "「ここで走ってみたい」と", 12.5, INK)
    g += _txt(344, 156, "言いました。", 12.5, INK)
    g += _txt(344, 180, "拾うのは、立ち止まった場所と、その場の一言", 10.5, SOFT)
    return _svg(204, "見学メモの内容が志望理由書の一文になる流れの図", g)


HEROES = {
    "gansho-ai-kakikata.html": hero_ai,
    "shibouriyusho-chatgpt-bareru.html": hero_eye,
    "shougakkoujuken-gansho-reibun.html": hero_reibun,
    "gansho-aippoi-naoshikata.html": hero_fix,
    "chugakujuken-shibouriyusho-kakikata.html": hero_chugaku,
}

FIGURES = {
    "signs": (fig_signs, "AIっぽさは感覚ではなく、抽象語・接続詞・語尾という具体的なクセとして現れます。"),
    "scene": (fig_scene, "同じ出来事でも、その日の場面に置き換えるだけで読み手に絵が浮かびます。"),
    "split": (fig_split, "型を整える作業はAIが得意ですが、素材そのものは家庭にしかありません。"),
    "3step": (fig_3step, "この3つを順に通すと、下書きは「たたき台」から「家庭の文章」に変わります。"),
    "blind": (fig_blind, "書いた本人の頭は足りない情報を勝手に補うため、自分では抜けに気づけません。"),
    "loop": (fig_loop, "一度で仕上げようとせず、小さく直して読み返すほうが早く整います。"),
    "struct": (fig_struct, "並び順に迷ったら、この型に当てはめるところから始められます。"),
    "ratio": (fig_ratio, "字数の配分に迷ったら、真ん中をいちばん厚くするところから考えてみてください。"),
    "memo": (fig_memo, "その場で書きとめた短いメモが、いちばん書き直しの少ない材料になります。"),
}
