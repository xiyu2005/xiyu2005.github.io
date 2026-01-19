#!/bin/bash

# --- 自动更新和发布主脚本 (路径修复版) ---

# 【关键修改】脚本真正的家是在 website 下的 quartz 里
SCRIPT_DIR="/Users/kaisenye/Desktop/website.nosync/quartz"

echo "--- $(date): 开始全自动同步流程 ---"

# 检查脚本是否存在
if [ ! -f "$SCRIPT_DIR/save_notes.sh" ]; then
    echo "❌ 错误：找不到文件 $SCRIPT_DIR/save_notes.sh"
    echo "请确认该文件就在 quartz 目录下！"
    exit 1
fi

# 赋予执行权限 (防止因权限问题报错)
chmod +x "$SCRIPT_DIR/save_notes.sh"

# 运行脚本
"$SCRIPT_DIR/save_notes.sh"

echo "--- $(date): 流程结束 ---"