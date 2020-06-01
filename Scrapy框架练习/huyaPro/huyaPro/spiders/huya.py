# -*- coding: utf-8 -*-
import scrapy
from huyaPro.items import HuyaproItem

class HuyaSpider(scrapy.Spider):
    name = 'huya'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.huya.com/g/xingxiu']

    # 基于终端指令存储操作不能存到数据库中
    # def parse(self, response):
    #     li_list = response.xpath('//*[@id="js-live-list"]/li')
    #     all_data = []
    #     for li in li_list:
    #         # li.xpath('./a[2]/text()') 拿到列表列表中是Selector对象
    #         # .extract_first()才可以直接拿到列表中的Selector对象中的字符串
    #         # //text()则拿到的是所有的文本，那么用extract()则拿到多个
    #         # 文本组成的列表
    #         title = li.xpath('./a[2]/text()').extract_first()
    #         author = li.xpath('./span/span[1]/i/text()').extract_first()
    #         hot = li.xpath('./span/span[2]/i[2]/text()').extract_first()
    #         dic = {
    #             'title': title,
    #             'author':author,
    #             'hot':hot,
    #         }
    #         all_data.append(dic)
    #     return all_data

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






