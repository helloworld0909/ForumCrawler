import sys
from scrapy import cmdline


if len(sys.argv) == 0:
    print 'You should assign a spider'
else:
    for spider in str(sys.argv):
        cmdline.execute('scrapy crawl {}'.format(spider).split())
