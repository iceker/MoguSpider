# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from scrapy.http import Request
from MoguSpider.items import WsySPiderItem
import datetime

class ViviSpider(scrapy.Spider):
    name = 'vivi'
    allowed_domains = ['www.vvic.com']
    start_urls = ['https://www.vvic.com/gz/list/index.html/']

    def parse(self, response):
        firstlinks = response.css(".nav-pid a");
        for link in firstlinks:
            pid = link.css("a::attr(data-val)").extract_first("")
            firstId = pid
            firstName = link.css("a::text").extract_first("")
            if firstName != "全部":
                url = parse.urljoin(response.url, url)
                request = scrapy.Request(parse.urljoin(response.url, url), callback=self.parse2)
                request.meta['parentId'] = firstId
                yield request

    def parse2(self,response):
        secondlinks = response.css(".catid .nav-category a")
        for link in secondlinks:
            pid = link.css("a::attr(data-val)").extract_first("")
            secondid = pid
            secondName = link.css("a::text").extract_first("")
            if secondid!='0':
                wsyItem = WsySPiderItem()
                wsyItem["Name"] = secondName
                wsyItem["SourceId"] = secondid
                wsyItem["ParentId"] = response.meta['parentId']
                wsyItem['CreatedDate'] = datetime.datetime.now()
                wsyItem['SyncTime'] = datetime.datetime.now()
                yield wsyItem

        pass
