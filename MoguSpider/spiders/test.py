# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['mogujie.com']
    start_urls = ['http://shop.mogujie.com/detail/1kj33me?acm=3.ms.1_4_1kj33me.15.1633-22922.05NORqE2aMkly.t_05NNORqE2aMkly-lc_3']

    def parse(self, response):
        request = scrapy.Request(response.url,callback=self.parse2)
        yield request

    def parse2(self,response):
        pass
