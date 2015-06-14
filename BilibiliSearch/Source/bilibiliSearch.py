# -*- coding: utf-8 -*-

import sys
from Feedback import *
from support import *
import datetime
import hashlib

def GetSign(params, appkey, AppSecret=None):
    """
    获取新版API的签名，不然会返回-3错误
待添加：【重要！】
    需要做URL编码并保证字母都是大写，如 %2F
    """
    params['appkey']=appkey
    data = ""
    paras = params.keys()
    paras.sort()
    for para in paras:
        if data != "":
            data += "&"
        data += para + "=" + str(params[para])
    if AppSecret == None:
        return data
    m = hashlib.md5()
    m.update(data+AppSecret)
    return data+'&sign='+m.hexdigest()

def biliVideoSearch(appkey, AppSecret, keyword, order = 'default', pagesize = 20, page = 1):
    """
【注】：
    旧版Appkey不可用，必须配合AppSecret使用！！

根据关键词搜索视频
输入：
    order：排序方式  默认default，其余待测试
    keyword：关键词
    pagesize:返回条目多少
    page：页码
    """
    paras = {}
    paras['keyword'] = GetString(keyword)
    paras['order'] = GetString(order)
    paras['pagesize'] = GetString(pagesize)
    paras['page'] = GetString(page)
    url =  'http://api.bilibili.cn/search?' + GetSign(paras, appkey, AppSecret)
    jsoninfo = JsonInfo(url)
    videolist = []
    for video_idx in jsoninfo.Getvalue('result'):
        if video_idx['type'] != 'video':
            continue
        video = Video(video_idx['aid'], video_idx['title'])
        video.typename = video_idx['typename']
        video.author = User(video_idx['mid'], video_idx['author'])
        video.acurl = video_idx['arcurl']
        video.description = video_idx['description']
        video.arcrank = video_idx['arcrank']
        video.cover = video_idx['pic']
        video.guankan = video_idx['play']
        video.danmu = video_idx['video_review']
        video.shoucang = video_idx['favorites']
        video.commentNumber = video_idx['review']
        video.date = video_idx['pubdate']
        video.tag = video_idx['tag'].split(',')
        videolist.append(video)
    return videolist

query = '{query}'
appkey = '70472776da900153'
secretkey = 'f7d9146f9363f3407d31098918493336'
videoList = biliVideoSearch(appkey,secretkey,query, pagesize = 30)
fb = Feedback()

try:
    for video in videoList:
        fb.add_item(video.title,subtitle="%s : http://www.bilibili.com/video/%s(%s)"%(video.typename,video.aid,datetime.datetime.utcfromtimestamp(video.date).strftime(r"%Y/%m/%d")),arg=video.aid)

except SyntaxError as e:
    if ('EOF', 'EOL' in e.msg):
        fb.add_item('...')
    else:
        fb.add_item('SyntaxError', e.msg)
except Exception as e:
        fb.add_item(e.__class__.__name__,subtitle=e.message)
print fb
