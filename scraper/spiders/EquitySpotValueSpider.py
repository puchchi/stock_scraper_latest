'''This spider is used to crawl and save spot 
    value of equites like SBIN, YESBANK,    
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
from scraper.items import kEquitySpotItem

# start logger
log = logging.getLogger(__name__)

class kEquitySpotValueSpider(scrapy.Spider):
    
    name = 'kEquitySpotValueSpider'
    allowed_domains = ['www.nseindia.com']
    
    def __init__(self, symbol, startYear, endYear, * args, **kwargs):
        super(kEquitySpotValueSpider, self).__init__(*args, **kwargs)
        self.symbol = symbol
        #this list will store day range with month range in the form of [[[start day,end day],[start month,end month]]]
        self.dayMonthRange=[[['01','31'],['01','03']],[['01','30'],['04','06']],[['01','30'],['07','09']],[['01','31'],['10','12']]]
        self.year=startYear  #This will be start year
        self.currentYear=endYear

        # url = https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol={symbol}&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate={startDate}&toDate={endDate}&dataType=PRICEVOLUMEDELIVERABLE

    def start_requests(self):
        scrapy.Spider.start_requests(self)
        log.info("Creating Start_url list: ")
        iterobj=0
        while self.year<self.currentYear:
            for dayIter in self.dayMonthRange:
                self.startDate = dayIter[0][0]+'-'+dayIter[1][0]+'-'+str(self.year)
                self.endDate = dayIter[0][1]+'-'+dayIter[1][1]+'-'+str(self.year)
                iterobj+=1
                url = "https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol={symbol}&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate={startDate}&toDate={endDate}&dataType=PRICEVOLUMEDELIVERABLE".format(symbol=self.symbol.lower(), startDate=self.startDate, endDate=self.endDate)
                log.info('%s : %s '%(iterobj,url))
                yield scrapy.Request(url,self.parse, headers={'Referer':'https://www.nseindia.com/products/content/equities/equities/eq_security.htm'})
            self.year+=1
    
    # used to save respective xpath value with their item,
    # later we can iterate through it.
    item_fields = {  
                'Date':'./td[3]//text()',
                'Open':'./td[5]//text()',
                'High':'./td[6]//text()',
                'Low':'./td[7]//text()',
                'Close':'./td[9]//text()',
                'SharesTraded':'./td[11]//text()',
                'Turnover':'./td[12]//text()'
                }
    
    def parse(self, response):
        
        log.info("RESPONSE_URL_INFO : %s"%response._url)
        # checking for response, wheather it contains records or not
        if (response.xpath("//tr[2]//text()").extract()[0].find("No Records") > 0):
            log.crtical("No Records found for URL %s"%(response.url))
            
        else:   
            # Storing all selector except top 2(which contains waste data)
            res = response.xpath('//tr[position()>2]')
            # val will iterate from 0 to (last -1), because last res item is waste
            for val in res[0:(len(res) - 1)]:
                loader = ItemLoader(kEquitySpotItem(), val)
                loader.default_input_processor = MapCompose(unicode.strip)
                loader.default_output_processor = Join()
                
                for item, xpath in self.item_fields.iteritems():
                    loader.add_xpath(item, xpath)
                yield loader.load_item()
