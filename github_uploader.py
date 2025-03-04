import os
import base64
import requests
from datetime import datetime
import json

class GitHubUploader:
    def __init__(self, token, repo_owner, repo_name):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def check_folder_exists(self, folder_path):
        """检查GitHub仓库中是否存在指定文件夹"""
        try:
            url = f'{self.base_url}/contents/{folder_path}'
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            print(f"Error checking folder: {e}")
            return False
    
    def upload_file(self, local_file_path, github_file_path):
        """上传文件到GitHub仓库"""
        try:
            # 读取文件内容并进行base64编码
            with open(local_file_path, 'rb') as file:
                file_content = file.read()
            encoded_content = base64.b64encode(file_content).decode('utf-8')
            
            # 检查文件是否已存在
            url = f'{self.base_url}/contents/{github_file_path}'
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                # 文件已存在，跳过上传
                print(f"File {github_file_path} already exists, skipping.")
                return False
            
            # 创建或更新文件
            data = {
                'message': f'Upload {os.path.basename(github_file_path)} on {datetime.now().strftime("%Y-%m-%d")}',
                'content': encoded_content
            }
            
            response = requests.put(url, headers=self.headers, data=json.dumps(data))
            if response.status_code in [201, 200]:
                print(f"Successfully uploaded {github_file_path}")
                return True
            else:
                print(f"Failed to upload {github_file_path}: {response.status_code}, {response.text}")
                return False
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False
    
    def upload_folder(self, local_folder, github_folder):
        """上传整个文件夹到GitHub仓库"""
        success_count = 0
        for filename in os.listdir(local_folder):
            local_file_path = os.path.join(local_folder, filename)
            if os.path.isfile(local_file_path):
                github_file_path = f"{github_folder}/{filename}"
                if self.upload_file(local_file_path, github_file_path):
                    success_count += 1
        return success_count