import json
import re
from urlparse import urlparse

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LinkSpider(CrawlSpider):
    name = 'Link'
    allowed_domains = ['1point3acres.com']
    # Only crawl forum, thread and user sites
    rules = (
        Rule(LinkExtractor(allow=('bbs/forum.*html', 'bbs/space.*html', 'bbs/thread.*')), callback='parse_link'),
    )
    count = 0
    # Regular expression tmp
    forum = re.compile(r'forum.*html')
    thread = re.compile(r'thread.*')
    user = re.compile(r'space.*html')

    def start_requests(self):
        url = 'http://www.1point3acres.com/bbs/'
        cookies = json.load(open('cookies.json', 'r'))
        return [Request(url, callback=self.parse_link, cookies=cookies, meta={'cookies': cookies})]

    def parse_link(self, response):
        links = response.xpath('//*[@id="hd"]/following::a/@href').extract()
        for link in links:
            link_category = self.link_type(link)
            if link_category == 'out':
                continue
            else:
                yield {'url': link, 'category': link_category}
                yield Request(
                    link,
                    callback=self.parse_link,
                    cookies=response.meta['cookies'],
                    meta={'cookies': response.meta['cookies']}
                )

    def link_type(self, link):
        # Assign a category to the link
        url = urlparse(link)
        groups = url.path.strip('/').split('/')
        if groups[0] == 'bbs' and len(groups) > 1:
            if re.match(self.thread, groups[1]):
                return 'thread'
            elif re.match(self.user, groups[1]):
                return 'user'
            elif re.match(self.forum, groups[1]):
                return 'forum'
            else:
                return 'out'
        else:
            return 'out'
