# -*- coding: utf-8 -*-
import re
import json
from bs4 import BeautifulSoup as BS
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ForumCrawler.items import BoardItem, PostItem


class ForumSpider(CrawlSpider):
    name = 'Forum'
    allowed_domains = ['1point3acres.com']
    rules = (
        # Board page
        Rule(LinkExtractor(allow=('bbs/forum.*html',), restrict_xpaths='//*[@id="hd"]/following::*'),
             callback='parse_board', follow=True, process_request='append_cookies'),
        # Post page(subject)
        Rule(LinkExtractor(allow=('bbs/thread-\d+-1-',), restrict_xpaths='//*[@id="hd"]/following::*'),
             callback='parse_post', follow=True, process_request='append_cookies'),
        # User page
        Rule(LinkExtractor(allow=('bbs/space.*html',), restrict_xpaths='//*[@id="hd"]/following::*'),
             callback='parse_user', follow=True, process_request='append_cookies'),
        # Post page(replies)
        Rule(LinkExtractor(allow=('bbs/thread-\d+-1\d', 'bbs/thread-\d+-[2-9]'),
             restrict_xpaths='//*[@id="hd"]/following::*'), follow=True, process_request='append_cookies')
    )
    # Get cookies from a json file
    start_urls = ['http://www.1point3acres.com/bbs/']
    with open('cookies.json', 'r') as cookies_file:
        cls_cookies = json.load(cookies_file)

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
                pages = -1
                name = ''
            else:
                pages = 1
        item = BoardItem()
        item['url'] = response.url
        item['name'] = name
        item['pages'] = pages
        yield item

    def parse_post(self, response):
        url = response.url
        name = response.xpath('//span[@id="thread_subject"]/text()').extract_first(default='')
        author_name = response.xpath('//div[@class="authi"]/a/text()').extract_first(default='')
        author_url = response.xpath('//div[@class="authi"]/a/@href').extract_first(default='')
        try:
            pv, replies = [int(num) for num in
                           response.xpath('//div[@class="hm ptn"]/span[@class="xi1"]/text()').extract()]
        except:
            pv, replies = -1, -1
        date_time = response.xpath('//div[@class="authi"]/em').re_first(r'\d+-\d+-\d+\s\d+:\d+:\d+')

        # Eliminate trash nodes using bs4, maybe there is an alternative solution
        raw_content = response.xpath('//td[@class="t_f"]').extract_first(default='')
        raw_content_soup = BS(raw_content, 'lxml')
        [s.extract() for s in raw_content_soup(['i', 'span'])]
        [s.extract() for s in raw_content_soup.select('.jammer')]
        [s.extract() for s in raw_content_soup.select('.a_pr')]
        [s.extract() for s in raw_content_soup.select('.attach_nopermission')]
        [s.extract() for s in raw_content_soup.select('ignore_js_op')]
        content = raw_content_soup.text.strip()

        item = PostItem()
        item['url'] = url
        item['name'] = name
        item['author_url'] = author_url
        item['author_name'] = author_name
        item['pv'] = pv
        item['replies'] = replies
        item['date_time'] = date_time
        item['content'] = content
        yield item

    def parse_user(self, response):
        # TODO parse_user
        pass
