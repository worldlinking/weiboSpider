# encoding: utf-8
import random
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


# 随机请求头
class UserAgentMiddleware(object):
    def __init__(self):
        self.user_agents_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
            'Opera/8.0 (Windows NT 5.1; U; en)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
            'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
        ]

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agents_list)
        request.headers['User-Agent'] = user_agent


class CookiesMiddleware(object):
    def __init__(self):
        import os
        current_path = os.getcwd()
        with open(current_path+'/weibo/cookie.txt', 'rt', encoding='utf-8') as f:
            COOKIE = f.readlines()
            print(COOKIE, '-------------')
        self.COOKIE_LIST = [d.strip() for d in COOKIE]

    def process_request(self, request, spider):
        cookie = self.COOKIE_LIST[0]
        request.headers['Cookie'] = cookie


# 设置随机cookie
class RandomCookiesMiddleware(object):
    def __init__(self):
        import pymysql
        mysql_config = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'port': settings.get('MYSQL_PORT', 3306),
            'user': settings.get('MYSQL_USER', 'root'),
            'password': settings.get('MYSQL_PASSWORD', '123456'),
            'db': settings.get('MYSQL_DATABASE', 'weibo'),
            'charset': 'utf8mb4'
        }
        self.db = pymysql.connect(**mysql_config)
        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT cookie FROM cookie")
        result = self.cursor.fetchall()
        self.COOKIE_LIST = []
        for item in result:
            self.COOKIE_LIST.append(item[0])

    def process_request(self, request, spider):
        cookie = random.choice(self.COOKIE_LIST)
        # cookie=self.COOKIE_LIST[0]
        request.headers['Cookie'] = cookie


class IPProxyMiddleware(object):
    """
    代理IP中间件
    """

    @staticmethod
    def fetch_proxy():
        """
        获取一个代理IP
        """
        # You need to rewrite this function if you want to add proxy pool
        # the function should return an ip in the format of "ip:port" like "12.34.1.4:9090"
        return None

    def process_request(self, request, spider):
        """
        将代理IP添加到request请求中
        """
        proxy_data = self.fetch_proxy()
        if proxy_data:
            current_proxy = f'http://{proxy_data}'
            spider.logger.debug(f"current proxy:{current_proxy}")
            request.meta['proxy'] = current_proxy
