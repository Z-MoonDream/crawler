# -*- coding: utf-8 -*-
import requests
from lxml import etree
import random
import time
from fake_useragent import UserAgent
import pymysql
from multiprocessing.dummy import Pool
from multiprocessing import Lock
headers = {
    'User-Agent': str(UserAgent().random),
    'Host': 'search.51job.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',

}

# 获取请求url
def produce(item, page):
    '''

    :param item:查询职位
    :param page:查询页数
    :return:url列表

    '''

    start_url_before = f'https://search.51job.com/list/000000,000000,0000,00,9,99,{item},2,'
    start_url_after = '.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='

    url_list = list((start_url_before + str(i) + start_url_after for i in range(70, page + 1)))
    return url_list

# 解析数据
def get_request(url):

    message_data_list=[]
    try:
        response = requests.get(url=url,headers=headers,timeout=0.5).content.decode('gb2312', 'ignore').encode('gb2312')
    except Exception:
        return
    html = etree.HTML(response)
    try:
        div_list = html.xpath('//*[@id="resultList"]/div')[3:]
    except Exception:
        return
    for div in div_list:
        message_data = {}
        try :
            position = div.xpath('./p/span/a/@title')[0]
            company = div.xpath('./span[1]/a/@title')[0]
            site = div.xpath('./span[2]/text()')[0]
            pay = div.xpath('./span[3]/text()')[0]
            time_ = div.xpath('./span[4]/text()')[0]
            position_url = div.xpath('./p/span/a/@href')[0]
            company_url = div.xpath('./span[1]/a/@href')[0]
            time.sleep(0.8)
            try :
                res_pos = requests.get(url=position_url,headers=headers,timeout=0.5).content.decode('gb2312', 'ignore').encode('gb2312')
            except Exception:
                continue
            pos_htm = etree.HTML(res_pos)
            message_list = pos_htm.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/@title')[0].replace('|','').strip().split()
            for i in message_list:
                if '经验' in i:
                    experience = i
                if '本科' in i or '专科' in i or '大专' in i:
                    education = i

                if '招' in i or '人' in i:
                    demand = i
            message_data['position']=position
            message_data['company']=company
            message_data['site']=site
            message_data['pay']=pay
            message_data['time_']=time_+'发布'
            message_data['experience']=experience
            message_data['education']=education
            message_data['demand']=demand
            message_data['position_url']=position_url
            message_data['company_url']=company_url
            message_data_list.append(message_data)

        except IndexError as e:
            continue
        except UnboundLocalError as e:
            continue
    return message_data_list

# 持久化存储
def persistence(list_data):
    try :

        for i in list_data:
            lock.acquire()
            sql = 'insert into message_data(职位,公司名称,公司地点,薪资,发布时间,工作经验,学历,需求,前程无忧网址,公司网址) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            try:
                cursor.execute(sql,[i['position'],i['company'],i['site'],i['pay'],i['time_'],i['experience'],i['education'],i['demand'],i['position_url'],i['company_url']])
                conn.commit()
            except Exception as e:
                return
            lock.release()
    except TypeError:
        return

if __name__ == '__main__':
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="", database="前程无忧",charset="utf8")
    cursor = conn.cursor()
    lock = Lock()
    pool = Pool(30)
    # map(回调函数，参数])
    # 这个参数必须是一个列表，里面中有很多个参数，这样才能执行并发
    # 也就是执行了回调(参数),如果你的参数要是多个的话那么就把参数定义为一个[参数1，参数2]
    # map(回调函数,[[参数1,参数2],[参数1,参数2]] 这样是并发执行两次回调函数,如果函数有返回值，那么返回值将存入列表中最终一起返回
    # 比如 ：
    # def get_html(proxies):
    # return proxies 
    # bb = pool.map(get_html,[[1,2],2,3,4]) 
    # print(bb) [[1, 2], 2, 3, 4]
    list_data = pool.map(get_request,produce('大数据',500))
    pool.map(persistence,list_data)
    cursor.close()
    conn.close()

