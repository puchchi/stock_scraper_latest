'''This module will help in automating process of 
    execution of spider and will set appropriate setting.
    You can set User Agent to random value for every 
    time spider will crawl, this will reduce chance of 
    getting banned.
'''

import scrapy, stock_scraper, logging
from stock_scraper.spiders import StockOptionSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# start logger
log = logging.getLogger(__name__)

# get_project_stting() will return project setting,which will be set as default setting in crawler
process = CrawlerProcess(get_project_settings())
    # crawl will take Spider name with its *args
process.crawl(StockOptionSpider , symbol='NIFTY 50', startYear=2014, endYear=2015)
        # Everything is set to go and crawl.
process.start()

