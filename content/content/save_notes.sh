#!/bin/bash
# --- 绝对路径同步脚本 (在哪运行都能成功) ---

# ================= 绝对路径配置 (关键!) =================
# 1. 你的 Obsidian 原始笔记路径
SRC_PATH="/Users/kaisenye/Desktop/大学资料.nosync"

# 2. 你的 Quartz 网站项目根路径
QUARTZ_ROOT="/Users/kaisenye/Desktop/website.nosync/quartz"

# 3. Quartz 里的 content 路径 (自动拼接)
DEST_PATH="${QUARTZ_ROOT}/content"
# ======================================================

echo "=========================================="
echo "   🚀 开始全自动同步 (双轨制)"
echo "   📂 源目录: $SRC_PATH"
echo "   📂 目标目录: $DEST_PATH"
echo "=========================================="

# ---------------------------------------------------------
# 阶段一：私有备份 (备份到 my-obsidian-notes)
# ---------------------------------------------------------
echo ""
echo ">>>>> [1/4] 🔐 正在备份到私有仓库..."

# 强制跳转到 Obsidian 目录 (不管你在哪)
cd "$SRC_PATH" || { echo "❌ 错误：找不到源目录 $SRC_PATH"; exit 1; }

git add .
if ! git diff-index --quiet HEAD --; then
    git commit -m "Auto backup: $(date "+%Y-%m-%d %H:%M:%S")"
fi
# 推送到私有库
git push origin main --force
echo "✅ 私有备份完成！"

# ---------------------------------------------------------
# 阶段二：搬运文件 (从 Obsidian -> Quartz)
# ---------------------------------------------------------
echo ""
echo ">>>>> [2/4] 🚚 正在将笔记搬运到网站目录..."

# 确保目标目录存在
if [ ! -d "$DEST_PATH" ]; then
    echo "❌ 错误：目标 content 目录不存在，请检查路径配置！"
    exit 1
fi

# 执行同步 (注意目录后的斜杠 / 处理)
rsync -av --delete \
    --exclude '.git' \
    --exclude '.github' \
    --exclude '.obsidian' \
    --exclude '.DS_Store' \
    --exclude 'node_modules' \
    "$SRC_PATH/" "$DEST_PATH/"

echo "✅ 文件搬运完成！"

# ---------------------------------------------------------
# 阶段三：上传笔记内容 (推送到 public 仓库)
# ---------------------------------------------------------
echo ""
echo ">>>>> [3/4] ☁️ 正在上传网站内容..."

# 强制跳转到 Quartz content 目录
cd "$DEST_PATH" || exit

git add .
if ! git diff-index --quiet HEAD --; then
    git commit -m "Update site content: $(date "+%Y-%m-%d %H:%M:%S")"
    echo "📄 检测到内容更新，已提交。"
else
    echo "📄 内容无变化。"
fi

# 强制推送到公开库 (确保 Action 能读到最新文件)
git push origin main --force

# ---------------------------------------------------------
# 阶段四：触发网站构建 (通知 Quartz 外壳)
# ---------------------------------------------------------
echo ""
echo ">>>>> [4/4] 🚀 触发 GitHub Action 构建..."

# 强制跳转到 Quartz 根目录
cd "$QUARTZ_ROOT" || exit

git add content
if ! git diff-index --quiet HEAD --; then
    git commit -m "Trigger build: $(date "+%Y-%m-%d %H:%M:%S")"
fi

git push origin main --force

echo ""
echo "🎉======================================🎉"
echo "   所有同步任务已完成！"
echo "   请等待 2-3 分钟后刷新你的网站。"
echo "🎉======================================🎉"