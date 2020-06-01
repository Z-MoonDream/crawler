# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from time import sleep



class WangyiproDownloaderMiddleware(object):


    # 参数：
    # request：拦截到的请求对象(一个请求对象对应唯一的一个响应对象)由请求对象确定响应对象
    # response：拦截到所有的响应对象(1+5+n)
    # spider：爬虫类实例化的对象，可以实现爬虫类和中间件类(当前类，也有管道类)的数据交互
    def process_response(self, request, response, spider):
        # 爬虫类中的name属性
        # spider.name
        # 我们要拦截到5个板块对应的响应对象，将其替换成5个符合去需求的新的响应对象(有动态加载的数据)进行返回到爬虫类中进行后续解析

        # 1.找出5个板块对应的5个不符合需求的响应对象
        # 因为每个请求对象对应唯一的响应对象，所以我们可以通过请求对象(发送的url)来获取对应的不符合需求的响应对象
        if request.url in spider.model_urls:
            # 5个请求对象对应的响应对象
            # request = request 就是新的响应对象对应的请求对象(就是5个板块对应的请求对象这个值不用变)
            # url: 响应对象对应的请求对象对应的url(就是5大板块对应的请求对象的url)
            # body: 满足需求的响应数据 就是包含ajax数据的整张页面源码数据(可以通过selenium中的page_source获取)
            bro = spider.bro
            bro.get(request.url)
            page_text = bro.page_source # 包含了动态加载的新闻数据，可见即可的

            new_response = HtmlResponse(url=request.url,body=page_text,encoding='utf-8',request=request)

            return new_response
        # 返回(1+n)的响应对象 它们满足需求
        else:return response
