import hashlib
import json
import re
import urllib

import os

import math
import scrapy
import time
from scrapy import Request

from CatchBuilding.items import BuildingsItem


class HaozuSpider(scrapy.spiders.Spider):
    name = "haozu"
    allowed_domains = []
    base_url = 'http://f.haozu.com/building/detail/?building_id='
    base_url1 = '__house%2Fdetail11624951171020012123166215211867959004&cryp' \
                '=eyJjaXR5X2lkIjoiMTciLCJkZXZpY2VJZCI6ImIzNWQ5ZDUwZjBkMzFmNjQiLCJwbGF0Zm9ybSI6IkFuZHJvaWQiLCJhcGlWZX' \
                'JzaW9uIjoiMS4wLjAiLCJhcHBWZXJzaW9uIjoiMS4wIn0%253D'

    def start_requests(self):
        for i in range(35000, 39144):
            url = self.base_url + str(i) + self.base_url1
            yield Request(url, self.parse)

    def parse(self, response):
        basename = response.url.split("/")[-1]
        basename = basename.split("__")[0]
        basename = basename.split("=")[1]  # 房源id
        path = "./return/haozu/"
        filename = path + basename

        # if not os.path.exists(path):
        #     os.makedirs(path)
        #
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        responseBody = json.loads(response.body)
        data = responseBody['data']
        if len(data) > 0:
            m2 = hashlib.md5()
            m2.update(basename.encode("utf8"))
            idMd5 = m2.hexdigest()

            timeStr = time.time()

            buildingId = idMd5 + str(timeStr)
            m2.update(buildingId.encode("utf8"))

            longitudeLatitude = data['longitud_latitude'].split("-")
            longitude = longitudeLatitude[0]
            latitude = longitudeLatitude[1]

            item = BuildingsItem()
            z = []
            if type(data['picture_urls']) == list:
                y = ''
                for index in range(len(data['picture_urls'])):
                    x = data['picture_urls'][index]
                    x = x.split("@")[0]
                    if index == 0:
                        y += x
                    else:
                        y += ',' + x
                    z.append(x)
                data['picture_urls'] = y
            # 经纬度转换
            lonLat = bd09togcj02(float(longitude), float(latitude))
            longitude = lonLat[0]
            latitude = lonLat[1]

            item['original_id'] = basename
            item['building_id'] = m2.hexdigest()
            item['building_name'] = data['building_name']
            item['address'] = data['address']

            item['longitude'] = longitude
            item['latitude'] = latitude
            item['description'] = data['description']
            item['type'] = data['type']
            item['total_floor'] = re.sub("\D", "", data['total_ceng'])
            item['standard_area'] = re.sub("\D", "", data['biaozhun_area'])
            item['covered_area'] = re.sub("\D", "", data['jianzhu_area'])
            item['clear_height'] = re.sub("\D", "", data['jinggao'])
            item['floor_height'] = re.sub("\D", "", data['cenggao'])
            item['room_rate'] = re.sub("\D", "", data['room_rate'])
            item['completion_time'] = data['jungong_time']
            item['developer'] = data['developer']
            item['property_fee'] = data['wuye_fee']
            item['elevators_number'] = data['elevator_total']
            item['parking_number'] = re.sub("\D", "", data['total_chewei'])
            item['conditioning_type'] = data['kongtiao_type']
            item['security_system'] = data['anfang']
            item['property_company'] = data['wuye_company']
            item['public_transport'] = data['public_transport']
            item['picture_urls'] = data['picture_urls']

            item['image_urls'] = z

            key = '8c0989313af10e423fae467f29bfd294'
            location = str(longitude) + ',' + str(latitude)
            url = 'http://restapi.amap.com/v3/geocode/regeo?key=' + key + '&location=' + location
            print(key)
            yield scrapy.Request(url, callback=self.get_location, meta={'item': item})

    def get_location(self, response):
        responseBody = json.loads(response.body)
        item = response.meta['item']
        if responseBody['status'] == "1":
            addressComponent = responseBody['regeocode']['addressComponent']
            item['province'] = '' if type(addressComponent['province']) == list else addressComponent['province']
            item['city'] = '' if type(addressComponent['city']) == list else addressComponent['city']
            item['county'] = '' if type(addressComponent['district']) == list else addressComponent['district']
        print("xxxxxxxxxxxxxxxxxxx")

        print(item)
        return item


def bd09togcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]
