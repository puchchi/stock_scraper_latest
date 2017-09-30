from utility import *
from items import *
import logging


#This will help in logging all spider
logging.basicConfig(filename='/root/stock_scraper/stock_scraper.log',filemode='a',format='%(asctime)-15s : %(module)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)