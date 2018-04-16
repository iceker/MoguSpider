# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['vvic.com']
    start_urls = ['http://qq.com']

    def parse(self, response):
        id = 5773623
        request = scrapy.Request("https://app.vvic.com/v1/item?id=" + str(id), callback=self.parsea)
        yield request

    def parsea(self,response):
        id=11
        pass
