# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
try:
    import urlparse as parse
except:
    from urllib import parse
from scrapy.loader import ItemLoader
from MoguSpider.items import MoguspiderItem, MoguItemLoader
import json
import datetime


class MogujieSpider(scrapy.Spider):
    name = 'mogujie'
    allowed_domains = ['mogujie.com']
    start_urls = ['http://list.mogujie.com/book/clothing/']
    list_url = "http://list.mogujie.com/search?_version=8193&ratio=2%3A3&ad=2&mt=12.848.r82959.3253&_mgjuuid=299dbf70-a402-42ea-bce7-eccf2bcf039b&sort=pop&ptp=1.mayf4._cate.0.ekTwhWS&_b_key=clothing_0.pagani.1.1.pccatenav.0.area-1_fcid-50262_title-%E6%A3%89%E6%9C%8D.1&userId=1a1tyxk&showH=330&cKey=15&fcid={0}&width=220&action=clothing&page=1&showW=220&height=330&_=1513480912696"



    def parse(self, response):
        type_urls = response.css(".type_section dd a::attr(href)").extract()
        type_urls = [parse.urljoin(response.url, url) for url in type_urls]
        for url in type_urls:
            yield Request(url=url,callback=self.parse_detail)

    def parse_detail(self,response):
        parentName= response.css("li.on a::text").extract_first("")
        name = response.css("a.on::text").extract_first("")
        url = response.url
        match_re =  re.match(".*?(\d+).*", url)
        fcid = match_re.group(1)
        moguItem =  MoguspiderItem()

        moguItem["name"] = name
        moguItem["parentName"] = parentName
        moguItem["fcid"] = fcid
        request = scrapy.Request(self.list_url.format(fcid), callback=self.parse_detail2)
        request.meta['item'] = moguItem
        yield request

    def parse_detail2(self,response):
        detail_json = json.loads(response.text)
        detail_url = detail_json['result']['wall']['docs'][0]['link']
        request = scrapy.Request(detail_url, callback=self.parse_detail3)
        request.meta['item'] = response.meta['item']
        yield request

    def parse_detail3(self,response):
        pattern = re.compile('.*"cids":"(.*)","shopId"')
        rawData = pattern.findall(response.text)
        rawData = "".join(rawData)
        moguItem = response.meta['item'];
        moguItem['rawData'] = rawData
        moguItem['createdDate'] = datetime.datetime.now()
        yield moguItem


    def start_requests(self):
        yield Request(url='http://shop.mogujie.com/detail/1llz1c2?acm=3.ms.1_4_1llz1c2.15.1633-22922.2odKRqE4einqc.t_2odKRqE4einqc-lc_3","itemMarks":"-1","acm":"3.ms.1_4_1llz1c2.15.1633-22922.2odKRqE4einqc.t_2odKRqE4einqc-lc_3',callback=self.start_detail)


    def start_detail(self,response):
        yield Request(url='http://list.mogujie.com/book/clothing/', callback=self.start)

    def start(self,response):
        nav_urls = response.css(".nav_list a::attr(href)").extract()
        nav_urls = [parse.urljoin(response.url, url) for url in nav_urls]
        self.start_urls = nav_urls
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True)
