# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import urllib
import json
import re
from meituan_spider.items import MeituanSpiderItem,MeituanRestaurantItem,MeutuanCommentItem
from meituan_spider.items import MeituanCommentNumItem

class MeituanSpider(scrapy.Spider):
    name = "meituan"
    allowed_domains = ["http://waimai.meituan.com/home/wmpmm31wkxvs/"]
    start_urls = [
        "http://waimai.meituan.com/home/wmpmm31wkxvs/"
    ]



    def parse(self, response):
        item = MeituanSpiderItem()
        shopcode = response.xpath("//div/@data-poiid").extract()
        shopname = response.xpath("//div/@data-title").extract()
        arrival_times = response.xpath('//span[@class ="send-time"]/text()').extract()
        start_price = response.xpath('//span[@class="start-price"]/text()').extract()
        poi_score = response.xpath('//span[@class="score-num fl"]/text()').extract()
        bulletin = response.xpath('//div/@data-bulletin').extract()
        item['waimai_shopcode'] = shopcode
        item['waimai_shopname'] = shopname
        item['waimai_arrival_times'] = arrival_times
        item['waimai_start_price'] = start_price
        item['waimai_poi_score'] = poi_score
        item['waimai_shopbulletin'] = bulletin
        for code in shopcode:
            yield scrapy.Request('http://waimai.meituan.com/restaurant/%s'%code,
                                 callback=self.parse_restaurant,dont_filter=True)
            yield scrapy.Request('http://waimai.meituan.com/comment/%s' % code,
                                  callback=self.parse_comment, dont_filter=True)
        for i in range(1,4):
            for j in range(1,21):
                yield scrapy.FormRequest("http://waimai.meituan.com/ajax/comment",
                                   formdata={'wmpoiIdStr': '30340', 'offset':str(j), 'has_content': '0',
                                             'score_grade': str(i)},
                                   callback=self.comment,dont_filter=True)
        yield item

    def parse_restaurant(self, response):
        item = MeituanRestaurantItem()
        address = response.xpath('//div[@class="rest-info-thirdpart"]/text()').extract()[0]
        business_hours = response.xpath('//span[@class="info-detail"]/text()').extract()[0]
        telephone = response.xpath('//div[@class="telephone"]/text()').extract()[0]
        foodname = response.xpath('//span/@title').extract()
        monthlysalse = response.xpath('//div[@class="sold-count ct-lightgrey"]/span/text()').extract()
        foodzai = response.xpath('//span[@class="cc-lightred-new"]/text()').extract()
        foodprice = response.xpath('//div[@class="only"]/text()').extract()
        item['waimai_shopaddress'] = address.strip()
        item['waimai_business_hours'] = business_hours.strip()
        item['waimai_telephone'] = telephone.strip().split('：')[1]
        item['waimai_foodname'] = foodname
        item['waimai_monthlysalse'] = monthlysalse
        item['waimai_foodzai'] = foodzai
        item['waimai_foodprice'] = foodprice
        yield item

    def parse_comment(self,response):
        item = MeituanCommentNumItem()
        comment = response.xpath('//em/text()').extract()
        item['waimai_allcomment_num'] = comment[0].strip('(').strip(')')
        item['waimai_goodcomment_num'] = comment[1].strip('(').strip(')')
        item['waimai_middlecomment_num'] = comment[2].strip('(').strip(')')
        item['waimai_badcomment_num'] = comment[3].strip('(').strip(')')
        yield item

    def comment(self,response):
        item = MeutuanCommentItem()
        sites = response.body.decode()
        sites = sites.strip()
        pattern_comment = re.compile(r"(?:\"comment\":\")([^\"]+)")
        pattern_username = re.compile(r"(?:\"username\":\")([^\"]+)")
        pattern_commentTime = re.compile(r"(?:\"commentTime\":\")([^\"]+)")
        comment = []
        username = []
        commentTime = []
        for m in re.finditer(pattern_username,sites):
            if m:
                username.append(m.group())
        for m in re.finditer(pattern_comment, sites):
            if m:
                comment.append(m.group())
        for m in re.finditer(pattern_commentTime, sites):
            if m:
                commentTime.append(m.group())
        # print(comment)
        # print(commentTime)
        # print(username)
        # print(pattern_username.search(sites).group())
        # comment = pattern_comment.search(sites)
        # print(comment.group(1))
        # username = pattern_username.search(sites)
        # print(username.group(1))
        # commentTime = pattern_commentTime.search(sites)
        # if comment and commentTime and username:
        if comment:
            item['waimai_commentwords'] = comment
        if username:
            item['waimai_commentusername'] = username
        if commentTime:
            item['waimai_commentTime'] =commentTime
        if item:
            yield item