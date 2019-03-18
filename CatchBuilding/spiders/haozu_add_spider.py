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
    """
    写字楼地址爬取
    """
    name = "haozuA"
    allowed_domains = []
    base_url = 'https://m.haozu.com/sz_xzl_'

    def start_requests(self):
        # for i in range(1, 39144):
        for i in range(17910, 39144):
            url = self.base_url + str(i) + '/'
            yield Request(url, self.parse)

    def parse(self, response):
        basename = response.url.split("/")[-2]
        buildId = basename.split("_")[-1]
        print(buildId)
        htmlP = response.css('div[class=mapBuildingWrap]>p:first-child').extract()
        print(buildId + htmlP[0])
        address = htmlP[0].split("]")
        print(buildId + address[-1])
        address = address[-1].split("<")
        print(buildId + address[0])

        #
        # path = "./return/haozuAdd/"
        # filename = path + buildId + address[0]
        #
        # if not os.path.exists(path):
        #     os.makedirs(path)
        #
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        if len(address[0]) > 0:
            item = BuildingsItem()
            item['address'] = address[0]
            item['original_id'] = buildId

            yield item
