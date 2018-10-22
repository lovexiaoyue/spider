# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class AmazonPipeline(object):
    def process_item(self, item, spider):
        return item


class MobilePipeline(object):
    """将数据保存到MongoDB数据库中"""
    def open_spider(self, spider):
        """spider开启时建立数据库连接"""
        if spider.name == 'amazon':
            self.clinet = MongoClient()
            self.mobile = self.clinet['amazon']['mobile']

    def process_item(self, item, spider):
        """将数据保存"""
        if spider.name == 'amazon':
            t = self.mobile.find_one({'sku_url':item['sku_url']})
            if t is None:
                self.mobile.save(dict(item))

    def close_spider(self, spider):
        """spider关闭时断开数据库连接"""
        if spider.name == 'amazon':
            self.clinet.close()
