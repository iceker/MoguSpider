# -*- coding: utf-8 -*-
import scrapy


class ZwdSpider(scrapy.Spider):
    name = 'zwd'
    allowed_domains = ['17zwd.com']
    start_urls = ['http://hz.17zwd.com/sks.htm?cateid=0']

    def parse(self, response):
        firstlinks = response.css(".promote-market-nav-item-right:nth-child(2) a::text");
        for link in firstlinks:
            url = link.css("a::attr(href)").extract_first("")
            match_re = re.match(".*?(\d+).*", url)
            if match_re is not None:
                pid = match_re.group(1)
                firstId = pid
                firstName = link.css("a::text").extract_first("")
                wsyItem = WsySPiderItem()
                wsyItem["Name"] = firstName
                wsyItem["SourceId"] = firstId
                wsyItem["ParentId"] = "0"
                wsyItem['CreatedDate'] = datetime.datetime.now()
                wsyItem['SyncTime'] = datetime.datetime.now()
                yield wsyItem
                url = parse.urljoin(response.url, url)
                request = scrapy.Request(parse.urljoin(response.url, url), callback=self.parse2)
                request.meta['parentId'] = firstId
                yield request
        pass
