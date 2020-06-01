import requests
from lxml import etree
import os
import time


# 需求：
# 使用xpath爬取图片名称和图片数据
# http://pic.netbian.com/4kmeinv/

# 分析网站,没有动态加载的数据,目前没发现反扒机制(UA 和多次爬禁IP这个??）

headers =  {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36',
    'Referer':'http://pic.netbian.com/4kmeinv/'

}

# url = "http://pic.netbian.com/4kmeinv/"
# response = requests.get(url=url,headers=headers)

# 解决乱码
# response.encoding = "gbk"
# page_text = response.text

# 存文件夹
dirName = "GirlsLib"
if not os.path.exists(dirName):
    os.mkdir(dirName)

#定义一个通用的url模板

for i in range(1,6):
    if i==1:
        url = "http://pic.netbian.com/4kmeinv/"
    else:

        url = f"http://pic.netbian.com/4kmeinv/index_{i}.html"
    response = requests.get(url=url,headers=headers)

    # 解决乱码
    response.encoding = "gbk"
    page_text = response.text

    # 图片名称+图片数据
    tree = etree.HTML(page_text) #parse是本地HTML是网上请求到的源码
    li_list = tree.xpath('//div[@class="slist"]/ul/li') # //li也可以
    for li in li_list:
        # print(type(tree)) <class 'lxml.etree._Element'>
        # print(type(li)) <class 'lxml.etree._Element'>
        # li的数据类型和tree的数据类型一样！！
        # li也可以继续调用xpath方法(比BeaufifulSoup好的地方，灵活)
        img_title = li.xpath('./a/img/@alt')[0] + '.jpg' #进行局部数据解析 .//img也可以
        img_src = 'http://pic.netbian.com' + li.xpath('./a/img/@src')[0] #请求到的src没有域名要加上
        img_data = requests.get(url=img_src,headers=headers).content # content 是二进制文件流用来写入图片视频音频等非文本数据?
        imgPath = dirName +'/' +img_title # 图片存放路径
        with open(imgPath,'wb') as f:
            f.write(img_data)
        # print(img_title,'爬取完毕')
        time.sleep(0.1)

    # print(f'第{i}页爬取完毕')











