# -*- coding: utf-8 -*-
import scrapy


class MiddleSpider(scrapy.Spider):
    name = 'middle'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://www.baidu.com/s?wd=ip']

    def parse(self, response):
        page_text = response.text
        with open('ip.html','w',encoding='utf-8') as f:
            f.write(page_text)
