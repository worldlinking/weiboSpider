import scrapy
import os
import json
import re
from scrapy import Spider, Request
# from spiders.common import parse_tweet_info, parse_long_tweet
from datetime import datetime, timedelta
import dateutil.parser


class SearchSpider(scrapy.Spider):
    name = 'search'

    def __init__(self, task_id=None, keyword=None,startdate=None,enddate=None, *args, **kwargs):
        super(SearchSpider, self).__init__(*args, **kwargs)
        # super().__init__(**kwargs)
        self.base_url = "https://s.weibo.com/"
        self.start_date = startdate  # 格式为 年-月-日-小时, 2022-10-01-0 表示2022年10月1日0时
        self.end_date = enddate  # 格式为 年-月-日-小时, 2022-10-07-23 表示2022年10月7日23时
        self.task_id = int(task_id)
        self.keyword = keyword

    def start_requests(self):
        """
        爬虫入口
        """
        # 这里keywords可替换成实际待采集的数据
        keywords = self.keyword.split(',')
        print('-------------------------------------',keywords)
        start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(self.end_date,
                                     '%Y-%m-%d') + timedelta(days=1)

        start_str = start_date.strftime('%Y-%m-%d') + '-0'
        end_str = end_date.strftime('%Y-%m-%d') + '-0'

        is_search_with_specific_time_scope = True  # 是否在指定的时间区间进行推文搜索
        for keyword in keywords:
            if is_search_with_specific_time_scope:
                url = f"https://s.weibo.com/weibo?q={keyword}&timescope=custom%3A{start_str}%3A{end_str}&page=1"

            else:
                url = f"https://s.weibo.com/weibo?q={keyword}&page=1"
            base_url = 'https://s.weibo.com/weibo?q=%s' % keyword
            yield Request(url, callback=self.parse,
                          meta={'keyword': keyword, 'base_url': base_url, 'start_time': start_str[:-2],
                                'end_time': end_str[:-2]})

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        # 获取所有页码
        print('--------------------------------------', response.request.headers)
        keyword = response.meta.get('keyword')
        is_empty = response.xpath(
            '//div[@class="card card-no-result s-pt20b40"]')
        page_count = len(response.xpath('//ul[@class="s-scroll"]/li'))
        print('页码数:', len(response.xpath('//ul[@class="s-scroll"]/li')))
        start_time = response.meta.get('start_time')
        end_time = response.meta.get('end_time')
        if is_empty:
            print('当前页面搜索结果为空')
        elif page_count < 46:
            html = response.text
            tweet_ids = re.findall(r'\d+/(.*?)\?refer_flag=1001030103_\'\)">复制微博地址</a>', html)
            for tweet_id in tweet_ids:
                url = f"https://weibo.com/ajax/statuses/show?id={tweet_id}"
                yield Request(url, callback=self.parse_tweet, meta=response.meta)
            next_page = re.search('<a href="(.*?)" class="next">下一页</a>', html)
            if next_page:
                url = "https://s.weibo.com" + next_page.group(1)
                yield Request(url, callback=self.parse_page, meta=response.meta)
        else:
            start_date = datetime.strptime(start_time, '%Y-%m-%d')
            end_date = datetime.strptime(end_time, '%Y-%m-%d')
            while start_date <= end_date:
                start_str = start_date.strftime('%Y-%m-%d') + '-0'
                start_date = start_date + timedelta(days=1)
                end_str = start_date.strftime('%Y-%m-%d') + '-0'
                url = f"https://s.weibo.com/weibo?q={keyword}&timescope=custom%3A{start_str}%3A{end_str}&page=1"
                # 获取一天的搜索结果
                yield Request(url, callback=self.parse_by_day, meta={'keyword': keyword,
                                                                     'date': start_str[:-2]})

    def parse_by_day(self, response):
        """以天为单位筛选"""
        keyword = response.meta.get('keyword')
        date = response.meta.get('date')
        is_empty = response.xpath(
            '//div[@class="card card-no-result s-pt20b40"]')
        page_count = len(response.xpath('//ul[@class="s-scroll"]/li'))
        if is_empty:
            print('当前页面搜索结果为空')
        elif page_count < 46:
            html = response.text
            tweet_ids = re.findall(r'\d+/(.*?)\?refer_flag=1001030103_\'\)">复制微博地址</a>', html)
            for tweet_id in tweet_ids:
                url = f"https://weibo.com/ajax/statuses/show?id={tweet_id}"
                yield Request(url, callback=self.parse_tweet, meta=response.meta)
            next_page = re.search('<a href="(.*?)" class="next">下一页</a>', html)
            if next_page:
                url = "https://s.weibo.com" + next_page.group(1)
                yield Request(url, callback=self.parse_page, meta=response.meta)
        else:
            start_date_str = date + '-0'
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d-%H')
            for i in range(1, 25):
                start_str = start_date.strftime('%Y-%m-%d-X%H').replace(
                    'X0', 'X').replace('X', '')
                start_date = start_date + timedelta(hours=1)
                end_str = start_date.strftime('%Y-%m-%d-X%H').replace(
                    'X0', 'X').replace('X', '')
                url = f"https://s.weibo.com/weibo?q={keyword}&timescope=custom%3A{start_str}%3A{end_str}&page=1"
                # 获取一小时的搜索结果
                yield Request(url, callback=self.parse_by_hour, meta={'keyword': keyword,
                                                                      'start_time': start_str,
                                                                      'end_time': end_str})

    def parse_by_hour(self, response):
        """以小时为单位筛选"""
        keyword = response.meta.get('keyword')
        start_time = response.meta.get('start_time')
        end_time = response.meta.get('end_time')
        is_empty = response.xpath(
            '//div[@class="card card-no-result s-pt20b40"]')
        page_count = len(response.xpath('//ul[@class="s-scroll"]/li'))
        if is_empty:
            print('当前页面搜索结果为空')
        elif page_count < 46:
            html = response.text
            tweet_ids = re.findall(r'\d+/(.*?)\?refer_flag=1001030103_\'\)">复制微博地址</a>', html)
            for tweet_id in tweet_ids:
                url = f"https://weibo.com/ajax/statuses/show?id={tweet_id}"
                yield Request(url, callback=self.parse_tweet, meta=response.meta)
            next_page = re.search('<a href="(.*?)" class="next">下一页</a>', html)
            if next_page:
                url = "https://s.weibo.com" + next_page.group(1)
                yield Request(url, callback=self.parse_page, meta=response.meta)
        else:
            url = f"https://s.weibo.com/weibo?q={keyword}&timescope=custom%3A{start_time}%3A{end_time}&page=1"
            # 获取一小时的搜索结果
            yield Request(url, callback=self.parse_page, meta={'keyword': keyword})

    def parse_page(self, response, **kwargs):
        html = response.text
        tweet_ids = re.findall(r'\d+/(.*?)\?refer_flag=1001030103_\'\)">复制微博地址</a>', html)
        for tweet_id in tweet_ids:
            url = f"https://weibo.com/ajax/statuses/show?id={tweet_id}"
            yield Request(url, callback=self.parse_tweet, meta=response.meta)
        next_page = re.search('<a href="(.*?)" class="next">下一页</a>', html)
        if next_page:
            url = "https://s.weibo.com" + next_page.group(1)
            yield Request(url, callback=self.parse_page, meta=response.meta)

    def parse_tweet(self, response):
        """
        解析推文
        """
        data = json.loads(response.text)
        item = parse_tweet_info(data)
        item['keyword'] = response.meta['keyword']
        item['task_id'] = self.task_id
        if item['isLongText']:
            url = "https://weibo.com/ajax/statuses/longtext?id=" + item['mblogid']
            yield Request(url, callback=parse_long_tweet, meta={'item': item})
        else:
            yield item


