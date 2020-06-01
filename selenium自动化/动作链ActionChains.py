# 动作链:一系列连续的动作(滑动动作)
from selenium.webdriver import ActionChains
from selenium import webdriver
from time import sleep

url = 'https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'

bro = webdriver.Chrome(executable_path='chromedriver.exe')
bro.get(url)
sleep(1)

# 如果通过find系列的函数进行标签定位发现标签是存在
# 与iframe(第二窗口)下面,就会定位失败
# 解决方案使用switch_to即可
bro.switch_to.frame('iframeResult')
div_tag = bro.find_element_by_xpath('//*[@id="draggable"]')

# 对div_tag进行滑动操作
action = ActionChains(bro) # 选中的对象是bro 浏览器打开的对象
action.click_and_hold(div_tag)# 单击且长按 这样才能滑动

for i in range(6):
    # perform让动作链立即执行
    action.move_by_offset(10,15).perform()#右下10,15像素
    sleep(0.5)
action.release() # 松开长按









