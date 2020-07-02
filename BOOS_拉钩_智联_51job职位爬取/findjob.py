# -*- coding: utf-8 -*-
from multiprocessing import Pool
import os
from BOOS_拉钩_智联_51job职位爬取.core.ZhiLian import Zlian
from BOOS_拉钩_智联_51job职位爬取.core.lag import Lg
from BOOS_拉钩_智联_51job职位爬取.core.job_51 import Job
from BOOS_拉钩_智联_51job职位爬取.core.BOOS import Boos
from BOOS_拉钩_智联_51job职位爬取.core.save import Save


def run(obj, city, position, age_limit):
    run = obj(city, position, age_limit)
    run.main()


if __name__ == '__main__':

    pool = Pool(4)
    if not os.path.exists('cookie'):
        os.mkdir('cookie')
    while 1:
        city = input('请输入查询城市：北京或杭州：').strip()
        position = input('\n(请不要精确搜索，越模糊数据越多)\n请输入职位名：').strip()
        age_limit = input('请输入查询年限：1-3年或实习：').strip()
        if (city == '北京' or city == '杭州') and (age_limit == '1-3年' or age_limit == '实习'):
            break
        else:
            print('输入有误请重新输入')

    result = []
    for i in [Lg, Zlian, Job, Boos]:
        r = pool.apply_async(run, args=(i, city, position, age_limit))
    pool.close()
    pool.join()

    print('数据爬取完成 OVER！！！！！')

    Save().main(position='web')

    print('''/*
*      
*          ┌─┐       ┌─┐
*       ┌──┘ ┴───────┘ ┴──┐
*       │                 │
*       │       ───       │
*       │  ─┬┘       └┬─  │
*       │                 │
*       │       ─┴─       │
*       │                 │
*       └───┐         ┌───┘
*           │         │
*           │         │
*           │         │
*           │         └──────────────┐
*           │                        │
*           │                        ├─┐
*           │                        ┌─┘    
*           │                        │
*           └─┐  ┐  ┌───────┬──┐  ┌──┘         
*             │ ─┤ ─┤       │ ─┤ ─┤         
*             └──┴──┘       └──┴──┘ 
*                 神兽保佑 
*                 代码无BUG! 
*/''')


    print('数据清洗完毕，OVER！！！！')

