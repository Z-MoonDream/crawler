import requests
from lxml import etree


# 网站的咨询是动态加载的数据要通过抓包工具全局搜索拿到ajax数据包url

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.50'
}

# 如果headers里面没有cookie的话会返回404
# 手动copy的cookie比较方便但是有有效时长一般是5分钟左右吧
# 而如果不是自动获取的cookie而是通过抓包工具copy的cookie的话会存在有效时长的问题
# 用了自动获取的cookie每次请求都是新的cookie就非常灵活了

session = requests.Session() # 创建好了seion对象
# 第一次使用session捕获且存储cookie,猜测对雪球网首页发起的请求可能会产生cookie
main_url = 'https://xuequi.com/'
session.get(main_url,headers=headers) # 捕获且存储cookie


# 含有ajax数据包的url
url = 'https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id=20370786&count=15&category=-1'
page_text = session.get(url=url,headers=headers).json()
print(page_text)










