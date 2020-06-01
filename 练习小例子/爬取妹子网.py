# 练习代码



# coding=utf-8

import requests
from bs4 import BeautifulSoup
import pickle
#
# url = 'http://www.mzitu.com/26685'
# header = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
#                   '(KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36',
#     'Referer':'https://www.mzitu.com/'
# }
# # 反爬机制1：Refer
# # 图片网站有反爬机制，是识别爬虫的"Refer”字段，这个字段是用来判断请求的来源
# # 也就是通过headr来判断的，所以我们要模拟正常从主页进入，要在hearder中加入"Referer"键，值为主页网址
# #
#
#
# html = requests.get(url, headers=header)
# soup = BeautifulSoup(html.text, 'html.parser')
# # print(html.text)
# #
# # # # 最大页数在span标签中的第10个
# pic_max = soup.find_all('span')[9].text
# # print(pic_max)
# title = soup.find('h2',class_='main-title').text
# #
# # # # 输出每个图片页面的地址
# for i in range(1, int(pic_max) + 1):
#     href = url + '/' + str(i)
#     html = requests.get(href, headers=header)
#     mess = BeautifulSoup(html.text, "html.parser")
#     #虽然html.text也可以显示源码，但是BeautifulSoup(html.text，"html.parser")更快，文档容错能力强
#
#     pic_url = mess.find('img',alt = title) #获取img标签，其中包含图片地址
#
#     html = requests.get(pic_url['src'],headers = header)
#     file_name = pic_url['src'].split(r'/')[-1]
#     print(file_name)
    # # print(html.content)
    # f = open(f"E:\plus_len\练习\爬虫\{file_name}", 'wb')
    # f.write(html.content)
    # f.close()

# 完整代码


# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import time

all_url = 'https://www.mzitu.com'

# http请求头
Hostreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'https://www.mzitu.com/'
}
# 此请求头Referer破解盗图链接
# Picreferer = {
#     'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
#     'Referer': 'http://i.meizitu.net'
# }

Picreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'https://www.mzitu.com/'
}

# 对mzitu主页all_url发起请求，将返回的HTML数据保存，便于解析
start_html = requests.get(all_url, headers=Hostreferer)

# Linux保存地址
# path = '/home/Nick/Desktop/mzitu/'

# Windows保存地址
path = r'E:\plus_len\练习\爬虫\资源放置\\' #要在后面加上\\来表示在资源放置中，而不是与资源放置目录同级
# E:\plus_len\练习\爬虫\资源放置 +标题名   创建
# E:\plus_len\练习\爬虫\资源放置\标题名    创建

# 获取最大页数
soup = BeautifulSoup(start_html.text, "html.parser")
page = soup.find_all('a', class_='page-numbers')
print(page)
max_page = page[-2].text #-1是下一页


# same_url = 'http://www.mzitu.com/page/'   # 主页默认最新图片
# 获取每一类MM的网址
same_url = 'https://www.mzitu.com/mm/page/'  # 也可以指定《qingchun MM系列》

for n in range(1, int(max_page) + 1):
# for n in range(1,2):
    # 拼接当前类MM的所有url

    # 修改?拼接转换页
    ul = same_url + str(n)


# #
#     # 分别对当前类每一页第一层url发起请求
#
#     # 修改?分别对当前页url发起请求
    start_html = requests.get(ul, headers=Hostreferer)


#
# #     # 提取所有MM的标题
    soup = BeautifulSoup(start_html.text, "html.parser")
    all_a = soup.find('div', class_='postlist').find_all('a', target='_blank')
    print(all_a)
# #
#     # 遍历所有MM的标题
    for a in all_a:
        # 提取标题文本，作为文件夹名称

        title = a.get_text()
        # print(a)
        # print(a.get_text())
        #  有问题点 具体分析吧
        # 问题点:get_text如果返回了相同的文字的话，就会用后面的覆盖前面相同的
        # 最终结果就是一串文字而不是相同的几串

        if (title != ''):
            # print(path)
            print("准备扒取：" + title)

#
#             # windows不能创建带？的目录，添加判断逻辑
#             if (os.path.exists(path + title.strip().replace('?', ''))):
            if (os.path.exists(path + title.strip())):

                print('目录已存在')
                flag = 1
            else:
                # os.makedirs(path + title.strip().replace('?', ''))
                os.makedirs(path + title.strip())

                flag = 0

#             # 切换到上一步创建的目录

              # 切换到刚刚创建的目录中要加入图片了
#             os.chdir(path + title.strip().replace('?', ''))
            os.chdir(path + title.strip())


#
            # 提取第一层每一个MM的url，并发起请求
            href = a['href']


            html = requests.get(href, headers=Hostreferer)
            mess = BeautifulSoup(html.text, "html.parser")
#
#             # 获取第二层最大页数

              # 进入图片网址的那一层，里层
            pic_max = mess.find_all('span')
            pic_max = pic_max[9].text
            # print(pic_max)
            if (flag == 1 and len(os.listdir(path + title.strip().replace('?', ''))) >= int(pic_max)):
                # 必须满足文件目录存在并且文件目录中的图片全部下载完毕才可以跳过，虽然文件中有图片，但是
                # 没有下载完的话要从头下载进行现在的数据对之前没下载完的数据进行覆盖，虽然影响效率
                # 但是确保准确性，有待提升(从已经下载的数据后面在下载，相当于追加下载)

                print('已经保存完毕，跳过')
                continue
#
            # 遍历第二层每张图片的url

            # 如果没有下载完则执行这里

            for num in range(1, int(pic_max) + 1):
                # 拼接每张图片的url
                pic = href + '/' + str(num)

#                 # 发起请求
                html = requests.get(pic, headers=Hostreferer)
                mess = BeautifulSoup(html.text, "html.parser")
                pic_url = mess.find('img', alt=title)
                print(pic_url['src'])
                # print(pic_url)
                html = requests.get(pic_url['src'], headers=Picreferer)

#
#                 # 提取图片名字
                file_name = pic_url['src'].split(r'/')[-1]
                # split将字符串https://i3.mmzztt.com/2020/03/09a01.jpg转换成列表
#
#                 # 保存图片
                f = open(file_name, 'wb')
                f.write(html.content)
                f.close()
                # time.sleep(0.7)

            print('完成')

    print('第', n, '页完成')

