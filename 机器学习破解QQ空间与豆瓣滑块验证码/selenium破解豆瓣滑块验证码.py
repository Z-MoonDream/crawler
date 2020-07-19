# -*- coding: utf-8 -*-

import random
from time import sleep

import requests
import cv2
import numpy as np

from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



# 进行登录操作
def login():
    # 生成全局变量，这个变量最后接收的是一种点击滑块的这个操作对象
    global element
    # 背景图片url
    global background_image_url
    # 滑块图片url
    global slider_image_url

    url = 'https://www.douban.com/'
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    bro = webdriver.Chrome(chrome_options=chrome_options)
    bro.get(url)
    sleep(1)
    # 切换到内部窗口
    bro.switch_to.frame(0)
    bro.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]').click()
    bro.find_element_by_id('username').clear()  # 清除默认值
    bro.find_element_by_id('username').send_keys('xxxx')

    bro.find_element_by_id('password').send_keys('xxxx')
    # 点击确定
    bro.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]').click()
    sleep(2)
    # 切换到内部窗口
    bro.switch_to.frame(0)

    # 定位到滑块
    div_tag = bro.find_element_by_xpath('//*[@id="tcaptcha_drag_thumb"]')

    # 动作链点击并且保持点击滑块
    element = ActionChains(bro).click_and_hold(on_element=div_tag)
    # 如果通过find系列的函数进行标签定位发现标签是存在
    # 与iframe(第二窗口)下面,就会定位失败
    # 解决方案使用switch_to即可
    background_image_url = bro.find_element_by_id('slideBkg').get_attribute('src')
    slider_image_url = bro.find_element_by_id('slideBlock').get_attribute('src')

# 将url中的图片请求下来，保存到本地
def get_image(img_url, imgname):
    # https://www.cnblogs.com/nul1/p/9172068.html
    # requests的这个参数stream是下载大文件的时候用，装B的
    image = requests.get(img_url, stream=True)
    with open(imgname, 'wb') as f:
        for chunk in image.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()  # flush方法是用来刷新缓冲区的，即将缓冲区中的数据立刻写入文件，同时清空缓冲区
        f.close()


# 使用opencv模块 计算缺口的偏移值
def get_image_offset(background_image_url, slider_image_url):
    back_image = 'back_image.png'  # 背景图像命名
    slider_image = 'slider_image.png'  # 滑块图像命名
    get_image(background_image_url, back_image)
    get_image(slider_image_url, slider_image)
    # 获取图片并灰度化，二值是指只有两种值即黑或者白
    # 而灰度是灰色(0-255)当灰度值为0是即全黑，255即全白
    # https://blog.csdn.net/rhyijg/article/details/106934061
    # >0返回3通道彩色图
    # =0返回灰度图
    # <0返回原图
    block = cv2.imread(slider_image, 0)
    template = cv2.imread(back_image, 0)
    # 0是高度 1是宽度 [::1]是取出所有
    # w是高度，1是宽度
    w, h = block.shape[::1]

    # 灰度化后图片名称
    block_name = 'block.jpg'
    template_name = 'template.jpg'
    # 保存灰度化后的图片，默认当前路径下
    cv2.imwrite(block_name, block)
    cv2.imwrite(template_name, template)
    # https://blog.csdn.net/zhang_cherry/article/details/88951259
    # cv2.imread()和cv2.cvtColor() 的使用
    # 读取出BGR格式数据
    block = cv2.imread(block_name)
    # 转化为灰度图片，参数COLOR_RGB2GRAY是灰度图
    # COLOR_BGR2RGB是将BGR格式转换成RGB格式
    # 返回的是numpy多维数组，里面是图片灰度化后的每个像素点的RGB值
    block = cv2.cvtColor(block, cv2.COLOR_RGB2GRAY)

    # 求绝对值，越接近0即越白，越接近255即越黑，这里是将其保持中间值
    # 如果block大了则结果变小，即变白，如果block小了，则结果变大，即变黑
    # 使现在图与原本图差异明显
    block = abs(255 - block)
    # 保存灰度图到本地
    cv2.imwrite(block_name, block)
    # 不写默认是原图,因为此时原图就是灰度图，所以不管数字是多少都是灰度图
    block = cv2.imread(block_name)
    template = cv2.imread(template_name)
    # 获取偏移量
    # 模板匹配，查找block在template中的位置，返回result是一个矩阵，是每个点的匹配结果
    # https://blog.csdn.net/weixin_42081389/article/details/87935735
    # CV_TM_CCORR_NORMED 归一化相关匹配法
    result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)
    # x为最大值列数，y为最大值行数
    # 至于为什么能通过行数来确定位置，这个就是归一化匹配法做的事情了
    # 相关方法还有很多，不懂原理就一个一个试，找资料吧，我也不太懂
    x, y = np.unravel_index(result.argmax(), result.shape)
    # print(x,y)
    # print(np.unravel_index(result.argmax(), result.shape))
    # print(result)

    # 由于获取到的验证码图片像素与实际的像素有差(实际：136*136 原图：680*390)，故对获取到的坐标进行处理
    # 每台驱动浏览器获得的的像素值不同，要对应处理，找出合适的参数值
    # offset = y * (136/ 680)
    # offset = y * (200/ 680)
    # offset = y * (250/ 680)
    # offset = y * (300/ 680)
    # 找到比较合适的参数值
    offset = y * (285/ 680)

    # print(offset)
    # 画矩形圈出匹配的区域
    # 参数解释：1.原图 2.矩阵的左上点坐标 3.矩阵的右下点坐标 4.画线对应的bgr颜色 5.线的宽度,注意，x，y是相反的
    cv2.rectangle(template, (y, x), (y + w, x + h), (7, 249, 151), 2)
    cv2.imwrite("origin.jpg", template)

    # 返回位移(偏移值)
    return offset


