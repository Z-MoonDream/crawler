# -*- coding: utf-8 -*-
import requests
from lxml import etree
import random
from fake_useragent import UserAgent

headers = {
          'User-Agent': str(UserAgent().random)
     }

def get_request(url):
     reponse = requests.get(url=url,headers=headers).content
     print(len(reponse))

if __name__ == '__main__':
    for i in range(10):
         get_request('https://cn.bing.com/search')