# -*- coding: utf-8 -*-

import random

import requests
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import cv2
import numpy as np
def login():
    global element
    global background_image_url
    global slider_image_url

    url = 'https://www.douban.com/'
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    bro = webdriver.Chrome(chrome_options=chrome_options)
    bro.get(url)
    sleep(1)
    bro.switch_to.frame(0)
    bro.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]').click()
    bro.find_element_by_id('username').clear()  # 清除默认值
    bro.find_element_by_id('username').send_keys('1803957813')

    bro.find_element_by_id('password').send_keys('zhouzebo110')
    bro.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]').click()
    sleep(2)
    bro.switch_to.frame(0)

    div_tag = bro.find_element_by_xpath('//*[@id="tcaptcha_drag_thumb"]')

    element = ActionChains(bro).click_and_hold(on_element=div_tag)
    # 如果通过find系列的函数进行标签定位发现标签是存在
    # 与iframe(第二窗口)下面,就会定位失败
    # 解决方案使用switch_to即可
    background_image_url = bro.find_element_by_id('slideBkg').get_attribute('src')
    slider_image_url = bro.find_element_by_id('slideBlock').get_attribute('src')

# 将url中的图片请求下来，保存到本地
def get_image(img_url, imgname):
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
    # 获取图片并灰度化
    block = cv2.imread(slider_image, 0)
    template = cv2.imread(back_image, 0)
    w, h = block.shape[::-1]

    # 二值化后图片名称
    block_name = 'block.jpg'
    template_name = 'template.jpg'
    # 保存二值化后的图片
    cv2.imwrite(block_name, block)
    cv2.imwrite(template_name, template)
    block = cv2.imread(block_name)
    block = cv2.cvtColor(block, cv2.COLOR_RGB2GRAY)
    block = abs(255 - block)
    cv2.imwrite(block_name, block)
    block = cv2.imread(block_name)
    template = cv2.imread(template_name)
    # 获取偏移量
    # 模板匹配，查找block在template中的位置，返回result是一个矩阵，是每个点的匹配结果
    result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)

    # 由于获取到的验证码图片像素与实际的像素有差(实际：280*158 原图：680*390)，故对获取到的坐标进行处理
    offset = y * (280 / 680)
    # 画矩形圈出匹配的区域
    # 参数解释：1.原图 2.矩阵的左上点坐标 3.矩阵的右下点坐标 4.画线对应的rgb颜色 5.线的宽度
    cv2.rectangle(template, (y, x), (y + w, x + h), (7, 249, 151), 2)

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


# 的边框距离就是总位移
def slide():
# 进行动作链模拟人滑动滑块操作
    for i in track:
        element.move_by_offset(i, 0).perform()
        element.reset_actions()
    sleep(0.8)
    element.release().perform()
login()
distance = get_image_offset(background_image_url, slider_image_url) # 滑块到缺口的偏移值
track = get_tracks(distance+random.randint(5,6)) # 缺口偏移值加上滑块的边框距离就是总位移
slide()

