# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Vespa
"""

from support import *
def Danmaku2ASS(input_files, output_file, stage_width, stage_height, reserve_blank=0, font_face='sans-serif', font_size=25.0, text_opacity=1.0, comment_duration=5.0, is_reduce_comments=False, progress_callback=None):
    """
获取弹幕转化成ass文件
input_files：弹幕文件，可由GetDanmuku(cid)获得
output_file：输出ASS文件路径
    """
    fo = None
    comments = ReadComments(input_files, font_size)
    try:
        fo = ConvertToFile(output_file, 'w')
        ProcessComments(comments, fo, stage_width, stage_height, reserve_blank, font_face, font_size, text_opacity, comment_duration, is_reduce_comments, progress_callback)
    finally:
        if output_file and fo != output_file:
            fo.close()


if __name__ == "__main__":
    xmlid = "{query}"
    Desktop_Path = '%s/Desktop/'%(os.path.expanduser('~'))
    fid = open('%s%s.xml'%(Desktop_Path,xmlid))
    Danmaku2ASS(fid.read(),r'%s%s.ass'%(Desktop_Path,xmlid), 640, 360, 0, 'sans-serif', 15, 0.5, 10, False)