# 本地安装包导航

## 架构
使用flask+bootstrap+sqlite3 简单实现安装包下载

## 使用
1. 安装依赖
```sh
# 运行
pip install -r requirements.txt
nohup python app.py &
```

2. docker 运行
```sh
docker build -t downloadsite .
```

3. docker-compose 运行
```sh
docker-compose up -d
```

## 页面
- admin 管理员界面
- edit 编辑界面
- index 主页
- add 添加界面