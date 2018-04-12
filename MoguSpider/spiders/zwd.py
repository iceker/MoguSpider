# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from scrapy.http import Request
from MoguSpider.items import ZwdSPiderItem
import datetime

class ZwdSpider(scrapy.Spider):
    name = 'zwd'
    allowed_domains = ['17zwd.com']
    start_urls = ['http://gz.17zwd.com/sks.htm?cateid=0']

    def parse(self, response):
        firstlinks = response.xpath('//*[@id="J_MarkServer"]/div[2]/div[2]/div[2]/a');
        length = len(firstlinks)
        for link in firstlinks:
            url = link.css("a::attr(href)").extract_first("")
            match_re = re.match(".*?(\d+).*", url)
            if match_re is not None:
                pid = match_re.group(1)
                firstId = pid
                firstName = link.css("a::text").extract_first("")
                zwdItem = ZwdSPiderItem()
                zwdItem["Name"] = firstName
                zwdItem["SourceId"] = firstId
                zwdItem["ParentId"] = 0
                zwdItem['CreatedDate'] = datetime.datetime.now()
                zwdItem['SyncTime'] = datetime.datetime.now()
                yield zwdItem
                request = scrapy.Request(parse.urljoin(response.url, url), callback=self.parse2)
                request.meta['parentId'] = firstId
                url = parse.urljoin(response.url, url)
                request = scrapy.Request(parse.urljoin(response.url, url), callback=self.parse2)
                request.meta['parentId'] = firstId
                yield request
        pass

        # request = scrapy.Request(parse.urljoin(response.url, "http://gz.17zwd.com/sks.htm?cateid=16"), callback=self.parse2)
        # request.meta['parentId'] = 16
        # yield request

    def parse2(self, response):
        item = response.xpath('//*[@id="J_MarkServer"]/div[2]/div[2]/div[2]/a[@class="promote-market-nav-item-link server-clicked"]').extract()
        if len(item):
            return
        firstlinks = response.xpath('//*[@id="J_MarkServer"]/div[2]/div[2]/div[2]/a')
        length = len(firstlinks)
        for link in firstlinks:
            url = link.css("a::attr(href)").extract_first("")
            match_re = re.match(".*?(\d+).*", url)
            if match_re is not None:
                pid = match_re.group(1)
                firstId = pid
                firstName = link.css("a::text").extract_first("").strip()
                if firstName!="<< 返回上级":
                    parentId= response.meta['parentId']
                    url = parse.urljoin(response.url, url)
                    zwdItem = ZwdSPiderItem()
                    zwdItem["Name"] = firstName
                    zwdItem["SourceId"] = firstId
                    zwdItem["ParentId"] = response.meta['parentId']
                    zwdItem['CreatedDate'] = datetime.datetime.now()
                    zwdItem['SyncTime'] = datetime.datetime.now()
                    request = scrapy.Request(parse.urljoin(response.url, url), callback=self.parse2)
                    request.meta['parentId'] = firstId
                    yield zwdItem
                    yield request
        pass
