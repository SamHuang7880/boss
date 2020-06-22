# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class BossPipeline:
   
    def __init__(self):
        with open("D:\\111\zhihu.csv","a",newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["txt"])
    
    def process_item(self, item, spider):
        txt = item['txt']
        with open("D:\\111\zhihu.csv","a",newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([txt])
        return item