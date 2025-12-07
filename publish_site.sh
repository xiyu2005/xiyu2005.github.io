#!/bin/bash
# --- 发布网站脚本 (带错误处理+SSH修复) ---

# 切换到quartz目录（确保路径正确）
QUARTZ_DIR="/Users/kaisenye/Desktop/website.nosync/quartz"
cd "$QUARTZ_DIR" || { echo "ERROR: 无法进入quartz目录 $QUARTZ_DIR"; exit 1; }

echo ">>>>> 正在发布网站..."

# 步骤1：更新子模块 (拉取最新的笔记)
echo "--> 步骤 1/3: 拉取最新笔记..."
git submodule update --remote || { echo "ERROR: 子模块更新失败！"; exit 1; }

# 步骤2：检查子模块是否有更新，再添加
git status --porcelain | grep -q "content"
if [ $? -eq 0 ]; then
    echo "--> 步骤 2/3: 准备提交更新..."
    git add content || { echo "ERROR: git add content 执行失败！"; exit 1; }

    # 步骤3：提交并推送（优先使用传入的参数作为提交信息）
    COMMIT_MESSAGE="${1:-Update site with latest notes}"
    git commit -m "$COMMIT_MESSAGE" || { echo "WARNING: 无更新可提交，跳过commit！"; }

    # 推送前先拉取远程最新
    git pull origin main --allow-unrelated-histories || { echo "ERROR: git pull 执行失败！"; exit 1; }
    git push origin main || { echo "ERROR: git push 执行失败！"; exit 1; }
else
    echo "--> 步骤 2/3: 子模块无更新，跳过提交！"
fi

echo ">>>>> 网站发布指令已发送！请等待 GitHub Actions 部署完成。"