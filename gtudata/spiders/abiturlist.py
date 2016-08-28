# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.loader import ItemLoader
from scrapy.selector import HtmlXPathSelector, Selector
from gtudata.items import GtudataItem


class AbiturLoader(ItemLoader):
    default_output_processor = Identity()


class AbiturlistSpider(CrawlSpider):
    name = "abiturlist"
    allowed_domains = ["oreluniver.ru"]
    start_urls = ["http://oreluniver.ru/abits?src=all_postupil"]

    rules = (
        #Rule(SgmlLinkExtractor(allow=('spec_id=', 'spec_title=')), follow=True),
        Rule(LinkExtractor(allow=('spec_id=04.03.01')), callback='parse_item'),
    )

    def parse_item(self, response):
        hxs = Selector(response)
        all = hxs.xpath("//tr[position()>1]")
        pg_spec = hxs.xpath("//div[@class='page-content']/b/div/text()").extract()[0].strip()
        for fld in all:
            Item = GtudataItem()
            FIO = fld.xpath("./td[2]/p/text()").extract()[0].split()
            Item['family'] = FIO[0]
            Item['name'] = FIO[1]
            Item['surname'] = FIO[2]
            Item['spec'] = fld.xpath("./td[last()]/p/text()").extract()[0]
            ball = fld.xpath("string(./td[3]/p)").extract()[0]
            Item['ball'] = ball
            Item['url'] = response.url
            Item['pagespec'] = pg_spec
            yield Item


