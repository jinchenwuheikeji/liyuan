# hostloc_tools

## 介绍
一些Hostloc的小工具

## 软件架构
Python

## 使用说明

前置环境： Python3 / pip / git

### 1. 新帖监控推送

    0. git clone https://gitee.com/Sage668/hostloc_tools.git

    1. cd hostloc_tools/newPostPush
    
    # 修改配置信息(Token)
    # 监控的关键词
    2. vi newPostPush.py 
    
    3. pip install requests
    
    4. python newPostPush.py