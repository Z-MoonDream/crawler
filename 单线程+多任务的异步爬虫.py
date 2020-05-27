# -*- coding: utf-8 -*-
import requests
from lxml import etree
import random
from fake_useragent import UserAgent
from multiprocessing.dummy import Pool
from time import sleep
import time

headers = {
          'User-Agent': str(UserAgent().random)
     }

def get_request(url):

     response = requests.get(url=url,headers=headers).content
     return response

def parse_response(response_html):

    return len(response_html)

# 同步代码
# if __name__ == '__main__':
#     for i in range(10):
#          get_request('https://cn.bing.com/search')

# 异步代码
urls = ['http://127.0.0.1:8000/custom.html' for i in range(100)]
if __name__ == '__main__':
    start = time.time()
    pool = Pool(20) # 不写的话模式开启的线程数量是CPU数
    # 使用get_request作为回调函数，需要基于异步的形式对urls中的每一个列表元素进行操作
    # 保证回调函数必须且只有一个参数，和返回值(如果要传入多个可以将这个参数接收的是字典形式，然后在函数内部进行调用
    # get_request的返回值会返回给map，并且是一个列表
    result_list = pool.map(get_request,urls)
    # 对响应进行解析
    result_response_list = pool.map(parse_response,result_list)
    # 两个map之间是串行的，同一个map是异步的
    print(time.time()-start)
    print(result_response_list)
    # print(result_list)  [114056, 114056, 113716, 113953, 113716, 114056, 114056, 113716, 114056, 114056]


