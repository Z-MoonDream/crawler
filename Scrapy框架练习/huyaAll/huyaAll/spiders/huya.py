# -*- coding: utf-8 -*-
import scrapy

from huyaAll.items import HuyaproItem

class HuyaSpider(scrapy.Spider):
    # name = 'huya'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.huya.com/g/xingxiu']

    def parse(self, response):
        li_list = response.xpath('//*[@id="js-live-list"]/li')

        for li in li_list:
            title = li.xpath('./a[2]/text()').extract_first()
            author = li.xpath('./span/span[1]/i/text()').extract_first()
            hot = li.xpath('./span/span[2]/i[2]/text()').extract_first()

            # 实例化item类型对象
            item = HuyaproItem()
            item['title'] = title
            item['author'] = author
            item['hot'] = hot

            # 将item提交给管道(pipelines)
            yield item
        # 手动发起请求
        for page in range(2,5):
            new_url = f'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId=1663&tagAll=0&page={page}'
            # 发起的是get请求
            yield scrapy.Request(url=new_url ,callback=self.parse_othor)
    # 回调执行的函数(callback)
    def parse_othor(self,response):
        print(response.text)