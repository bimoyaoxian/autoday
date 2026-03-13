#!/usr/bin/env python3
import os
import sys
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re

# 企业微信机器人Webhook地址
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=550f678c-bff5-4968-8ae3-f184785d0bdd"

def get_wallstreetcn_breakfast():
    """爬取华尔街见闻早餐FM-Radio"""
    news_list = []
    try:
        url = "https://wallstreetcn.com/articles/3880655"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://wallstreetcn.com/"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            
            # 获取日期标题
            title_elem = soup.select_one(".article-header-title, .title, h1")
            if title_elem:
                title_text = title_elem.get_text(strip=True)
                # 匹配日期格式
                date_match = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)', title_text)
                if date_match:
                    news_list.append(f"华尔街见闻早餐FM-Radio | {date_match.group(1)}")
            
            # 获取文章内容
            content_elem = soup.select_one(".article-content, .content, .article-body")
            if content_elem:
                paragraphs = content_elem.select("p")
                for p in paragraphs[:5]:
                    text = p.get_text(strip=True)
                    if text and len(text) > 10:
                        # 清理文本
                        text = re.sub(r'[\u3000\xa0]+', ' ', text)
                        if text:
                            news_list.append(text)
    except Exception as e:
        print(f"华尔街见闻失败: {e}")
    
    return news_list

def get_weibo_hot():
    """爬取微博热搜榜"""
    news_list = []
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://weibo.com"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("ok") == 1:
                realtime = data.get("data", {}).get("realtime", [])
                for item in realtime[:8]:
                    title = item.get("word", "")
                    if title:
                        news_list.append(title)
    except Exception as e:
        print(f"微博热搜失败: {e}")
    
    return news_list

def get_baidu_hot():
    """爬取百度实时热点"""
    news_list = []
    try:
        url = "https://top.baidu.com/board?tab=realtime"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            items = soup.select(".item-wrap")[:8]
            for item in items:
                title = item.select_one(".title")
                if title:
                    news_list.append(title.get_text(strip=True))
    except Exception as e:
        print(f"百度热点失败: {e}")
    
    return news_list

def get_douyin_hot():
    """爬取抖音热榜"""
    news_list = []
    try:
        url = "https://www.douyin.com/aweme/v1/web/hot/search/list/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status_code") == 0:
                word_list = data.get("data", {}).get("word_list", [])
                for item in word_list[:8]:
                    title = item.get("word", "")
                    if title:
                        news_list.append(title)
    except Exception as e:
        print(f"抖音热榜失败: {e}")
    
    return news_list

def get_news():
    """获取热点新闻 - 爬虫方式"""
    # 优先获取华尔街见闻
    news = get_wallstreetcn_breakfast()
    
    # 如果没有华尔街见闻数据，获取其他来源
    if not news:
        news = get_weibo_hot()
    if not news:
        news = get_baidu_hot()
    if not news:
        news = get_douyin_hot()
    
    return news[:8]

def get_boss_jobs():
    """爬取Boss直聘热门岗位"""
    jobs_list = []
    try:
        url = "https://www.zhipin.com/web/geek/job-list?city=101010100&page=1"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.zhipin.com/"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            items = soup.select(".job-card")[:10]
            for item in items:
                title = item.select_one(".job-title")
                salary = item.select_one(".salary")
                if title:
                    text = title.get_text(strip=True)
                    if salary:
                        text += " " + salary.get_text(strip=True)
                    if text and len(text) > 2:
                        jobs_list.append(text)
    except Exception as e:
        print(f"Boss直聘失败: {e}")
    
    return jobs_list

def get_51job_jobs():
    """爬取前程无忧热门岗位"""
    jobs_list = []
    try:
        url = "https://www.51job.com/search/joblist.php?jobarea=000000&keyword=&issuedate=1&sort=date"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            items = soup.select(".joblist .el")[:10]
            for item in items:
                title = item.select_one("a")
                salary = item.select_one(".salary")
                if title:
                    text = title.get_text(strip=True)
                    if salary:
                        text += " " + salary.get_text(strip=True)
                    if text and len(text) > 5:
                        jobs_list.append(text)
    except Exception as e:
        print(f"前程无忧失败: {e}")
    
    return jobs_list

def get_lagou_jobs():
    """爬取拉勾网热门岗位"""
    jobs_list = []
    try:
        url = "https://www.lagou.com/jobs/list_Python"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            items = soup.select(".con_list_item")[:10]
            for item in items:
                title = item.select_one(".position-link")
                salary = item.select_one(".money")
                if title:
                    text = title.get_text(strip=True)
                    if salary:
                        text += " " + salary.get_text(strip=True)
                    if text and len(text) > 2:
                        jobs_list.append(text)
    except Exception as e:
        print(f"拉勾网失败: {e}")
    
    return jobs_list

def get_jobs():
    """获取热门岗位 - 爬虫方式"""
    jobs = get_boss_jobs()
    if not jobs:
        jobs = get_51job_jobs()
    if not jobs:
        jobs = get_lagou_jobs()
    
    return jobs[:5]

def send_daily_report():
    """发送每日简报"""
    try:
        date_str = datetime.now().strftime("%Y年%m月%d日")
        
        # 获取新闻
        news = get_news()
        news_text = ""
        if news:
            for n in news:
                news_text += f"• {n}\n"
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
        message += f"**【华尔街见闻 + 热点新闻】**\n{news_text}\n"
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
