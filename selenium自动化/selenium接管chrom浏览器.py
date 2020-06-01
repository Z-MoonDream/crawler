from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
#本机安装好的谷歌驱动路径(要与添加的环境变量的那个驱动路径相同)
chrome_driver = "E:\plus_len\练习\爬虫\selenium自动化"

driver = webdriver.Chrome(executable_path=chrome_driver,chrome_options=chrome_options)
print(driver.title)
