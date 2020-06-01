import requests
from bs4 import BeautifulSoup
import openpyxl
headers={'origin':'https://movie.douban.com/top250?start=',
         'referer':'https://www.douban.com/group/beijingzufang/',
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
list_all=[]

# https://www.douban.com/group/beijingzufang/discussion?start=0 这是第一页
# https://www.douban.com/group/beijingzufang/discussion?start=25 这是第二页  可以看出浏览器是通过最后的start+25来实现翻页的
# 模拟翻页
for j in [f"https://www.douban.com/group/beijingzufang/discussion?start={i}" for i in range(0,125,25)]:
    res = requests.get(j, headers=headers)
    bs = BeautifulSoup(res.text, 'html.parser')
    list = bs.find_all('td', class_='title')
    for i in list:
        tag= i.find('a')
        name = tag['title']
        URL = tag['href']
        list_all.append([name,URL])
web=openpyxl.Workbook()
sheet = web.active
sheet.title = '租房信息'
for i in list_all:
   sheet.append(i)
web.save(r'C:\Users\1\Desktop\豆瓣租房信息.xlsx')