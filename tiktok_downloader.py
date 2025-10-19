#!/usr/bin/env python3
"""
TikTok 视频下载器
使用 yt-dlp 库自动下载指定博主的 TikTok 视频
"""

import os
import sys
import subprocess
import yt_dlp
from pathlib import Path

def main():
    # 目标博主链接
    channel_url = "https://www.tiktok.com/@fukada0318"
    
    # 使用 os.path.expanduser 定义用户主目录
    home_dir = os.path.expanduser("~")
    
    # 下载目录路径
    download_dir = os.path.join(home_dir, "下载", "fukada0318")
    
    # 下载记录文件路径
    archive_file = os.path.join(download_dir, "download_archive.txt")
    
    # 确保下载目录存在
    Path(download_dir).mkdir(parents=True, exist_ok=True)
    
    # 添加一些用户代理和请求头来绕过限制
    import random
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    ]
    
    # yt-dlp 配置
    ydl_opts = {
        'outtmpl': os.path.join(download_dir, '%(title)s - %(upload_date)s.%(ext)s'),
        'download_archive': archive_file,
        'format': 'best',  # 使用最佳可用格式
        'writesubtitles': False,
        'writeautomaticsub': False,
        'ignoreerrors': True,  # 忽略单个视频的错误，继续下载其他视频
        'no_warnings': False,
        'extract_flat': False,
        'sleep_interval': 1,  # 减少下载间隔
        'max_sleep_interval': 5,
        'retries': 5,  # 增加重试次数
        'fragment_retries': 5,
        'http_chunk_size': 10485760,  # 10MB chunks
        'http_headers': {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        },
        'cookiesfrombrowser': ('chrome',),  # 尝试使用浏览器cookies
        'playlistend': 200,  # 尝试下载更多视频
        'playliststart': 1,  # 从第一个视频开始
        'extractor_args': {
            'tiktok': {
                'webpage_url_basename': 'fukada0318',
                'api_hostname': 'api.tiktokv.com',
            }
        },
    }
    
    print(f"开始下载 TikTok 视频...")
    print(f"博主链接: {channel_url}")
    print(f"下载目录: {download_dir}")
    print(f"记录文件: {archive_file}")
    print("-" * 50)
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 先尝试获取频道信息
            try:
                info = ydl.extract_info(channel_url, download=False)
                print(f"成功获取频道信息，开始下载...")
                ydl.download([channel_url])
                print("\n下载完成！")
            except Exception as extract_error:
                print(f"无法访问该 TikTok 账号: {extract_error}")
                print("\n可能的原因:")
                print("1. 该账号是私有的")
                print("2. 该账号禁用了嵌入功能")
                print("3. 网络连接问题")
                print("4. TikTok 的反爬虫机制")
                print("\n建议:")
                print("1. 检查账号是否为公开账号")
                print("2. 尝试使用 VPN 或更换网络")
                print("3. 稍后重试")
                print("4. 如果知道具体的视频链接，可以直接下载单个视频")
                
                # 提供手动输入视频链接的选项
                print("\n" + "="*50)
                print("替代方案：手动输入视频链接")
                print("="*50)
                
                while True:
                    video_url = input("\n请输入要下载的 TikTok 视频链接 (输入 'quit' 退出): ").strip()
                    if video_url.lower() == 'quit':
                        break
                    if video_url.startswith('https://www.tiktok.com/'):
                        try:
                            print(f"正在下载: {video_url}")
                            ydl.download([video_url])
                            print("下载完成！")
                        except Exception as video_error:
                            print(f"下载失败: {video_error}")
                    else:
                        print("请输入有效的 TikTok 视频链接")
        
    except Exception as e:
        print(f"程序运行错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
