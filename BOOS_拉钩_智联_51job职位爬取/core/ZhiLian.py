# -*- coding: utf-8 -*-
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import pandas as pd
import re
import requests
from fake_useragent import UserAgent
import os
headers = {
    'User-Agent': UserAgent(verify_ssl=False).random
}


class Zlian:
    def __init__(self, city='北京', position='爬虫', age_limit='1-3年'):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # 无头浏览器各种BUG，还是不加了
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
        self.browser = webdriver.Chrome(executable_path=self.path+'/conf/chromedriver.exe', options=options)
        script = ''' Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) '''
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        self.etree = etree
        self.city = city
        self.position = position
        self.age_limit = age_limit
        # 去重
        self.tag = 0
        self.data_list = []

    def yield_url(self, num):
        # 杭州：653
        # 北京：530
        # 1-3年：0103
        # 实习生：0000
        if self.city == '北京':
            self.city = '530'
        else:
            self.city = '653'
        if self.age_limit == '1-3年':
            self.age_limit = '0103'
        else:
            self.age_limit = '0000'
        if num == 1:
            return [f'https://sou.zhaopin.com/?jl={self.city}&we={self.age_limit}&kw={self.position}']
        url_list = [f'https://sou.zhaopin.com/?p={i}jl={self.city}&we={self.age_limit}&kw={self.position}' for i in
                    range(1, num + 1)]

        return [f'https://sou.zhaopin.com/?jl={self.city}&we={self.age_limit}&kw={self.position}']+url_list

    @staticmethod
    def formatting(data_list):
        return list(map(lambda x: re.sub(r'\s', '', x), data_list))

    def get_html_selenium(self, url):
        self.browser.get(url)
        time.sleep(2)
        self.browser.refresh()
        time.sleep(5)
        html = self.browser.page_source
        return html

    def get_cookie(self, url):
        self.browser.get(url)
        cookies = self.browser.get_cookies()
        with open(self.path+'/cookie/acw_sc__v2.json', 'w') as f:
            f.write(json.dumps(cookies))

    def get_html_requests(self, url):
        with open(self.path+'/cookie/acw_sc__v2.json', 'r') as f:
            cookies = json.load(f)
        value = ''
        for dic in cookies:
            if dic['name'] == 'acw_sc__v2':
                value = dic['value']
                break
        headers_ = {
            'User-Agent': UserAgent().random,
            'cookie': f'acw_sc__v2={value}'
        }
        time.sleep(0.5)
        response = requests.get(url, headers=headers_, timeout=5).text
        return response

    def parser(self, html):
        etree = self.etree.HTML(html)
        company = etree.xpath('//div[contains(@class,"commpanyName")]/a/text()')
        position = etree.xpath('//div[@class="contentpile__content__wrapper clearfix"]/div/a/@title')
        pay = etree.xpath('//div[contains(@class,"jobDesc")]/p/text()')
        pay = self.formatting(pay)
        site = etree.xpath('//div[contains(@class,"jobDesc")]/ul/li[1]/text()')
        site = self.formatting(site)
        age = etree.xpath('//div[contains(@class,"jobDesc")]/ul/li[2]/text()')
        age = self.formatting(age)
        edu = etree.xpath('//div[contains(@class,"jobDesc")]/ul/li[3]/text()')
        edu = self.formatting(edu)
        url = etree.xpath('//div[contains(@class,"clearfix")]/a/@href')
        # 如果标志位与company相同说明是同一页重复加载，那么结束分页爬取
        if self.tag==company:
            return True
        else:
            self.tag = company
        for i in range(len(company)-1):
            dict_ = {
                '职位名': '',
                '公司名': '',
                '薪资': '',
                '发布日期': '',
                '工作时间/学历': '',
                '地点': '',
                '技术栈': '',
                '详情页': '',
            }
            if self.position not in position[i]:
                continue
            try:
                self.get_html_requests(url=url[i])
            except (FileNotFoundError,IndexError):

                self.get_cookie(url[i])
            response = self.get_html_requests(url=url[i])
            etree = self.etree.HTML(response)
            try:
                time_ = etree.xpath('//span[@class="summary-plane__time"]//text()')
                time_ = self.formatting(time_)[0]
            except IndexError as e:
                print(e, url[i],'请检查页面结构完善，更新维护')
                self.get_cookie(url[i])
                continue
            skill = '/'.join(etree.xpath('//div[@class="describtion__skills-content"]//text()'))

            dict_['职位名'] = position[i]
            dict_['公司名'] = company[i]
            dict_['薪资'] = pay[i]
            dict_['发布日期'] = time_
            dict_['工作时间/学历'] = age[i] + edu[i]
            dict_['地点'] = site[i]
            dict_['技术栈'] = skill
            dict_['详情页'] = url[i]
            print(f'爬取职位：{dict_["职位名"]}，平台：智联，完毕')
            self.data_list.append(dict_.copy())
        return False

    def save(self):
        data_list = sorted(self.data_list, key=lambda x: x['发布日期'])
        df = pd.DataFrame(data_list)
        df.to_csv(self.path+'/csv/职位_智联.csv', encoding='utf-8')

    def main(self):
        for i in self.yield_url(8):
            html = self.get_html_selenium(i)
            if  self.parser(html):
                break
        self.save()
        self.browser.close()
