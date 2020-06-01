# crawler

#### 前程无忧数据爬取+可视化

- 数据爬取+持久化
  - 爬取前程无忧500页数据，搜索关键字：大数据
  - 使用多线程(30)进行爬取，共耗时25min
  - 使用pymysql进行持久化，添加线程锁lock防止数据混乱
- 数据清洗
  - 基于pandas中DataFrame进行去除重复数据、不符合要求数据(职位不含有数据关键字)、空值清洗
  - 基于sqlalchemy进行入库(mysql)
- 数据可视化
  - 基于pyecharts中：Funnel(漏斗图)、Geo(地理坐标系图)、Pie(饼图)，生成可视化html文件

#### Scrapy框架练习

- wangyiPro
  - 爬取网易新闻五大板块(军事、航空、无人机、公益、媒体)中的动态数据
  - 请求传参进入二级页面，下载中间件+selenium获取动态数据返回爬虫类，pymysql进行持久化存储
- sunCrawlPro
  - 爬取阳关问政平台数据
  - 基于CrawlSpider进行深度爬取，LinkExtractor与Rule
- midllePro
  - 测试下载中间件的代理IP与UA伪装
  - 构建IP池与UA池
- 等等

#### selenuim自动化

- 捕获cookie，携带cookie进行数据爬取
- 动作链破解滑动验证码
- 基于selenium获取动态加载数据(ajax)