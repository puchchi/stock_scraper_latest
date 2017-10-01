'''This spider is used to crawl and save spot 
    value of indices like NIFTY 50, BANKNIFTY,    
    etc. You need to provide SYMBOL, STARTDATE,
    & ENDDATE as argument to this spider.
'''

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import scrapy, logging, scraper
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.loader.processors import Join, MapCompose
from scraper.items import StockSpotItem

# start logger
log = logging.getLogger(__name__)

class kSpotValueSpider(scrapy.Spider):
    
    name = 'kSpotValueSpider'
    allowed_domains = ['www.nseindia.com']
    
    def __init__(self, symbol, startYear, endYear, * args, **kwargs):
        super(kSpotValueSpider, self).__init__(*args, **kwargs)
        self.symbol = symbol
        #this list will store day range with month range in the form of [[[start day,end day],[start month,end month]]]
        self.dayMonthRange=[[['01','31'],['01','03']],[['01','30'],['04','06']],[['01','30'],['07','09']],[['01','31'],['10','12']]]
        self.year=startYear  #This will be start year
        self.currentYear=endYear
        self.symbol='NIFTY 50'
        #self.start_urls = ["http://www.nseindia.com/products/dynaContent/equities/indices/historicalindices.jsp?indexType={symbol}&fromDate={startDate}&toDate={endDate}".format(symbol=self.symbol, startDate=self.startDate, endDate=self.endDate),
        #             ]
    
    def start_requests(self):
        scrapy.Spider.start_requests(self)
        log.info("Creating Start_url list: ")
        iterobj=0
        while self.year<self.currentYear:
            for self.dayIter in self.dayMonthRange:
                self.startDate=self.dayIter[0][0]+'-'+self.dayIter[1][0]+'-'+str(self.year)
                self.endDate=self.dayIter[0][1]+'-'+self.dayIter[1][1]+'-'+str(self.year)
                iterobj+=1
                url="http://www.nseindia.com/products/dynaContent/equities/indices/historicalindices.jsp?indexType={symbol}&fromDate={startDate}&toDate={endDate}".format(symbol=self.symbol, startDate=self.startDate, endDate=self.endDate)
                log.info('%s : %s '%(iterobj,url))
                yield scrapy.Request(url,self.parse)
            self.year+=1
    
    # used to save respective xpath value with their item,
    # later we can iterate through it.
    item_fields = {  
                'Date':'./td[1]//text()',
                'Open':'./td[2]//text()',
                'High':'./td[3]//text()',
                'Low':'./td[4]//text()',
                'Close':'./td[5]//text()',
                'SharesTraded':'./td[6]//text()',
                'Turnover':'./td[7]//text()'
                }
    
    def parse(self, response):
        
        log.info("RESPONSE_URL_INFO : %s"%response._url)
        # checking for response, wheather it contains records or not
        if (response.xpath("//tr[3]//text()").extract()[0].find("No Records") > 0):
            log.crtical("No Records found for URL %s"%(response.url))
            
        else:   
            # Storing all selector except top 3(which contains waste data)
            res = response.xpath('//tr[position()>3]')
            # val will iterate from 0 to (last -1), because last res item is waste
            for val in res[0:(len(res) - 1)]:
                loader = ItemLoader(StockSpotItem(), val)
                loader.default_input_processor = MapCompose(unicode.strip)
                loader.default_output_processor = Join()
                
                for item, xpath in self.item_fields.iteritems():
                    loader.add_xpath(item, xpath)
                yield loader.load_item()
