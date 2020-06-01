# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time
import pymysql


# 写入文件中
class HuyaproPipeline(object):
    # item就是接受到爬虫类提交过来的item对象
    # 提交几次item就会调用几次process_item 所以不能在process_item里面打开文件

    #重写父类方法
    def open_spider(self,spider):
        self.t = time.time()
        self.fp = open('huyazhibo.txt','w',encoding='utf-8')

    def process_item(self, item, spider):
        self.fp.write(item['title']+':'+item['author']+':'+item['hot']+'\n')

        print(item['title'],'写入成功！！！')

        # 如果优先级高的管道类执行了并且你的process_item
        # 中没有return的话另一个低优先级的管道类就会接收到
        # 空的item
        return item

    def close_spider(self,spider):
        print(time.time()-self.t)
        self.fp.close()


# 写入数据库的管道
class mysqlPipeLine(object):
    conn= None
    cursor=None

    def open_spider(self,spider):
        self.conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='',db='spider',charset='utf8')
        print(self.conn)
    def process_item(self,item,spider):
        # sql = f'insert into huya(title,auto,hot) values({item["title"]},{item["author"]},{item["hot"]})'
        sql = f'insert into huya(title,auto,hot) values(%s,%s,%s)'


        # 得到课执行sql的光标对象
        self.cursor = self.conn.cursor()

        # 执行事务保证数据完整性 要么全写入数据库要么全不写入数据库
        # 尝试执行
        try:
            self.cursor.execute(sql,[item["title"],item["author"],item["hot"]])
            # 没有问题则提交保存(没提交之前是在内存中的)
            self.conn.commit()
        except Exception as e:
            # 如果报错打印报错信息
            print(e)
            # 回滚事务 也就是删除该改条sql执行插入一半的数据
            self.conn.rollback()
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()