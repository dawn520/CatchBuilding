# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib

import scrapy
import time
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

from CatchBuilding.mysqlPipelines.DB import DB


class BuildingsImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        url = request.meta['image_url']
        ext = url.split(".")[-1]
        m2 = hashlib.md5()
        path = 'uploads/buildings/' + time.strftime("%Y/%m/%d", time.localtime()) + '/'
        filename = url + path
        m2.update(filename.encode("utf8"))
        filename = m2.hexdigest()
        path += filename
        path += '.' + ext
        return path

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'image_url': image_url})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            print('failed')
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        db = DB()
        data = []
        for x in image_paths:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            data.append({'building_id_md5': item['building_id'], 'filename': x, 'created_at': now, 'updated_at': now})
            print(data)
        db.insert(data, 'images')
        return item
