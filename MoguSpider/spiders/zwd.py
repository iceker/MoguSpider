# -*- coding: utf-8 -*-
import scrapy


class ZwdSpider(scrapy.Spider):
    name = 'zwd'
    allowed_domains = ['17zwd.com']
    start_urls = ['http://hz.17zwd.com/sks.htm?cateid=0']

    def parse(self, response):
        pass
