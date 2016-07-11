# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Vespa
"""

import os

from Feedback import *

fb = Feedback()

Desktop_Path = '%s/Desktop/'%(os.path.expanduser('~'))
list_dirs = os.listdir(Desktop_Path)
for line in list_dirs:
    filepath = os.path.join(Desktop_Path,line)
    if not os.path.isdir(filepath):
        if line.endswith('xml'):
            xmlid = line.split('.')[0]
            fb.add_item(xmlid+'.xml',subtitle='转化'+xmlid+'.xml',arg=xmlid)

print fb