from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# 创建一个参数对象,用来控制chrome以无界面模式打开
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 创建浏览器对象
browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)

# 上网
browser.set_window_size(1920, 1080)
browser.get('http://www.baidu.com/')
time.sleep(3)

# 进行截屏
browser.save_screenshot('baidu.png')

# 输出源码
print(browser.page_source)

# 关闭浏览器
browser.quit()
