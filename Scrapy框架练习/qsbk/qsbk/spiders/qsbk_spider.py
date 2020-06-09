# -*- coding: utf-8 -*-
import scrapy
from qsbk.items import QsbkItem

class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']

    page = 2
    def parse(self, response):
        div_list = response.xpath('//div[@class="col1 old-style-col1"]/div')
        for div in div_list:
            item = QsbkItem()
            text = div.xpath('.//div[@class="content"]/span//text()').extract()
            text_new = ''.join(text).strip()
            # print(text_new)
            item['text'] = text_new
            yield item
        if self.page<5:
            print(self.page)

            next_url = f'https://www.qiushibaike.com/text/page/{self.page}/'
            self.page+=1
            yield scrapy.Request(next_url,callback=self.parse)
