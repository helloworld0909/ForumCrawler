# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import requests
import scrapy
from scrapy.http import Request

from ForumCrawler.util.cookies import cookies_to_dict
from ForumCrawler.items import UserItem, OfferItem
from ForumCrawler.custom import gter_settings as settings


class GterSpider(scrapy.Spider):
    name = 'gter'
    custom_settings = {
        'LOG_PATH': settings.LOG_PATH,
        'LOG_FILE': settings.LOG_FILE,
        'MYSQL_DB': settings.MYSQL_DB,
        'TABLE_INFO': settings.TABLE_INFO
    }
    allowed_domains = ['gter.net']
    with open(os.getcwd() + '/cookies.txt', 'r') as cookies_file:
        cookies = cookies_to_dict(cookies_file.read())

    def start_requests(self):
        print self.settings['MYSQL_DB']
        start_url = 'http://bbs.gter.net/'
        res = requests.get(url=start_url, cookies=self.cookies)

        selector = scrapy.Selector(text=res.text)
        link_list = selector.xpath('//div[@id="category_454"]/table/tr/td/h2/a')
        url_list = link_list.xpath('./@href').extract()
        offer_type_list = link_list.xpath('./text()').extract()
        assert len(url_list) == len(offer_type_list)
        for url, offer_type in zip(url_list, offer_type_list):
            yield Request(url=url, callback=self.parse_offer_rank, cookies=self.cookies,
                          meta={'cookiejar': 1, 'offer_type': offer_type})

    def parse_offer_rank(self, response):
        try:
            url = response.xpath('//a[contains(text(), "Offer榜")]/@href').extract()[-1]
        except:
            raise Exception('Parse offer rank error: {}'.format(response.url))
        yield Request(url=url, callback=self.parse_offer,
                      meta={'cookiejar': 1, 'offer_type': response.meta['offer_type']})

    def parse_offer(self, response):
        pass
