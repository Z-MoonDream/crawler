# -*- coding: utf-8 -*-

import os

# 不传值默认返回当前路径，传入几返回上几层(绝对路径)
def os_path_dirname(file,num=0):
    # file 为你使用该函数时的__file__
    # 循环版
    # start = file
    # for i in range(num):
    #     start = os.path.dirname(start)
    # return start
    # 递归版
    start = file
    if not num:
        return start
    return os.path.dirname(os_path_dirname(file,num-1))

