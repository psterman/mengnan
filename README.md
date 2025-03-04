# Fuliba图片爬虫

这是一个自动化爬虫程序，用于每天凌晨从 fuliba2025.net 网站抓取特定页面的jpg图片，并将其上传到GitHub仓库中。

## 功能特点

- 自动抓取fuliba2025.net网站特定文章的第2、3、4页中的jpg图片
- 只抓取小于1MB的图片
- 按日期创建文件夹并上传到GitHub
- 自动检测网站更新，避免重复抓取
- 实现请求延迟，避免被网站封禁

## 环境要求

- Python 3.6+
- 以下Python库：
  - requests
  - beautifulsoup4

## 安装

1. 克隆此仓库到本地
2. 安装依赖：

```bash
pip install requests beautifulsoup4
```

## 配置

在运行程序前，需要设置以下环境变量：

- `GITHUB_TOKEN`: GitHub个人访问令牌，用于API认证
- `GITHUB_REPO_OWNER`: GitHub仓库所有者用户名
- `GITHUB_REPO_NAME`: GitHub仓库名称

### 获取GitHub Token

1. 登录GitHub账号
2. 点击右上角头像 -> Settings -> Developer settings -> Personal access tokens -> Generate new token
3. 勾选`repo`权限，生成并复制token

## 使用方法

运行主程序：

```bash
python main.py
```

程序将在每天凌晨检查网站更新，抓取图片并上传到GitHub。

## 注意事项

- 程序设计为长期运行，建议在服务器上使用nohup或screen等工具在后台运行
- 请遵守网站的robots.txt规则和使用条款
- 定期检查GitHub仓库空间使用情况

## 文件说明

- `fuliba_scraper.py`: 实现网站爬虫功能
- `github_uploader.py`: 实现GitHub上传功能
- `main.py`: 主程序，整合爬虫和上传功能，实现定时任务# mengnan
