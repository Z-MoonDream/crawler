import requests
from json import loads

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36',
}


# pageIndex是 1 pageSize是 10 的话 爬取的是第一页的数据

url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'

data={
    'cname':"",
    "pid":"",
    "keyword":"北京",
    "pageIndex":"1",
    "pageSize":"10",
}

response = requests.post(url=url,headers=headers,data=data)
print(response)
print(response.headers)
print(response.headers)
# print(response.json()["Table1"])
# print(loads(response.content)['Table1'])


# for index in response.json()["Table1"]:
#     print(index['storeName']+'餐厅',index['addressDetail'])


# pageSize 控制多少数据，第一页就10个数据
# pageIndex 1 pageSize 70爬取的是第一页的70个数据,居然没报错??
# 前台设置渲染了？倒是方便了爬虫爬数据，按理说应该爬不到的
# 以为一页就显示10个数据啊，所以我们按正常流程走
# 循环改变data(数据)字典的pageIndex(控制页数的参数)

# url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
# for page in range(1,9):
#
#     data={
#         'cname':"",
#         "pid":"",
#         "keyword":"北京",
#         "pageIndex":str(page),
#         "pageSize":"10",
#     }
#
#     response = requests.post(url=url,headers=headers,data=data)
#
#     for index in response.json()["Table1"]:
#         print(index['storeName']+'餐厅',index['addressDetail'])