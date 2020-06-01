from selenium import webdriver
from time import sleep

# 后面是你的浏览器驱动位置，记着前面加上r防止字符转义
# 如果驱动程序放入环境变量中就可以不写参数,但是我没配0.0
driver = webdriver.Chrome(executable_path='chromedriver.exe')

# 用get打开百度页面
driver.get('http://www.baidu.com')
# 查找页面的"设置"选项,并进行点击
driver.find_elements_by_link_text('设置')[0].click()
# 防止加载不出来停1秒
sleep(1)
# 点击搜索设置
driver.find_elements_by_link_text('搜索设置')[0].click()
sleep(1)

# 选中每页显示50条数据
m = driver.find_element_by_id('nr')
sleep(1)
m.find_element_by_xpath('//*[@id="nr"]/option[3]').click()
m.find_element_by_xpath('.//option[3]').click()
sleep(1)

# 点击保存设置
driver.find_elements_by_class_name("prefpanelgo")[0].click()
sleep(1)

# 处理弹出的警告页面,点击确定是accept() 点击取消dismiss()
driver.switch_to_alert().accept()
sleep(1)

# 找到百度的输入框,并输入 美女 也可以用xpath来做
driver.find_element_by_id('kw').send_keys('美女')
sleep(2)
# 点击搜索按钮进行跳转页面
driver.find_element_by_id('su').click()

# 注意一定要防止页面没加载出来
sleep(2)
# 在打开的页面中找到美女_海量精选高清图片_百度图片并逐个点击'

driver.find_element_by_xpath('//*[@id="1"]/h3/a').click()
sleep(1)

# 关闭浏览器
driver.quit()