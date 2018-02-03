# -*- coding: utf-8 -*-
import scrapy


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['list.suning.com']
    start_urls = ['https://list.suning.com/']

    def parse(self, response):
        pass
