# -*- coding: utf-8 -*-
import requests
from lxml import etree
from time import sleep
import pymysql
conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='',db='爬虫招聘信息',charset='utf8')
cursor = conn.cursor()

headers =  {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36',

     'Cookie':'Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1587551222,1587781653,1587787385,1588149888; __a=50115059.1587810474.1587810474.1588149888.18.2.3.18; __zp_stoken__=492bn9ad7SOKeedmxYzdRpSegOUO0clNQZJq%2F%2FKT1XsKAxz4wL%2BNFNck1kjgvXMCOooPjlCjZqicb2DYQsLNT9Dt0oot%2F8FZasMwdBJX3D6Vof%2BzpDUitFWSWRoXhd6AJDd3'
}
response = requests.get(url=url,headers=headers)

# main_url = 'https://www.zhipin.com/?ka=header-home'
# session = requests.Session()
# session.get(main_url,headers=headers)
#
# response = session.get(url=url,headers=headers)

for page in range(1,4):
    url = 'https://www.zhipin.com/c100010000/?query=python%E7%88%AC%E8%99%AB%E5%B7%A5%E7%A8%8B%E5%B8%88&page={i}&ka=page-{i}'

    response = requests.get(url=url,headers=headers)
    sleep(2)

    page_text = response.text

    tree = etree.HTML(page_text)

    li_list = tree.xpath('//*[@id="main"]/div/div[2]/ul/li')
    for li in li_list:
        # 技术栈
        skill = li.xpath('./div/div[2]/div[1]//text()')
        skill_new = skill
        for index in skill_new:
            if '\n' in index:
                skill_new.remove(index)
        skill_new = '/'.join(skill_new)
        region = li.xpath('./div/div[1]/div[1]/div[1]/div[1]//span[@class="job-area"]/text()')
        # 职位
        # position = li.xpath('./div/div[1]/div[1]/div[1]/div[1]//span[@class="job-name"]/a/text()')
        # print(position)
        # 地区
        area = li.xpath('././div/div[1]/div[1]/div[1]/div[1]//span[@class="job-area"]/text()')[0]
        # 薪资
        pay = li.xpath('.//div[@class="job-limit clearfix"]/span/text()')[0]
        # 工作时间，学历
        education_time = '/'.join(li.xpath('.//div[@class="job-limit clearfix"]/p/text()'))
        # 详情页
        position_url = 'https://www.zhipin.com/'+li.xpath('.//div[@class="job-title"]/span[1]/a/@href')[0]
        sql = 'insert into BOOS_data(skill,position_url,pay,area,education_time) values(%s,%s,%s,%s,%s)'
        try:
            # cursor.execute(sql,[skill_new,position_url,pay,area,education_time])
            cursor.execute(sql, [skill_new,position_url,pay,area,education_time])
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
cursor.close()
conn.close()












