ForumCrawler
------
###### A Scrapy ForumCrawler on 1point3acres.com/bbs/

A Crawler crawls board pages, posts and user info on 1point3acres.com/bbs/,
and the data will be stored in MySQL database.
It can be modified to work on some other regular forum web sites.

#### To run the crawler, please input in console:
    python run.py

#### Dependency:
1. python2.7<br>
2. scrapy<br>
3. pywin32<br>
3. bs4(BeautifulSoup4)<br>
4. MySQLdb<br>

### Change Log
------
v0.31<br>
Parse post context(admission info, user background, etc)<br>
Changes:
* Parse post context()
* Parse admission board correctly
* trivial Bugs fixed

v0.3<br>
Finish User page parsing<br>
Changes:
* User page and profile parsing
* from __future__ import unicode_literals
* Fix names of attributes
* Parse board_url and board_name of each post
* log filename relates to time_local()

v0.23<br>
Finish login<br>
Changes:
* Add class variable 'cookies', and pass it on to every request

v0.22<br>
Finish forum parser and post parser<br>
Changes:
* Finish parse_post(), PostItem
* Change the name of the project
* MySQL tables use MyISAM engine

v0.21<br>
Use Rule to crawl forum, add forum info into MySQL<br>
Changes: (Only finish forum part)
* Scrape forum info
* Add separate rules with respect to forum, post and user
* Add separate items
* Manage the process of creating tables in settings.py (TABLE_INFO)

v0.2<br>
Only Crawl urls of board, thread and user sites<br>
Changes:
* Replace BeautifulSoup with XPath
* Read cookies from json
* Add Rules in ForumSpider
* Add run.py

v0.1<br>
Crawl all links under the domain.
