#!/bin/bash
# --- 终极简化版同步脚本 (去除了子模块的复杂性) ---

# ================= 绝对路径配置 =================
SRC_PATH="/Users/kaisenye/Desktop/大学资料.nosync"
QUARTZ_ROOT="/Users/kaisenye/Desktop/website.nosync/quartz"
DEST_PATH="${QUARTZ_ROOT}/content"
# ==============================================

echo "🚀 开始同步..."

# 1. 私有备份 (保持不变，安全第一)
echo ">>>>> [1/3] 🔐 正在备份到私有仓库..."
cd "$SRC_PATH" || exit 1
git add .
if ! git diff-index --quiet HEAD --; then
    git commit -m "Auto backup: $(date)"
fi
git push origin main --force
echo "✅ 私有备份完成"

# 2. 搬运笔记
echo ">>>>> [2/3] 🚚 正在搬运笔记..."
if [ ! -d "$DEST_PATH" ]; then mkdir -p "$DEST_PATH"; fi
rsync -av --delete \
    --exclude '.git' --exclude '.github' --exclude '.obsidian' --exclude '.DS_Store' \
    "$SRC_PATH/" "$DEST_PATH/"
echo "✅ 搬运完成"

# 3. 整体推送 (最关键的修改)
# 不再单独推 content，而是把整个 quartz 一起推
echo ">>>>> [3/3] 🚀 正在发布网站..."
cd "$QUARTZ_ROOT" || exit 1

# 强制把 content 当作普通文件添加
git add .

if ! git diff-index --quiet HEAD --; then
    git commit -m "Site Update: $(date)"
fi

# 强制推送到 main
git push origin main --force

echo "🎉 完成！请等待 GitHub Actions 构建。"