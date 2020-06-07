# -*- coding: utf-8 -*-
import pymysql
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
from pyecharts import Funnel,Pie,Geo
import re


plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
conn = pymysql.connect(host='127.0.0.1',user='root',password='',database='前程无忧',charset='utf8')

df = pd.read_sql('select * from new_message_data',conn)
df.index = df.index+1

pay = df['薪资']
site = df['公司地点']
edu = df['学历']
exp = df['工作经验']
pay_list = []
site_list = []
exp_list = []
edu_list = []
# site_list = (i.split('-')[0] for i in df['公司地点'])
# edu_list = (i for i in df['学历'])
# exp_list = (i for i in df['工作经验'])

# 有单个值存在的情况，抛弃一整行数据
for i in range(1,len(df)+1):
    try:
        pay_list.append([re.findall(r'\d*\.?\d+',pay[i])[0],re.findall(r'\d*\.?\d+',pay[i])[1]])
        site_list.append(site[i].split('-')[0])
        exp_list.append(exp[i])
        edu_list.append(edu[i])
    except IndexError:
        pass
min_s = []
max_s = []
for i in pay_list:
    min_s.append(float(i[0]))
    max_s.append(float(i[1]))

# 工作时间圆环图
# 数据太少，普通线图体现不出价值
# ——————————————————————————————
# my_df = pd.DataFrame({'工作经验':list(exp_list),'最小工资':min_s,'最大工资':max_s})
# data1 = my_df.groupby('工作经验')['最小工资'].mean().plot(kind='line')
# plt.show()

# plt.figure(figsize=(15,15))
# my_df2 = pd.DataFrame({'学历':list(edu_list),'最小工资':min_s,'最大工资':max_s})
# data2 = my_df2.groupby('学历')['最小工资'].mean().plot(kind='line')
# plt.show()
# ——————————————————————————————


def get_exp(list_):
    edu_dic = {}
    for i in set(list_):
        edu_dic[i] = list_.count(i)
    return edu_dic
dir1 = get_exp(exp_list)
keys_list1 = dir1.keys()
value_list1 = dir1.values()
# 标题，标题居中
pie = Pie('年限需求',title_pos='center')
pie.add('',keys_list1,value_list1,radius=[40, 75],
    label_text_color=None,
    is_label_show=True,
    legend_orient="vertical",
    legend_pos="left",
    is_random=False,
    rosetype="radius",
        ) # resetype='radius'是玫瑰图，默认为饼图
# pie.render('年限需求圆环图.html')
pie.render('年限需求玫瑰图.html')
#
# # 大数据城市需求地理坐标热力分布图
# def get_site(list_):
#     site_dic = {}
#     for i in set(list_):
#         site_dic[i] = list_.count(i)
#     site_dic.pop('异地招聘')
#     site_dic.pop('黔东南')
#     site_dic.pop('安徽省')
#     site_dic.pop('浙江省')
#     site_dic.pop('广东省')
#     site_dic.pop('湖北省')
#     return site_dic
# geo = Geo('大数据人才需求分布图',title_color='#2E2E2E',title_text_size=24,title_top=20,title_pos='center',width=1300,height=600)
# dir2 = get_site(site_list)
# keys_list2 = dir2.keys()
# value_list2 = dir2.values()
# geo.add('',keys_list2,value_list2,type='effectScatter',is_random=True, visual_range=[0, 1000], maptype='china',symbol_size=8, effect_scale=5, is_visualmap=True)
# geo.render('大数据城市需求分布图.html')

# 工作经验漏斗图
# def get_exp_funnel(list_):
#     exp_dic = {}
#     for i in set(list_):
#         exp_dic[i] = list_.count(i)
#     return exp_dic
# dir3 = get_exp_funnel(exp_list)
# keys_list3 = dir3.keys()
# value_list3 = dir3.values()
# funnel = Funnel('工作经验漏斗图',title_pos='center')
# funnel.add('',keys_list3,value_list3,is_label_show=True,label_pos="inside", label_text_color="#fff",legend_orient='vertical',legend_pos='left')
# funnel.render('工作经验漏斗图.html')
