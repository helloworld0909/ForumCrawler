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
        for table_name, table_items in settings.TABLE_INFO.items():
            self.cur.execute('create table if not exists {}({})'.format(table_name, table_items))

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        col = ','.join(item.keys())
        placeholders = ','.join(len(item) * ['%s'])
        sql = 'insert ignore into {}({}) values({})'.format(item.category, col, placeholders)
        self.cur.execute(sql, item.values())
        return item
