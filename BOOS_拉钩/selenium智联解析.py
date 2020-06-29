import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import pandas as pd
import re
import requests
from fake_useragent import UserAgent
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

    def get_html_selenium(self, url):
        self.browser.get(url)
        html = self.browser.get_cookies()
        print(html)

        return html

    def main(self):
        self.get_html_selenium('https://jobs.zhaopin.com/CC152362529J00038850912.htm')


zhilian = Zlian()
zhilian.main()

# html = self.browser.get_cookies() == a
a = [{'domain': '.zhaopin.com', 'expiry': 1624967083, 'httpOnly': False, 'name': 'jobRiskWarning', 'path': '/', 'secure': False, 'value': 'true'}, {'domain': '.zhaopin.com', 'httpOnly': False, 'name': 'sts_chnlsid', 'path': '/', 'secure': False, 'value': 'Unknown'}, {'domain': '.zhaopin.com', 'expiry': 1593432881, 'httpOnly': False, 'name': 'sts_sid', 'path': '/', 'secure': False, 'value': '172ffe4c3da68-02314626ca1ec7-4353760-2073600-172ffe4c3dbb71'}, {'domain': '.zhaopin.com', 'expiry': 1593432881, 'httpOnly': False, 'name': 'sts_evtseq', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.zhaopin.com', 'expiry': 1608983078, 'httpOnly': False, 'name': 'ssxmod_itna', 'path': '/', 'secure': False, 'value': 'QqmhAK8KD5YKitDXDnBmUqCi5tDQDy00l1rGx0HIeGzDAxn40iDtoPTa3rlhl2YWfqsKGxbXaDVm4omIhYAWoNoDU4i8DCLGeKbDeW=D5xGoDPxDeDADYo6DAqiOD7k=DEDmb8DYxGAnKqDgDYQDGMPjD7QDId=DjOGNbuNjeWtPhkDVC0hnD0tKxBLqe1bq56nNRdp2DB=HxBQSmd6yWeDHBh+WYG4o/GvXKAH5425YYxYo+++5o3wG1G+Ab/hN/Z+GpKDAnKqxD==='}, {'domain': '.zhaopin.com', 'httpOnly': False, 'name': 'sts_sg', 'path': '/', 'secure': False, 'value': '1'}, {'domain': 'jobs.zhaopin.com', 'expiry': 1596109479.65857, 'httpOnly': True, 'name': 'acw_tc', 'path': '/', 'secure': False, 'value': 'ac11000115934310787114061e010f49bf443d2b07e81e09557e3da4eed53c'}, {'domain': 'jobs.zhaopin.com', 'expiry': 1593434679.264268, 'httpOnly': False, 'name': 'acw_sc__v2', 'path': '/', 'secure': False, 'value': '5ef9d4263e33992422dfd3148edb4294e4d6bfb3'}, {'domain': '.zhaopin.com', 'expiry': 7900631080, 'httpOnly': False, 'name': 'sensorsdata2015jssdkcross', 'path': '/', 'secure': False, 'value': '%7B%22distinct_id%22%3A%22172ffe4beef329-07a447625d85d4-4353760-2073600-172ffe4bef078c%22%2C%22%24device_id%22%3A%22172ffe4beef329-07a447625d85d4-4353760-2073600-172ffe4bef078c%22%2C%22props%22%3A%7B%7D%7D'}, {'domain': '.zhaopin.com', 'httpOnly': False, 'name': 'ZL_REPORT_GLOBAL', 'path': '/', 'secure': False, 'value': '{%22jobs%22:{%22recommandActionidShare%22:%2217e6b3de-835c-416f-85de-59a31fd6e7ad-job%22}}'}, {'domain': '.zhaopin.com', 'httpOnly': False, 'name': 'zp_src_url', 'path': '/', 'secure': False, 'value': 'https%3A%2F%2Fjobs.zhaopin.com%2FCC152362529J00038850912.htm'}, {'domain': '.zhaopin.com', 'expiry': 1593446399, 'httpOnly': False, 'name': 'sajssdk_2015_cross_new_user', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.zhaopin.com', 'expiry': 1908791080, 'httpOnly': False, 'name': 'sts_deviceid', 'path': '/', 'secure': False, 'value': '172ffe4bee3333-0445facc2d2a6-4353760-2073600-172ffe4bee43a3'}, {'domain': '.zhaopin.com', 'expiry': 1608983078, 'httpOnly': False, 'name': 'ssxmod_itna2', 'path': '/', 'secure': False, 'value': 'QqmhAK8KD5YKitDXDnBmUqCi5tDQDy00l1rDnK3c25DshD90Dj4xo=M5307XDLxijN4D'}, {'domain': 'jobs.zhaopin.com', 'expiry': 1593432879.280918, 'httpOnly': False, 'name': 'acw_sc__v3', 'path': '/', 'secure': False, 'value': '5ef9d427f5cd20897049d31746c431efc49b546a'}, {'domain': '.zhaopin.com', 'expiry': 4747031079.401981, 'httpOnly': False, 'name': 'x-zp-client-id', 'path': '/', 'secure': False, 'value': 'a0ad3f46-72eb-4233-8609-dcd42a553e59'}]

for i in a:
    print(i['name'],i['value'])