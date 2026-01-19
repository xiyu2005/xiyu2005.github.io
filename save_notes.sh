#!/bin/bash
# --- 保存笔记脚本 (带同步功能 - 终极修复版) ---

# ================= 配置区域 =================
# 1. 设置你的 Obsidian 仓库路径 (注意结尾要有斜杠 /)
#    请确保这个路径是你电脑上真实的路径！
SOURCE_DIR="/Users/kaisenye/Desktop/大学资料.nosync/"

# 2. 设置 Quartz 的 content 路径 (相对脚本的位置)
DEST_DIR="./content/"
# ===========================================

echo ">>>>> [1/3] 正在从 Obsidian 同步最新笔记..."

# 检查源目录是否存在
if [ ! -d "$SOURCE_DIR" ]; then
    echo "ERROR: 源目录不存在: $SOURCE_DIR"
    echo "请检查脚本中的 SOURCE_DIR 配置是否正确！"
    exit 1
fi

# 使用 rsync 进行同步
# -a: 归档模式，保留属性
# -v: 显示过程
# --delete: 如果源目录删除了文件，这里也同步删除
# --exclude: 排除不需要发布的文件 (.git, .obsidian, .DS_Store 等)
rsync -av --delete \
    --exclude '.git' \
    --exclude '.github' \
    --exclude '.obsidian' \
    --exclude '.DS_Store' \
    --exclude 'node_modules' \
    "$SOURCE_DIR" "$DEST_DIR"

if [ $? -ne 0 ]; then
    echo "ERROR: 文件同步失败！"
    exit 1
fi

echo ">>>>> [2/3] 同步完成，开始检查 Git 状态..."

# 进入 content 目录确保操作正确
cd "$DEST_DIR" || exit

# 步骤1：检查是否有未提交的变更
# (因为刚才同步了文件，如果有修改，这里一定会检测到)
git status --porcelain | grep -q .
if [ $? -ne 0 ]; then
    # 额外检查：也许有本地commit还没推送到远程
    NEED_PUSH=$(git log origin/main..HEAD --oneline)
    if [ -z "$NEED_PUSH" ]; then
        echo ">>>>> 无笔记变更，无需保存！"
        # 回到脚本所在目录，以免影响后续操作
        cd ..
        exit 0
    else
        echo ">>>>> 检测到本地有未推送的提交，准备推送..."
    fi
else
    # 步骤2：添加所有更改
    git add . || { echo "ERROR: git add 执行失败！"; exit 1; }

    # 步骤3：提交更改
    COMMIT_MESSAGE="${1:-Update notes content}"
    git commit -m "$COMMIT_MESSAGE" || { echo "ERROR: git commit 执行失败！"; exit 1; }
fi

# 步骤4：拉取远程最新提交
echo ">>>>> [3/3] 拉取远程更新并推送..."
git pull origin main --rebase || { echo "ERROR: git pull 执行失败！"; exit 1; }

# 步骤5：推送到远程仓库
git push origin main || { echo "ERROR: git push 执行失败！"; exit 1; }

# 回到脚本目录
cd ..

echo ">>>>> 笔记已成功保存到云端！"