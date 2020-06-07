# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from 工具 import os_path_dirname
import os
import requests
from scrapy.pipelines.images import  ImagesPipeline
from bmw import settings
class BmwPipeline(object):

    def open_spider(self,request):
        self.img_path = os.path.join(os_path_dirname(__file__,2),'images')
        if not os.path.exists(self.img_path):
            os.mkdir(self.img_path)
    def process_item(self, item, spider):
        title = item['title']
        img_url_list = item['img_url_list']
        title_path = os.path.join(self.img_path,title)
        if not os.path.exists(title_path):
            os.mkdir(title_path)
        for url in img_url_list:
            name = url.split('_')[-1]
            with open(os.path.join(title_path,name),'wb') as f:
                f.write(requests.get(url).content)
        return item

class BMWImagesPipeline(ImagesPipeline):

    # def get_media_requests(self, item, info):
    #     return [Request(x) for x in item.get(self.images_urls_field, [])]
    def get_media_requests(self, item, info):

        requests_objs = super(BMWImagesPipeline,self).get_media_requests(item,info)
        for requests_obj in requests_objs: # 这里的item就是这次请求时yield发过来的 item 取值就是item['XXX']
            # 将item给到request中 为什么能传递item还没搞清楚
            requests_obj.item=item
            # print(type(requests_obj)) # <class 'scrapy.http.request.Request'>

        return requests_objs # 与之对应    return [Request(x) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        # def file_path(self, request, response=None, info=None):
        #     image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        #     return 'full/%s.jpg' % (image_guid)
        path = super(BMWImagesPipeline,self).file_path(request,response,info)
        title = request.item['title']
        # 读取配置文件中的信息
        images_store = settings.IMAGES_STORE
        # 目录路径
        title_path = os.path.join(images_store,title)
        if not os.path.exists(title_path):
            os.mkdir(title_path)
        # 将path返回值的full替换为空就得到图片的名字了，当然也可以吧jpg改成png等等操作？图片质量会改变吗并不会，只是骗自己，真要jpg转png要用格式工厂等软件
        image_name = path.replace('full/','')
        image_path = os.path.join(title_path,image_name) # 图片路径
        return image_path # 与之对应   return 'full/%s.jpg' % (image_guid)

