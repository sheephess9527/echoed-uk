#!/usr/bin/env bash
# echoed.uk —— 一键推送到 GitHub
# 用法：先在 GitHub 网页上 New repository 建一个空仓库（不要勾任何初始化选项），
# 然后把下面的 GH_USER 改成你的 GitHub 用户名，保存后运行： bash push.sh

set -e

GH_USER="你的用户名"        # ← 改成你的 GitHub 用户名
REPO="echoed-site"          # ← 如需改仓库名，改这里（要和你在网页上建的一致）

if [ "$GH_USER" = "你的用户名" ]; then
  echo "请先编辑 push.sh，把 GH_USER 改成你的 GitHub 用户名。"
  exit 1
fi

# 确保在仓库目录内
cd "$(dirname "$0")"

git branch -M main
git remote add origin "https://github.com/${GH_USER}/${REPO}.git" 2>/dev/null \
  || git remote set-url origin "https://github.com/${GH_USER}/${REPO}.git"
git push -u origin main

echo ""
echo "✅ 推送完成。接下来去仓库 Settings → Pages，"
echo "   Source 选 main 分支根目录，保存，几分钟后即可访问。"
