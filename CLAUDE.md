# CLAUDE.md — echoed.uk

这是给 Claude Code 的项目交接说明。打开本目录后请先读这份文件。

## 项目是什么

`echoed.uk` —— 一个**静态个人策展站**。主题：在信息噪音中筛出值得留下的「回响」。
品牌调性：安静、有力量、思考型、温暖而专业。
核心价值：共鸣 > 噪音 · 深度 > 广度 · 持久 > 短暂。

## 技术栈

- 纯静态 HTML，**无构建步骤、无依赖、无框架**。
- 字体经 Google Fonts 引入：思源宋体 Noto Serif SC（中文）+ Fraunces（拉丁字标）。
- 每个页面自包含（内联 CSS + 原生 JS），可单独用浏览器打开。

## 文件结构

- `index.html` — 首页：回声 Hero（canvas 波纹，可点击）+ 宣言 + 精选回响 + 订阅页脚
- `explore.html` — 探索回响：按类型筛选的策展精选列表
- `about.html` — 关于：品牌故事
- `echo-signal.html` — 回响详情：单篇阅读页（含阅读进度条），范例长文
- `README.md` / `push.sh` — 说明与一键推送脚本

## 设计约定（改动时请保持一致）

- 配色 token 定义在每页 `:root`：背景 `#07090F`，墨色文字 `#EDE9E0`，信号暖琥珀 `#F0B35E`，次要文字 `#7C8694`。
- 信号色（暖琥珀）是品牌唯一强调色，克制使用。
- 内容版式上：「原文/来源」用安静的灰色，「我的点评（回响）」用带暖色左缘的样式强调——这是品牌隐喻，勿打乱。
- 已支持：响应式到手机、键盘焦点、`prefers-reduced-motion`。新加交互请延续。

## 现在需要你做的第一件事

把这个站推到我的 GitHub 并开启 Pages：

1. 用 `gh` CLI 在我账号下新建一个**公开**仓库 `echoed-site`（如果 `gh` 未登录，提示我先 `gh auth login`）。
2. 把当前目录推送上去（仓库已 `git init` 并有提交历史，默认分支用 `main`）。
3. 开启 GitHub Pages（main 分支根目录），把最终访问网址告诉我。

参考命令（按需调整）：

```bash
gh repo create echoed-site --public --source=. --remote=origin --push
gh api -X POST repos/{owner}/echoed-site/pages -f "source[branch]=main" -f "source[path]=/" 2>/dev/null || \
  echo "若 Pages API 失败，请到仓库 Settings → Pages 手动开启 main / root"
```

## 之后可以继续的事（内容侧）

- 把样例点评替换为真实内容
- 订阅框接入邮件服务（Buttondown / Substack / ConvertKit）
- 补 `rss.xml` 与 `sitemap.xml`
- 替换页脚的社交 / 邮箱链接
