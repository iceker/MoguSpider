# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class MoguspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'cloudsoft_global', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into mogujie(name, parentName, fcid, rawData,createdDate)
            VALUES (%s, %s, %s, %s,%s)
        """
        self.cursor.execute(insert_sql, (item["name"], item["parentName"], item["fcid"], item["rawData"],item["createdDate"]))
        self.conn.commit()

class Mysql2Pipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'cloudsoft_global', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql, params = item.get_insert_sql()
        print(insert_sql, params)
        self.cursor.execute(insert_sql, params)
        self.conn.commit()