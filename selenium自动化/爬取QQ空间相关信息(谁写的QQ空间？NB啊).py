# from lxml import etree
# from time import sleep
# from selenium import webdriver
# from selenium.webdriver import ActionChains
#
# driver = webdriver.Chrome()
# driver.get('https://qzone.qq.com')
#
# # 小心frame窗口 webDriver每次只能在一个页面上
# # 识别元素，对于frame 嵌套内的页面上的元素,直接定位的
# # 时候就需要通过switch_to_from()方法将当前定位的主体切换到frame窗口里
#
# driver.switch_to.frame('login_frame')
# # driver.find_element_by_id('switcher_plogin').click()
#
# # driver.find_element_by_id('u').clear() # 清除默认值
# # driver.find_element_by_id('u').send_keys('1803957813')
# #
# # driver.find_element_by_id('p').send_keys('zzb1803957813')
# #
# driver.find_element_by_xpath('//*[@id="qlogin_list"]/a[1]').click()
# sleep(1)
# driver.find_element_by_xpath('//*[@id="aIcenter"]').click()
#
#
# sleep(3)
# driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
# sleep(3)
# driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
# paget_text = driver.page_source
#
# tree = etree.HTML(paget_text)
# # driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
#
#
# # html_list = []
# # 执行解析操作
# # for i in range(10):
#
# #
# li_list = tree.xpath('//*[@id="feed_friend_list"]/li[2]/ul')
# print(li_list)
# for li in li_list:
#     title = li.xpath('.//div[@class="f-nick"]/a/text()')
#     content = li.xpath('.//div[@class="f-info"]/text()')
#     print(title)
#     print(content)
#     # for i in range(4):
#     #     print(f"{title[i]}:{content[i]}")
#     #     print('')
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
