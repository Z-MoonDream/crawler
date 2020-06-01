# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from fbsPro.items import FbsproItem

class FbsSpider(RedisCrawlSpider):
    name = 'fbs'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['http://www.xxx.com/']
    redis_key = 'fbsQueue'

    rules = (
        Rule(LinkExtractor(allow=r'id=1&page=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        li_list = response.xpath('/html/body/div[2]/div[3]/ul[2]/li')
        for li in li_list:
            # !!!!xpath中不能出现tbody标签会为空 将tbody标签改成/就好
            status = li.xpath('./span[2]/text()').extract_first().split()
            title = li.xpath('./span[3]/a/text()').extract_first()
            item = FbsproItem()
            item['title'] = title
            item['status'] = status

            yield item