# echoed.uk

> 在噪音中，寻找信号。一个安静的个人策展站。

一个静态个人网站，把读到、听到、想过之后值得留下的东西，作为「回响」分享出来。
核心价值：**共鸣 > 噪音 · 深度 > 广度 · 持久 > 短暂**。

## 页面

| 文件 | 页面 | 说明 |
| --- | --- | --- |
| `index.html` | 首页 | 回声 Hero（可点击产生波纹）+ 宣言 + 精选回响 + 订阅 |
| `explore.html` | 探索回响 | 可按类型筛选的策展精选列表 |
| `about.html` | 关于 | 品牌故事 |
| `echo-signal.html` | 回响详情 | 单篇完整阅读页（含阅读进度条），范例长文 |

纯静态，无构建步骤，无依赖。字体经 Google Fonts 引入（思源宋体 + Fraunces）。

## 本地预览

直接用浏览器打开 `index.html` 即可；或起一个本地服务器：

```bash
python3 -m http.server 8000
# 浏览器访问 http://localhost:8000
```

## 部署

任意静态托管都可以。推荐 Cloudflare Pages 或 GitHub Pages：

- **GitHub Pages**：仓库 Settings → Pages → Source 选 `main` 分支根目录 → 保存。
- **Cloudflare Pages**：连接此仓库，构建命令留空，输出目录填 `/`。

绑定自定义域名 `echoed.uk` 后，把 DNS 指向托管商即可。

## 待办（内容侧）

- [ ] 把样例点评替换为真实内容
- [ ] 订阅框接入邮件服务（Buttondown / Substack / ConvertKit）
- [ ] 补充 `rss.xml` 与 `sitemap.xml`
- [ ] 替换社交/邮箱链接

---

© 2026 echoed.uk
