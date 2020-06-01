import requests
from selenium import webdriver
import time



# driver = webdriver.Chrome(executable_path='chromedriver.exe')
# # driver.maximize_window()
# driver.get('https://www.zhihu.com')
# 不考虑验证码的情况
# driver.find_element_by_xpath('//button[@data-za-detail-view-id="2278"]').click() # 点击登录进入登录界面
# driver.find_element_by_xpath('//input[@name=username"]').send_keys('account')#发送账号名
# driver.find_element_by_xpath('//input[@name="password]').send_keys('password',Keys.ENTER) # 发送密码并回车
# time.sleep(10)
from time import sleep
from selenium import webdriver

# 自动登录
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://qzone.qq.com/')
# driver.set_window_position(20, 40)
# driver.set_window_size(1100,700)
# 表单在该框架下
driver.switch_to_frame('login_frame')
sleep(0.5)
driver.find_element_by_xpath('//*[@id="bottom_qlogin"]/a[1]').click()
driver.find_element_by_xpath('//*[@id="u"]').send_keys('1803957813')
driver.find_element_by_xpath('//*[@id="p"]').send_keys('zzb1803957813')
driver.find_element_by_xpath('//*[@id="login_button"]').click()

# 获取cookie
cookies = driver.get_cookies()
cookies_list = []
for i in cookies:
    cookies_list.append(' '+i['name']+ '='+ i['value']) # 取出键值对，键值对前面都有一个空格，除了第一个键值对前面没有空格

cookiestr = ';'.join(cookies_list)

headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    'Cookie':cookiestr[1:] # 开头的键值对并不需要前面的空格，如果有则会报错

}

url = 'https://user.qzone.qq.com/1803957813'
response = requests.get(url,headers=headers).content.decode('utf-8')
# 成功输出登录后页面
print(response)





