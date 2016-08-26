# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.loader import ItemLoader
from scrapy.selector import HtmlXPathSelector, Selector
from gtudata.items import SpecItem


class SpecSpider(CrawlSpider):
    name = "speclist"
    allowed_domains = ["oreluniver.ru"]
    start_urls = ["http://oreluniver.ru/abits?src=all_postupil"]

    rules = (
        #Rule(SgmlLinkExtractor(allow=('spec_id=', 'spec_title=')), follow=True),
        Rule(LinkExtractor(allow = ('src=all_postupil')), callback='parse_item'),
    )

    def parse_item(self, response):
        hxs = Selector(response)
        all = hxs.xpath('//a[contains(@href, "spec_id")]/text()').extract()  #
        print 'test'
        for fld in all:
            txt = fld.strip()
            Item = SpecItem()
            Item['SpecName'] = txt[9:]
            Item['spec'] = txt[:8]
            yield Item