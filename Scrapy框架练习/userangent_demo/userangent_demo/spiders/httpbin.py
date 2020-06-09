# -*- coding: utf-8 -*-
import scrapy
import json

class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['https://httpbin.org/user-agent']

    def parse(self, response):
        #  json.dumps()用于将dict类型的数据转成str因为如果直接将dict类型的数据写入json文件中会发生报错，因此在将数据写入时需要用到该函数
        #  json.loads()用于将str类型的数据转成dict
        user_agent = json.loads(response.text)['user-agent']
        print('='*30)
        print(user_agent)
        print('=' * 30)
        yield scrapy.Request(self.start_urls[0],dont_filter=True)

