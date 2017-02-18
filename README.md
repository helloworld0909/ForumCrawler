ForumCrawler
------
#### A Scrapy + MySQL ForumCrawler on 1point3acres.com

#### To run the crawler, please input in console:
    python run.py

v0.23<br/>
Finish login<br/>
Changes:
* Add class variable 'cookies', and pass it on to every request

v0.22<br/>
Finish forum parser and post parser<br/>
Changes:
* Finish parse_post(), PostItem
* Change the name of the project
* MySQL tables use MyISAM engine

v0.21
Use Rule to crawl forum, add forum info into MySQL

Changes: (Only finish forum part)
* Scrape forum info
* Add separate rules with respect to forum, post and user
* Add separate items
* Manage the process of creating tables in settings.py (TABLE_INFO)

v0.2<br/>
Only Crawl urls of board, thread and user sites<br/>
Changes:
* Replace BeautifulSoup with XPath
* Read cookies from json
* Add Rules in ForumSpider
* Add run.py

v0.1<br/>
Crawl all links under the domain.
