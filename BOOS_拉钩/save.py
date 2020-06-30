# -*- coding: utf-8 -*-
import pandas as pd
import os
import datetime
import re
# boos = pd.read_csv('爬虫职位_BOOS.csv')
#
# boos.drop(['Unnamed: 0'],axis=1,inplace=True)
# dict_ = boos.to_dict(orient='records')
# dict_new = []
# for dic in dict_:
#     if '爬虫'  in dic['职位名']:
#         dic['招聘网站'] = 'BOOS'
#         dict_new.append(dic)
# csv = pd.DataFrame(dict_new)
# # 根据详情页这个列名取出重复项，并保留第一个，然后在原数据上修改
# csv.drop_duplicates('详情页','first',inplace=True,)
# csv.to_csv('清洗完毕_BOOS.csv',encoding='utf-8',index=False)

# lg = pd.read_csv('爬虫职位_拉钩.csv')
# columns = ['职位名','公司名','薪资','发布日期','工作时间/学历','地点','技术栈','详情页','Unnamed: 0']

# lg.drop(['Unnamed: 0'],axis=1,inplace=True)
# dict_ = lg.to_dict(orient='records')
#
# dict_new = []
# for dic in dict_:
#     if '爬虫'  in dic['职位名']:
#         dic['招聘网站'] = '拉钩'
#         time_ = datetime.datetime.strptime(dic['发布日期'],"%Y-%m-%d %H:%M:%S")
#         try:
#             dic['发布日期'] = f'发布于{time_.month}月{time_.day}日'
#         except Exception:
#             continue
#         dict_new.append(dic)
# csv = pd.DataFrame(dict_new)
# # # 根据详情页这个列名取出重复项，并保留第一个，然后在原数据上修改
# csv.drop_duplicates('详情页','first',inplace=True,)
# csv.to_csv('清洗完毕_拉钩.csv',encoding='utf-8',index=False)

# zhilian = pd.read_csv('爬虫职位_智联.csv')
# zhilian.drop('Unnamed: 0',axis=1,inplace=True)
# dic = zhilian.to_dict(orient='records')
# dic_new = []
# for i in dic:
#     if '爬虫' in i['职位名']:
#         if ':' in i['发布日期']:
#             i['发布日期'] = i['发布日期'].replace('更新于',f'发布于{datetime.datetime.now().month}'
#             f'月{datetime.datetime.now().day}日')
#         i['发布日期'] = i['发布日期'].replace('更新于','发布于')
#         dic_new.append(i)
# csv = pd.DataFrame(dic_new)
# csv.drop_duplicates('详情页','first',inplace=True)
# csv.to_csv('清洗完毕_智联.csv',encoding='utf-8',index=False)




class Save:

    def job_51(self,name):
        job = pd.read_csv(name)
        job.drop('Unnamed: 0', axis=1, inplace=True)
        dict_ = job.to_dict(orient='records')
        dict_new = []
        for i in dict_:
            if '爬虫' in i['职位名']:
                if 'Java' not in i['职位名']:
                    i['招聘网站'] = '51job'
                    i['发布日期'] = i['发布日期'].replace('-', '月') + '日'
                    # 发布于05月06日 将05中的0去掉
                    i['发布日期'] = re.sub('于0','于',i['发布日期'])
                    dict_new.append(i)
        return dict_new

    def boos(self,name):
        boos_ = pd.read_csv(name)
        boos_.drop(['Unnamed: 0'],axis=1,inplace=True)
        dict_ = boos_.to_dict(orient='records')
        dict_new = []
        for dic in dict_:
            if '爬虫'  in dic['职位名']:
                if 'Java' not in dic['职位名']:
                    dic['招聘网站'] = 'BOOS'
                    dic['发布日期'] = dic['发布日期'].replace('昨天',f'{datetime.datetime.now().month}月'
                    f'{datetime.datetime.now().day-1}日')
                    # 发布于05月06日 将05中的0去掉
                    dic['发布日期'] = re.sub('于0', '于', dic['发布日期'])
                    dict_new.append(dic)
        return dict_new

    def lag(self,name):
        lg = pd.read_csv(name)
        lg.drop(['Unnamed: 0'],axis=1,inplace=True)
        dict_ = lg.to_dict(orient='records')
        dict_new = []
        for dic in dict_:
            if '爬虫'  in dic['职位名']:
                time_ = datetime.datetime.strptime(dic['发布日期'],"%Y-%m-%d %H:%M:%S")
                try:
                    dic['发布日期'] = f'发布于{time_.month}月{time_.day}日'
                except Exception:
                    continue
                if 'Java' not in dic['职位名']:
                    dic['招聘网站'] = '拉钩'
                    # 发布于5月8日 将5月8日改成5月08日，用于排列
                    # 如果是5月18日，就不做操作
                    if not re.search('\d\d日', dic['发布日期']):
                        dic['发布日期'] = re.sub('月', '月0', dic['发布日期'])
                    dict_new.append(dic)
        return dict_new

    def zhilian(self,name):
        zhilian = pd.read_csv(name)
        zhilian.drop('Unnamed: 0',axis=1,inplace=True)
        dict_ = zhilian.to_dict(orient='records')
        dict_new = []
        for i in dict_:
            if '爬虫' in i['职位名']:
                if ':' in i['发布日期']:
                    i['发布日期'] = i['发布日期'].replace('更新于',f'发布于{datetime.datetime.now().month}'
                    f'月{datetime.datetime.now().day}日')
                    # 发布于6月30日08:07 我只要发布于6月30日，将后面的时间去掉
                    i['发布日期'] = i['发布日期'][:i['发布日期'].find('日')+1]
                i['发布日期'] = i['发布日期'].replace('更新于','发布于')
                if 'Java' not in i['职位名']:
                    i['招聘网站'] = '智联'
                    # 发布于5月8日 将5月8日改成5月08日，用于排列
                    # 如果是5月18日，就不做操作
                    if not re.search('\d\d日', i['发布日期']):
                        i['发布日期'] = re.sub('月', '月0', i['发布日期'])
                    dict_new.append(i)
        return dict_new

    def main(self):
        dict_list = self.boos('爬虫职位_BOOS.csv')+self.lag('爬虫职位_拉钩.csv')\
                    +self.zhilian('爬虫职位_智联.csv')+self.job_51('爬虫职位_51job.csv')
        dict_list = sorted(dict_list,key=lambda x:x['发布日期'])

        csv = pd.DataFrame(dict_list)
        columns = list(csv)
        # print(list(csv))
        # csv.pop(csv.index('详情页'))
        # csv.append('详情页')
        columns.insert(-1,columns.pop(columns.index('招聘网站')))
        csv = csv[columns]
        csv.to_csv('爬虫职位_拉钩-51-boos-智联.csv',encoding='utf-8',index=False)

save = Save()
save.main()