def parse_time(s):
    """
    Wed Oct 19 23:44:36 +0800 2022 => 2022-10-19 23:44:36
    """
    return dateutil.parser.parse(s).strftime('%Y-%m-%d %H:%M:%S')


def parse_user_info(data):
    """
    解析用户信息
    """
    # 基础信息
    user = {
        "_id": str(data['id']),
        "avatar_hd": data['avatar_hd'],
        "nick_name": data['screen_name'],
        "verified": data['verified'],
    }
    # 额外的信息
    keys = ['description', 'followers_count', 'friends_count', 'statuses_count',
            'gender', 'location', 'mbrank', 'mbtype', 'credit_score']
    for key in keys:
        if key in data:
            user[key] = data[key]
    if 'created_at' in data:
        user['created_at'] = parse_time(data.get('created_at'))
    if user['verified']:
        user['verified_type'] = data['verified_type']
        if 'verified_reason' in data:
            user['verified_reason'] = data['verified_reason']
    return user


def parse_tweet_info(data):
    """
    解析推文数据
    """
    ip_location = data.get('region_name', None)
    ip = None
    if ip_location:
        ip = ip_location.split()[1]
    tweet = {
        "_id": str(data['mid']),
        "mblogid": data['mblogid'],
        "created_at": parse_time(data['created_at']),
        "geo": data['geo'],
        "ip_location": ip,
        "reposts_count": data['reposts_count'],
        "comments_count": data['comments_count'],
        "attitudes_count": data['attitudes_count'],
        "source": data['source'],
        "content": data['text_raw'].replace('\u200b', '').replace('\n', ',').replace(' ', ''),
        "pic_urls": ["https://wx1.sinaimg.cn/orj960/" + pic_id for pic_id in data.get('pic_ids', [])],
        "pic_num": data['pic_num'],
        'isLongText': False,
        "user": parse_user_info(data['user']),
    }
    if 'page_info' in data and data['page_info'].get('object_type', '') == 'video':
        tweet['video'] = data['page_info']['media_info']['mp4_720p_mp4']
    tweet['url'] = f"https://weibo.com/{tweet['user']['_id']}/{tweet['mblogid']}"
    if 'continue_tag' in data and data['isLongText']:
        tweet['isLongText'] = True
    return tweet


def parse_long_tweet(response):
    """
    解析长推文
    """
    data = json.loads(response.text)['data']
    item = response.meta['item']
    item['content'] = data['longTextContent'].replace('\u200b', '').replace('\n', ',').replace(' ', '')
    yield item
