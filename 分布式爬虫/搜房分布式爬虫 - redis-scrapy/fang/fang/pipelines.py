# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from fang.fang.items import NewHouseItem,EsfHouseItem

class FangPipeline(object):
    def open_spider(self,spider):
        self.new_f = open('new_house.json','w',encoding='utf-8')
        self.esf_f = open('esf_house.json','w',encoding='utf-8')
    def process_item(self, item, spider):
        # 如果item是属于NewHouseItem实例化的那么就写入new_house.josn
        # 否则写入esf_house.json
        # isinstance 判断某个实例是否是指定类的实例  如果是返回True
        # 实例名.__class__.__name__ 获取类实例的名称
        if isinstance(item,NewHouseItem):
            self.new_f.write(json.dumps(dict(item),ensure_ascii=False)+'\n')
        else:
            self.esf_f.write(json.dumps(dict(item),ensure_ascii=False)+'\n')
        return item
    def close_spider(self,spider):
        self.esf_f.close()
        self.new_f.close()