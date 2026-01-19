#!/bin/bash

# --- 自动更新和发布主脚本 (一键搞定) ---

# 设定脚本所在的绝对路径 (防止找不到 save_notes.sh)
SCRIPT_DIR="/Users/kaisenye/Desktop/website.nosync/quartz"

echo "--- $(date): 开始全自动同步流程 ---"

# 直接运行那个全能的 save_notes.sh
# 确保文件有执行权限: chmod +x save_notes.sh
"$SCRIPT_DIR/save_notes.sh"

echo "--- $(date): 流程结束 ---"