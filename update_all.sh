#!/bin/bash
# --- 自动更新和发布主脚本 (带错误终止) ---

# 定义脚本完整路径（根据实际存放位置修改）
SAVE_NOTES_SCRIPT="./save_notes.sh"  # 若在其他目录，改为绝对路径，比如 /Users/kaisenye/xxx/save_notes.sh
PUBLISH_SITE_SCRIPT="./publish_site.sh"

# 1. 保存笔记（失败则终止脚本）
echo "--- $(date): 开始保存笔记 ---"
bash "$SAVE_NOTES_SCRIPT" "Automated note update" || { echo "ERROR: 保存笔记失败！"; exit 1; }

# 2. 发布网站（失败则终止脚本）
echo "--- $(date): 开始发布网站 ---"
bash "$PUBLISH_SITE_SCRIPT" "Automated site publish" || { echo "ERROR: 发布网站失败！"; exit 1; }

echo "--- $(date): 所有任务执行完毕 ---"