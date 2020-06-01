# import requests
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
#                        '(KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36',
# }

# # 请求网址里面带有等于号 而等号后面是请求参数添加请求参数才可以获取数据，一般请求参数都会做一些加密之类的(json?)
# url = 'https://movie.douban.com/typerank?type_name=%E5%8A%A8%E4%BD%9C&type=5&interval_id=100:90&action='
#
# html = requests.get(url=url,headers=headers)
#
# # 发现并没有想要的数据，因为数据是动态JS加载的ajax
# #
# print(html.text)


# 真正电影数据放的地方，也就是通过ajax发现的有数据的请求包url
# url  = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20'



# 进行参数定制 ?后面是放请求参数的地方对其进行params定制

# url = 'https://movie.douban.com/j/chart/top_list'

# 必须都是字符串形式的键值对才可以
# params = {
#     'type': '5',
#     'interval_id': '100:90',
#     'action':'',
#     'start': '0',
#     'limit': '20',
# }

# star 是从第几个开始，limit是到那个结束
# response = requests.get(url=url,params=params,headers=headers).content

# 因为获取的是json格式的字符串
# 要进行反序列化变成列表或者字典(也就是原数据类型,而不是json格式的)

# for index in response.json():
#     # print(index) 是一个字典里面包含数据的键值对
#     name = index['title'] # 标题  福尔摩斯二世 ...
#     score = index['score'] # 评分 9.5....
#     print(name,score)
