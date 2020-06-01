import requests
from hashlib import md5

#!/usr/bin/env python
# coding:utf-8



class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

def tranformImgCode(imgPath,imgType):
    chaojiying = Chaojiying_Client('toptop', 'ZZb1803957813', '904440')  # 用户中心>>软件ID 生成一个替换 96001
    im = open(imgPath, 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    return chaojiying.PostPic(im, imgType)['pic_str']  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
# imgPath 图片地址
# imgType 验证码类型


from selenium.webdriver.common.action_chains import  ActionChains
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import  Options # 无头浏览器
import time
from lxml import etree


# 创建一个参数对象,用来控制chrome以无界面模式打开
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')

# 创建浏览器对象
# bro = webdriver.Chrome(executable_path='chromedriver.exe',chrome_options=chrome_options)
bro = webdriver.Chrome(executable_path='chromedriver.exe')

# 调整浏览器窗口大小
bro.set_window_size(1920,1080)

# 上网
bro.get('https://kyfw.12306.cn/otn/login/init')
time.sleep(1)

# 当前页面截图保存
bro.save_screenshot('12306.png')

# 确定验证码照片对应的左上角和右下角坐标(确定剪切区域)
code_img_ele = bro.find_element_by_xpath('//*[@id="loginForm"]/div/ul[2]/li[4]/div/div/div[3]/img')

# 验证码图片左上角的坐标x,y 是一个字典
location = code_img_ele.location

# 验证码图片的宽和高 以左上角为起点
size = code_img_ele.size

# 四个参数 前两个是左上角的x,y坐标,后两个是右下角的x,y坐标(左上角x加上width是右下角的x坐标)(左上角的y加上height是右下角的y坐标)
rangle = (location['x'],location['y'], (location['x'] + size['width']) ,(location['y']+size['height']  ))
# 确定下来裁剪区域准确位置了,进行裁剪

# 获取全屏图片
i = Image.open('./12306.png')

# 为裁剪图片命名
code_img_name = 'code.png'

# 对图片裁剪
frame = i.crop(rangle)

#保存到本地
frame.save(code_img_name)

# 将验证码图片提交给超级鹰进行识别 返回要点击的图片位置
result = tranformImgCode('code.png',9004)
# 96,79|246,90 要点击的图片位置
# x   y  x   y

# 将图片坐标给动作链
all_list = []
if "|" in result:
    list_1 = result.split('|')
    for i in list_1:
        xy_list = [int(j) for j in i.split(',')]
        all_list.append(xy_list)
else:
    all_list.append(int(j) for j in result.split(','))

# [[123, 77], [31, 71]]
print(all_list)

# 让动作链点击图片坐标
for l in all_list:
    x,y = l[0],l[1]
    # 将浏览器对象给动作链,切换到当前窗口下定位到的图片位置进行x,y位置点击立即执行
    ActionChains(bro).move_to_element_with_offset(code_img_ele,x,y).click().perform()
    time.sleep(0.5)

# 录入用户名密码点击登录
bro.find_element_by_id('username').send_keys('18617670187')
time.sleep(2)
bro.find_element_by_id('password').send_keys('ZZb1803957813')
bro.find_element_by_id('loginSub').click()
time.sleep(10)



bro.quit()






