# -*- coding: utf-8 -*-
import pandas as pd
import os

boos = pd.read_csv('爬虫职位_BOOS.csv')

boos.drop(['Unnamed: 0'],axis=1,inplace=True)
dict_ = boos.to_dict(orient='records')
dict_new = []
for dic in dict_:
    if '爬虫'  in dic['职位名']:
        dic['招聘网站'] = 'BOOS'
        dict_new.append(dic)
csv = pd.DataFrame(dict_new)
# 根据详情页这个列名取出重复项，并保留第一个，然后在原数据上修改
csv.drop_duplicates('详情页','first',inplace=True,)
csv.to_csv('清洗完毕_BOOS.csv',encoding='utf-8',index=False)




