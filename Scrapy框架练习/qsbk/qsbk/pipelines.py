# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class QsbkPipeline(object):
    def open_spider(self,spider):
        self.fp = open('qsbk.json','w',encoding='utf-8')


    def process_item(self, item, spider):
        text_json = json.dumps(dict(item),ensure_ascii=False)
        self.fp.write(text_json+'\n')

        return item

    def close_spider(self,spider):
        self.fp.close()

