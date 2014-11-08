# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Administrator
"""


from support import * 
import hashlib
import io
import xml.dom.minidom
import random
import math
import os
import sys
from Feedback import * 

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
    

def GetVedioInfo(aid,appkey,page = 1,AppSecret=None,fav = None):
    paras = {'id': GetString(aid),'page': GetString(page)};
    if fav != None:
        paras['fav'] = fav;
    url =  'http://api.bilibili.cn/view?'+GetSign(paras,appkey,AppSecret);
    jsoninfo = JsonInfo(url);
    vedio = Vedio(aid,jsoninfo.Getvalue('title'));
    vedio.guankan = jsoninfo.Getvalue('play')
    vedio.commentNumber = jsoninfo.Getvalue('review')
    vedio.danmu = jsoninfo.Getvalue('video_review')
    vedio.shoucang = jsoninfo.Getvalue('favorites');
    vedio.description = jsoninfo.Getvalue('description')
    vedio.tag = [];
    taglist = jsoninfo.Getvalue('tag');
    if taglist != None:
        for tag in taglist.split(','):
            vedio.tag.append(tag);
    vedio.cover = jsoninfo.Getvalue('pic');
    vedio.author = User(jsoninfo.Getvalue('mid'),jsoninfo.Getvalue('author'));
    vedio.page = jsoninfo.Getvalue('pages');
    vedio.date = jsoninfo.Getvalue('created_at');
    vedio.credit = jsoninfo.Getvalue('credit');
    vedio.coin = jsoninfo.Getvalue('coins');
    vedio.spid = jsoninfo.Getvalue('spid');
    vedio.cid = jsoninfo.Getvalue('cid');
    vedio.offsite = jsoninfo.Getvalue('offsite');
    vedio.partname = jsoninfo.Getvalue('partname');
    vedio.src = jsoninfo.Getvalue('src');
    vedio.tid = jsoninfo.Getvalue('tid')
    vedio.typename = jsoninfo.Getvalue('typename')
    vedio.instant_server = jsoninfo.Getvalue('instant_server');
    return vedio
    
def GetSign(params,appkey,AppSecret=None):
    """
    获取新版API的签名，不然会返回-3错误
待添加：【重要！】
    需要做URL编码并保证字母都是大写，如 %2F
    """
    params['appkey']=appkey;
    data = "";
    paras = params.keys();
    paras.sort();
    for para in paras:
        if data != "":
            data += "&";
        data += para + "=" + params[para];
    if AppSecret == None:
        return data
    m = hashlib.md5()
    m.update(data+AppSecret)
    return data+'&sign='+m.hexdigest()

fb = Feedback()
av = '{query}'
appkey = "03fc8eb101b091fb"
regex = re.compile('http:/*[^/]+/video/av(\\d+)(/|/index.html|/index_(\\d+).html)?(\\?|#|$)')
regex_match = regex.match(av)
if regex_match:
    aid = regex_match.group(1)
    pid = regex_match.group(3) or '1'
    vedio = GetVedioInfo(aid,appkey,AppSecret=None,page = pid)
    try:
        if pid == '1':
            fb.add_item('转化'+vedio.title,subtitle="弹幕cid:%d"%(vedio.cid),arg=str(vedio.cid)+'------'+vedio.title+'------'+pid)
        else:
            fb.add_item('转化'+vedio.title,subtitle="弹幕cid:%d (%s P)"%(vedio.cid,pid),arg=str(vedio.cid)+'------'+vedio.title+'------'+pid)

        if pid == '1':
            fb.add_item('不转化'+vedio.title,subtitle="弹幕cid:%d"%(vedio.cid),arg='')
        else:
            fb.add_item('不转化'+vedio.title,subtitle="弹幕cid:%d (%s P)"%(vedio.cid,pid),arg='')
    except SyntaxError as e:
        if ('EOF', 'EOL' in e.msg):
            fb.add_item('...')
        else:
            fb.add_item('SyntaxError', e.msg)
    except Exception as e:
            fb.add_item(e.__class__.__name__,subtitle=e.message)    
    print fb
    
    # Danmaku2ASS(GetDanmuku(vedio.cid),r'%s/Desktop/%s-%s.ass'%(os.path.expanduser('~'),vedio.title,pid), 640, 360, 0, 'sans-serif', 15, 0.5, 10, False)