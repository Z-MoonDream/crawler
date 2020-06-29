# -*- coding: utf-8 -*-


import requests
from lxml import etree
import time
from fake_useragent import UserAgent
import pandas as pd
headers = {
    'User-Agent': str(UserAgent().random),
    'Host': 'search.51job.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',

}
class Job:
    def __init__(self):
        self.data_list = []
        self.etree = etree

    def yield_url(self,num):
        # 注意这个010000, 这个 01控制地区01是北京00是全国
        start_url_before = f'https://search.51job.com/list/010000,000000,0000,00,9,99,爬虫,2,'
        #
        start_url_after = '.html?workyear=02'
        # 产生url列表
        url_list = list((start_url_before + str(i) + start_url_after for i in range(1, num + 1)))
        return url_list
    def get_html(self,url):
        try:
            time.sleep(0.8)
            response = requests.get(url=url, headers=headers, timeout=0.5).content.decode('gb2312', 'ignore')

            return response
        except Exception as e :
            print(e)


    # 解析数据
    def parse(self,html):
        html = self.etree.HTML(html)
        try:
            div_list = html.xpath('//*[@id="resultList"]/div')[3:]
        except Exception:
            return

        for div in div_list:
            try:
                message_data = {}
                position = div.xpath('./p/span/a/@title')[0]
                company = div.xpath('./span[1]/a/@title')[0]
                site = div.xpath('./span[2]/text()')[0]
                pay = div.xpath('./span[3]/text()')[0]
                time_ = div.xpath('./span[4]/text()')[0]
                position_url = div.xpath('./p/span/a/@href')[0]
            except IndexError:
                continue
            try:
                pos_htm = self.etree.HTML(self.get_html(position_url))
                message_list = pos_htm.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/@title')[0].replace('|',
                                                                                                                  '').strip().split()

                for i in message_list:
                    if '经验' in i:
                        experience = i
                    if '本科' in i or '专科' in i or '大专' in i:
                        education = i
                message_data['职位名'] = position
                message_data['公司名'] = company
                message_data['地点'] = site
                message_data['薪资'] = pay
                message_data['发布日期'] = '发布于' + time_
                message_data['工作时间/学历'] = experience + '/' + education
                message_data['详情页'] = position_url

                self.data_list.append(message_data.copy())
            except (Exception,IndexError,TypeError) as e :
                print(e)
                continue
    def save(self):
        data_list = sorted(self.data_list,key=lambda x:x['发布日期'])
        df = pd.DataFrame(data_list)
        columns = ['职位名','公司名','薪资','发布日期','工作时间/学历','地点','详情页']
        df.to_csv('爬虫职位_51job.csv',columns=columns,encoding='utf-8',index=False)






    def main(self):

        for i in self.yield_url(1):
            self.parse(self.get_html(i))
        self.save()






jb = Job()
jb.main()
