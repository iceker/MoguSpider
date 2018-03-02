# -*- coding: utf-8 -*-
import scrapy
import re
from MoguSpider.items import SuningSpiderItem
import datetime


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['list.suning.com']
    start_urls = ['https://list.suning.com/']

    def parse(self, response):
        search_divs = response.css(".search-main > div")
        for search_div in search_divs:
            firstId = search_div.css("div::attr(id)").extract_first("")
            firstName = search_div.css("h2::text").extract_first("")
            suningItem = SuningSpiderItem()
            suningItem["Name"] = firstName
            suningItem["SourceId"] = firstId
            suningItem["ParentId"] = "0"
            suningItem['CreatedDate'] = datetime.datetime.now()
            suningItem['SyncTime'] = datetime.datetime.now()
            yield suningItem
            boxs = search_div.css(".title-box")
            for box in boxs:
                secondUrl = box.css(".t-left a::attr(href)").extract_first("")
                martch_re = re.match(".*-(\d+)-.*",secondUrl);
                secondId = martch_re.group(1)
                secondName = box.css(".t-left a::attr(title)").extract_first("")
                rights = box.css(".t-right a")
                for right in rights:
                    thirdUrl = right.css("a::attr(href)").extract_first("")
                    martch_re = re.match(".*-(\d+)-.*",thirdUrl);
                    thirdId = martch_re.group(1)
                    thirdName = right.css("a::text").extract_first("")
        pass
