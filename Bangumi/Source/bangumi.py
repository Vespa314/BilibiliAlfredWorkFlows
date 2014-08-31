# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Administrator
"""


from support import * 
import hashlib
import datetime
import sys

import xml.etree.ElementTree as et
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class Feedback():
    """Feeback used by Alfred Script Filter

    Usage:
        fb = Feedback()
        fb.add_item('Hello', 'World')
        fb.add_item('Foo', 'Bar')
        print fb

    """

    def __init__(self):
        self.feedback = et.Element('items')

    def __repr__(self):
        """XML representation used by Alfred

        Returns:
            XML string
        """
        return et.tostring(self.feedback)

    def add_item(self, title, subtitle = "", arg = "", valid = "yes", autocomplete = "", icon = "icon.png"):
        """
        Add item to alfred Feedback

        Args:
            title(str): the title displayed by Alfred
        Keyword Args:
            subtitle(str):    the subtitle displayed by Alfred
            arg(str):         the value returned by alfred when item is selected
            valid(str):       whether or not the entry can be selected in Alfred to trigger an action
            autcomplete(str): the text to be inserted if an invalid item is selected. This is only used if 'valid' is 'no'
            icon(str):        filename of icon that Alfred will display
        """
        item = et.SubElement(self.feedback, 'item', uid=str(len(self.feedback)), arg=arg, valid=valid, autocomplete=autocomplete)
        _title = et.SubElement(item, 'title')
        _title.text = title
        _sub = et.SubElement(item, 'subtitle')
        _sub.text = subtitle
        _icon = et.SubElement(item, 'icon')
        _icon.text = icon


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

def GetGangumi(appkey,btype = None,weekday = None,AppSecret=None,mode = None):
    """
获取新番信息
输入：
    btype：番剧类型 2: 二次元新番 3: 三次元新番 默认：所有
    weekday:周一:1 周二:2 ...周六:6 
    """
    paras = {};
    if btype != None and btype in [2,3]:
        paras['btype'] = GetString(btype)
    if weekday != None:
        paras['weekday'] = GetString(weekday)
    url =  'http://api.bilibili.cn/bangumi?' + GetSign(paras,appkey,AppSecret);
    jsoninfo = JsonInfo(url);
    bangumilist = [];
    for bgm in jsoninfo.Getvalue('list'):
        if mode == 't' and bgm['weekday'] != int(time.strftime("%w",time.localtime())):
            continue;
        bangumi = Bangumi();
        bangumi.lastupdate = bgm['lastupdate']
        if mode == 'r' and datetime_timestamp(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))-bangumi.lastupdate>24*3600:
            continue;
        bangumi.title = bgm['title']
        bangumi.lastupdate_at = bgm['lastupdate_at']
        bangumi.weekday = bgm['weekday']
        bangumi.recentupdate = bgm['new']
        bangumi.bgmcount = bgm['bgmcount']
        bangumi.attention = bgm['click']
        bangumilist.append(bangumi)
    if mode == 'r':
        bangumilist = sorted(bangumilist,key=lambda x:x.lastupdate)
        bangumilist.reverse();
    return bangumilist
        
def datetime_timestamp(dt):
     time.strptime(dt, '%Y-%m-%d %H:%M:%S')
     s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
     return int(s)
     
def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt
     
def Getweek(num):
    string = ['日','一','二','三','四','五','六']
    return string[num]

query = '{query}'
# t:今天新番
# r:最近更新
# 3：三次元
# qx:查询星期n
if query == "":
    query = "t"
appkey='03fc8eb101b091fb';
secretkey = None;

fb = Feedback()
validlist = ['t','r'];
if query[-1] in validlist:
    validflag = 1;
    if len(query) == 1:
        bangumilist = GetGangumi(appkey,btype = 2,weekday=0,AppSecret=secretkey,mode = query[-1]);
    elif len(query) == 2 and query[0]=='3':
        bangumilist = GetGangumi(appkey,btype = 3,weekday=0,AppSecret=secretkey,mode = query[-1]);
    else:
        validflag = 0;
    if validflag:
        try:
            for bgm in bangumilist:
                if bgm.recentupdate:
                    fb.add_item(bgm.title,subtitle="【周%s】最后更新时间:%s,现有%s集,%d人浏览"%(Getweek(bgm.weekday),bgm.lastupdate_at,bgm.bgmcount,bgm.attention),arg=bgm.title)
                else:
                    fb.add_item(bgm.title,subtitle="【周%s】最后更新时间:%s,最近未更新,现有%s集,%d人浏览"%(Getweek(bgm.weekday),bgm.lastupdate_at,bgm.bgmcount,bgm.attention),arg=bgm.title)
            
        except SyntaxError as e:
            if ('EOF', 'EOL' in e.msg):
                fb.add_item('...')
            else:
                fb.add_item('SyntaxError', e.msg)
        except Exception as e:
                fb.add_item(e.__class__.__name__,subtitle=e.message)    
print fb