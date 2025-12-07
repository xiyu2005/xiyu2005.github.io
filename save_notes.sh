#!/bin/bash
# --- 保存笔记脚本 (带错误处理) ---

echo ">>>>> 正在保存笔记到私人仓库..."

# 步骤1：检查是否有未提交的变更
git status --porcelain | grep -q .
if [ $? -ne 0 ]; then
    echo ">>>>> 无笔记变更，无需保存！"
    exit 0
fi

# 步骤2：添加所有更改
git add . || { echo "ERROR: git add 执行失败！"; exit 1; }

# 步骤3：提交更改（优先使用传入的参数作为提交信息）
COMMIT_MESSAGE="${1:-Update notes}"
git commit -m "$COMMIT_MESSAGE" || { echo "ERROR: git commit 执行失败！"; exit 1; }

# 步骤4：拉取远程最新提交（解决推送被拒）
echo ">>>>> 拉取远程main分支最新内容..."
git pull origin main --allow-unrelated-histories || { echo "ERROR: git pull 执行失败！"; exit 1; }

# 步骤5：推送到远程仓库
git push origin main || { echo "ERROR: git push 执行失败！"; exit 1; }

echo ">>>>> 笔记已成功保存到云端！"