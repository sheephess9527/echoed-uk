# CLAUDE.md — echoed.uk

给 Claude Code 的项目交接说明。**打开本目录请先读这份，再读 `README.md`**——README 里有完整的接手手册（接手须知 / 新增文章 Runbook / 提交命令 / 技术备忘 / 变更记录）。沟通用中文。

## 项目是什么

`echoed.uk` —— 一个**静态个人策展站**。主题：在信息噪音中筛出值得留下的「回响」。
品牌调性：安静、有力量、思考型、温暖而专业。
核心价值：**共鸣 > 噪音 · 深度 > 广度 · 持久 > 短暂**。

## 技术栈

- 纯静态 HTML，**无构建步骤、无依赖、无框架**。
- 每个页面自包含（内联 CSS + 原生 JS），可单独用浏览器打开。
- 字体经 Google Fonts 引入：思源宋体 Noto Serif SC（中文）+ Fraunces（拉丁字标）。

## 现状（截至 2026·06）

- **已上线**：GitHub Pages 从 `master` 分支根目录发布，线上地址 **https://echoed.uk**（自定义域名已绑定）。早期「建仓库 + 开 Pages」的任务**早已完成**，不要再做。
- **内容**：约 49 篇回响（`echo-*.html`），完整清单见 README《内容清单》。

## 文件结构

- `index.html` — 首页：回声 Hero（canvas 波纹，可点击）+ 宣言 + 精选回响 + 订阅页脚
- `explore.html` — 探索回响：按类型（文章 / 观点 / 对话 / 书）筛选的时间线
- `about.html` — 关于：品牌故事
- `echo-*.html` — 每篇文章独立成页（含阅读进度条、分享按钮）；当前约 49 篇，清单见 README
- `README.md` — **完整接手手册**（接手须知 / Runbook / 命令 / 技术备忘 / 作者事实档指引 / 变更记录）
- `.private-notes.md` — 私人事实档（本地、已 `.gitignore`、**不入库**；写个人记述前先看）
- `sitemap.xml` · `rss.xml` · `site.webmanifest` · `assets/`（图标 / 启动图 / OG 图）
- `push.sh` — 一键推送脚本

## 工作流（铁律，细节见 README）

- 开发分支 **`claude/website-review-o0eglu`** → 提交并推送 → `git checkout master && git merge --ff-only` → 推 `master`（触发 Pages 重建，约 1～2 分钟生效）。
- **未经许可不推到其它分支；不主动建 Pull Request。**
- 本环境**没有 `gh` CLI**；用 `git` + GitHub MCP 工具操作 GitHub。
- **每次改动后，更新 README《变更记录》。**
- 新增文章严格照 README《新增一篇文章的完整流程（Runbook）》，并同步 `explore.html` / `sitemap.xml` / `rss.xml` / `README.md`，详情页底部做交叉互链。

## 设计约定（改动时保持一致）

- **双主题**（日间默认 / 夜间）。配色 token 定义在每页 `:root`，并由 `html[data-theme="dark"]` 覆盖：

  | 角色 | 日间 | 夜间 |
  | --- | --- | --- |
  | 背景 | `#F6F2E8` | `#07090F` |
  | 墨色文字 | `#23262E` | `#EDE9E0` |
  | 信号暖琥珀（**唯一**强调色，克制用） | `#B27517` | `#F0B35E` |
  | 次要文字 | `#6A7079` | `#7C8694` |

- 内容版式：「原文 / 来源」用安静的灰色，「我的点评（回响）」用带**暖色左缘**的样式强调——品牌隐喻，勿打乱。
- **每页自包含**（内联 CSS/JS，无公共文件）→ 「跨全站」的统一改动（如改分享逻辑）必须**批量遍历 `echo-*.html`**。
- 已支持：响应式到手机、键盘焦点、`prefers-reduced-motion`、PWA / iOS 主屏、阅读进度条、分享按钮（微信·朋友圈 / 微博 / 复制链接）。新增交互请延续这些。

## 个人记述（重要）

涉及站主本人或家人的私人事实，一律以本地 `.private-notes.md` 为准，**不得与既有文章冲突，也不要臆造**。仓库是**公开**的——不要把私人事实写回任何会被提交的文件。没有该文件时（如全新克隆），向站主索取，或参照已发布文章（`echo-hangzhou` / `echo-tangtang` / `echo-father`）。

## 待办（内容侧）

- [ ] 把样例点评替换为真实内容
- [ ] 订阅框接入邮件服务（Buttondown / Substack / ConvertKit）
- [ ] 替换页脚的社交 / 邮箱链接
