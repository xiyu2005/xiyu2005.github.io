---
title: 下载MCM官方论文的脚本
draft: 
tags:
  - 数学建模
---
只需要修改url即可
page_url = "https://dxs.moe.gov.cn/zx/a/hd_sxjm_sxjmlw_2024qgdxssxjmjslwzs_2024btlw/241104/1977943.shtml"
```python
import requests
from bs4 import BeautifulSoup
from PIL import Image
import os
import re
import hashlib # 导入哈希库
from urllib.parse import urljoin

def fetch_image_urls(page_url):
    """
    访问指定网页，查找并返回所有符合命名规则的图片URL。
    """
    image_urls = []
    print(f"正在访问网页: {page_url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(page_url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img', src=re.compile(r'95\d{5}\.jpg'))

        if not img_tags:
            print("警告：在页面上没有找到符合 '9546xxx.jpg' 格式的图片。")
            return []

        print(f"初步找到了 {len(img_tags)} 张符合条件的图片。")

        for img in img_tags:
            src = img.get('src')
            if src:
                absolute_url = urljoin(page_url, src)
                image_urls.append(absolute_url)

        image_urls.sort()
        return image_urls

    except requests.exceptions.RequestException as e:
        print(f"访问网页时出错: {e}")
        return []

def download_images(image_urls, save_dir='downloaded_images'):
    """
    下载图片并保存到本地文件夹。
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"创建文件夹: {save_dir}")

    local_image_paths = []
    for i, url in enumerate(image_urls):
        try:
            print(f"正在下载图片 {i+1}/{len(image_urls)}: {url}")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            filename = os.path.basename(url)
            file_path = os.path.join(save_dir, filename)

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)

            local_image_paths.append(file_path)

        except requests.exceptions.RequestException as e:
            print(f"下载图片时出错 {url}: {e}")

    return local_image_paths

def filter_consecutive_duplicates(image_paths):
    """
    【新增功能】通过文件内容的哈希值过滤掉列表中连续重复的图片。

    Args:
        image_paths (list): 已下载的本地图片文件路径列表。

    Returns:
        list: 移除了连续重复项的图片路径列表。
    """
    if not image_paths:
        return []

    print("\n开始检测连续的重复图片...")
    unique_image_paths = []
    last_image_hash = None

    for path in image_paths:
        try:
            with open(path, 'rb') as f:
                # 读取文件内容并计算SHA256哈希值
                current_image_hash = hashlib.sha256(f.read()).hexdigest()

            # 如果当前图片的哈希值与上一张不同，则保留
            if current_image_hash != last_image_hash:
                unique_image_paths.append(path)
                last_image_hash = current_image_hash
            else:
                print(f"发现并过滤重复图片: {os.path.basename(path)}")
        except FileNotFoundError:
            print(f"警告：文件未找到，跳过: {path}")

    filtered_count = len(image_paths) - len(unique_image_paths)
    if filtered_count > 0:
        print(f"检测完成，共过滤了 {filtered_count} 张连续的重复图片。")
    else:
        print("检测完成，未发现连续的重复图片。")

    return unique_image_paths

def create_pdf_from_images(image_paths, pdf_filename='output.pdf'):
    """
    将一组图片合并成一个PDF文件。
    """
    if not image_paths:
        print("没有可用于创建PDF的图片。")
        return

    print(f"\n正在将 {len(image_paths)} 张唯一图片合并为PDF...")

    pil_images = []
    for path in image_paths:
        try:
            img = Image.open(path)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            pil_images.append(img)
        except Exception as e:
            print(f"打开图片失败 {path}: {e}")
            continue

    if not pil_images:
        print("所有图片都无法打开，无法创建PDF。")
        return

    first_image = pil_images[0]
    other_images = pil_images[1:]

    try:
        first_image.save(
            pdf_filename,
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=other_images
        )
        print(f"PDF文件已成功创建: {pdf_filename}")
    except Exception as e:
        print(f"创建PDF时出错: {e}")

def main():
    """
    主执行函数
    """
    page_url = "https://dxs.moe.gov.cn/zx/a/hd_sxjm_sxjmlw_2024qgdxssxjmjslwzs_2024btlw/241104/1977943.shtml"

    # 1. 获取所有图片的URL
    image_urls = fetch_image_urls(page_url)

    if image_urls:
        # 2. 下载所有找到的图片
        local_image_paths = download_images(image_urls)

        if local_image_paths:
            # 3. 【新步骤】过滤连续的重复图片
            unique_image_paths = filter_consecutive_duplicates(local_image_paths)

            # 4. 使用过滤后的唯一图片列表创建PDF
            if unique_image_paths:
                create_pdf_from_images(unique_image_paths, "cucmc2024b159.pdf")

                # 清理工作：如果您想在生成PDF后删除所有下载的图片，可以取消下面的注释
                # print("\n正在清理已下载的图片文件...")
                # for path in local_image_paths: # 注意：这里删除的是所有下载的图片，包括重复的
                #     os.remove(path)
                # os.rmdir('downloaded_images')
                # print("清理完成。")

if __name__ == '__main__':
    main()
```