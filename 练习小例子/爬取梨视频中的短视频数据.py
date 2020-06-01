# 反爬机制：
# 要的视频数据并没有在html 属性中而是在js文本中
# 只能靠re获取或者BeautifulSoup(string=re.complie())获取
import requests
from lxml import etree
import re
import os

headers =  {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36',
    'Referer':'https://www.pearvideo.com/category_2'

}

# 存放文件夹
dirName = '资源放置/HotspotMovie'
if not os.path.exists(dirName):
    os.mkdir(dirName)

# 通用url
url = 'https://www.pearvideo.com/category_2'

response = requests.get(url=url,headers=headers).text
tree = etree.HTML(response)
href = tree.xpath('//div[@class="category-top"]//a[@class="vervideo-lilink actplay"]')

# 遍历获取视频请求url，第四个不是热门视频去掉
n=1
for a in href:
    if n==4:
        break
    movie_href ='https://www.pearvideo.com/'+ a.xpath('./@href')[0]
    response = requests.get(url = movie_href,headers=headers).text
    tree = etree.HTML(response)

    # xpath可以提取js中数据，就是文本
    movie_mp4_text = tree.xpath('//*[@id="detailsbd"]/div[1]/script[1]/text()')
    movie_title = tree.xpath('//div[@id="poster"]/img/@alt')[0] + '.mp4'
    movie_mp4 =re.findall('srcUrl="(.*?)"',movie_mp4_text[0])[0]
    movie_data = requests.get(url=movie_mp4,headers=headers).content
    movie_path = dirName +'/' +movie_title
    with open(movie_path,'wb') as f :
        f.write(movie_data)
    n+=1