# 轨迹函数
# 采用物理加速度位移相关公式按照先快后慢的人工滑动规律进行轨迹计算，
def get_tracks(distance):
    # 拿到移动的总位移，模仿人的滑动行为，先匀加速，快到位置后匀减速
    #     匀变速基本公式：
    #     1、位移与时间的关系公式：
    #     s = v0*t+ 0.5*a**t
    #     2、速度于时间的关系公式：
    #     v = v0+a*t
    #     3、位移与速度的关系公式：
    #     vt**2 - v0**2 = 2*a*s
    '''

    :param displace: 计算出的总位移 滑块到缺口的总长度
    :return: 轨迹列表
    '''
    # 轨迹列表
    track_list = []
    # 起始位置
    current = 0
    # 快到这个位置的时候，就要匀减速
    mid = distance * 3 / 4
    # 时间为随机时间，0.2或0.3
    t = random.randint(2, 3) / 10
    # 一开始的速度
    v = 0
    # distance：终止位置
    while current < distance:
        if current < mid:
            # 加速度越小，单位时间内的位移越小，我们模拟的轨迹越多越详细
            a = 2
        else:
            a = -3
        # 初速度
        v0 = v
        # 此时的速度为
        v = v0 + a * t
        # 计算出匀变速下的位移
        move = v0 * t + 1 / 2 * a * t * t
        # 下一次的起始位置
        current += move
        # 将计算出的位移加入到轨迹列表中，并且保留两位小数
        track_list.append(round(move, 2))
    return track_list


# 进行动作链模拟人滑动滑块操作
# https://liushilive.github.io/github_selenium_docs_api_py/md/selenium/webdriver/common/action_chains.html
def slide():
    for i in track:
        # 这个element是全局对象，就是一直点击滑块的那个对象
        # 参数1是x轴距离，参数2是y轴距离
        # perform执行操作
        element.move_by_offset(i, 0).perform()
        # 清除已储存在远端的操作，保险一些
        element.reset_actions()
    # 暂停一下，更模仿人为操作
    sleep(0.8)
    # 释放鼠标按钮
    element.release().perform()
login()
distance = get_image_offset(background_image_url, slider_image_url) # 滑块到缺口的偏移值
track = get_tracks(distance+random.randint(12,12)) # 缺口偏移值加上滑块的边框距离就是总位移
slide()

