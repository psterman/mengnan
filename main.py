import os
import time
from datetime import datetime
from fuliba_scraper import get_latest_post_number, scrape_images, save_images
from github_uploader import GitHubUploader

def get_next_post_number(current_number):
    return current_number + 1

def main():
    # GitHub配置
    github_token = os.getenv('GITHUB_TOKEN')
    repo_owner = os.getenv('GITHUB_REPO_OWNER')
    repo_name = os.getenv('GITHUB_REPO_NAME')
    
    if not all([github_token, repo_owner, repo_name]):
        print("请设置必要的环境变量：GITHUB_TOKEN, GITHUB_REPO_OWNER, GITHUB_REPO_NAME")
        return
    
    uploader = GitHubUploader(github_token, repo_owner, repo_name)
    current_post = 2025032  # 从第32期开始
    
    while True:
        now = datetime.now()
        # 每天凌晨运行
        if now.hour == 0:
            latest_post = get_latest_post_number()
            if latest_post and latest_post > current_post:  # 只在有新一期时下载
                today = now.strftime('%Y%m%d')
                temp_folder = f'temp_{today}'
                
                # 创建临时文件夹
                if not os.path.exists(temp_folder):
                    os.makedirs(temp_folder)
                
                # 抓取图片
                images = scrape_images(current_post)
                if images:
                    # 保存图片到临时文件夹
                    save_images(images, temp_folder)
                    
                    # 上传到GitHub
                    if not uploader.check_folder_exists(today):
                        success_count = uploader.upload_folder(temp_folder, today)
                        print(f'Successfully uploaded {success_count} images for post {current_post}')
                        current_post = get_next_post_number(current_post)
                
                # 清理临时文件夹
                for file in os.listdir(temp_folder):
                    os.remove(os.path.join(temp_folder, file))
                os.rmdir(temp_folder)
        
        # 等待1小时再检查
        time.sleep(3600)

if __name__ == '__main__':
    main()