#!/usr/bin/env python3
"""为每篇 echo-*.html 写入正确的 og:image / twitter:image（各自专属 OG 图）
并（重新）生成 Article JSON-LD。幂等：可反复运行，新增文章后跑一次即可。
用法：python3 tools/gen_meta.py"""
import os, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def field(html, pat):
    m = re.search(pat, html)
    return m.group(1) if m else ""

def run():
    n = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "echo-*.html"))):
        slug = os.path.basename(f)[:-5]
        html = open(f, encoding="utf-8").read()
        orig = html
        og_url = f"https://echoed.uk/assets/og/{slug}.png"

        # 强制 og:image / twitter:image 指向本篇专属 OG 图
        html = re.sub(r'(<meta property="og:image" content=")[^"]*(")', r'\1' + og_url + r'\2', html)
        html = re.sub(r'(<meta name="twitter:image" content=")[^"]*(")', r'\1' + og_url + r'\2', html)

        # 移除旧的 JSON-LD，再按当前 meta 重新生成
        html = re.sub(r'\n?<script type="application/ld\+json">.*?</script>', '', html, flags=re.S)
        data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": field(html, r'<meta property="og:title" content="([^"]+)"'),
            "description": field(html, r'<meta name="description" content="([^"]+)"'),
            "datePublished": field(html, r'article:published_time" content="([^"]+)"'),
            "dateModified": field(html, r'article:published_time" content="([^"]+)"'),
            "author": {"@type": "Organization", "name": "echoed", "url": "https://echoed.uk/"},
            "publisher": {"@type": "Organization", "name": "echoed",
                          "logo": {"@type": "ImageObject", "url": "https://echoed.uk/assets/icon-512.png"}},
            "image": og_url,
            "mainEntityOfPage": {"@type": "WebPage", "@id": field(html, r'<link rel="canonical" href="([^"]+)"')},
            "inLanguage": "zh-CN",
        }
        block = '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n</script>\n</head>'
        html = html.replace("</head>", block, 1)

        if html != orig:
            open(f, "w", encoding="utf-8").write(html)
            n += 1
    print(f"gen_meta: {n} 篇更新（og:image + JSON-LD）")

if __name__ == "__main__":
    run()
