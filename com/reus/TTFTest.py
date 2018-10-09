#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""woff文件解析"""

from fontTools.ttLib import TTFont

font = TTFont("/Users/reus/Desktop/xhVWYXjG.woff")
cmap = font.getBestCmap()
print(cmap)
str = '&#100366;&#100363;&#100363;&#100367;&#100363;&#100370'
str = str.replace('&#', '')
arr_str = str.split(';')
for num in arr_str:
    ch = cmap.get(int(num))
    print(ch)
