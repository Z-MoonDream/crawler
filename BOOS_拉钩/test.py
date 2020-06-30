# -*- coding: utf-8 -*-
import re

a = '发布于3月11日'
if not re.search('\d\d日',a):
    print(re.sub('月','月0',a))



