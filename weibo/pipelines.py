# -*- coding: utf-8 -*-
import datetime
import json
import os.path
import time
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class JsonWriterPipeline(object):
    """
    写入json文件的pipline
    """

    def __init__(self):
        self.file = None
        if not os.path.exists('../output'):
            os.mkdir('../output')

    def process_item(self, item, spider):
        """
        处理item
        """
        if not self.file:
            now = datetime.datetime.now()
            file_name = spider.name + "_" + now.strftime("%Y%m%d%H%M%S") + '.jsonl'
            self.file = open(f'../output/{file_name}', 'wt', encoding='utf-8')
        item['crawl_time'] = int(time.time())
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        self.file.flush()
        return item


class MysqlPipeline(object):
    def create_database(self, mysql_config):
        """创建MySQL数据库"""
        import pymysql
        sql = """CREATE DATABASE IF NOT EXISTS %s DEFAULT
            CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci""" % settings.get(
            'MYSQL_DATABASE', 'weibo')
        db = pymysql.connect(**mysql_config)
        cursor = db.cursor()
        cursor.execute(sql)
        db.close()

    def create_table(self):
        """创建MySQL表"""
        sql = """
                CREATE TABLE IF NOT EXISTS weibo (
                id varchar(20) NOT NULL,
                bid varchar(12) NOT NULL,
                user_id varchar(20),
                screen_name varchar(30),
                text varchar(2000),
                article_url varchar(100),
                longitude FLOAT,
                latitude FLOAT,
                location varchar(100),
                attitudes_count INT,
                comments_count INT,
                reposts_count INT,
                created_at DATETIME,
                pics varchar(3000),
                video_url varchar(1000),
                PRIMARY KEY (id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
        self.cursor.execute(sql)

    def open_spider(self, spider):
        try:
            import pymysql
            mysql_config = {
                'host': settings.get('MYSQL_HOST', 'localhost'),
                'port': settings.get('MYSQL_PORT', 3306),
                'user': settings.get('MYSQL_USER', 'root'),
                'password': settings.get('MYSQL_PASSWORD', '123456'),
                'charset': 'utf8mb4'
            }
            self.create_database(mysql_config)
            mysql_config['db'] = settings.get('MYSQL_DATABASE', 'weibo')
            self.db = pymysql.connect(**mysql_config)
            self.cursor = self.db.cursor()
            self.create_table()
        except ImportError:
            spider.pymysql_error = True
        except pymysql.OperationalError:
            spider.mysql_error = True

    def process_item(self, item, spider):
        temp_data = dict(item)
        data = {
            "id": temp_data['_id'],
            "bid": temp_data['mblogid'],
            "user_id": temp_data['user']['_id'],
            "screen_name": temp_data['user']['nick_name'],
            "text": temp_data['content'],
            "article_url": temp_data['url'],
            "longitude": temp_data['geo']['coordinates'][1] if temp_data['geo'] else None,
            "latitude": temp_data['geo']['coordinates'][0] if temp_data['geo'] else None,
            "location": temp_data['ip_location'],
            "reposts_count": temp_data['reposts_count'],
            "comments_count": temp_data['comments_count'],
            "attitudes_count": temp_data['attitudes_count'],
            "created_at": temp_data['created_at'],
            "pics": temp_data['pic_urls'],
            "video_url": temp_data.get('video', None),
            "task_id": temp_data['task_id']
        }
        data['pics'] = ','.join(data['pics'])
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = """INSERT INTO {table}({keys}) VALUES ({values}) ON
                     DUPLICATE KEY UPDATE""".format(table='weibo',
                                                    keys=keys,
                                                    values=values)
        update = ','.join([" {key} = {key}".format(key=key) for key in data])
        sql += update
        # try:
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        # except Exception:
        #     self.db.rollback()
        return item

    def close_spider(self, spider):
        try:
            self.db.close()
        except Exception:
            pass


class PostgresPipeline(object):
    def open_spider(self, spider):
        try:
            import psycopg2
            mysql_config = {'host': settings.get('PG_HOST', 'localhost'), 'port': settings.get('PG_PORT', 5432),
                            'user': settings.get('PG_USER', 'root'), 'password': settings.get('PG_PASSWORD', '123456'),
                            'database': settings.get('PG_DATABASE', 'weibo')}
            self.db = psycopg2.connect(**mysql_config)
            self.cursor = self.db.cursor()
        except ImportError:
            spider.pymysql_error = True
        except psycopg2.OperationalError:
            spider.mysql_error = True

    def process_item(self, item, spider):
        temp_data = dict(item)
        data = {
            "id": temp_data['_id'],
            "bid": temp_data['mblogid'],
            "user_id": temp_data['user']['_id'],
            "screen_name": temp_data['user']['nick_name'],
            "text": temp_data['content'],
            "article_url": temp_data['url'],
            "longitude": temp_data['geo']['coordinates'][1] if temp_data['geo'] else None,
            "latitude": temp_data['geo']['coordinates'][0] if temp_data['geo'] else None,
            "location": temp_data['ip_location'],
            "reposts_count": temp_data['reposts_count'],
            "comments_count": temp_data['comments_count'],
            "attitudes_count": temp_data['attitudes_count'],
            "created_at": temp_data['created_at'],
            "pics": temp_data['pic_urls'],
            "video_url": temp_data.get('video', None),
            "task_id": temp_data['task_id']
        }
        data['pics'] = ','.join(data['pics'])
        key = ["\"" + key + "\"" for key in data.keys()]
        keys = ', '.join(key)
        values = ', '.join(['%s'] * len(data))
        sql = """INSERT INTO {table}({keys}) VALUES ({values})""".format(table='weibo',
                                                                         keys=keys,
                                                                         values=values)
        # update = ','.join([" {key} = {key}".format(key=key) for key in data])
        # sql += update
        # print('--------',sql)
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()
        except Exception:
            self.db.rollback()
        return item

    def close_spider(self, spider):
        try:
            self.db.close()
        except Exception:
            pass
