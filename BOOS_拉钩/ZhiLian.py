# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import pandas as pd
import re
import requests
from fake_useragent import UserAgent

headers = {
    'User-Agent': UserAgent().random
}


class Zlian:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.browser = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
        script = ''' Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) '''
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        self.etree = etree
        self.data_list = []

    def yield_url(self, num):
        if num==1:
            return ['https://sou.zhaopin.com/?jl=530&we=0103&kw=%E7%88%AC%E8%99%AB&kt=3']
        url_list = (f'https://sou.zhaopin.com/?p={i}jl=530&we=0103&kw=%E7%88%AC%E8%99%AB&kt=3' for i in
                    range(1, num + 1))
        return url_list

    @staticmethod
    def formatting(data_list):
        return list(map(lambda x: re.sub(r'\s', '', x), data_list))

    def get_html_selenium(self, url):
        self.browser.get(url)
        input('页面加载完毕后按回车继续:')
        html = self.browser.page_source
        return html

    def get_html_requests(self, url):
        headers_ = {
            'User-Agent': UserAgent().random,
            'cookie':'acw_sc__v2=5ef9cb68005d493e0ed46ef39d4964d487f37ed9'
        }
        time.sleep(0.8)
        response = requests.get(url, headers=headers_).text
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
        for i in range(len(company)):
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
            response = self.get_html_requests(url=url[i])
            etree = self.etree.HTML(response)
            try:
                time_ = etree.xpath('//span[@class="summary-plane__time"]//text()')
                time_ = self.formatting(time_)[0]
            except IndexError as e :
                print(e,url[i],etree.xpath('//span[@class="summary-plane__time"]//text()'))
                continue
            skill = '/'.join(etree.xpath('//div[@class="describtion__skills-content"]//text()'))
            dict_['职位名'] = position[i]
            dict_['公司名'] = company[i]
            dict_['薪资'] = pay[i]
            dict_['发布日期'] =time_
            dict_['工作时间/学历'] = age[i]+edu[i]
            dict_['地点'] = site[i]
            dict_['技术栈'] = skill
            dict_['详情页'] = url[i]
            print(f'爬取{dict_["职位名"]}页面完毕')
            self.data_list.append(dict_.copy())


    def main(self):
        for i in self.yield_url(1):
            html = self.get_html_selenium(i)
            self.parser(html)
        print(self.data_list)



zhilian = Zlian()
zhilian.main()
