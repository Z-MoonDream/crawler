from selenium import webdriver
from time import sleep

#1.基于浏览器的驱动程序实例化一个浏览器对象

# 如果驱动程序放入环境变量中就可以不写参数,但是我没配0.0
bro = webdriver.Chrome(executable_path='chromedriver.exe')

# 对目的网站发起请求(用浏览器发起，就是你的驱动程序)
bro.get('https://www.jd.com/')

# 我想在京东的搜索框中录入一个东西点击搜索
# 先定位到搜索框
search_text = bro.find_element_by_xpath('//*[@id="key"]')
search_text.send_keys('苹果') # 向标签中录入数据

# 定位到搜索按钮
btn = bro.find_element_by_xpath('//*[@id="search"]/div/div[2]/button')
btn.click() # 模拟鼠标单击一下

sleep(1) # 停2S

# 在搜索结果页面进行滚轮向下滑动的操作(执行JS操作：js注入)
# window.scrollTo(x,y) x：向左右滑动x像素 y向上下滑动y像素 正值是下右 负值是上左
# document.body.scrollHeight是自动计算出到底部的距离
# 最终实现效果是滑动到底部 目的：让动态数据全部加载到html源码中
bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
sleep(1)
bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
print(bro.page_source)
# 2s后关闭浏览器
sleep(2)


