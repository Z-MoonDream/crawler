# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 这个类实例化的对象就是Item对象
class FirstbloodItem(scrapy.Item):

    # 如果你想在这里定义一个字段或属性，可以用如下的方式
    # define the fields for your item here like:
    # name = scrapy.Field()

    content = scrapy.Field() # Field是一个万能的数据类型 可以存任何类型的数据





