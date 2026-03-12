# autoday 每日自动推送

每天早上8点自动获取新闻和招聘岗位信息，推送到企业微信群。

## 功能特性

- 📰 财经新闻、国家大事、科技资讯
- 💼 热门岗位招聘信息（Python、前端、算法工程师等）
- ⏰ 每天北京时间8点自动推送

## 快速部署

### 1. 配置Webhook

在 `src/wechat.py` 中修改你的企业微信机器人Webhook地址：

```python
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=你的key"
```

### 2. 推送到GitHub

1. 创建GitHub仓库
2. 上传所有代码
3. 设置Secrets（可选）：
   - 进入仓库 Settings → Secrets and variables → Actions
   - 添加 `WEBHOOK_KEY` 为你的机器人key

### 3. 自动运行

GitHub Actions会自动在每天UTC 0点（即北京时间8点）执行任务。

## 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 运行
cd src
python main.py
```

## 文件结构

```
AutoShell/
├── .github/workflows/daily.yml  # GitHub Actions配置
├── src/
│   ├── main.py    # 主程序入口
│   ├── news.py    # 新闻获取
│   ├── jobs.py    # 招聘获取
│   └── wechat.py  # 微信推送
├── requirements.txt
└── README.md
```

## 注意事项

- GitHub Actions每月免费2000分钟，足够使用
- 确保机器人Webhook地址正确
- 如需修改推送时间，修改 `.github/workflows/daily.yml` 中的cron表达式
