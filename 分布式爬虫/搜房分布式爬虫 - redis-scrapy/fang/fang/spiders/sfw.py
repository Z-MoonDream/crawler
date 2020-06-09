# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy_redis.spiders import RedisSpider

from fang.items import NewHouseItem,EsfHouseItem


class SfwSpider(RedisSpider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    # start_urls = ['https://www.fang.com/SoufunFamily.htm']
    redis_key = 'sfw:start_url'

    # 获取所有城市的省份名称二手房url新房url
    def parse(self, response):
        trs = response.xpath('//div[@id="c02"]//tr')
        province = None
        for tr in trs:
            # 第一个是省
            # 第二个是城市
            tds = tr.xpath('.//td[not(@class)]')
            # 获取省文本，可能有会空的情况
            province_text = tds[0].xpath('.//text()').extract_first()
            # 将空白字符替换为空
            province_text = re.sub(r'\s','',province_text)
            # 如果有值说明有省份，如果没有值那么就用上一次的省份(为空说明属于上一次的省)
            if province_text:
                province = province_text
            # 不爬取海外城市房源
            if province =='其它':
                continue
            city_list = tds[1].xpath('.//a')
            for city in city_list:
                city_name = city.xpath('./text()').extract_first()
                city_link = city.xpath('./@href').extract_first()
                # 构建新房url
                city_link_new = city_link.replace('fang.com','newhouse.fang.com/house/s')
                # 构建二手房url
                city_link_esf = city_link.replace('fang.com','esf.fang.com')
                # 发起请求callback是执行回调函数，meta用来请求传参，将本次的信息传递给回调函数中
                yield scrapy.Request(url=city_link_new,callback=self.parse_newhouse,meta={'info':[province,city_name]})
                yield scrapy.Request(url=city_link_esf, callback=self.parse_esfhouse,meta={'info': [province, city_name]})


    # 解析新房页面
    def parse_newhouse(self,response):
        province,city_name = response.meta['info']
        li_list = response.xpath('//div[@id="newhouse_loupai_list"]//li[not(@style)]')
        for li in li_list:
            try:
                house_name = li.xpath('.//div[@class="nlcd_name"]/a/text()').extract_first().strip()
            except AttributeError:
                house_name = ''
            rooms_area_list = li.xpath('.//div[contains(@class,"house_type")]//text()').extract()
            # 将空白字符用正则去掉后进行拼接操作，结果为 1居/2居/3居－35~179平米.....
            # 因为后面要大量使用这个map函数，所以可以封装一个函数，优化点
            rooms_area = ''.join(list(map(lambda x:re.sub(r'\s','',x),rooms_area_list)))
            # 如果不是居室情况就改成[]
            if '居' not in rooms_area:
                rooms_area=[]
            else:
                # 格式变得更好看
                rooms_area = rooms_area.replace(r'－','/总面积:')
            address = li.xpath('.//div[@class="address"]/a/@title').extract_first()
            try:
                district = li.xpath('.//div[@class="address"]/a//text()').extract()
                # 里面是字符串形式的列表列表中是行政区 [怀来] [门头沟] XXX
                district =list(map(lambda x: re.sub(r'\s', '', x), district))[1][1:-1]
            except IndexError:
                district = ''
            sale = li.xpath('.//div[@class="fangyuan"]/span/text()').extract_first()
            price = li.xpath('.//div[@class="nhouse_price"]//text()').extract()
            price = ''.join(list(map(lambda x: re.sub(r'\s', '', x), price)))
            # response.urljoin是将缺失的url拼接完整
            # //feicuigongyuan.fang.com/ 自动拼接成https://feicuigongyuan.fang.com/ 如果完整就不会做操作
            house_link_url = response.urljoin(li.xpath('.//div[@class="nlcd_name"]/a/@href').extract_first())
            phone = li.xpath('.//div[@class="tel"]/p/text()').extract_first()
            item = NewHouseItem(province=province,city_name=city_name,house_name=house_name,price=price,rooms_area=rooms_area,address=address,district=district,sale=sale,house_link_url=house_link_url,phone=phone)
            yield item
        # 获取下一页的url
        # 爬取到最后5页的时候next就会变成上一页的url，可优化!
        next_url = response.urljoin(response.xpath('.//div[@class="page"]//a[@class="next"]/@href').extract_first())
        # 分页爬取
        yield scrapy.Request(url=next_url,callback=self.parse_newhouse,meta={'info': [province,city_name]})

    # 解析二手房页面
    def parse_esfhouse(self,response):
        # print(response.url)
        province,city_name = response.meta['info']
        dl_list = response.xpath('//div[@class="shop_list shop_list_4"]/dl[not(@dataflag="bgcomare")]')
        for dl in dl_list:
            house_name = dl.xpath('.//p[@class="add_shop"]/a/@title').extract_first()
            address = dl.xpath('.//p[@class="add_shop"]/span/text()').extract_first()
            try:
                price = dl.xpath('.//dd[@class="price_right"]/span[1]//text()').extract()
                price = price[1] + price[2]
            except IndexError:
                price = ''
            # price = price[1]+price[2]
            try:
                unit = dl.xpath('.//dd[@class="price_right"]/span[2]/text()').extract_first().strip()
            except AttributeError:
                unit = ''
            house_link_url = response.urljoin(dl.xpath('.//h4[@class="clearfix"]/a/@href').extract_first())
            infos = dl.xpath('.//p[@class="tel_shop"]/text()').extract()
            try:
                infos = list(map(lambda x:re.sub(r'\s','',x),infos))
                # 去除掉不和规矩的少数数据
                if '厅' not in infos[0] or len(infos) !=7:
                    continue
                for info in infos:
                    if '厅' in info:
                        rooms = info
                    elif '层' in  info:
                        floor = info
                    elif '向' in info:
                        orientation = info
                    elif '㎡' in info:
                        area = info
                    elif '建' in info:
                        year = info
                item = EsfHouseItem(province=province,city_name=city_name,house_name=house_name,address=address,price=price,unit=unit,rooms=rooms,floor=floor,area=area,year=year,orientation=orientation,house_link_url=house_link_url)
                yield item
            except (IndexError,UnboundLocalError) :
                continue
        # 分页爬取
        next_url = response.urljoin(response.xpath('.//div[@class="page_al"]/p[1]/a/@href').extract_first())
        # print(next_url)
        yield scrapy.Request(url=next_url,callback=self.parse_esfhouse,meta={'info':[province,city_name]})







