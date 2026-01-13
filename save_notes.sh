#!/bin/bash
# --- 保存笔记脚本 (带错误处理 - 修复版) ---

echo ">>>>> 正在保存笔记到私人仓库..."

# 步骤1：检查是否有未提交的变更
git status --porcelain | grep -q .
if [ $? -ne 0 ]; then
    # 额外检查：虽然没文件变更，但也许有本地commit还没推送到远程
    NEED_PUSH=$(git log origin/main..HEAD --oneline)
    if [ -z "$NEED_PUSH" ]; then
        echo ">>>>> 无笔记变更，无需保存！"
        exit 0
    else
        echo ">>>>> 检测到本地有未推送的提交，准备推送..."
    fi
else
    # 步骤2：添加所有更改
    git add . || { echo "ERROR: git add 执行失败！"; exit 1; }

    # 步骤3：提交更改
    COMMIT_MESSAGE="${1:-Update notes}"
    git commit -m "$COMMIT_MESSAGE" || { echo "ERROR: git commit 执行失败！"; exit 1; }
fi

# 步骤4：拉取远程最新提交（关键修改：使用 --rebase 自动解决分歧）
echo ">>>>> 拉取远程main分支最新内容..."
git pull origin main --rebase || { echo "ERROR: git pull 执行失败！"; exit 1; }

# 步骤5：推送到远程仓库
git push origin main || { echo "ERROR: git push 执行失败！"; exit 1; }

echo ">>>>> 笔记已成功保存到云端！"