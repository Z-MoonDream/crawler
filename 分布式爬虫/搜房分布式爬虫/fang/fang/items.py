# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市名字
    city_name = scrapy.Field()
    # 小区名字
    house_name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 居室和面积情况
    rooms_area = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 行政区
    district = scrapy.Field()
    # 是否在售
    sale = scrapy.Field()
    # 电话
    phone = scrapy.Field()
    # 房天下详情页面url
    house_link_url = scrapy.Field()


class EsfHouseItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市名字
    city_name = scrapy.Field()
    # 小区名字
    house_name = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 总价格
    price = scrapy.Field()
    # 单价
    unit = scrapy.Field()
    # 居室
    rooms = scrapy.Field()
    # 层
    floor = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 年代
    year = scrapy.Field()
    # 朝向
    orientation = scrapy.Field()
    # 房天下详情页面url
    house_link_url = scrapy.Field()

