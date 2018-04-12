# -*- coding: utf-8 -*-
import scrapy
import re
from MoguSpider.items import ViviSPiderItem
import datetime

class ViviSpider(scrapy.Spider):
    name = 'hznzcn'
    allowed_domains = ['hznzcn.com']
    start_urls = ['http://www.hznzcn.com/gallery-150-grid.html','http://www.hznzcn.com/gallery-151-grid.html']
    def parse(self, response):
        firstlinks = response.xpath('//*[@id="productclasslist_div"]/div[2]/div/a');
        match_rep = re.match(".*?(\d+).*", response.url)
        if match_rep is not None:
            parentid = match_rep.group(1)
        for link in firstlinks:
            firstName = link.css("a::text").extract_first("")
            if firstName!="全部":
                url = link.css("a::attr(href)").extract_first("")
                match_re = re.match(".*?(\d+).*", url)
                if match_re is not None:
                    pid = match_re.group(1)
                    firstId = pid
                    wsyItem = ViviSPiderItem()
                    wsyItem["Name"] = firstName
                    wsyItem["SourceId"] = firstId
                    wsyItem["ParentId"] = parentid
                    wsyItem['CreatedDate'] = datetime.datetime.now()
                    wsyItem['SyncTime'] = datetime.datetime.now()
                    yield wsyItem
        pass
