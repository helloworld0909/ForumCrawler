# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from LinkCrawler import settings


class LinkPipeline(object):
    def open_spider(self, spider):
        self.conn = MySQLdb.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            db=settings.MYSQL_DB,
            charset=settings.MYSQL_CHARSET
        )
        self.conn.autocommit(True)
        self.cur = self.conn.cursor()
        self.cur.execute('create table if not exists {}({})'.format(settings.TABLE_NAME, settings.TABLE_CREATE))

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        col = ','.join(item.keys())
        placeholders = ','.join(len(item) * ['%s'])
        sql = 'insert ignore into {}({}) values({})'.format(settings.TABLE_NAME, col, placeholders)
        self.cur.execute(sql, item.values())
        return item
