#!/usr/bin/env python3
"""从当前文件重新生成 sitemap.xml，为每个 URL 写入 <lastmod>。
文章的 lastmod 取其 article:published_time；首页/explore/about 取全站最新文章日期。
用法：python3 tools/gen_sitemap.py"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://echoed.uk/"

def pub_date(f):
    m = re.search(r'article:published_time" content="(\d{4}-\d{2}-\d{2})"', open(f, encoding="utf-8").read())
    return m.group(1) if m else "2026-06-16"

def run():
    echoes = sorted(glob.glob(os.path.join(ROOT, "echo-*.html")))
    dates = {os.path.basename(f): pub_date(f) for f in echoes}
    latest = max(dates.values())

    rows = [
        (BASE, "weekly", "1.0", latest),
        (BASE + "explore.html", "weekly", "0.9", latest),
        (BASE + "about.html", "monthly", "0.7", latest),
    ]
    # 文章按发布日期由新到旧
    for name in sorted(dates, key=lambda k: dates[k], reverse=True):
        rows.append((BASE + name, "monthly", "0.8", dates[name]))

    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, cf, pr, lm in rows:
        out += ["  <url>",
                f"    <loc>{loc}</loc>",
                f"    <lastmod>{lm}</lastmod>",
                f"    <changefreq>{cf}</changefreq>",
                f"    <priority>{pr}</priority>",
                "  </url>"]
    out.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"gen_sitemap: {len(rows)} 条 URL，最新日期 {latest}")

if __name__ == "__main__":
    run()
