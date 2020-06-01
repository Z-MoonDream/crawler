# -*- coding: utf-8 -*-

# Scrapy settings for fbsPro project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'fbsPro'

SPIDER_MODULES = ['fbsPro.spiders']
NEWSPIDER_MODULE = 'fbsPro.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.50'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'fbsPro (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# LOG_LEVEL = 'ERROR'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'fbsPro.middlewares.FbsproSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'fbsPro.middlewares.FbsproDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'fbsPro.pipelines.FbsproPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline':400
}

# 增加了一个去重容器类的配置，作用使用Redis的set集合来存储请求的指纹数据，从而实现请求去重的持久化（也就是用的scrapy_redis封装好的过滤器,毕竟调度器都是scrapy_redis共享的了)
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
# 使用scrapy-redis组件自己的调度器
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
# 配置调度器是否要持久化，也就是说当爬虫结束了，要不要清空Redis中请求队列和去重指纹的set。如果是True，就表示要持久化存储，就不清空数据，否则清空数据。(就是可以实现增量式已经爬过的数据下次在爬的时候就不会爬了只会爬新的数据)
SCHEDULER_PERSIST = True
# 本机192.168.1.2 就会存到本机的redis数据库中了，其他机器的redis服务器中就没有数据相当于帮忙干活
REDIS_HOST = '192.168.1.2'
REDIS_PORT = 6379