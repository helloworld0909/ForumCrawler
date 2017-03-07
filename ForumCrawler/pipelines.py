# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES custom
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


class MySQLPipeline(object):
    # TODO insert many tuples each time, executemany
    def open_spider(self, spider):
        self.conn = MySQLdb.connect(
            host=spider.settings['MYSQL_HOST'],
            port=spider.settings['MYSQL_PORT'],
            user=spider.settings['MYSQL_USER'],
            passwd=spider.settings['MYSQL_PASSWD'],
            db=spider.settings['MYSQL_DB'],
            charset=spider.settings['MYSQL_CHARSET']
        )
        self.conn.autocommit(True)
        self.cur = self.conn.cursor()
        for table_name, table_items in spider.settings['TABLE_INFO'].iteritems():
            sql = 'create table if not exists {}({})'
            table_items_sql = ','.join([k + ' ' + v for k, v in table_items['attrs'].iteritems()])
            if 'pk' in table_items and table_items['pk']:  # Primary key(pk)
                table_items_sql += ',' + 'primary key({})'.format(','.join(table_items['pk']))
            if 'fk' in table_items and table_items['fk']:  # Foreign key(fk) references table(attr)
                table_items_sql += ',' + 'foreign key({d[0]}) references {d[1]}({d[2]})'.format(d=table_items['fk'])
            if 'engine' in table_items and table_items['engine']:   # Engine=SOMETYPE
                sql += ' engine={}'.format(table_items['engine'])
            self.cur.execute(sql.format(table_name, table_items_sql))

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        col = ','.join(item.keys())
        placeholders = ','.join(len(item) * ['%s'])
        sql = 'insert ignore into {}({}) values({})'.format(item.category, col, placeholders)
        self.cur.execute(sql, item.values())
        return item
