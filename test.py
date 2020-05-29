# -*- coding: utf-8 -*-

import re

c = '4-5千/月'

# b =re.findall(r'[\d\D]*千/月',c)
# b =re.findall(r'\d*\.?\d+',c)c
# print(re.findall(r'\d*\.?\d+','4.5-0.6千/月'))
x = re.findall(r'\d*\.?\d+',c)
#print(x)
# min_ = float(x[0])  #转换成浮点型并保留两位小数
max_ = format(float(x[1])/12,'.2f')
print(max_)

# li3[i][1] = min_+'-'+max_+u'万/月'