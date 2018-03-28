# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime




class MoguspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    parentName = scrapy.Field()
    fcid = scrapy.Field()
    rawData = scrapy.Field()
    createdDate = scrapy.Field()

class MoguItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()


class SuningSpiderItem(scrapy.Item):
    Id = scrapy.Field()
    Name = scrapy.Field()
    SourceId = scrapy.Field()
    ParentId = scrapy.Field()
    CreatedDate = scrapy.Field()
    SyncTime = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
            insert into suningCategories(name, sourceId, ParentId, createdDate, syncTime
              ) VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            self["Name"], self["SourceId"],self["ParentId"],self["CreatedDate"],self["SyncTime"]
        )

        return insert_sql, params

class WsySPiderItem(scrapy.Item):
    Id = scrapy.Field()
    Name = scrapy.Field()
    SourceId = scrapy.Field()
    ParentId = scrapy.Field()
    CreatedDate = scrapy.Field()
    SyncTime = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
            insert into wsycategory(name, sourceId, ParentId, createdDate, syncTime
              ) VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            self["Name"], self["SourceId"],self["ParentId"],self["CreatedDate"],self["SyncTime"]
        )

        return insert_sql, params
