# -*- coding: utf-8 -*-
import random

BOT_NAME = 'weibo'

SPIDER_MODULES = ['weibo.spiders']
NEWSPIDER_MODULE = 'weibo.spiders'

# LOG_LEVEL = 'DEBUG'		# log等级设置为debug模式
# LOG_FILE = "mySpider.log"

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 1
# CONCURRENT_REQUESTS = 100
# CONCURRENT_REQUESTS_PER_DOMAIN = 100
# CONCURRENT_REQUESTS_PER_IP = 100
# REACTOR_THREADPOOL_MAXSIZE = 20
DOWNLOAD_TIMEOUT = 30
RANDOMIZE_DOWNLOAD_DELAY = True

REACTOR_THREADPOOL_MAXSIZE = 128
CONCURRENT_REQUESTS = 256
CONCURRENT_REQUESTS_PER_DOMAIN = 256
CONCURRENT_REQUESTS_PER_IP = 256

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 0.25
AUTOTHROTTLE_TARGET_CONCURRENCY = 128
AUTOTHROTTLE_DEBUG = True

RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 401, 403, 404, 405, 406, 407, 408, 409, 410, 429]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'weibo.middlewares.IPProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 101,
    'weibo.middlewares.UserAgentMiddleware': 543,
    'weibo.middlewares.CookiesMiddleware': 743,
    # 'weibo.middlewares.RandomCookiesMiddleware': 743,
}

ITEM_PIPELINES = {
    'weibo.pipelines.JsonWriterPipeline': 300,
    # 'weibo.pipelines.MysqlPipeline': 302,
    # 'weibo.pipelines.TXTPipeline': 301,
    # 'weibo.pipelines.PostgresPipeline': 302,
}

MYSQL_HOST = ''
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DATABASE = ''


PG_HOST=''
PG_PORT=5432
PG_USER=''
PG_PASSWORD=''
PG_DATABASE=''