# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from scrapy.http import Request
from MoguSpider.items import WsySPiderItem
import datetime

class ZwdSpider(scrapy.Spider):
    name = 'zwd'
    allowed_domains = ['17zwd.com']
    start_urls = ['http://hz.17zwd.com/sks.htm?cateid=0']

    def parse(self, response):
        firstlinks = response.css(".promote-market-nav-item-right:nth-child(2) a").extract();
        length = len(firstlinks)
        for link in firstlinks:
            url = link.css("a::attr(href)").extract_first("")
            match_re = re.match(".*?(\d+).*", url)
            if match_re is not None:
                pid = match_re.group(1)
                firstId = pid
                firstName = link.css("a::text").extract_first("")
                url = parse.urljoin(response.url, url)
                request = scrapy.Request(parse.urljoin(response.url, url), callback=self.parse2)
                request.meta['parentId'] = firstId
                yield request
        pass

        # request = scrapy.Request(parse.urljoin(response.url, "http://gz.17zwd.com/sks.htm?cateid=50008906"), callback=self.parse2)
        # request.meta['parentId'] = 50008906
        # yield request

    def parse2(self, response):
        item = response.css(".promote-market-nav-item-right:nth-child(2) .promote-market-nav-item-link.server-clicked");
        if(len(item)):
            pass
        firstlinks = response.css("div.promote-market-nav-item-right:nth-child(2) a").extract();
        length = len(firstlinks)
        for link in firstlinks:
            url = link.css("a::attr(href)").extract_first("")
            match_re = re.match(".*?(\d+).*", url)
            if match_re is not None:
                pid = match_re.group(1)
                firstId = pid
                firstName = link.css("a::text").extract_first("")
                parentId= response.meta['parentId']
                url = parse.urljoin(response.url, url)
                request = scrapy.Request(parse.urljoin(response.url, url), callback=self.parse2)
                request.meta['parentId'] = firstId
                yield request

        pass
