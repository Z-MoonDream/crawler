# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SuncrawlproPipeline(object):
    def process_item(self, item, spider):
        # 我们要做数据汇总，可以在 第一个Rule里面请求传参来解决
        # 或者说学数据分析用共同的标示位
        # 也可以放在数据库中进行合并 group by
        # 如果没有标示位可以设置标示位，如果不能设置标示位，就可以crawlspider结合request进行请求传参

        # 获取提交过来的item的类名(item是实例化的他有实例化的类)
        if item.__class__.__name__ =='Detail_item':
            content = item['content']
            num = item['num']
            # print(item)
        else:
            title = item['title']
            num = item['num']
            # print(item)

        return item
