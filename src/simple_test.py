#!/usr/bin/env python3
import os
import sys
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json

# 企业微信机器人Webhook地址
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=550f678c-bff5-4968-8ae3-f184785d0bdd"

def get_news():
    """获取财经新闻"""
    news_list = []
    
    # 方式1：腾讯新闻热点
    try:
        url = "https://r.inews.qq.com/gw/event/hot_ranking"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "idlist" in data and len(data["idlist"]) > 0:
                items = data["idlist"][0]["itemlist"]
                for item in items[:8]:
                    title = item.get("title", "").strip()
                    if title and len(title) > 5:
                        news_list.append(title)
    except Exception as e:
        print(f"腾讯新闻获取失败: {e}")
    
    # 方式2：新浪新闻热点
    if not news_list:
        try:
            url = "https://top.news.sina.com.cn/ws/Rank_apiInner_0_0_1_1_50_0_1_1.html"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "data" in data:
                    for item in data["data"][:8]:
                        title = item.get("title", "").strip()
                        if title:
                            news_list.append(title)
        except Exception as e:
            print(f"新浪新闻获取失败: {e}")
    
    return news_list

def get_jobs():
    """获取热门岗位"""
    jobs_list = []
    
    # Boss直聘热门岗位
    try:
        url = "https://www.zhipin.com/web/geek/job/list?city=101010100&page=1"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            items = soup.select(".job-card")[:10]
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
        print(f"Boss直聘获取失败: {e}")
    
    # 备用：前程无忧
    if not jobs_list:
        try:
            url = "https://www.51job.com/"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "lxml")
                items = soup.select(".joblist .el")[:10]
                for item in items:
                    title = item.select_one("a")
                    if title:
                        jobs_list.append(title.get_text(strip=True))
        except Exception as e:
            print(f"前程无忧获取失败: {e}")
    
    return jobs_list[:5]

def send_daily_report():
    """发送每日简报"""
    try:
        date_str = datetime.now().strftime("%Y年%m月%d日")
        
        # 获取新闻
        news = get_news()
        news_text = ""
        if news:
            for i, n in enumerate(news, 1):
                news_text += f"{i}. {n}\n"
        else:
            news_text = "暂无新闻数据\n"
        
        # 获取岗位
        jobs = get_jobs()
        jobs_text = ""
        if jobs:
            for j in jobs:
                jobs_text += f"• {j}\n"
        else:
            jobs_text = "暂无岗位数据\n"
        
        # 组装消息
        message = f"📅 **{date_str} 每日简报**\n\n"
        message += f"**【今日热点新闻】**\n{news_text}\n"
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
    
    print("\n正在获取新闻和岗位数据...")
    success = send_daily_report()
    
    if success:
        print("\n🎉 发送完成！")
        sys.exit(0)
    else:
        print("\n❌ 发送失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
