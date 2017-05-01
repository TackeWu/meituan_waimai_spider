# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#店家
class MeituanSpiderItem(scrapy.Item):
    waimai_shopcode = scrapy.Field()
    waimai_shopname = scrapy.Field()
    waimai_arrival_times = scrapy.Field()
    waimai_start_price = scrapy.Field()
    waimai_poi_score = scrapy.Field()
    waimai_shopbulletin = scrapy.Field()

#菜单
class MeituanRestaurantItem(scrapy.Item):
    waimai_shopaddress = scrapy.Field()
    waimai_business_hours = scrapy.Field()
    waimai_telephone = scrapy.Field()
    waimai_foodname = scrapy.Field()
    waimai_monthlysalse = scrapy.Field()
    waimai_foodzai = scrapy.Field()
    waimai_foodprice = scrapy.Field()
    waimai_foodcategory = scrapy.Field()
#评论数
class MeituanCommentNumItem(scrapy.Item):
    waimai_allcomment_num = scrapy.Field()
    waimai_goodcomment_num = scrapy.Field()
    waimai_middlecomment_num = scrapy.Field()
    waimai_badcomment_num = scrapy.Field()
#评论
class MeutuanCommentItem(scrapy.Item):
    waimai_commentusername = scrapy.Field()
    waimai_commentTime = scrapy.Field()
    waimai_commentwords = scrapy.Field()

