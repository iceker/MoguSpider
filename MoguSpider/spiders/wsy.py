# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from scrapy.http import Request
from MoguSpider.items import WsySPiderItem
import datetime

class WsySpider(scrapy.Spider):
    name = 'wsy'
    allowed_domains = ['wsy.com']
    start_urls = ['https://www.wsy.com/category.htm/']
    list_url = ""
    def parse(self, response):
        firstlinks = response.css(".type_section:nth-child(1) li a");
        for link in firstlinks:
            url = link.css("a::attr(href)").extract_first("")
            match_re = re.match(".*?(\d+).*", url)
            if match_re is not None:
                pid = match_re.group(1)
                firstId = pid
                firstName = link.css("a::text").extract_first("")
                wsyItem = WsySPiderItem()
                wsyItem["Name"] = firstName
                wsyItem["SourceId"] = firstId
                wsyItem["ParentId"] = "0"
                wsyItem['CreatedDate'] = datetime.datetime.now()
                wsyItem['SyncTime'] = datetime.datetime.now()
                yield wsyItem
                url = parse.urljoin(response.url, url)
                request = scrapy.Request(parse.urljoin(response.url, url), callback=self.parse2)
                request.meta['parentId'] = firstId
                yield request
        pass
    def parse2(self,response):
        secondlinks = response.css(".type_section:nth-child(2) li a")
        for link in secondlinks:
            url = link.css("a::attr(href)").extract_first("")
            match_re = re.match(".*(\d+).*", url)
            pid = match_re.group(1)
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