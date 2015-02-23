# -*- coding: utf-8 -*-

import sys
from Feedback import *
from support import *
def biliVedioSearch(keyword, order = 'default', pagesize = 20, page = 1):
    """
根据关键词搜索视频
输入：
    order：排序方式  默认default，其余待测试
    keyword：关键词
    pagesize:返回条目多少
    page：页码
    """
    url = "http://api.bilibili.cn/search?keyword=%s&order=%s&pagesize=%d&page=%d"%(keyword, order, pagesize, page)
    jsoninfo = JsonInfo(url)
    videolist = []
    for video_idx in jsoninfo.Getvalue('result'):
        if video_idx['type'] != 'video':
            continue
        video = Vedio(video_idx['aid'], video_idx['title'])
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
videoList = biliVedioSearch(query, pagesize = 30)
fb = Feedback()

try:
    for video in videoList:
        fb.add_item(video.title,subtitle="%s : http://www.bilibili.com/video/%s"%(video.typename,video.aid),arg=video.aid)

except SyntaxError as e:
    if ('EOF', 'EOL' in e.msg):
        fb.add_item('...')
    else:
        fb.add_item('SyntaxError', e.msg)
except Exception as e:
        fb.add_item(e.__class__.__name__,subtitle=e.message)    
print fb
