# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from lxml import etree
import os
import json
import pandas as pd


class Boos:

    def __init__(self, city='北京', position='爬虫', age_limit='1-3年'):

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # executable_path:你的内核地址 options:是你的隐藏自动化方式之一 chrome_options:是无头浏览器打开
        # 无头浏览器打开会被检测出来，待解决

        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
        self.browser = webdriver.Chrome(executable_path=self.path+'/conf/chromedriver.exe', options=options)
        script = ''' Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) '''
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        self.etree = etree
        self.city = city
        self.position = position
        self.age_limit = age_limit
        self.data_list = []


    def yield_url(self, num):
        # e_104:工作经验：1-3年
        # e_103：工作经验：1年以内
        # e_102：工作经验：应届生
        # e_108：工作经验：在校生
        # period:5是1个月以内 4是15天以内
        # 北京：c101010100
        # 杭州：c101210100

        if self.city == '北京':
            self.city = 'c101010100'
        else:
            self.city = 'c101210100'
        if self.age_limit == '1-3年':
            self.age_limit = 'e_104'
        else:
            self.age_limit = 'e_108'


        url_list = (f'https://www.zhipin.com/{self.city}/{self.age_limit}/?query={self.position}&period=5&page={i}' for
                    i in range(1, num + 1))
        return url_list

    def get_html(self, url):
        self.browser.get(url)
        html = self.browser.page_source

        return html

    def parse(self, html):
        tree = self.etree.HTML(html)
        li_list = tree.xpath('//*[@id="main"]/div/div[2]/ul/li')
        for li in li_list:
            data = {
                '职位名': '',
                '公司名': '',
                '薪资': '',
                '发布日期': '',
                '工作时间/学历': '',
                '地点': '',
                '技术栈': '',
                '详情页': '',
            }
            data['职位名'] = li.xpath('.//div[@class="job-title"]/span[@class="job-name"]/a/text()')[0]
            data['公司名'] = li.xpath('.//div[@class="company-text"]/h3/a/text()')[0]

            # cookie过期后，登录失效，导致不显示日期，要重新登陆
            try:
                data['发布日期'] = li.xpath('.//div[@class="job-title"]/span[@class="job-pub-time"]//text()')[0]
            except IndexError:
                self.browser.get('https://login.zhipin.com/?ka=header-login')
                input('请登录BOOS平台后按回车继续：')
                cookies = self.browser.get_cookies()
                with open(self.path + '/cookie/BOOS_cookies.json', 'w') as f:
                    f.write(json.dumps(cookies))
                self.main()

            # 技术栈
            skill = li.xpath('./div/div[2]/div[1]//text()')
            skill_new = skill
            for index in skill_new:
                if '\n' in index:
                    skill_new.remove(index)
            skill_new = '/'.join(skill_new)
            data['技术栈'] = skill_new
            data['地点'] = li.xpath('./div/div[1]/div[1]/div[1]/div[1]//span[@class="job-area"]/text()')[0]
            # 薪资
            data['薪资'] = li.xpath('.//div[@class="job-limit clearfix"]/span/text()')[0]
            # 工作时间，学历
            data['工作时间/学历'] = '/'.join(li.xpath('.//div[@class="job-limit clearfix"]/p/text()'))
            # 详情页
            data['详情页'] = 'https://www.zhipin.com/' + li.xpath('.//div[@class="job-title"]/span[1]/a/@href')[0]
            print(f'爬取职位:{data["职位名"]}，平台：BOOS，完毕')
            self.data_list.append(data.copy())

    def save(self):

        data_list = sorted(self.data_list, key=lambda x: x['发布日期'])
        df = pd.DataFrame(data_list)
        df.to_csv(self.path+'/csv/职位_BOOS.csv', encoding='utf-8')

    def main(self):
        # 获取cookie并保存到本地
        if not os.path.exists(self.path+'/cookie/BOOS_cookies.json'):
            self.browser.get('https://login.zhipin.com/?ka=header-login')
            input('请登录BOOS平台后按回车继续：')
            cookies = self.browser.get_cookies()
            with open(self.path+'/cookie/BOOS_cookies.json', 'w') as f:
                f.write(json.dumps(cookies))
                self.browser.close()
                return
        with open(self.path+'/cookie/BOOS_cookies.json', "r") as fp:
            # 注意添加cookie的时候一定要保证页面已经出现，然后在添加cookie访问下一个页面，空域会报无法添加cookie的错误
            # 先请求页面，防止空域加载cookie抛出异常
            self.browser.get('https://www.zhipin.com/c101010100/e_104/?query=爬虫&period=5&ka=sel-city-101010100')
            cookies = json.load(fp)
            for cookie in cookies:
                self.browser.add_cookie(cookie)
        # 分页爬取
        for url in self.yield_url(8):
            html = self.get_html(url)
            time.sleep(4)
            self.parse(html)
        self.save()
        self.browser.close()
