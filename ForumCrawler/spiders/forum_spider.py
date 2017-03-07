# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import json
from bs4 import BeautifulSoup as BS
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request

from ForumCrawler.items import BoardItem, PostItem, UserItem
from ForumCrawler.custom import acres_settings as settings


class ForumSpider(CrawlSpider):
    name = 'Forum'
    custom_settings = {
        'JOBDIR': 'job',
        'LOG_PATH': settings.LOG_PATH,
        'LOG_FILE': settings.LOG_FILE,
        'MYSQL_DB': settings.MYSQL_DB,
        'TABLE_INFO': settings.TABLE_INFO,
    }
    allowed_domains = ['1point3acres.com']
    rules = (
        # Board page(first page)
        Rule(LinkExtractor(allow=('bbs/forum-\d+-1.',), restrict_xpaths='//*[@id="hd"]/following::*'),
             callback='parse_board', follow=True, process_request='append_cookies'),

        # Board page(other pages) DO NOT PARSE
        Rule(LinkExtractor(allow=('bbs/forum-\d+-1\d', 'bbs/forum-\d+-[2-9]'),
             restrict_xpaths='//*[@id="hd"]/following::*'), follow=True, process_request='append_cookies'),

        # Board page(other pages，another url format) DO NOT PARSE
        Rule(LinkExtractor(allow=('bbs/forum.php?mod=forumdisplay'),
             restrict_xpaths='//*[@id="hd"]/following::*'), follow=True, process_request='append_cookies'),

        # Post page(first page)
        Rule(LinkExtractor(allow=('bbs/thread-\d+-1-',), restrict_xpaths='//*[@id="hd"]/following::*'),
             callback='parse_post', follow=True, process_request='append_cookies'),

        # Post page(other replies) DO NOT PARSE
        Rule(LinkExtractor(allow=('bbs/thread-\d+-1\d', 'bbs/thread-\d+-[2-9]'),
             restrict_xpaths='//*[@id="hd"]/following::*'), follow=True, process_request='append_cookies'),

        # User page
        Rule(LinkExtractor(allow=('bbs/space-uid-\d+',), restrict_xpaths='//*[@id="hd"]/following::*'),
             callback='parse_user', follow=True, process_request='append_cookies'),
    )
    # Get cookies from a json file
    start_urls = ['http://www.1point3acres.com/bbs/']
    with open('cookies.json', 'r') as cookies_file:
        cls_cookies = json.load(cookies_file)

    # 重写Rule类的append_cookies函数，本来是直接return request，现在加上cookies再return，实现利用cookies的login
    def append_cookies(self, request):
        request.cookies = self.cls_cookies
        return request

    def parse_board(self, response):
        name = response.xpath('//*[@class="xs2"]/a/text()').extract_first()
        try:
            pages_str = re.search('\d+', response.xpath('//label/span/text()').extract_first()).group(0)
            pages = int(pages_str)
        except:
            if not name:
                self.logger.error('parse error: Board error\nBoard url = {}'.format(response.url))
                pages = -1
                name = ''
            else:
                pages = 1
        item = BoardItem()
        item['board_url'] = response.url
        item['board_name'] = name
        item['pages'] = pages
        yield item

    def parse_post(self, response):
        item = PostItem()
        item['post_url'] = response.url
        item['post_name'] = response.xpath('//span[@id="thread_subject"]/text()').extract_first(default='')

        try:
            board_url = response.xpath('//div[@id="pt"]/div/a/@href').extract()[-2]
            board_name = response.xpath('//div[@id="pt"]/div/a/text()').extract()[-2]
        except:
            board_url = ''
            board_name = ''
            self.logger.error('parse error: Post error\nPost url = {}'.format(response.url))
        item['board_url'] = board_url
        item['board_name'] = board_name

        item['user_name'] = response.xpath('//div[@class="authi"]/a/text()').extract_first(default='')
        item['user_url'] = response.xpath('//div[@class="authi"]/a/@href').extract_first(default='')
        try:
            pv, replies = [int(num) for num in
                           response.xpath('//div[@class="hm ptn"]/span[@class="xi1"]/text()').extract()]
        except:
            pv, replies = -1, -1
        date_time = response.xpath('//div[@class="authi"]/em').re_first(r'\d+-\d+-\d+\s\d+:\d+:\d+')
        item['pv'] = pv
        item['replies'] = replies
        item['date_time'] = date_time

        # Delete abundant nodes using BeautifulSoup
        raw_content = response.xpath('//td[@class="t_f"]').extract_first(default='')
        raw_content_soup = BS(raw_content, 'lxml')
        [s.extract() for s in raw_content_soup(['i', 'span'])]
        [s.extract() for s in raw_content_soup.select('.jammer')]
        [s.extract() for s in raw_content_soup.select('.a_pr')]
        [s.extract() for s in raw_content_soup.select('.attach_nopermission')]
        [s.extract() for s in raw_content_soup.select('ignore_js_op')]
        content = raw_content_soup.text.strip()
        item['content'] = content

        # Parse context
        result = response.xpath('//div[@class="pcb"]/u').xpath('string(.)').extract_first(default='')
        bkg = '\n'.join(response.xpath('//div[@class="pcb"]/li').xpath('string(.)').extract())
        if result or bkg:
            item['context'] = result + '\n\n' + bkg
        else:
            item['context'] = ''

        yield item

    def parse_user(self, response):
        item = UserItem()        
        item['user_url'] = response.url
        item['user_name'] = response.xpath(r'//h2[@class="xs2"]/a/text()').extract_first(default='')
        try:
            item['uid'] = re.search(r'.*uid-(\d+)', response.url).group(1)
            profile_url = response.xpath(r'//div[@id="nv"]/ul/li/a/@href').extract()[-1]
        except:
            # Fail to get profile web page
            # self.logger.error('parse error: User profile error\nUser url = {}'.format(response.url))
            pass
        else:
            yield Request(url=profile_url, callback=self.parse_user_profile, meta={'item': item})

    def parse_user_profile(self, response):
        # The user profile page is not structured, therefore I saved them in text format
        item = response.meta['item']
        profile_list = response.css('.pf_l').extract()
        item['profile'] = '\n'.join(profile_list)
        yield item



