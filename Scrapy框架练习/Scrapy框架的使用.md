*  pySpider(不用这个)
*  什么是框架？
  * 就是一个具有很强通用性且集成了很多功能的项目模板(可以被应用在各种需求中)
* scrapy集成好的功能：
  *  高性能的数据解析操作:(xpath 不是etree中的那个xpath)
  *  高性能的数据下载(请求和下载 基于异步)
  * 高性能的持久化存储(以前都用的with open 现在可以用高性能的！管道！来存储)
* 中间件
  * 拦截请求和响应(获取头信息等原始信息)
* 全栈数据爬取操作(一个页码对应的所有数据进行爬取)
* 分布式(搭建分布式集群 对同一数据源进行联合且分布步的爬取 每一个分布(机器)还可以基于scrapy进行异步的爬取)
  * 只能用redis(数据库)一般不用 你没那么多电脑也没环境 并且会redis吗？？？yes！！！

        

* 请求传参的机制(适用在深度爬取中 从首页跳到详情页在到详情页中的详情页在到......)
* 在scrapy中可以合理的应用selenium(可以爬取动态加载的数据 如果你没法解决的话)

## 环境的安装

  * 1.pip3 install wheel
  * 2.下载twisted [http://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted](http://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted)
  * 3.pip3 install pywin32
  *  4.pip3 install scrapy

##  创建工程(在cmd中执行)

  * scrapy startproject firstBlood(创建一个名称为firstBlood的工程)
  * cd ProNmae(工程文件夹 firstBllod)
  *  scrapy genspider spiderName(爬虫文件名称) [www.xxx.com(随意的url](http://www.xxx.com(随意的url) 可以后面更改):创建爬虫文件
  *  执行:scrapy crawl spiderName(爬虫文件名称)
  * settings:
    * 不遵从robots协议
    *  进行UA伪装
    *  LOG_LEVEL = 'ERROR'# 控制台输出报错信息
    * LOG_FLE = 'aa.txt'# 存到文件中
## scrapy的数据解析

  *  extract():列表是有多个列表元素
  *  extract_first():列表是只有单个
## scrapy的持久化存储

* 基于终端指令:
  * 只可以将parse方法的返回值存储到磁盘文件中(不能存到数据库中)

            # spiderName 是你的执行文件名

  *  scrapy crawl spiderName -o 文件名.csv(文件后缀有要求 只能是.excel .json .csv 不能是txt)
*  基于管道的持久化存储: pipelines.py
  * 编码流程:
    * 1.数据解析(爬虫类)
    * 2.在items.py的类中定义相关的属性
    * 3.将解析的数据存储封装到item类型的对象中 要访问属性的话应该是 实例化对象['属性名']的方式去调用因为该类的父类有

        特殊的双下方法(__getitem__(self, key),__setitem__(self, key,     value),__getattr__(self, name),__getattribute__(self, name))

               

    * 4.将item对象提交给管道 yield item(爬虫类)
    * 5.在管道类中的process_item(每次被调用接收一个)负责接收item对象,然后对item进行任意形式的持久化存储
    * 6.在配置文件中开启管道
*  细节补充：
  *  管道文件中的一个管道类标识将数据存储到某一种形式的平台中。
  * 如果管道文件(pipelines)文件中定义了多个管道类，爬虫类提交的item会

    给到优先级最高的管道类数值越低优先级越高。(只会提交一个管道 除非有return item)

  *  在process_item方法的实现中的return item的操作表示将item传递给下一个即将被执行的管道类

            我们要通过这个return来保证所有的管道类都能接受到item

## 基于Spider父类进行全站数据的爬取

* 全站数据的爬取：
  * 全站数据的爬取：将所有页码对应的页面数据进行爬取
  * 手动请求的发送(get):
    * yield scrapy.Rqurst(url,callback)
  * 对yield的总结：
    * 向管道提交item的时候：yield item（要用)
    * 手动请求发送：yield scrapy.Request(url,callbak)
  * 手动发起post请求：
    * yield scrapy.FormRquest(url,formdata,callback):formdata是一个字典 里面是请求参数
    * 一般post请求是结合着模拟登陆的scrapy是进行大数量的数据进行爬取一般不用post请求，post请求还是request来做的好
## CrawlSpider

* 基于scrapy进行全站数据爬取的一种新的技术手段
* CrawlSpider就是Spider的一个子类(子类有父类的方法，并且还可以派生出自己的方法)
  * 链接提取器：LinkExtractor
  * 规则解析器：Rule
* 使用流程：
  * 新建一个工程
  * cd 工程中
  * 新建一个爬虫文件 ：scrapy genspider -t crawl spiderName [www.xxx.com](http://www.xxx.com)
```python
# 爬虫类
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from sunCrawlPro.items import SuncrawlproItem,Detail_item

class SunSpider(CrawlSpider):
    name = 'sun'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest?id=1&page=1']
    # 实例化了一个链接提取器对象
    # 作用：根据指定规则(allow='正则表达式')进行指定链接的提取
    # 只会提取出链接 不会提取出字符串
    # 如果是False的话则只会提取当前页前后的两个页面链接，而不是目前页所看到的所有链接
    # 获取页码的链接
    # 如果follow=True：将链接提取器，继续作用到链接提取器提取到的，链接所对应的，页面中
    # 比如：我对首页发起提取，follow=True 我提取到了页面源码中的页码链接然后我继续对页码链接中的页码继续进行提取符合规则的链接，也就是对首页提取页码就会提取出1,2,3,4,5然后对第二页提取页码提取出2,3,4,5,6然后对第三页提取页码提取出4,5,6,7，这样 虽然会有大量重复的链接，但是这些重复的链接都被调度器过滤掉了所以根本不用担心
    link = LinkExtractor(allow=r'id=1&page=\d+')
    # 获取新闻详情页的链接 正则中如果要将符号转移成字符串的话要加\
    # 拿到新闻详情页的链接后，对链接发起请求，然后在对响应数据进行解析出自己想要的数据来
    # ！！！一定要注意？和.这些都要转移成字符串的
    link_detail = LinkExtractor(allow=r'index\?id=\d+')
    # 所有的规则解析都要放在这个rules里面，可以放多个Rule(规则解析器)
    rules = (
        # 三个参数 一个类的实例化，将link作用到了Rule构造方法的参数1中
        # 作用:用于解析页面源码数据的，里面有回调函数callback
        # Rule可以对链接发送请求有几个链接发几次请求
        # 对链接发起请求，可以执行回调
        # 只要有一个页码链接的规则解析器就可以进行对页码链接页数的详情页中的详情页中的符合规则的数据进行爬取，好像是讲页码链接的url放入调读器中了，然后爬详情页数据的那个规则解析器爬完首页后，还会继续爬调度器中的url看看调度器中的其他url，对其发起请求看看它里面还有没有符合需求的数据(所以只要一个规则解析器解析出页码，在来规则解析器来解析其他数据就可以实现随着页码变多对不同页码的数据进行爬取！！！NB)
        Rule(link, callback='parse_item', follow=False),
        Rule(link_detail, callback='parse_detail', follow=False),
    )

    def parse_item(self, response):
        # 如果打印response的话就是响应的链接
        # 如果对response进行.xpath解析的话就是响应的html源码数据
        # 此时的response就是页面源码对应的数据，同时还包括了链接
        # <200 http://wz.sun0769.com/political/index/politicsNewest?id=1&page=4>
        li_list = response.xpath('/html/body/div[2]/div[3]/ul[2]/li')
        for li in li_list:
            # !!!!xpath中不能出现tbody标签会为空 将tbody去掉
            num = li.xpath('./span[1]/text()').extract_first()
            title = li.xpath('./span[3]/a/text()').extract_first()
            item = SuncrawlproItem()
            item['title'] = title
            item['num'] = num
            yield item
    def parse_detail(self,response):
        content = response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/pre/text()').extract_first()
        num = response.xpath('/html/body/div[3]/div[2]/div[2]/div[1]/span[4]/text()').extract_first().split(':')[-1]
        item = Detail_item()
        item['content'] = content
        item['num'] = num

        yield item

# 管道类
class SuncrawlproPipeline(object):
    def process_item(self, item, spider):
        # 我们要做数据汇总，可以在 第一个Rule里面请求传参来解决
        # 或者说学数据分析用共同的标示位
        # 也可以放在数据库中进行合并 group by
        # 如果没有标示位可以设置标示位，如果不能设置标示位，就可以crawlspider结合request进行请求传参
        # 获取提交过来的item的类名(item是实例化的他有实例化的类)
        if item.__class__.__name__ =='Detail_item':
            content = item['content']
            num = item['num']
            print(item)
        else:
            title = item['title']
            num = item['num']
            print(item)
        return item
# item实例化类
import scrapy

class SuncrawlproItem(scrapy.Item):
    # define the fields for your item here like:
    num = scrapy.Field()
    title = scrapy.Field()
class Detail_item(scrapy.Item):
    content = scrapy.Field()
    num = scrapy.Field()
```

## scrapy五大核心组件

![图片](https://uploader.shimo.im/f/ESBU6s6ReSkUPzjK.png!thumbnail)

  * 爬虫(Spiders)
    * 爬虫是主要干活的(进行数据解析和决定请求那个url)，用于从特定的网页中提取自己所需要的信息，即所谓的实体(Item)。用户也可以从中提取出链接来上Scrapy继续抓取下一个页面(就是首页中的详情页中的详情页........)
  * 引擎(Scrapy)
    * 用来处理整个系统的数据流，
    * 触发事务(框架核心)
      * 通过数据流来判断后，自动进行对对象进行实例化并且调用实例化对象的方法
  * 调度器(Scheduler)
    * 用来接收引擎发送过来的请求(将请求url封装好最先发过来)，先过滤掉重复的url后在，压如队列中，并在引擎再次请求的时候返回，可以想像成一个URL(抓取网页的网址或者说是链接)的优先队列，由它来决定下一个要抓取得网址是什么，(队列是先进先出的 串行并不是异步)
  * 下载器(Downloader)
    * 用于下载网页内容，并且将网页内容返回给蜘蛛(Scrapy下载器是建立在Twisted这个高效的异步模型上的)
  * 管道(Pipeline)
    * 负责抓取爬虫从网页中抽取的实体，主要的功能是持久化实体、验证实体的有效性、清除不需要的信息、当页面被爬虫解析后封装成实体(Item)，之后实体将被发送到项目管道，并经过几个特定的次序处理数据(保存数据到Mysql 或者本地文件夹 或者Rieds)
## scrapy的请求传参

* 作用：实现深度爬取
* 使用场景：如果使用scrapy爬取的数据没有存在同一张页面中(爬取首页中的详情页中的详情页的数据之类的)
* 传递item：yield scrapy.Request(url,callback,meta)    meta是个字典
* 接受item：response.meta
## 提升scrpy爬取数据的效率

![图片](https://uploader.shimo.im/f/txLZzf56D6TYf5F2.png!thumbnail)

```python
# 最大并发量设为100
CONCURRENT_REQUESTS = 100
# 打印的日志信息登记为REROR只打印报错信息
LOG_LEVEL = 'ERROR'
# 禁用cookie(scrapy 是自动捕获cookie的)
COOKIES_ENABLED = False
# 禁用重试
RETRY_ENABLED = False
# 设置下载超时时间：(超过3秒就不在进行接收response响应了)
DOWNLOAD_TIMEOUT = 3
```
## scrapy的中间件

* 爬虫中间件
* 下载中间件(***)：处于引擎和下载器中间

![图片](https://uploader.shimo.im/f/U4yJLyuyMds2ziWY.png!thumbnail)

  * 作用：批量拦截所有的请求和响应
    * 为什么拦截请求？
      * 篡改请求的头信息(UA伪装等)
      * 修改请求对应的ip(代理ip)
```python
# 中间件中拦截请求方法
# 只拦截正常请求(不能拦截所有的请求)
def process_request(self, request, spider):
    # spider：
    # request：为拦截的正常的请求，也就是经过过滤器筛选后的请求
    # 进行UA伪装
    request.headers['User-Agent'] = random.choice(user_agent_list)
    # 代理IP
    # 可以构建IP池  然后随机拿取ip
    # request.meta['proxy'] = 'http://222.185.77.12:8118'
    return None
```
    * 为什么拦截响应
      * 篡改响应数据，篡改响应对象
```python
# 中间件中的 拦截响应方法
# 参数：
# request：拦截到的请求对象(一个请求对象对应唯一的一个响应对象)由请求对象确定响应对象
# response：拦截到所有的响应对象(1+5+n)
# spider：爬虫类实例化的对象，可以实现爬虫类和中间件类(当前类，也有管道类)的数据交互
def process_response(self, request, response, spider):
    # 爬虫类中的name属性
    # spider.name
    # 我们要拦截到5个板块对应的响应对象，将其替换成5个符合去需求的新的响应对象(有动态加载的数据)进行返回到爬虫类中进行后续解析
    # 1.找出5个板块对应的5个不符合需求的响应对象
    # 因为每个请求对象对应唯一的响应对象，所以我们可以通过请求对象(发送的url)来获取对应的不符合需求的响应对象
    if request.url in spider.model_urls:
        # 5个请求对象对应的响应对象
        # request = request 就是新的响应对象对应的请求对象(就是5个板块对应的请求对象这个值不用变)
        # url: 响应对象对应的请求对象对应的url(就是5大板块对应的请求对象的url)
        # body: 满足需求的响应数据 就是包含ajax数据的整张页面源码数据(可以通过selenium中的page_source获取)
        bro = spider.bro
        bro.get(request.url)
        page_text = bro.page_source # 包含了动态加载的新闻数据，可见即可的
        new_response = HtmlResponse(url=request.url,body=page_text,encoding='utf-8',request=request)
        return new_response
    # 返回(1+n)的响应对象 它们满足需求
    else:return response
```
* selenium在scrapy中的使用流程
  * 在爬虫类中定义一个bro属性，就是实例化的浏览器对象
  * 在爬虫类中重写父类的一个closed(self,spider)!!!重写父类的方法必须加spider!!!!
  * 在中间件中进行浏览器自动化的操作
  * 可以可见即可得的获取ajax数据后返回给爬虫类进行解析
## 专门存储二进制的管道

```python
# 爬虫类
import scrapy
from imgPro.items import ImgproItem
class ImgSpider(scrapy.Spider):
    name = 'img'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://sc.chinaz.com/tupian/siwameinvtupian.html']
    def parse(self, response):
        div_list = response.xpath('//*[@id="container"]/div')
        for div in div_list:
            img_scr = div.xpath('./div/a/img/@src2').extract_first()
            item = ImgproItem()
            item['img_src'] = img_scr
            yield item

# 管道类
import scrapy
from scrapy.pipelines.images import ImagesPipeline
class ImgproPipeline(ImagesPipeline):
    # 是用来对媒体资源进行请求(数据下载),参数item就是接受到的爬虫类提交的item对象
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['img_src'])
    # 指明数据存储的路径(名称 也就是图片的名字)
    def file_path(self, request, response=None, info=None):
        return request.url.split('/')[-1]
    # 如果还有下一个管道类则 将item传递给下一个即将被执行的管道类
    def item_completed(self, results, item, info):
        return item
# setting.py 中加上
# 图片存储文件夹的名称+路径
IMAGES_STORE = './imgLibs'
```
## 分布式

* 概念：需要搭建一个分布式的机群，然后在机群的每一台电脑中执行同一组程序，让其对一个网站的数据进行联合分布爬取。
* 原生的scrapy框架是不可以实现分布式的 为什么呢？
  * 1.调度器不可以被共享
  * 2.管道不能共享，数据不能汇总
* 如何实现分布式
  * scrapy+scarpy_redis实现分布式
* scrapy-redis组件的作用是什么？
  * 提供可以被共享的调度器和管道
  * 特性：数据只可以存储到redis数据库中

![图片](https://uploader.shimo.im/f/Y0pa6TteaM65PZTR.png!thumbnail)

* 分布式的实现流程：
  * pip install scrapy-redis
  * 创建工程
  * cd 到工程目录中
  * 创建爬虫文件(a.创建基于Spider的爬虫文件 b.创建CrawlSpider的爬虫文件)
  * 修改爬虫类
    * 导包：**from **scrapy_redis.spiders **import **RedisCrawlSpider
    * 修改当前爬虫类的父类为RedisCrawlSpider
    * 删除allowed_domains和start_urls
    * 添加一个新属性：redis_key = **'fbsQueue'****，**表示的是可以被共享的调度器队列的名称
    * 编写爬虫类的常规操作
  * settings配置文件的配置
    * UA伪装
    * Rbots协议改为False
    * 开启管道
      * ITEM_PIPELINES = {

    **'scrapy_redis.pipelines.RedisPipeline'**:**400**

** **      }

```python
加入settings配置文件中
# 增加了一个去重容器类的配置，作用使用Redis的set集合来存储请求的指纹数据，从而实现请求去重的持久化（也就是用的scrapy_redis封装好的过滤器,毕竟调度器都是scrapy_redis共享的了)
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
# 使用scrapy-redis组件自己的调度器
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
# 配置调度器是否要持久化，也就是说当爬虫结束了，要不要清空Redis中请求队列和去重指纹的set。如果是True，就表示要持久化存储，就不清空数据，否则清空数据。(就是可以实现增量式已经爬过的数据下次在爬的时候就不会爬了只会爬新的数据)
SCHEDULER_PERSIST = True
```
      * 指定redis数据库
        * REDIS_HOST = 'redis服务器的ip地址' #本机192.168.1.2 就会存到本机的redis数据库中了，其他机器的redis服务器中就没有数据相当于帮忙干活
        * REDIS_PORT = 6379
      * 对redis的配置文件进行配置
        * 关闭默认绑定：56行 # bind 127.0.0.1
        * 关闭保护模式：75行  protected-mode no
      * 启动redis数据库服务端(带配置文件启动)
        * redis-server.exe redis.windows.conf
      * 启动redis数据库客户端
        * redis-cli
      * 启动程序：
        * scrapy runspider xxx.py(爬虫文件名)
      * 向调度器队列中扔如一个起始的url：
        * 队列是存在于redis中的
        * 在开启的redis的客户端中输入：lpush 你设置的redis_key的值 起始url
      * 

