'''This module is used to connect to MySQL database having
    database name StockDB,with user StockUser. This module
    will check & parse & insert data in database
'''

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import MySQLdb
from scraper import utility
from scrapy.exceptions import DropItem
import logging

# start logger
log = logging.getLogger(__name__)

class kStockScraperPipeline(object):
    
    def __init__(self):    
        self.db = MySQLdb.connect(utility.databaseHost, utility.databaseUsername,
						    utility.databasePassword, utility.databaseName, charset="utf8", use_unicode=True)
        log.info("Connected to DB")
        # Cursor will used in executing SQL query
        self.cursor = self.db.cursor()
        self.ids_seen = set()
    
    # def open_spider(self,spider):
    #    log.critical("SPIDER_PIPELINE_OPEN :")
    
    def process_item(self, item, spider):
        
        # StockOptionSpider pipeline
        if spider.name == 'kStockOptionSpider':
            # to get year from expiry date e.g 02022014CE7500 to 2014
            year = item['Expiry'][4:8]
            tableName = 'NiftyOption%s' % year
            
            SQL = """
                INSERT INTO %s (Date , Expiry , Open , High , Low , Close , NoOfContracts , Turnover , OpenInterest , ChangeInOI)
                VALUES (%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s)
            """ % (tableName, item['Date'].encode('utf-8'), item['Expiry'].encode('utf-8'), item['Open'].encode('utf-8'), item['High'].encode('utf-8'), item['Low'].encode('utf-8'), item['Close'].encode('utf-8'),
                 item['NoOfContracts'].encode('utf-8'), item['Turnover'].encode('utf-8'), item['OpenInterest'].encode('utf-8'), item['ChangeInOI'])
            
            try:
                self.cursor.execute(SQL)
                # After cursor will execute SQL successfully, DB will commit change
                self.db.commit()
            except:
                # In case of error, there will be rollback ...
                # If data is already present in table then there will be rollback 
                self.db.rollback()
                log.critical("DB_ROLLBACK_ERROR")
            return item               
            
            
        ###########################################################################################    
        # SpotValueSpider' pipeline
        elif spider.name == 'kSpotValueSpider':
            SQL = """ 
                INSERT INTO SpotValueOfNifty( Date,Open,High,Low,Close,SharesTraded,Turnover)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """ % (item['Date'].encode('utf-8'), item['Open'].encode('utf-8'), item['High'].encode('utf-8'),
                   item['Low'].encode('utf-8'), item['Close'].encode('utf-8'), item['SharesTraded'].encode('utf-8'),
                   item['Turnover'].encode('utf-8'))

            
            if item['Date'] in self.ids_seen:
                log.critical("Duplicate item found for date : %s" % item['Date'])
                raise DropItem("Duplicate item found: %s" % item)
            else:
                # to check for duplicate item
                self.ids_seen.add(item['Date'])
                try:
                    self.cursor.execute(SQL)
                    # After cursor will execute SQL successfully, DB will commit change
                    self.db.commit()
                except:
                    # In case of error, there will be rollback ...
                    # If data is already present in table then there will be rollback 
                    self.db.rollback()
                    print "DB Rollback error"
                    log.critical("DB_ROLLBACK_ERROR")
            return item
        return item
    
    def close_spider(self, spider):
        self.db.close()
