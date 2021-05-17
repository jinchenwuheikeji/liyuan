# -*- coding:UTF-8 -*-
import requests
import time
import datetime
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

# 参数配置
# 监控的网站RSS地址
url = "https://hostloc.com/forum.php?mod=rss&auth=0"

# 监控的关键词 ： 指定关键词使用第一个，监控所有则使用第二个
# keywords = ["白嫖", "福利", "T楼", "t楼"]
keywords = ["all"]

# 请求间隔时间, 不要小于30，不然容易触发js验证，这里暂时没有处理这种情况
requestIntervalTime = 30

# 时间格式化字符串
timeFormatStr = "%a, %d %b %Y %H:%M:%S +0000"


'''
推送结果
'''
def pushRes(post, keyword):
    title = "HostLoc 有新帖子啦！！！ 触发关键词：{}".format(keyword)
    text = "标题：{}\n作者：{}\n链接：{}".format(post["title"], post["author"], post["link"])

    mokaPush(title, text)



'''
推送方式1： 摩卡酱TG
文档：https://www.yuque.com/wanglingdadadajuntuan/moka/aq33zp
'''
def mokaPush(title, text):
    # 1. 摩卡酱TG通知
    mokaToken = "你的Token"
    mokaUrl = "https://moka.sage.run/api/send?token={}&title={}&text={}".format(mokaToken, title, text)

    res = requests.get(mokaUrl)
    if (res.status_code == 200):
        print("信息推送成功！")
    else:
        print("信息推送出错: " + res.text)


'''
请求接口
获取RSS内容
'''
def getRssRes():
    res = ""

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "referer": "https://hostloc.com/forum.php?mod=rss&auth=0",
        "authority": "hostloc.com"
    }

    try:
        res = requests.get(url, headers = headers).text
    except:
        while (True):
            try:
                res = requests.get(url, headers = headers).text
                break
            except:
                print("请求接口出错，请检查网络是否正常")
                time.sleep(requestIntervalTime)

    return res

'''
解析出请求结果的所有返回结果
'''
def parseXmlOfAllPosts(res):
    # 结果
    posts = []

    try:
        root = et.fromstring(res)
    except:
        # 出错直接跳过本次，等待下次
        print(res)
        return posts

    # 循环出所有的item，进入posts
    channel = root.find("channel")
    for child in channel:
        if (child.tag == "item"):
            post = {}
            post["title"] = child.find("title").text
            post["link"] = child.find("link").text
            post["description"] = child.find("description").text
            post["author"] = child.find("author").text
            post["pubDate"] = child.find("pubDate").text

            posts.append(post)

    return posts

def start():
    # 最后的帖子发布时间
    lastPostPubDate = ""

    # 第一次运行 记录当前最新帖子的时间
    nowPost = parseXmlOfAllPosts(getRssRes())[0]
    lastPostPubDate = datetime.datetime.strptime(nowPost["pubDate"], timeFormatStr)
    print("当前最新的帖子：" + nowPost["title"])
    print("当前最新的帖子时间：" + datetime.datetime.strftime(lastPostPubDate, timeFormatStr))
    time.sleep(requestIntervalTime)

    # 循环运行
    while (True):
        posts = parseXmlOfAllPosts(getRssRes())
    
        for post in posts:
            postTime = datetime.datetime.strptime(post["pubDate"], timeFormatStr)
            if postTime > lastPostPubDate:
                print(post["title"])
                print(post["pubDate"])

                # 循环关键词
                for keyword in keywords:
                    if (keyword == 'all'):
                        pass
                    else:
                        if keyword not in post["title"]:
                            continue
                    
                    # 符合推送条件
                    print("触发关键词: {}".format(keyword))
                    pushRes(post, keyword)

        lastPostPubDate = datetime.datetime.strptime(posts[0]["pubDate"], timeFormatStr)

        time.sleep(requestIntervalTime)


if __name__ == "__main__":
    print("开始运行......")
    start()