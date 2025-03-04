import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import time
import re
from PIL import Image
from io import BytesIO

def get_latest_post_number():
    url = 'https://fuliba2025.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    latest_post = soup.find('h2', class_='entry-title')
    if latest_post:
        post_url = latest_post.find('a')['href']
        post_number = re.search(r'/(\d+)\.html', post_url)
        if post_number:
            return int(post_number.group(1))
    return None

def scrape_images(post_number):
    base_url = f'https://fuliba2025.net/{post_number}.html'
    images = []
    
    # 抓取第2、3、4页
    for page in range(2, 5):  # 抓取第2、3、4页
        # 构建正确的分页URL
        url = f'{base_url}/{page}' if page > 1 else base_url
        print(f"正在抓取: {url}")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"页面 {page} 不存在或无法访问，状态码: {response.status_code}")
                break
        except Exception as e:
            print(f"请求页面 {page} 时出错: {e}")
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        # 网站图片没有使用class='aligncenter'，而是直接在文章内容中的img标签
        article_content = soup.find('article', class_='article-content')
        img_tags = article_content.find_all('img') if article_content else []
        page_images = []
        for img in img_tags:
            if 'src' in img.attrs:
                img_url = img['src']
                if img_url.endswith('.jpg'):
                    try:
                        img_size = int(requests.head(img_url).headers.get('content-length', 0))
                        if 10 * 1024 <= img_size < 2 * 1024 * 1024:  # 大于10KB且小于2MB
                            images.append(img_url)
                            page_images.append(img_url)
                    except:
                        print(f"无法获取图片大小: {img_url}")
        print(f"第{page}页找到 {len(page_images)} 张符合条件的图片")
        time.sleep(1)  # 避免请求过于频繁
    
    print(f"总共找到 {len(images)} 张符合条件的图片")
    return images

def save_images(images, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    saved_count = 0
    for i, img_url in enumerate(images):
        try:
            response = requests.get(img_url)
            if response.status_code == 200:
                file_name = f'image_{saved_count+1}.jpg'
                file_path = os.path.join(folder, file_name)
                try:
                    # 使用PIL处理图片
                    img = Image.open(BytesIO(response.content))
                    
                    # 确保图像是RGB模式，这样可以保存为JPEG
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # 如果图片大小超过2MB，进行压缩
                    img_size = len(response.content)
                    if img_size > 2 * 1024 * 1024:
                        # 计算压缩质量
                        quality = int(90 * (2 * 1024 * 1024 / img_size))
                        quality = max(min(quality, 95), 60)  # 限制质量在60-95之间
                        
                        # 保存压缩后的图片
                        img.save(file_path, 'JPEG', quality=quality, optimize=True)
                    else:
                        # 直接保存原图
                        img.save(file_path, 'JPEG')
                    saved_count += 1
                except Exception as e:
                    print(f"无法处理图片 {img_url}: {e}")
                    continue
        except Exception as e:
            print(f"下载图片失败 {img_url}: {e}")
        time.sleep(1)  # 避免请求过于频繁
    return saved_count

def main():
    # 从第28期到第33期依次下载
    start_post = 2025028  # 第28期
    end_post = 2025033   # 第33期
    
    for post_number in range(start_post, end_post + 1):
        print(f'\n开始抓取第 {post_number} 期的图片...')
        folder = os.path.join(os.getcwd(), str(post_number))
        images = scrape_images(post_number)
        if images:
            save_images(images, folder)
            print(f'成功抓取第 {post_number} 期的 {len(images)} 张图片，保存在文件夹 {folder}')
        else:
            print(f'第 {post_number} 期未找到符合条件的图片')
        time.sleep(2)  # 每期抓取完成后稍作等待

if __name__ == '__main__':
    main()