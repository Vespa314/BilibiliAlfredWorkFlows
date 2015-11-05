# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Vespa
"""


from support import *
from Feedback import *

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36'
APPKEY = '85eb6835b0a1034e'
APPSEC = '2ad42749773c441109bdc0191257a664'

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
    video.cid = jsoninfo.Getvalue('cid')
    return video

def GetBilibiliUrl(url):
    global video
    overseas=False
    url_get_media = 'http://interface.bilibili.com/playurl?' if not overseas else 'http://interface.bilibili.com/v_cdn_play?'
    regex_match = re.findall('http:/*[^/]+/video/av(\\d+)(/|/index.html|/index_(\\d+).html)?(\\?|#|$)',url)
    if not regex_match:
        raise ValueError('Invalid URL: %s' % url)
    aid = regex_match[0][0]
    pid = regex_match[0][2] or '1'
    cid_args = {'type': 'json', 'id': aid, 'page': pid}

    cid = video.cid
    media_args = {'otype': 'json', 'cid': cid, 'type': 'mp4', 'quality': 4, 'appkey': APPKEY}
    resp_media = getURLContent(url_get_media+GetSign(media_args,APPKEY,APPSEC))
    resp_media = dict(json.loads(resp_media.decode('utf-8', 'replace')))
    media_urls = resp_media.get('durl')
    res = []
    for media_url in media_urls:
        res.append(media_url.get('url'))
    return res

def GetSign(params,appkey,AppSecret=None):
    params['appkey']=appkey;
    data = "";
    paras = sorted(params)
    paras.sort();
    for para in paras:
        if data != "":
            data += "&";
        data += para + "=" + str(params[para]);
    if AppSecret == None:
        return data
    m = hashlib.md5()
    m.update((data+AppSecret).encode('utf-8'))
    return data+'&sign='+m.hexdigest()

def ChangeFuck(params):
    data = "";
    paras = params;
    for para in paras:
        if data != "":
            data += "&";
        data += para + "=" + str(params[para]);
    return data

fb = Feedback()
url = '{query}'
# url = 'http://www.bilibili.com/video/av2968792/'
av = GetRE(url,r"\d+")[0]
video = GetVideoInfo(av,appkey=APPKEY,AppSecret=APPSEC)
downloadUrls = GetBilibiliUrl(url)
# print video.title
# for downloadUrl in downloadUrls:
#     print downloadUrl

for id,downloadUrl in enumerate(downloadUrls):
    fb.add_item('获取'+url+'下载地址',subtitle="%s(%d P)"%(video.title,id+1),arg=downloadUrl)

print fb