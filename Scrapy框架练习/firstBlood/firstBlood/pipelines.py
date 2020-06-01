# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# 管道类 专门用于持久化存储 接收item对象
class FirstbloodPipeline(object):
    fp=None
    def open_spider(self,spider):
        print('我只会在爬虫开始的时候执行一次！！！')
        self.fp=open('./data.txt','w',encoding='utf-8')

    # 会被调用多次 所以打开文件的操作不能用with open 应该在开始的时候
    # 打开一次文件,全部写完后在关闭文件才行,如果写入process_item
    # 中就会开关多次如果是'w'还会覆盖！！！
    def process_item(self, item, spider):
        # item对象中属性content的值为取得的字符串
        content = item['content']
        self.fp.write(content)

        return item
    def close_spider(self,spider):
        print('我只会在爬虫结束的时候调用一次！！！')
        self.fp.close()

    # 注意点：open_spider 与close_spider都是重写父类的方法
    # 其他方法写了也不会被scrapy引擎执行

# 定义的别的管道类 但是因为爬虫文件只能提交一个item
# 提交的是优先级最高的那个管道类中
# 要进行设置