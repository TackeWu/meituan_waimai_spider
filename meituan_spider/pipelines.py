# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from meituan_spider.items import  MeituanSpiderItem,MeutuanCommentItem,MeituanCommentNumItem,MeituanRestaurantItem
import json
from meituan_spider import settings
class MeituanSpiderPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient('localhost',27017)
        db = connection["meituan"]
        self.meituan_MSI = db["meituan_MSI"]
        self.meituan_MRI = db['meituan_MRI']
        self.meituan_MCNI = db['meituan_MCNI']
        self.meituan_MCI  = db['meituan_MCI']

    def process_item(self, item, spider):
        print('MongoDBItem',item)

        if isinstance(item,MeituanSpiderItem):
            print('MeituanSpiderItem True')
            try :
                self.meituan_MSI.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item,MeituanRestaurantItem):
            print('MeituanRestaurantItem,True')
            try :
                self.meituan_MRI.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item,MeituanCommentNumItem):
            print('MeituanCommentNumItem,True')
            try:
                self.meituan_MCNI.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item,MeutuanCommentItem):
            print('MeutuanCommentItem,True')
            try:
                self.meituan_MCI.insert(dict(item))
            except Exception:
                pass
        else :
            print("unable output")
        return item