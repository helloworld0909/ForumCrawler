import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from LinkCrawler.items import ForumItem


class LinkSpider(CrawlSpider):
    name = 'Link'
    allowed_domains = ['1point3acres.com']
    # Only crawl forum, thread and user sites
    rules = (
        Rule(LinkExtractor(allow=('bbs/forum.*html',), restrict_xpaths='//*[@id="hd"]/following::*'),
             callback='parse_forum', follow=True),
        Rule(LinkExtractor(allow=('bbs/thread.*',), restrict_xpaths='//*[@id="hd"]/following::*'),
             callback='parse_post', follow=True),
        Rule(LinkExtractor(allow=('bbs/space.*html',), restrict_xpaths='//*[@id="hd"]/following::*'),
             callback='parse_user', follow=True)
    )
    # Regular expression tmp
    # forum = re.compile(r'.*forum-\d+.*')
    # thread = re.compile(r'.*thread-\d+.*')
    # user = re.compile(r'.*space-\d+.*')

    start_urls = ['http://www.1point3acres.com/bbs/']
    # def start_requests(self):
    #     url = 'http://www.1point3acres.com/bbs/'
    #     cookies = json.load(open('cookies.json', 'r'))
    #     return [Request(url, callback=self.parse_index, cookies=cookies, meta={'cookies': cookies})]
    #
    # def parse_index(self, response):
    #     links = LinkExtractor(allow=('bbs/forum.*html',)).extract_links(response)
    #     for link in links:
    #         yield Request(link.url)


    def parse_forum(self, response):
        try:
            name = response.xpath('//*[@class="xs2"]/a/text()').extract()[0]
        except Exception, e:
            print 'ERROR: ' + response.url, e, '(No permission to enter this forum)'
            name = ''
        try:
            pages_str = re.search('\d+', response.xpath('//label/span/text()').extract()[0]).group(0)
            pages = int(pages_str)
        except:
            if name == '':
                pages = 0
            else:
                pages = 1
        item = ForumItem()
        item['url'] = response.url
        item['name'] = name
        item['pages'] = pages
        yield item

    def parse_post(self, response):
        # TODO parse_post
        pass

    def parse_user(self, response):
        # TODO parse_user
        pass

    # def link_type(self, link):
    #     # Assign a category to the link
    #     url = urlparse(link)
    #     groups = url.path.strip('/').split('/')
    #     if groups[0] == 'bbs' and len(groups) > 1:
    #         if re.match(self.thread, groups[1]):
    #             return 'thread'
    #         elif re.match(self.user, groups[1]):
    #             return 'user'
    #         elif re.match(self.forum, groups[1]):
    #             return 'forum'
    #         else:
    #             return 'out'
    #     else:
    #         return 'out'
