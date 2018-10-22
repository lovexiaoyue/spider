# -*- coding: utf-8 -*-

# Scrapy settings for Amazon project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Amazon'

SPIDER_MODULES = ['Amazon.spiders']
NEWSPIDER_MODULE = 'Amazon.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
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
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'Amazon.middlewares.AmazonSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# 下载中间键
DOWNLOADER_MIDDLEWARES = {
   # 'Amazon.middlewares.AmazonDownloaderMiddleware': 543,
   # 'Amazon.middlewares.RefererMiddleware': 543,
   'Amazon.middlewares.ALMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'Amazon.pipelines.AmazonPipeline': 300,

   'Amazon.pipelines.MobilePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 2.1  配置去重类: 用于把请求的指纹数据存储到Redis的set集合中
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 2.1 配置调度器类: 用于把请求对象序列化为二进制数据, 存储到Redis的zset集合中
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 2.2 配置去重数据和请求数据是否要持久化:
#  True就表示当前程序结束了, 请求和指纹数据依然会保存在Redis数据中
#  False: 程序结束的时候, 就会删除Redis数据中的请求和指纹数据.
SCHEDULER_PERSIST = True
# 2.3(可选) 配置使用Redis管道, 把抓取到的数据存储到Redis数据看中
# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline': 400,
# }
# 2.4 配置Redis数据库连接
# 2.4.1: 方式1: 分别配置IP和端口号
# REDIS_HOST = '127.0.0.1'
# REDIS_PORT = 6379

# 2.4.2: 方式2: 配置RedisURL (reids数据库)
REDIS_URL = 'redis://127.0.0.1:6379/10'