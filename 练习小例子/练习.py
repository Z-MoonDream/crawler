# -*- coding: utf-8 -*-
import requests

import  re

t = ' s  100 sdd 11'
b='1'
print(re.search('(\d+)',t).group(1))


