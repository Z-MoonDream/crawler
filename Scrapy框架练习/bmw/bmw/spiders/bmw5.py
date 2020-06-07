# -*- coding: utf-8 -*-
import scrapy
from bmw.items import BmwItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

# class Bmw5Spider(scrapy.Spider):
class Bmw5Spider(CrawlSpider):

    name = 'bmw5'
    allowed_domains = ['car.autohome.com.cn']
    # start_urls = ['https://car.autohome.com.cn/pic/series/202.html']
    start_urls = ['https://car.autohome.com.cn/pic/series/202-10.html#pvareaid=2042222']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'bmw.middlewares.ProcessAllExceptionMiddleware': 120,
        },
        'DOWNLOAD_DELAY': 1,  # 延时最低为2s
        'AUTOTHROTTLE_ENABLED': True,  # 启动[自动限速]
        'AUTOTHROTTLE_DEBUG': True,  # 开启[自动限速]的debug
        'AUTOTHROTTLE_MAX_DELAY': 10,  # 设置最大下载延时
        'DOWNLOAD_TIMEOUT': 15,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8  # 限制对该网站的并发请求数
    }


    rules = (
        Rule(LinkExtractor(allow=r'https://car.autohome.com.cn/pic/series/202-.+'),callback='parse_page',follow=True),)# 找到每个符合要求的链接(页码链接) 对页码发送回调函数parse_page，解析出对应html中需要的信息

    def parse_page(self, response): # 用了crawlspider的话就不能重写parse方法了
        title = response.xpath('//div[@class="uibox"]/div/text()').extract()[0]
        # href 是引用 多用于 css 文档文件或者a链接超文本 link
        # src是引入 多用于图片 js iframe
        # div中class="uibox-con carpic-list03 border-b-solid" 是由多个空格分隔的，所以我们要用这个 至于为什么只用uibox-con,是因为carpic-list03 border-b-solid是样式，我们不用class是样式的
        url_list = response.xpath('//div[contains(@class,"uibox-con")]//img/@src').extract()
        # 这下面的图片要改成2024....才可以正常访问
        if '202-51' in response.url:
            url_list = list(map(lambda url: response.urljoin(url.replace("autohomecar", "1024x0_1_q95_autohomecar")), url_list))
        url_list = list(map(lambda url:response.urljoin(url.replace("240x180_0_q95_c42_","")),url_list))
        item = BmwItem(title=title, image_urls=url_list)
        yield item


    # def old_code(self,response):
    #     div_list = response.xpath('//div[@class="uibox"]')[1:]
    #     for div in div_list:
    #         title = div.xpath('./div[1]/a/text()').extract_first()
    #         # li_list = div.xpath('./div[2]//li')[:-1]
    #         # for img in li_list:
    #         #     # img_url = 'https:' + img.xpath('./a/img/@src').extract_first()
    #         #     img_url = response.urljoin(img.xpath('./a/img/@src').extract_first()) # 会自动的将缺少的添加上与上面的功能相同
    #
    #         # 进阶写法
    #         img_url_list = div.xpath('.//img/@src').extract()
    #         img_url_list = list(map(lambda url: response.urljoin(url), img_url_list))
    #         # item=BmwItem()
    #         # item['title'] = title
    #         # item['img_url_list'] = img_url_list
    #
            # item = BmwItem(title=title, image_urls=img_url_list)
            # yield item




