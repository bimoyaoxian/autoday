#!/usr/bin/env python3
import os
import sys
import requests
from datetime import datetime

# 企业微信机器人Webhook地址
WEBHOOK_KEY = os.environ.get('WEBHOOK_KEY', '550f678c-bff5-4968-8ae3-f184785d0bdd')
WEBHOOK_URL = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={WEBHOOK_KEY}"

def send_simple_message():
    try:
        date_str = datetime.now().strftime("%Y年%m月%d日 %H:%M")
        message = f"🔧 **AutoShell 测试消息**\n\n" \
                  f"✅ GitHub Actions 连接测试成功\n" \
                  f"📅 时间: {date_str}\n" \
                  f"🎯 状态: 基础功能正常\n\n" \
                  f"---\n" \
                  f"*AutoShell 自动化推送系统*"
        
        data = {
            "msgtype": "markdown",
            "markdown": {"content": message}
        }
        
        print("正在发送测试消息...")
        response = requests.post(WEBHOOK_URL, json=data, timeout=10)
        result = response.json()
        
        if result.get("errcode") == 0:
            print("✅ 测试消息发送成功！")
            return True
        else:
            print(f"❌ 消息发送失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 发送消息时出错: {e}")
        return False

def main():
    print("=" * 50)
    print("AutoShell 基础功能测试")
    print("=" * 50)
    
    print("\n[1/2] 测试企业微信连接...")
    print("[2/2] 发送测试消息...")
    
    success = send_simple_message()
    
    if success:
        print("\n🎉 基础功能测试完成！")
        sys.exit(0)
    else:
        print("\n❌ 测试失败，请检查配置")
        sys.exit(1)

if __name__ == "__main__":
    main()
