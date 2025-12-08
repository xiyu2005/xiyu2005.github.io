#!/bin/bash

# --- 自动更新和发布主脚本 ---

# 1. 保存笔记
echo "--- $(date): 开始保存笔记 ---"
./save_notes.sh "Automated note update" # ！！！注意：修改成你的 save_notes.sh 的真实路径

# 2. 发布网站
echo "--- $(date): 开始发布网站 ---"   # ！！！注意：修改成你的“quartz”文件夹的真实路径
./publish_site.sh "Automated site publish" # ！！！注意：修改成你的 publish_site.sh 的真实路径

echo "--- $(date): 所有任务执行完毕 ---"