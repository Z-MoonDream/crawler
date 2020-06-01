#  # 基础步骤解释
# #
# import requests
# from bs4 import BeautifulSoup
# import pickle
# import time
# #
# url ="http://www.win4000.com/meinv189606.html"
# header = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
#                   '(KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36',
#     'Referer':'http://www.win4000.com/'}
#
# # 最大页数在第一个em标签里面
# html = requests.get(url,headers=header)
# soup = BeautifulSoup(html.text,"html.parser")
#
#
# # 获取标题
# title = soup.find('h1').text
# print(soup.find("h1"))
#
# # 获取最大页数
# pic_max = soup.find_all("em")[0].text
# print(soup.find_all("em"))
#
#
# # 对图片的页面地址进行对应更改
# url_change =[url.split(".")[2]+f"_{i}" for i in range(1,int(pic_max)+1)]
# print(url_change)


# # 循环获取图片
# for i in url_change:
#
#     # 图片的页面地址
#     href = url.replace(url.split(".")[2],i)
#     print(href)
#     # 获取图片页面地址的html源码
#     html = requests.get(href,headers=header)
#     # 虽然html.text也可以显示源码，但是BeautifulSoup(html.text，"html.parser")更快，文档容错能力强
#     mess = BeautifulSoup(html.text,"html.parser")
#     # 获取img标签，其中包含图片地址
#     pic_url = mess.find('img',class_="pic-large")
#     # print(pic_url)
#     # print('返回标签的内容：',pic_url.text)
#     # print('返回标签的属性：',pic_url.attrs)
#     # print('返回标签内容为字符串',pic_url.string)
#     # break
#     # 获取图片地址
#     html = requests.get(pic_url["url"],headers=header)
#     # 图片名字
#     file_name = pic_url["url"].split(r"/")[-1]
#     # 将图片保存到桌面
#     with open(fr"C:\Users\1\Desktop\{file_name}","wb") as f:
#         f.write(html.content)
#         f.close()
#     # print(html)# <Response [200]>  说明你没有加.text
#     #   过快同一个ip请求会被限制，要不加时间，要不用代理ip，代理ip版本正在研究中.....
#     time.sleep(0.2)



# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import time

# cosplay图片大全主页
all_url = "http://www.win4000.com/meinvtag26.html"

# http请求头
# 加入Referer破解盗图链接
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36',
    'Referer': 'http://www.win4000.com/'}
# Referer 的值为主页，模拟浏览器从主页进入防止反爬机制

# 对图片主页发起请求，将返回的源码数据保存用于解析
start_html = requests.get(all_url, headers=header)

# 保存地址
path = "E:\Results\\"

# 获取主页最大页数
soup = BeautifulSoup(start_html.text, "html.parser")

# .text 可以直接获取文本 get_text是去掉tag标签
pic_max = soup.find_all("a", rel="nofollow")[-2].text
all_url_change = [all_url.split(".")[2] + f"_{num}" for num in range(1, int(pic_max) + 1)]
n = 1
for i in all_url_change:

    # 拼接转换页并请求
    html_ull = all_url.replace(all_url.split(".")[2], i)
    start_html = requests.get(html_ull,headers=header)

    # 将请求结果保留用作之后解析
    soup = BeautifulSoup(start_html.text, "html.parser")

    # 提取所有的MM标题
    all_a = soup.find("div", class_="list_cont Left_list_cont Left_list_cont2").find_all("a")

    for a in all_a:
        # 遍历标题文本，作为文件夹名称
        title = a.find("p").text

        if (title != ""):

            print("准备爬取: " + title)

            if (os.path.exists(path + title.strip())):

                # 如果存在则把标示位该为1
                flag = 1

            else:

                # 如果不存在该目录则创建，并且把标示位改为0
                os.makedirs(path + title.strip())

                flag = 0

            # 进去刚刚创建好了的目录中，要下载图片了
            os.chdir(path + title.strip())

            # 获取主页每个MM的url，准备进入第二层(url)获取图片
            href = a["href"]  # find_all 的attrs参数可以查看属性 a.attrs

            # 发起请求
            html = requests.get(href, headers=header)
            mess = BeautifulSoup(html.text, "html.parser")

            # 获取里层(图片url)的最大页数，比如有16页就是有16张图要下载
            img_max = mess.find_all("em")[0].text

            # 如果同时满足标示位为1也就是存在目录，并且目录下图片全部下载完则跳过
            if (flag == 1 and len(os.listdir((path + title.strip()))) >= int(img_max)):
                print(f"{title}，已保存完毕，跳过")
                continue

            # # 如果没有下载完则进行下载
            # for num in range(1, int(img_max) + 1):

                # 对图片的页面地址进行更改
            url_change = [href.split(".")[2] + f"_{i}" for i in range(1, int(img_max) + 1)]

                # 循环获取图片
                # 获取要下载的图片的地址
            for j in url_change:
                href_img = href.replace(href.split(".")[2], j)

                # 获取其源码
                html = requests.get(href_img, headers=header)

                # 准备对源码进行解析
                mess = BeautifulSoup(html.text, "html.parser")

                # 获取img标签，其中包含图片的真正地址
                pic_url = mess.find("img", class_="pic-large")
                print(pic_url["url"])

                # 对img标签页进行请求，保留源码用于解析
                html = requests.get(pic_url["url"], headers=header)

                # 获取图片的名字，用于保存图片时命名
                file_name = pic_url["url"].split(r"/")[-1]

                # 将图片保存到目录(文件夹)中
                with open(file_name, "wb") as f:
                    f.write(html.content)

                # 请求过快会被浏览器限制，手动增加时间，或者更换代理IP，IP池正在研究中
                # (测试成功可用的代理IP请求浏览器还是失败0.0)
                time.sleep(0.1)

        print(f"下载：{title}完成")

    print(f"第{n}页下载完成")
    n += 1


