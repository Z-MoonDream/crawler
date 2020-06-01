from bs4 import BeautifulSoup
import  requests
import os
import zipfile

header =  {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36',
}

url = 'http://sc.chinaz.com/jianli/free.html'

html = requests.get(url=url,headers=header).content.decode('utf-8')
soup = BeautifulSoup(html,'lxml')


for index in soup.find_all("a",class_='title_wl'):
    title = index.string
    href = index["href"]
    html = requests.get(url=href,headers=header).content.decode('utf-8')
    soup = BeautifulSoup(html,'lxml')
    rar = soup.select('.clearfix>li>a')[1]['href']

    with open(f"./dataset/{title}.zip","wb") as f:
        f.write(requests.get(rar,headers=header).content)

# zip_file = zipfile.ZipFile("asd.zip")


    print(title,"爬取完毕")
