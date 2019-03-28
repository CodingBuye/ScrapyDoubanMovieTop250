# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'  # 爬虫名
    # 允许的域名，不在这个域名的不会被抓取
    allowed_domains = ['movie.douban.com']
    # 入口的url，扔到调度器里面去
    start_urls = ['https://movie.douban.com/top250']

    # 默认解析方法
    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for movie_item in movie_list:
            # 导入items文件
            douban_item = DoubanItem()
            # 写详细的xpath，进行数据的解析
            douban_item['serial_number'] = movie_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = movie_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            # 多行时的数据处理
            content = movie_item.xpath(".//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
            for content_item in content:
                content_s = "".join(content_item.split())
                douban_item['introduce'] = content_s
            douban_item['star'] = movie_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = movie_item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describe'] = movie_item.xpath(".//p[@class='quote']/span/text()").extract_first()
            # 通过yield将第一页的数据传到itemPipeline去
            yield douban_item
        # 解析下一页规则，取后页的xpath
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            # 传到调度器中
            yield scrapy.Request("https://movie.douban.com/top250"+next_link, callback=self.parse)
