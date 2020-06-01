# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from sunCrawlPro.items import SuncrawlproItem,Detail_item


class SunSpider(CrawlSpider):
    name = 'sun'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest?id=1&page=1']

    # 实例化了一个链接提取器对象
    # 作用：根据指定规则(allow='正则表达式')进行指定链接的提取
    # 只会提取出链接 不会提取出字符串
    # 如果是False的话则只会提取当前页前后的两个页面链接，而不是目前页所看到的所有链接
    # 获取页码的链接
    # 如果follow=True：将链接提取器，继续作用到链接提取器提取到的，链接所对应的，页面中
    # 比如：我对首页发起提取，follow=True 我提取到了页面源码中的页码链接然后我继续对页码链接中的页码继续进行提取符合规则的链接，也就是对首页提取页码就会提取出1,2,3,4,5然后对第二页提取页码提取出2,3,4,5,6然后对第三页提取页码提取出4,5,6,7，这样 虽然会有大量重复的链接，但是这些重复的链接都被调度器过滤掉了所以根本不用担心
    link = LinkExtractor(allow=r'id=1&page=\d+')
    # 获取新闻详情页的链接 正则中如果要将符号转移成字符串的话要加\
    # 拿到新闻详情页的链接后，对链接发起请求，然后在对响应数据进行解析出自己想要的数据来
    # ！！！一定要注意？和.这些都要转移成字符串的
    link_detail = LinkExtractor(allow=r'index\?id=\d+')

    # 所有的规则解析都要放在这个rules里面，可以放多个Rule(规则解析器)
    rules = (
        # 三个参数 一个类的实例化，将link作用到了Rule构造方法的参数1中
        # 作用:用于解析页面源码数据的，里面有回调函数callback
        # Rule可以对链接发送请求有几个链接发几次请求
        # 对链接发起请求，可以执行回调
        Rule(link_detail, callback='parse_detail', follow=False),
        # Rule(link, callback='parse_item', follow=True),

    )


    def parse_item(self, response):
        # 如果打印response的话就是响应的链接
        # 如果对response进行.xpath解析的话就是响应的html源码数据
        # 此时的response就是页面源码对应的数据，同时还包括了链接
        # <200 http://wz.sun0769.com/political/index/politicsNewest?id=1&page=4>

        li_list = response.xpath('/html/body/div[2]/div[3]/ul[2]/li')
        for li in li_list:

            # !!!!xpath中不能出现tbody标签会为空 将tbody标签改成/就好
            num = li.xpath('./span[1]/text()').extract_first()
            title = li.xpath('./span[3]/a/text()').extract_first()
            item = SuncrawlproItem()
            item['title'] = title
            item['num'] = num

            yield item

    def parse_detail(self,response):
        content = response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/pre/text()').extract_first()
        num = response.xpath('/html/body/div[3]/div[2]/div[2]/div[1]/span[4]/text()').extract_first().split(':')[-1]
        item = Detail_item()
        item['content'] = content
        item['num'] = num
        print(num)


        yield item


