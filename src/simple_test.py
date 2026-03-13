#!/usr/bin/env python3
import os
import sys
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# 企业微信机器人Webhook地址
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=550f678c-bff5-4968-8ae3-f184785d0bdd"

def get_wallstreet_news():
    """获取华尔街见闻财经新闻"""
    news_list = []
    try:
        url = "https://api.jin10.com/get_channel_list_all"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://wallstreetcn.com/",
            "x-app-id": "bVj1lGRVt5q0K2Ei"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                for item in data["data"][:8]:
                    title = item.get("title", "").strip()
                    if title:
                        news_list.append(title)
    except Exception as e:
        print(f"获取华尔街见闻失败: {e}")
    
    return news_list

def get_jobs():
    """获取热门岗位"""
    jobs_list = []
    
    # 获取热门招聘数据（综合类）
    try:
        url = "https://www.zhipin.com/web/geek/job-detail?jobCity=100010000&kw=%E7%83%AD%E9%97%A8"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            items = soup.select(".job-card")[:5]
            for item in items:
                title = item.select_one(".job-title")
                salary = item.select_one(".salary")
                if title:
                    job_text = title.get_text(strip=True)
                    if salary:
                        job_text += " " + salary.get_text(strip=True)
                    if job_text and len(job_text) > 2:
                        jobs_list.append(job_text)
    except Exception as e:
        print(f"获取招聘失败: {e}")
    
    # 如果Boss没数据，尝试其他方式
    if not jobs_list:
        jobs_list = ["骑手/配送员", "服务员", "快递员", "客服", "销售"]
    
    return jobs_list

def send_daily_report():
    """发送每日简报"""
    try:
        date_str = datetime.now().strftime("%Y年%m月%d日")
        
        # 获取华尔街新闻
        news = get_wallstreet_news()
        news_text = ""
        if news:
            for i, n in enumerate(news, 1):
                news_text += f"{i}. {n}\n"
        else:
            news_text = "暂无新闻数据\n"
        
        # 获取热门岗位
        jobs = get_jobs()
        jobs_text = ""
        if jobs:
            for j in jobs[:5]:
                jobs_text += f"• {j}\n"
        else:
            jobs_text = "暂无岗位数据\n"
        
        # 组装消息
        message = f"📅 **{date_str} 每日简报**\n\n"
        message += f"**【华尔街见闻 - 财经热点】**\n{news_text}\n"
        message += f"**【热门岗位推荐】**\n{jobs_text}\n"
        message += f"---\n"
        message += f"*每天8点自动推送 · AutoShell*"
        
        data = {"msgtype": "markdown", "markdown": {"content": message}}
        
        print("正在发送每日简报...")
        response = requests.post(WEBHOOK_URL, json=data, timeout=30)
        result = response.json()
        
        if result.get("errcode") == 0:
            print("✅ 每日简报发送成功！")
            return True
        else:
            print(f"❌ 发送失败: {result}")
            return False
    except Exception as e:
        print(f"❌ 发送出错: {e}")
        return False

def main():
    print("=" * 50)
    print("AutoShell 每日简报")
    print("=" * 50)
    
    print("\n正在获取财经新闻和热门岗位...")
    success = send_daily_report()
    
    if success:
        print("\n🎉 发送完成！")
        sys.exit(0)
    else:
        print("\n❌ 发送失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
