# -*- coding: utf-8 -*-
import requests
from lxml import etree
import random
from fake_useragent import UserAgent
from multiprocessing import Lock
from multiprocessing.dummy import Pool
headers = {'User-Agent':str(UserAgent().random),
           'Connection':'keep-alive',
           'Cache-Control':'no-cache',
           'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           }

def produce():

    start_url = 'https://www.xicidaili.com/wn/'
    url_list = [start_url + str(i) for i in range(1,41)]
    return url_list

def get_request(url):
    response = requests.get(url=url, headers=headers).content
    html = etree.HTML(response)
    ip_tr = html.xpath('//*[@id="ip_list"]//tr')[1:]
    ip_port_list = []
    for td in ip_tr:
        ip = td.xpath('./td[2]/text()')[0]
        port = td.xpath('./td[3]/text()')[0]
        ip_port = ip+':'+port
        try :
            response_ = requests.get(url='https://www.baidu.com/',headers={'User-Agent':str(UserAgent().random)},proxies={'https':ip_port},timeout=4)
            if response_.status_code == 200:
                # ip_port_list.append(ip_port)
                print(ip_port)
        except:
           pass

    # return ip_port_list
# def parse_response(ip_port_list):
#
#     for i in ip_port_list:
#         lock.acquire()
#         verified_file.write(i + '\n')
#         lock.release()


if __name__ == '__main__':
    # verified_file = open('./ip_port.txt', 'a')
    # lock = Lock()
    pool = Pool(100)
    verified_list = pool.map(get_request,produce())
    # save_file = pool.map(parse_response,verified_list)
