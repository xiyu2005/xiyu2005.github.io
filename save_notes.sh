#!/bin/bash

# --- 保存笔记脚本 ---

echo ">>>>> 正在保存笔记到私人仓库..."

# 1. 添加所有更改
git add .

# 2. 提交更改
#    - 如果你运行脚本时提供了参数，就用那个参数作为提交信息
#    - 如果没有提供，就用一个默认的信息
COMMIT_MESSAGE="${1:-Update notes}"
git commit -m "$COMMIT_MESSAGE"

# 3. 推送到远程仓库
git push origin main

echo ">>>>> 笔记已成功保存到云端！"