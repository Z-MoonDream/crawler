from lxml import etree
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
url = 'http://125.35.6.84:81/xk/'
bro = webdriver.Chrome(executable_path='chromedriver.exe')
bro.get(url)
page_text_list = [] #存放每一页的页面源码数据
sleep(1)
# 捕获到当前页面对应的页面源码数据
page_text = bro.page_source # 当前页面全部加装完毕后对应的所有数据(js代码和ajax也加载完了)
page_text_list.append(page_text)

# 点击下一页对打开的页进行请求获取其源码加入列表中用于后面解析
for i in range(2):
    next_page = bro.find_element_by_xpath('//*[@id="pageIto_next"]')

    print((By.ID, 'pageIto_next'))
    # next_page.click()
    # sleep(1)
    # page_text_list.append(bro.page_source) #page_source获取源码

# for page_text in page_text_list:
#     tree = etree.HTML(page_text)
#     li_list = tree.xpath('//*[@id="gzlist"]/li')
#     for li in li_list:
#         title = li.xpath('./dl/@title')[0]
#         print(title)
