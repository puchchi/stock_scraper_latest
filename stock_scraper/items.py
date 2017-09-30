'''This module will help in saving data through item
    field to database
'''

from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, Join
from stock_scraper import utility


class StockOptionItem(Item):
    # This class will contains Option(Call/Put) values only
    Date = Field(
                 input_processor=MapCompose(utility.dateEncoding),
                 output_processor=Join(),
                 )  # DDMMYYYY
    Expiry = Field(
                   input_processor=MapCompose(utility.expiryEncoding),
                   output_processor=Join(''),
                   )  # DDMMYYYY+OptionType+StrikePrice   
    Open = Field(
                 input_processor=MapCompose(utility.strToFloatNumber),
                 output_processor=Join(),
                 )# '7,500.00' to '7500.00'
    High = Field(
                 input_processor=MapCompose(utility.strToFloatNumber),
                 output_processor=Join(),
                 )# '7,500.00' to '7500.00'
    Low = Field(
                input_processor=MapCompose(utility.strToFloatNumber),
                output_processor=Join(),
                )# '7,500.00' to '7500.00'
    Close = Field(
                  input_processor=MapCompose(utility.strToFloatNumber),
                  output_processor=Join(),
                  )# '7,500.00' to '7500.00'
    NoOfContracts = Field(
                          input_processor=MapCompose(utility.strToIntNumber),
                          output_processor=Join(),
                          )# '7,500.00' to '7500'
    Turnover = Field(
                     input_processor=MapCompose(utility.strToFloatNumber),
                     output_processor=Join(),
                     )  # '7,500.00' to '7500.00'# In lacks
    OpenInterest = Field(
                         input_processor=MapCompose(utility.strToIntNumber),
                         output_processor=Join(),
                         )# '7,500.00' to '7500'
    ChangeInOI = Field(
                       input_processor=MapCompose(utility.strToIntNumber),
                       output_processor=Join(),
                       )# '7,500.00' to '7500'


class StockSpotItem(Item):
    # This class will contains spot values only
    
    Date = Field(
                 input_processor=MapCompose(utility.dateEncoding),
                 output_processor=Join(),
                 )  
    Open = Field()
    High = Field()
    Low = Field()
    Close = Field()
    SharesTraded = Field()
    Turnover = Field()  # In lacks
    
