# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from wangyiPro.items import WangyiproItem


class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://news.163.com/']
    model_urls = []

    # 实例化浏览器对象 在中间件中使用 获取ajax数据
    bro = webdriver.Chrome(executable_path=r'E:\plus_len\练习\爬虫\Scrapy框架\wangyiPro\wangyiPro\spiders\chromedriver.exe')

    def parse(self, response):
        # 解析出5个板块对应的url
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        model_index = [3, 4, 6, 7, 8]
        for index in model_index:
            # li依次表示的是5个板块对应的li标签
            li = li_list[index]

            # 5个板块对应的url
            model_url = li.xpath('./a/@href').extract_first()

            # 将5个板块对应的url封装进属性中方便中间件调用
            self.model_urls.append(model_url)

            # 对每一个url手动发起请求
            yield scrapy.Request(model_url, callback=self.parse_model)

    # 用于解析每一个板块对应页面数据中的新闻标题和新闻详情页的url
    def parse_model(self, response):

        # 该方法中获取的response对象是没有包含动态加载出来的新闻数据的(是一个不满足需求的response)
        #
        # 5+n个响应对象经过parse_modele
        # 5：5大板块对应的响应数据，是不满足需求的响应数据，里面没有新闻数据(是动态加载的ajax数据)
        # n：进入新闻详情页获取的简介不含ajax数据是满足需求的
        #
        # 如果下载中间件生效了 则返回的response响应数据里面包含了ajax请求
        # 则div_list就不是空的
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div/div/ul/li/div/div')
        for div in div_list:
            detail_url = div.xpath('./a/@href').extract_first()
            title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            item = WangyiproItem()
            item['title'] = title
            if detail_url == None:
                continue
            if title == None:
                continue

            # 对新闻详情页发手动请求
            yield scrapy.Request(detail_url, callback=self.parse_new_detail, meta={'item': item})

    # # 解析新闻内容
    def parse_new_detail(self, response):

        item = response.meta['item']
        content_list = response.xpath('//*[@id="endText"]//text()').extract()

        # 拼接字符串
        content = ''.join(content_list)
        item['content'] = content

        yield item

    #
    # 重写父类方法 该方法只会在整个程序结束时执行一次
    # ！！！！！！所有重写父类的方法，必须加上spider 这个
    # spider就相当于self一样，你不加spider必然报错
    def closed(self, spider):
        self.bro.quit()
