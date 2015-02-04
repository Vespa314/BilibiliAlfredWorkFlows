# -*- coding: utf-8 -*-

import sys
import re
import zlib
import urllib2
from Feedback import *

query = '{query}'
url = "http://www.bilibili.com/search?keyword=%s&orderby=&formsubmit="%query
req = urllib2.Request(url = url);
content = urllib2.urlopen(req,timeout = 10).read();
content = zlib.decompress(content, 16+zlib.MAX_WBITS)
content = content.replace("<label class='keyword'>",'')
content = content.replace("</label>",'')

reg = r'<div class="r_sp"><a href="http://www.bilibili.com/video/av(\d+)" target="_blank">\s*<div class="t"><span>([^<]*)</span>\s*([^<]*)</div>\s*</a>';
result = re.findall(reg,content,re.S)
fb = Feedback()

try:
    for item in result:
        avnum =  item[0]
        avtype = item[1]
        title = item[2].strip()
        fb.add_item(title,subtitle="%s : http://www.bilibili.com/video/%s"%(avtype,avnum),arg=avnum)
    
except SyntaxError as e:
    if ('EOF', 'EOL' in e.msg):
        fb.add_item('...')
    else:
        fb.add_item('SyntaxError', e.msg)
except Exception as e:
        fb.add_item(e.__class__.__name__,subtitle=e.message)    
print fb
    