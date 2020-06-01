# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql

class WangyiproPipeline(object):
    conn = None
    cursor = None
    def open_spider(self,spider):
        self.conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='',db='spider',charset='utf8')
        # print(self.conn)
    def process_item(self, item, spider):


        sql = 'insert into wangyi(title,content) values(%s,%s)'
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(sql,[item['title'],item['content']])
            self.conn.commit()
            # 没有问题则提交保存(没提交之前是在内存中的)
        except Exception as e:
            # 如果报错打印报错信息
            print(e)
            # 回滚事务 也就是删除该改条sql执行插入一半的数据
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()


