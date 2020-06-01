# -*- coding: utf-8 -*-
import scrapy
from moviePro.items import MovieproItem

class MovieSpider(scrapy.Spider):
    name = 'movie'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.4567kan.com/frim/index7.html']

    # url = f'https://www.4567kan.com/frim/index7-{}.html'
    # page要放在全局(实例化后的self.page互不影响)
    page = 2

    #专门用于解析电影名称和电影详情页url
    def parse(self, response):
        # page不能放在这里 这样会造成每次都是同样的page就不会增加了！！！
        # self.page = 2
        li_list = response.xpath('/html/body/div[1]/div/div/div/div[2]/ul/li')
        for li in li_list:
            name= li.xpath('./div/a/@title').extract_first()
            item = MovieproItem()
            item['name'] = name
            # 获取详情页url
            detail_url = 'https://www.4567kan.com'+  li.xpath('./div/a/@href').extract_first()
            # 对详情页url进行手动发送
            # 请求传参：让Request将一个数值(实体 item)(字典)传递给回调函数
            yield scrapy.Request(detail_url,callback=self.parse_detail,meta={'item':item})
        # 分页爬取 不能用for循环会死递归
        # for i in range(2,6):
        if self.page <6:
            print(self.page)
            new_url = f'https://www.4567kan.com/frim/index7-{self.page}.html'
            self.page += 1
            yield scrapy.Request(new_url,callback=self.parse)



    def parse_detail(self,response):
        # 接受请求传参的数据(字典) 调字典键获取值是用[]不是()
        item = response.meta['item']

        # 描述
        desc =  response.xpath('/html/body/div[1]/div/div/div/div[2]/p[5]/span[2]/text()').extract_first()
        item['desc'] = desc
        yield item



