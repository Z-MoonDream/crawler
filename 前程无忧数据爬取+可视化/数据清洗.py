# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame, Series
import re

import pymysql
from sqlalchemy import create_engine
import sqlalchemy
conn = pymysql.connect(host='127.0.0.1',user='root',password='',database='前程无忧',charset='utf8')

sql_df = pd.read_sql('select * from message_data',conn)

# for循环效率太低
# li = sql_df['职位']
# for i in range(len(li)):
#     # try:
#     if '数据' not in li[i]:
#         sql_df = sql_df.drop(i, axis=0)
# print(sql_df.info())

# sql_df = sql_df[ sql_df['职位'].str.contains('数据')==False ]
sql_df = sql_df[sql_df['职位'].str.contains('数据')]

# 正则替换
sql_df['需求'].replace('招若干人','招3人',regex=True,inplace=True)
# print(sql_df['需求'])

b3 =u'万/年'
b4 =u'千/月'
b5 =u'元/天'
li3 = sql_df.loc[:,'薪资']

# # 注释部分的print都是为了调试用的
# !!!!id从1开始的 要对应行号必须减一 id与行号不对应
for i in sql_df['id']-1:
    try:
        if b3 in li3[i]:
            x = re.findall(r'\d*\.?\d+',li3[i])
            min_ = format(float(x[0])/12,'.2f')#转换成浮点型并保留两位小数
            max_ = format(float(x[1])/12,'.2f')
            sql_df.loc[i,'薪资'] = min_+'-'+max_+u'万/月'
        if b4 in li3[i]:
            # print(li3[i], i)
            x = re.findall(r'\d*\.?\d+',li3[i])
            min_ = format(float(x[0])/10,'.2f')
            max_ = format(float(x[1])/10,'.2f')
            # print(sql_df.loc[i, ['薪资','职位']], i, li3[i])
            sql_df.loc[i,'薪资'] = min_ + '-' + max_ + u'万/月'
        if b5 in li3[i]:
            x = re.findall(r'\d*\.?\d+',li3[i])
            num_ = format(int(x[0])*30/10000,'.2f')
            sql_df.loc[i,'薪资'] = num_ + u'万/月'
    except KeyError:
        pass
conn = create_engine('mysql+pymysql://root:@localhost:3306/前程无忧?charset=utf8')

sql_df.to_sql('new_message_data',con=conn,index=False,if_exists='replace',dtype={'id':sqlalchemy.types.BigInteger()})

with conn.connect() as con:
    con.execute('alter table new_message_data add primary key (`id`)')


