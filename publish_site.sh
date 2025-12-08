#!/bin/bash

# --- 发布网站脚本 ---
cd /Users/kaisenye/Desktop/website.nosync/quartz

echo ">>>>> 正在发布网站..."

# 1. 更新子模块 (拉取最新的笔记)
echo "--> 步骤 1/3: 拉取最新笔记..."
git submodule update --remote

# 2. 添加子模块的更新
echo "--> 步骤 2/3: 准备提交更新..."
git add content

# 3. 提交并推送
#    - 同样，优先使用你提供的参数作为提交信息
COMMIT_MESSAGE="${1:-Update site with latest notes}"
git commit -m "$COMMIT_MESSAGE"
git push origin main

echo ">>>>> 网站发布指令已发送！请等待 GitHub Actions 部署完成。"