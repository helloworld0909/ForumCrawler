import re
from urlparse import urlparse

import scrapy
from bs4 import BeautifulSoup

from LinkCrawler.items import LinkItem


class LinkSpider(scrapy.Spider):
    name = 'Link'
    # allowed_domains = ['1point3acres.com']
    start_urls = []
    # regular expression cache
    forum = re.compile(r'forum.*html')
    thread = re.compile(r'thread.*')
    php = re.compile(r'forum.*php')
    user = re.compile(r'space.*html')
    home = re.compile(r'home.*php')

    def parse(self, response):
        links = []
        for each in BeautifulSoup(response.body, 'lxml').select('a'):
            if 'href' in each.attrs:
                links.append(each['href'])

        for link in links:
            link_category = self.link_type(link)
            if link_category == 'out':
                continue
            else:
                link_item = LinkItem()
                link_item['url'] = link
                link_item['category'] = link_category
                yield link_item
                yield scrapy.Request(link, callback=self.parse,
                                     cookies=response.meta['cookies'], meta={'cookies': response.meta['cookies']})

    def link_type(self, link):
        url = urlparse(link)
        groups = url.path.strip('/').split('/')
        if groups[0] == 'bbs' and url.netloc == 'www.1point3acres.com':
            if len(groups) > 1:
                if re.match(self.forum, groups[1]):
                    return 'forum'
                elif re.match(self.thread, groups[1]):
                    return 'thread'
                elif re.match(self.php, groups[1]):
                    return 'php'
                elif re.match(self.user, groups[1]):
                    return 'user'
                elif re.match(self.home, groups[1]):
                    return 'out'
                else:
                    return 'other'
            else:
                return 'index'
        else:
            return 'out'

    @staticmethod
    def get_headers():
        pass

    def start_requests(self):
        url = 'http://www.1point3acres.com/bbs/'
        cookies = {
            '4Oaf_61d6_saltkey': 'P11o15pF',
            '4Oaf_61d6_lastvisit': '1487080711',
            '4Oaf_61d6_visitedfid': '145',
            '4Oaf_61d6_viewid': 'tid_224104',
            '4Oaf_61d6_sendmail': '1',
            'sc_is_visitor_unique': 'rx4760979.1487084314.59EE14AB0E1F4F41E428F72774BB01FB.1.1.1.1.1.1.1.1.1',
            '__utmt': '1',
            '__utma': '142000562.1206298903.1487084315.1487084315.1487084315.1',
            '__utmb': '142000562.1.10.1487084315',
            '__utmc': '142000562',
            '__utmz': '142000562.1487084315.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            '4Oaf_61d6_lastact': '1487084324%09member.php%09logging',
            '4Oaf_61d6_ulastactivity': '100cI6RJUyCXSMEP9pELPGRLqynem5ezKnGZp2YlMvxEu5Gu0%2FJq',
            '4Oaf_61d6_sid': 'DMR6lm',
            '4Oaf_61d6_auth': '4f7dnbWH%2FTifX4rk9DkJuyxfkXq70xK%2BcNdkcArqJr9koJfVeEZx%2BvvLGafzw4k%2FVDR0H5%2FecGnxRdY6P7WDVczZ%2FB4',
            '4Oaf_61d6_lastcheckfeed': '257710%7C1487084324',
            '4Oaf_61d6_checkfollow': '1',
            '4Oaf_61d6_lip': '115.202.88.1%2C1487084297'
        }
        return [scrapy.Request(url, callback=self.parse, cookies=cookies, meta={'cookies': cookies})]
