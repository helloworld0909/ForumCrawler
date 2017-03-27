import sys
from scrapy import cmdline


if len(sys.argv) == 0:
    print 'You should assign a spider'
else:
    for spider in sys.argv[1:]:
        cmdline.execute('scrapy crawl {}'.format(str(spider)).split())
