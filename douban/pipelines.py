# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from douban.settings import mongo_host, mongo_port, mongo_db_name, mongo_db_connection


class DoubanPipeline(object):
    def __init__(self):
        host = mongo_host
        port = mongo_port
        db_name = mongo_db_name
        sheet_name = mongo_db_connection
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[db_name]
        self.post = mydb[sheet_name]

    # 需要在settings里开启itemPipelines
    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
