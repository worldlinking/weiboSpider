# weiboSpider

可自定义关键词获取一定时间范围内几乎所有数据的微博爬虫项目

本项目综合了https://github.com/nghuyong/WeiboSpider.git 和 https://github.com/dataabc/weibo-search.git 这两个项目的优点

1、https://github.com/nghuyong/WeiboSpider.git 实现了多种字段的快速获取，但是存在只能获取50页数据的问题

2、https://github.com/dataabc/weibo-search.git 通过切分时间片段可以获取时间范围内所有数据，突破了50页数据的问题，但由于是通过解析页面结构获取的数据，所以效率不高且字段少

3、本项目综合了前两者优点，可以快速获取多种字段，且不受50页的限制

本项目仅作学习参考或科研辅助，如有侵权立删

# 使用流程
**1、获取cookie值**

登录weibo.com，F12打开浏览器开发者工具network，然后获取微博网页cookie值并将其替换掉weibo/cookie.txt的内容

**2、运行程序**

在控制台输入命令语句： scrapy crawl search -a task_id=1  -a keyword=考试 -a startdate=2022-08-01 -a enddate=2022-08-02
 
*** task-id:爬虫任务id，类型为int，如1，2，3

*** keyword：爬取关键词，可以为单个关键词，也可以为多个关键词，如"考试"，或，“考试,期末”

*** startdate：爬取起始时间，如"2022-08-01"

*** enddate：爬取起始时间，如"2022-08-02"

默认存储为json数据，保存至output文件夹下，如需修改请见4.额外补充

**3、输出结果**

输出字段有{"_id", "mblogid", "created_at", "geo", "ip_location", "reposts_count", "comments_count", "attitudes_count", "source", "content", "pic_urls", "pic_num":, "isLongText", "user", "video", "url", "keyword", "crawl_time"}

其中geo是地理坐标信息，表示用户打卡地点的经纬度信息，只有10%爬取数据包含geo数据，其余均为空

ip数据是从2022年5月开始有的，所以之前时间的微博数据的ip均为空

具体数据说明详见output文件夹示例，最新测试时间为2023/10/25仍可正常运行，后期如果报错可能是网页结构发生变化，需要修改spiders/search.py

**4、额外补充**

本项目设置了多种数据存储方式，包含txt,json,Mysql,Postgres的存储，通过设置settings.py中的ITEM_PIPELINES即可开启各种存储

如采用Mysql,Postgres存储，则需在setting.py中添加数据库连接配置