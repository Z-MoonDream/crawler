# import os
# # "db" 这里 填写db文件与当前代码文件父目录的相对位置
# # db_path 是绝对路径
# db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "csv")
# print(db_path+'/bbb')
import datetime
import pandas as pd
import re
boos_ = pd.read_csv('E:\日常\crawler\BOOS_拉钩_智联_51job职位爬取\csv\职位_BOOS.csv')
boos_.drop(['Unnamed: 0'], axis=1, inplace=True)
dict_ = boos_.to_dict(orient='records')
dict_new = []
for dic in dict_:
    if 'python' in dic['职位名']:
        if 'Java' not in dic['职位名']:
            dic['招聘网站'] = 'BOOS'
            dic['发布日期'] = dic['发布日期'].replace('昨天', f'{datetime.datetime.now().month}月'
            f'{datetime.datetime.now().day - 1}日')
            # 发布于05月06日 将05中的0去掉
            dic['发布日期'] = re.sub('于0', '于', dic['发布日期'])
            if ':' in dic['发布日期']:
                dic['发布日期'] = re.sub('于\S*',f'{datetime.datetime.now().month}月'
                f'{datetime.datetime.now().day}日',dic['发布日期'])
            dict_new.append(dic)


