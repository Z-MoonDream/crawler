# -*- coding: utf-8 -*-
# 都是基于面向对象(之前学的大都都是面向过程的)

# 导包
import scrapy

# 引入管道类，准备用于实例化Item对象
from firstBlood.items import FirstbloodItem

# 定义了一个类自动生成的 Spider是基类
class FirstSpider(scrapy.Spider):

    # 爬虫文件的名称：爬虫源文件的唯一标识(通过这个标识就可以定位到该.py文件)
    # 可以有多个但是一般就一个
    name = 'first'

    # 允许的域名：进行域名限定,如果写了则下面的起始url中只有允许域名可以被请求成功,一般注释掉
    # allowed_domains = ['www.xxx.com']

    # 起始的url列表：起始创建的那个url可以更改
    # 列表中的列表元素会被scrapy自动的进行请求发送
    # start_urls = ['http://www.xxx.com/']
    start_urls = ['https://dig.chouti.com/']

    # 解析数据的,用来解析response收到的响应数据(会调用parse这个方法)
    # 有多个就会调用多次parse
    # def parse(self, response):
    #     # print(response) 输入了很多日志信息,说明response没有拿到，请求没有成功(没有反反爬策略)
    #     div_list = response.xpath('/html/body/main/div/div/div[1]/div/div[2]/div[1]')
    #     for div in div_list:
    #
    #         # 注意：xpath返回的列表中的列表元素是Selector对象,我们要解析获取的字符串数据是存储在该
    #         # 对象中的必须要经过一个extract()的操作才可以将该对象中存储的字符串数获取
    #         # etree中的xpath的/text()是获取直系的文本内容,scrapy中的response的xpath中/text()
    #         # 返回的是一个Selector对象<Selector xxx='adasd' data='字符串内容'>
    #         # 必须同<Slector对象...>.extract_first()来获取字符串内容
    #         content = div.xpath('./div//text()').extract_first()
    #         print(content)
    #
    #
    #         # //text()返回的是该元素的全部文本内容，将内容放入Selector对象中了
    #         # 当xpath返回的列表元素有多个(Selector对象),想要将每一个列表元素对应的Selector中的
    #         # 字符串去除应该直接加上.extract()
    #         # 此时返回的是每个Selector对象返回一个字符串，多个返回多个字符串加入列表中
    #         # content = response.xpath('./div/div/div[1]/a//text()').extract()

    def parse(self, response):

        div_list = response.xpath('/html/body/main/div/div/div[1]/div/div[2]/div[1]')
        for div in div_list:

            content = div.xpath('./div//text()').extract_first()
            item = FirstbloodItem()
            item['content'] = content
            print(content)

