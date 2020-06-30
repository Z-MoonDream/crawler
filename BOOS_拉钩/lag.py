# -*- coding: utf-8 -*-
import requests
import time
from fake_useragent import UserAgent
from lxml import etree
import pandas as pd
headers = {
    'User-Agent': UserAgent().random,
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'origin':'https://www.lagou.com',
    'Referer':f'https://www.lagou.com/jobs/list_{"爬虫".encode("utf-8")}/p-city_2?gj=3{"年及以下".encode("utf-8")}',

}

class Lg:
    def __init__(self):
        self.etree = etree
        self.session = requests.Session()
        self.session.get(url=f'https://www.lagou.com/jobs/list_爬虫/p-city_2?gj=3年及以下',headers=headers,timeout=3)
        self.cookies = self.session.cookies
        self.data_list = []
    def yield_url(self):
        url = 'https://www.lagou.com/jobs/positionAjax.json?gj=3年及以下&city=北京&needAddtionalResult=false'
        return url

    def get_data(self,url,data):

        response = requests.post(url,data=data,headers=headers,cookies=self.cookies).json()
        return response

    def parser(self,data):
        for i in data['content']['positionResult']['result']:
            data_list = {
                '职位名': '',
                '公司名': '',
                '薪资': '',
                '发布日期': '',
                '工作时间/学历': '',
                '地点': '',
                '技术栈': '',
                '详情页': '',
            }
            data_list['职位名'] = i['positionName']
            data_list['公司名'] = i['companyShortName']
            data_list['薪资'] = i['salary']
            data_list['发布日期'] = i['createTime']
            data_list['工作时间/学历'] = i['workYear']+'/'+i['education']
            data_list['地点'] = '北京' + '·' + i['district']
            data_list['技术栈'] = '/'.join(i['positionLables'])
            data_list['详情页'] = 'https://www.lagou.com/jobs/' + str(i['positionId']) + '.html'
            self.data_list.append(data_list.copy())


    def save(self):

        data_list = sorted(self.data_list,key=lambda x:x['发布日期'])
        df = pd.DataFrame(data_list)
        df.to_csv('爬虫职位_拉钩.csv',encoding='utf-8')

    def main(self):
        for i in range(1,5):
            data = {
                'first':'false',
                'pn':i,
                'kd':'爬虫',
            }
            response = self.get_data(self.yield_url(),data)
            self.parser(response)
        self.save()
lag = Lg()
lag.main()




