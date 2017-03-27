import sys
from scrapy import cmdline
sys.path.append('ForumCrawler/custom')

if len(sys.argv) == 0:
    print 'You should assign a spider'
elif len(sys.argv) > 1:
    print 'Only support one spider at a time'
else:
    spider = sys.argv[1]
    settings = __import__('{}_settings'.format(str(spider)))
    cmdline.execute('scrapy crawl {spider} -s LOG_FILE={log} -s JOBDIR={job}'.format(
        spider=str(spider), log=settings.LOG_FILE, job=settings.JOBDIR).split())
