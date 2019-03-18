# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BuildingsItem(scrapy.Item):
    # define the fields for your item here like:
    original_id = scrapy.Field()  # 写字楼id
    building_id = scrapy.Field()  # 写字楼id
    building_name = scrapy.Field()  # 写字楼名称
    province = scrapy.Field()  # 省
    city = scrapy.Field()  # 市
    county = scrapy.Field()  # 区
    address = scrapy.Field()  # 地址
    longitude = scrapy.Field()  # 经度
    latitude = scrapy.Field()  # 纬度
    description = scrapy.Field()  # 描述
    type = scrapy.Field()  # 类型
    total_floor = scrapy.Field()  # 总层数
    standard_area = scrapy.Field()  # 标准面积
    covered_area = scrapy.Field()  # 建筑面积

    clear_height = scrapy.Field()  # 净高
    floor_height = scrapy.Field()  # 层高
    room_rate = scrapy.Field()  # 得房率
    completion_time = scrapy.Field()  # 竣工时间

    developer = scrapy.Field()  # 开发商
    property_fee = scrapy.Field()  # 物业费
    elevators_number = scrapy.Field()  # 电梯数量
    parking_number = scrapy.Field()  # 车位数
    conditioning_type = scrapy.Field()  # 空调；类型
    security_system = scrapy.Field()  # 安防系统
    property_company = scrapy.Field()  # 物业公司
    public_transport = scrapy.Field()  # 公共交通

    picture_urls = scrapy.Field()  # 图片

    image_urls = scrapy.Field()  # 图片
    images = scrapy.Field()
    image_paths = scrapy.Field()  # 图片


    pass
