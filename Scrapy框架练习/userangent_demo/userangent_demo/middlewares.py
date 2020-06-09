# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals
from fake_useragent import UserAgent

class UserangentDemoDownloaderMiddleware(object):

    def process_request(self, request, spider):
        request.headers['User-Agent'] = UserAgent().random
        return None


    def process_response(self, request, response, spider):

        return response

class IPPRoxyDownloadMiddleware(object):
    PROXYIES = ['1.197.204.156:9999', '123.55.101.65:9999', '120.83.101.240:9999', '163.204.240.18:9999',
                '125.108.85.114:9000', '125.108.110.223:9000', '171.11.179.99:9999', '125.108.103.169:9000',
                '125.108.68.108:9000', '39.98.74.239:8080', '220.176.91.102:9000', '218.27.204.240:8000',
                '123.55.101.254:9999', '223.242.224.139:9999', '120.194.42.157:38185']

    def process_request(self,request,spider):
        proxy = 'http://'+'163.204.241.253:9999'
        request.meta['proxy'] = proxy


