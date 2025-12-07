#!/bin/bash
# --- 发布网站脚本 (最终修复版) ---

QUARTZ_DIR="/Users/kaisenye/Desktop/website.nosync/quartz"
cd "$QUARTZ_DIR" || { echo "ERROR: 无法进入quartz目录 $QUARTZ_DIR"; exit 1; }

echo ">>>>> 正在发布网站..."

# 步骤1：强制拉取子模块的 main 分支
echo "--> 步骤 1/3: 拉取最新笔记 (content)..."
git submodule update --remote --merge || { echo "ERROR: 子模块更新失败！"; exit 1; }

# 步骤2：添加所有变更 (关键修改：使用 . 而不是 content)
# 这样可以包含 .gitmodules 的修改，避免 rebase 报错
git add .

# 检查是否有变更待提交
if git diff-index --quiet HEAD --; then
    echo "--> 步骤 2/3: 暂存区无更新，跳过提交！"
else
    echo "--> 步骤 2/3: 检测到更新，准备提交..."
    
    COMMIT_MESSAGE="${1:-Update site with latest notes}"
    git commit -m "$COMMIT_MESSAGE" || { echo "WARNING: Commit 没有任何变化"; }

    # 步骤3：推送
    echo "--> 步骤 3/3: 推送到远程..."
    # 使用 --rebase 保持提交记录整洁，如果失败则尝试普通 merge
    git pull origin main --rebase || { echo "WARNING: Rebase 失败，尝试普通 Pull..."; git pull origin main; }
    
    git push origin main || { echo "ERROR: git push 失败！"; exit 1; }
    
    echo ">>>>> 网站发布指令已发送！"
fi