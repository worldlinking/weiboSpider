# weiboSpider
可自定义关键词获取一定时间范围内几乎所有数据的微博爬虫项目

本项目综合了https://github.com/nghuyong/WeiboSpider.git 和 https://github.com/dataabc/weibo-search.git 这两个项目的优点
1、https://github.com/nghuyong/WeiboSpider.git 实现了多种字段的快速获取，但是存在只能获取50页数据的问题
2、https://github.com/dataabc/weibo-search.git 通过切分时间片段可以获取时间范围内所有数据，突破了50页数据的问题，但由于是通过解析页面结构获取的数据，所以效率不高且字段少
3、本项目综合了前两者优点，可以快速获取多种字段，且不受50页的限制

本项目仅作学习参考或科研辅助，如有侵权立删
