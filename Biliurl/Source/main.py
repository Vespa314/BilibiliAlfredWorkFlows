# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Vespa
"""


from support import *
from Feedback import *

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def GetVideoInfo(aid, appkey,page = 1, AppSecret=None, fav = None):
    """
获取视频信息
输入：
    aid：AV号
    page：页码
    fav：是否读取会员收藏状态 (默认 0)
    """
    paras = {'id': GetString(aid),'page': GetString(page)}
    if fav:
        paras['fav'] = fav
    url =  'http://api.bilibili.cn/view?'+GetSign(paras,appkey,AppSecret)
    jsoninfo = JsonInfo(url)
    video = Video(aid,jsoninfo.Getvalue('title'))
    video.guankan = jsoninfo.Getvalue('play')
    video.commentNumber = jsoninfo.Getvalue('review')
    video.danmu = jsoninfo.Getvalue('video_review')
    video.shoucang = jsoninfo.Getvalue('favorites')
    video.description = jsoninfo.Getvalue('description')
    video.tag = []
    taglist = jsoninfo.Getvalue('tag')
    if taglist:
        for tag in taglist.split(','):
            video.tag.append(tag)
    video.cover = jsoninfo.Getvalue('pic')
    video.author = User(jsoninfo.Getvalue('mid'),jsoninfo.Getvalue('author'))
    video.page = jsoninfo.Getvalue('pages')
    video.date = jsoninfo.Getvalue('created_at')
    video.credit = jsoninfo.Getvalue('credit')
    video.coin = jsoninfo.Getvalue('coins')
    video.spid = jsoninfo.Getvalue('spid')
    video.cid = jsoninfo.Getvalue('cid')
    video.offsite = jsoninfo.Getvalue('offsite')
    video.partname = jsoninfo.Getvalue('partname')
    video.src = jsoninfo.Getvalue('src')
    video.tid = jsoninfo.Getvalue('tid')
    video.typename = jsoninfo.Getvalue('typename')
    video.instant_server = jsoninfo.Getvalue('instant_server')
    ## 以下三个意义不明。。
    # video.allow_bp = jsoninfo.Getvalue('allow_bp')
    # video.allow_feed = jsoninfo.Getvalue('allow_feed')
    # video.created = jsoninfo.Getvalue('created')
    return video

def GetBilibiliUrl(url, appkey, AppSecret=None):
    overseas=False
    url_get_media = 'http://interface.bilibili.com/playurl?' if not overseas else 'http://interface.bilibili.com/v_cdn_play?'
    regex_match = re.findall('http:/*[^/]+/video/av(\\d+)(/|/index.html|/index_(\\d+).html)?(\\?|#|$)',url)
    if not regex_match:
        return []
    aid = regex_match[0][0]
    pid = regex_match[0][2] or '1'
    video = GetVideoInfo(aid,appkey,pid,AppSecret)
    cid = video.cid
    media_args = {'cid': cid,'quality':4}
    resp_media = getURLContent(url_get_media+GetSign(media_args,appkey,AppSecret))
    media_urls = [str(k.wholeText).strip() for i in xml.dom.minidom.parseString(resp_media.decode('utf-8', 'replace')).getElementsByTagName('durl') for j in i.getElementsByTagName('url')[:1] for k in j.childNodes if k.nodeType == 4]
    return media_urls

fb = Feedback()
url = '{query}'
# url = 'http://www.bilibili.com/video/av2527767/'
appkey = "03fc8eb101b091fb"
av = GetRE(url,r"\d+")[0]
video = GetVideoInfo(av,appkey)
# print video.title
downloadUrl = GetBilibiliUrl(url,appkey)
# print downloadUrl

for item in downloadUrl:
    fb.add_item('获取'+url+'下载地址',subtitle=video.title,arg=item)
print fb