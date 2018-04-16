# -*- coding: utf-8 -*-
import scrapy
import re
from MoguSpider.items import YhdSPiderItem
import datetime

class YhdSpider(scrapy.Spider):
    name = 'yhd'
    allowed_domains = ['search.yhd.com']
    start_urls = ['http://search.yhd.com/c1315-0-0',#服饰内衣
                  'http://search.yhd.com/c11729-0-0',#鞋靴
                  'http://search.yhd.com/c9192-0-0',#医药保健
                  'http://search.yhd.com/c738-0-0',#家用电器
                  'http://search.yhd.com/c6728-0-0',#汽车用品
                  'http://search.yhd.com/c652-0-0',#数码
                  'http://search.yhd.com/c670-0-0',#电脑、办公

                  ]
    list_url = "http://search.yhd.com/c{0}-0-0"
    def parse(self, response):
        first = response.xpath('//*[@id="comParamId"]/div[2]/div[2]/div/div/ul/li[2]/span/a')
        firstName = first.css("a::text").extract_first("")
        url = first.css("a::attr(href)").extract_first("")
        match_re = re.match(".*?(\d+).*", url)
        if match_re is not None:
            pid = match_re.group(1)
            wsyItem = YhdSPiderItem()
            wsyItem["Name"] = firstName
            wsyItem["SourceId"] = pid
            wsyItem["ParentId"] = "0"
            wsyItem['CreatedDate'] = datetime.datetime.now()
            wsyItem['SyncTime'] = datetime.datetime.now()
            yield wsyItem
        secondlinks = response.xpath('//*[@id="group_attr"]/div[1]/div/div[2]/ul/li/a')
        for link in secondlinks:
            secondUrl = link.css("a::attr(href)").extract_first("")
            match_re = re.match(".*?(\d+).*", secondUrl)
            if match_re is not None:
                secondpid = match_re.group(1)
                secondName = link.css("a span::text").extract_first("")
                wsyItem = YhdSPiderItem()
                wsyItem["Name"] = secondName
                wsyItem["SourceId"] = secondpid
                wsyItem["ParentId"] = pid
                wsyItem['CreatedDate'] = datetime.datetime.now()
                wsyItem['SyncTime'] = datetime.datetime.now()
                yield wsyItem
            request = scrapy.Request(self.list_url.format(secondpid), callback=self.parse2)
            request.meta['parentId'] = secondpid
            yield request
        pass

    def parse2(self,response):
        links = response.xpath('//*[@id="group_attr"]/div[1]/div/div[2]/ul/li/div/a')
        for link in links:
            url = link.css("a::attr(href)").extract_first("")
            match_re = re.match(".*?(\d+).*", url)
            if match_re is not None:
                pid = match_re.group(1)
                name = link.css("a::text").extract_first("")
                wsyItem = YhdSPiderItem()
                wsyItem["Name"] = name
                wsyItem["SourceId"] = pid
                wsyItem["ParentId"] = response.meta['parentId']
                wsyItem['CreatedDate'] = datetime.datetime.now()
                wsyItem['SyncTime'] = datetime.datetime.now()
                yield wsyItem
        pass