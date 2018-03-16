# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CatchbuildingItem(scrapy.Item):
    # define the fields for your item here like:
    building_name = scrapy.Field()  # 写字楼名称
    longitude = scrapy.Field()      # 经度
    latitude = scrapy.Field()       # 纬度
    description = scrapy.Field()    # 描述
    type = scrapy.Field()           # 类型

    pass
