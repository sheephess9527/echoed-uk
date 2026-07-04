#!/usr/bin/env python3
import os, re, glob, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "og")
os.makedirs(OUT, exist_ok=True)

CJK = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

W, H = 1200, 630
BG = (246, 242, 232)      # #F6F2E8
INK = (35, 38, 46)        # #23262E
MUTED = (106, 112, 121)   # #6A7079
SIGNAL = (178, 117, 23)   # #B27517
LINE = (40, 38, 30)

MARGIN = 90
MAXW = W - MARGIN * 2

def cat_and_date(html):
    cat = re.search(r'<div class="meta"><span class="cat">([^<]+)</span>', html)
    d = re.search(r'article:published_time" content="(\d{4})-(\d{2})-(\d{2})"', html)
    cat = cat.group(1) if cat else ""
    date = f"{d.group(1)} · {d.group(2)} · {d.group(3)}" if d else ""
    return cat, date

def title_of(html):
    m = re.search(r'<meta property="og:title" content="([^"]+)"', html)
    return m.group(1) if m else ""

def wrap(draw, text, font, maxw):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        t = cur + ch
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = ch
    if cur:
        lines.append(cur)
    return lines

def render(html, out_path):
    title = title_of(html)
    cat, date = cat_and_date(html)
    eyebrow = " · ".join(x for x in [cat, date] if x)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # top accent bar (signal amber)
    d.rectangle([0, 0, W, 8], fill=SIGNAL)

    # faint echo motif: concentric arcs bottom-right
    cx, cy = W + 40, H + 40
    for i, r in enumerate([150, 230, 310, 390]):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(228, 220, 202), width=2)

    # eyebrow
    ey_font = ImageFont.truetype(CJK, 27)
    d.text((MARGIN, 96), eyebrow, font=ey_font, fill=MUTED)

    # thin rule under eyebrow
    d.line([MARGIN, 150, MARGIN + 70, 150], fill=SIGNAL, width=3)

    # title (auto-fit)
    size = 68
    while size >= 46:
        tf = ImageFont.truetype(CJK, size)
        lines = wrap(d, title, tf, MAXW)
        lh = int(size * 1.42)
        if len(lines) * lh <= 300:
            break
        size -= 4
    y = 196
    for ln in lines:
        d.text((MARGIN, y), ln, font=tf, fill=INK)
        y += lh

    # wordmark bottom-left: "echoed" + amber dot
    wm = ImageFont.truetype(SERIF, 44)
    wy = H - 108
    d.text((MARGIN, wy), "echoed", font=wm, fill=INK)
    ww = d.textlength("echoed", font=wm)
    d.text((MARGIN + ww + 2, wy), ".", font=wm, fill=SIGNAL)

    # tagline under wordmark
    tag = ImageFont.truetype(CJK, 24)
    d.text((MARGIN, wy + 58), "在噪音中，寻找信号", font=tag, fill=MUTED)

    img.save(out_path, "PNG")
    return title

def main():
    files = sorted(glob.glob(os.path.join(ROOT, "echo-*.html")))
    if len(sys.argv) > 1 and sys.argv[1] == "--one":
        files = [os.path.join(ROOT, "echo-hangzhou.html")]
    n = 0
    for f in files:
        slug = os.path.basename(f)[:-5]  # echo-xxx
        html = open(f, encoding="utf-8").read()
        out = os.path.join(OUT, slug + ".png")
        t = render(html, out)
        n += 1
        print(f"{slug}.png  ←  {t}")
    print(f"\n{n} OG images written to assets/og/")

main()
