#!/bin/bash
# --- 发布网站脚本 (优化版) ---

QUARTZ_DIR="/Users/kaisenye/Desktop/website.nosync/quartz"
cd "$QUARTZ_DIR" || { echo "ERROR: 无法进入quartz目录 $QUARTZ_DIR"; exit 1; }

echo ">>>>> 正在发布网站..."

# 步骤1：强制拉取子模块的 main 分支
echo "--> 步骤 1/3: 拉取最新笔记 (content)..."
# 这里的 --rebase 确保如果本地有修改不会产生复杂的 merge commit
git submodule update --remote --merge || { echo "ERROR: 子模块更新失败！"; exit 1; }

# 步骤2：检查状态
# 注意：有时候 submodule 指针变化了但 git status 不明显，强制 add 一下更保险
git add content

# 检查是否有变更待提交
if git diff-index --quiet HEAD --; then
    echo "--> 步骤 2/3: 子模块无更新 (检测到 workspace 干净)，跳过提交！"
else
    echo "--> 步骤 2/3: 检测到更新，准备提交..."
    
    COMMIT_MESSAGE="${1:-Update site with latest notes}"
    git commit -m "$COMMIT_MESSAGE" || { echo "WARNING: Commit 没有任何变化"; }

    # 步骤3：推送
    echo "--> 步骤 3/3: 推送到远程..."
    git pull origin main --rebase || { echo "ERROR: git pull 失败！"; exit 1; }
    git push origin main || { echo "ERROR: git push 失败！"; exit 1; }
    
    echo ">>>>> 网站发布指令已发送！"
fi