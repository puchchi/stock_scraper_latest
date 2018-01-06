'''This module will help in automating process of 
    execution of spider and will set appropriate setting.
    You can set User Agent to random value for every 
    time spider will crawl, this will reduce chance of 
    getting banned.
'''

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import scrapy, scraper, logging
from scraper.spiders import SpotValueSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class kAutoSpotValue:
    def __init__(self, stockName, startYear=2010, endYear=2017):
        self.stockName = stockName
        self.startYear = startYear
        self.endYear = endYear

        # start logger
        log = logging.getLogger(__name__)

    def __call__(self):
        # get_project_stting() will return project setting,which will be set as default setting in crawler
        process = CrawlerProcess(get_project_settings())


        # crawl will take Spider name with its *args
        process.crawl(SpotValueSpider.kSpotValueSpider, symbol=self.stockName, startYear=self.startYear, endYear=self.endYear)
        # Everything is set to go and crawl.
        process.start()

if __name__ == "__main__":
    autoSpotValue = kAutoSpotValue("NIFTY 50", 2010, 2017)
    autoSpotValue()
    






