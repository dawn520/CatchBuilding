# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

import math

import scrapy

from CatchBuilding.mysqlPipelines.DB import DB


class CatchBuildingPipeline(object):

    def process_item(self, item, spider):
        print(222222)
        print("开始处理")
        db = DB()
        data = {}

        for a in item:
            if item[a] == "":
                item[a] = ""
            if item[a] == "--":
                item[a] = ""
            data[a] = item[a]
        if data['completion_time'] == '':
            data['completion_time'] = time.strftime("%Y-%m-%d", time.localtime())
        if data['total_floor'] == '':
            data['total_floor'] = 0
        if data['floor_height'] == '':
            data['floor_height'] = 0
        if data['parking_number'] == '':
            data['parking_number'] = 0
        if data['room_rate'] == '':
            data['room_rate'] = 0

        if data['standard_area'] == '':
            data['standard_area'] = 0
        if data['covered_area'] == '':
            data['covered_area'] = 0
        if data['clear_height'] == '':
            data['clear_height'] = 0
        if data['floor_height'] == '':
            data['floor_height'] = 0

        data['created_at'] = data['updated_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(data)
        db.insert([data])


class CatchBuildingAddressPipeline(object):
    def process_item(self, item, spider):
        db = DB()
        data = {
            'address': item['address'],
            'original_id': item['original_id'],
        }
        db.insert(data, 'update')
