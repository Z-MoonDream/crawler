# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class ImgproPipeline(object):
#     def process_item(self, item, spider):
#         return item

import scrapy
from scrapy.pipelines.images import ImagesPipeline

class ImgproPipeline(ImagesPipeline):
    # 是用来对媒体资源进行请求(数据下载),参数item就是接受到的爬虫类提交的item对象
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['img_src'])

    # 指明数据存储的路径(名称 也就是图片的名字)
    def file_path(self, request, response=None, info=None):
        return request.url.split('/')[-1]

    # 如果还有下一个管道类则 将item传递给下一个即将被执行的管道类
    def item_completed(self, results, item, info):
        return item


