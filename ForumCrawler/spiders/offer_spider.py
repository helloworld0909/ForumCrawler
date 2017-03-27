# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re

import requests
import scrapy
from scrapy.http import Request

from ForumCrawler.custom import gter_settings as settings
from ForumCrawler.items import OfferItem
from ForumCrawler.util.cookies import cookies_to_dict
from ForumCrawler.util.general import wash

dictionary = {
    'TOEFL:': 'toefl',
    'IELTS:': 'ielts',
    'GRE:': 'gre',
    'SUB': 'sub',
    'GMAT:': 'gmat',
    '本科成绩和算法、排名:': 'undergraduate_gpa',
    '本科学校档次:': 'undergraduate_school',
    '本科专业:': 'undergraduate_major',
    '研究生成绩和算法、排名:': 'master_gpa',
    '研究生学校档次:': 'master_school',
    '研究生专业:': 'master_major',
    '其他说明:': 'other_info',

    '申请学校:': 'school',
    '学位:': 'degree',
    '专业:': 'major',
    '申请结果:': 'result',
    '入学年份:': 'enroll_year',
    '入学学期:': 'enroll_semester',
    '通知时间:': 'notice_time',
}


class GterSpider(scrapy.Spider):
    name = 'gter'
    custom_settings = {
        'LOG_PATH': settings.LOG_PATH,
        'LOG_FILE': settings.LOG_FILE,
        'MYSQL_DB': settings.MYSQL_DB,
        'TABLE_INFO': settings.TABLE_INFO
    }
    allowed_domains = ['gter.net']
    with open(os.getcwd() + '/' + settings.COOKIES_FILE, 'r') as cookies_file:
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
            yield Request(url=url, callback=self.parse_offer_list_first_page, cookies=self.cookies,
                          meta={'cookiejar': 1, 'offer_type': offer_type})

    def parse_offer_list_first_page(self, response):
        # return first page of an offer list
        try:
            url = response.xpath('//a[contains(text(), "Offer榜")]/@href').extract()[-1]
        except:
            raise Exception('Parse offer rank error: {}'.format(response.url))
        yield Request(url=url, callback=self.parse_offer_list,
                      meta={'cookiejar': 1, 'offer_type': response.meta['offer_type']})

    def parse_offer_list(self, response):
        # return rest of the offer lists using the page information on the first page
        max_page = re.search('\d+', response.xpath('//a[@class="last"]/text()').extract_first(default='0')).group(0)
        for page in range(1, int(max_page) + 1):
            url = response.url + '&page={}'.format(str(page))
            yield Request(url=url, callback=self.request_offer,
                          meta={'cookiejar': 1, 'offer_type': response.meta['offer_type']})

    def request_offer(self, response):
        # input an offer list, return request of each offer post
        urls = response.xpath('//tbody[starts-with(@id, "normalthread_")]/tr/th/a/@href').extract()
        for url in urls:
            yield Request(url=url, callback=self.parse_offer,
                          meta={'cookiejar': 1, 'offer_type': response.meta['offer_type']})

    def parse_offer(self, response):
        # Parse offer and user info
        user_url = response.xpath('//div[@class="authi"]/a/@href').extract_first(default='')
        try:
            uid = int(re.search('uid-(\d+).html', user_url).group(1))
        except:
            uid = -1

        item = OfferItem()
        item['url'] = response.url
        item['offer_type'] = response.meta['offer_type']
        item['uid'] = uid

        # User profile
        profile_selector = response.xpath('//div[@class="typeoption"]/table[@summary="个人情况"]/tbody/tr')
        for tr in profile_selector:
            label = tr.xpath('./th/text()').extract_first(default='')
            key = dictionary.get(label, None)
            if key:
                item[key] = wash(tr.xpath('./td/text()').extract_first(default='').strip())

        # Offer info
        offer_selector = response.xpath('//div[@class="typeoption"]/table[contains(@summary, "offer")]/tbody/tr')
        for tr in offer_selector:
            label = tr.xpath('./th/text()').extract_first(default='')
            key = dictionary.get(label, None)
            if key:
                try:
                    item[key] = wash(tr.xpath('./td').xpath('string(.)').extract_first(default=''))
                except:
                    continue

        yield item

