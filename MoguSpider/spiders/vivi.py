# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from scrapy.http import Request
from MoguSpider.items import WsySPiderItem
import datetime
import json

class ViviSpider(scrapy.Spider):
    name = 'vivi'
    allowed_domains = ['vvic.com']
    start_urls = ['https://www.vvic.com/gz/list/index.html/']
    list_url = "https://www.vvic.com/gz/list/index.html?merge=1&pid={0}&vcid={1}"

    def parse(self, response):
        firstlinks = response.css(".nav-pid a");
        for link in firstlinks:
            pid = link.css("a::attr(data-val)").extract_first("")
            url = link.css("a::attr(href)");
            firstId = pid
            firstName = link.css("a::text").extract_first("")
            if firstName != "全部":
                request = scrapy.Request(self.list_url.format(firstId,0), callback=self.parse2)
                request.meta['parentId'] = firstId
                yield request

    def parse2(self,response):
        secondlinks = response.css(".catid .nav-category a")
        for link in secondlinks:
            pid = link.css("a::attr(data-val)").extract_first("")
            secondid = pid
            request = scrapy.Request(self.list_url.format(response.meta['parentId'], secondid), callback=self.parse3)
            request.meta['parentId'] = response.meta['parentId']
            yield request
        pass

    def parse3(self,response):
        item = response.xpath('//*[@class="goods-list clearfix"]/ul/li[1]/div/div[1]/a')
        url = item.css("a::attr(href)").extract_first()
        martch_re = re.match(".*?(\d+).*", url)
        itemid = martch_re.group(1)
        request = scrapy.Request("https://app.vvic.com/v1/item?id="+itemid,callback=self.parse4)
        request.meta['parentId'] = response.meta['parentId']
        yield request
        pass
    def parse4(self,response):
        detail_json = json.loads(response.text)
        cid = detail_json['data']['item']['cid']
        pass
