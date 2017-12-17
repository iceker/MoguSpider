# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


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


