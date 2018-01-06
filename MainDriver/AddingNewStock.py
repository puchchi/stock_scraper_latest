# This file will do following steps.
# 1: Initialize db by creating table for given stock if it not present there.
# 2: Scrape data of that stock and fill in db.
# 3: Create CSV file from db.
# 4: Create all Indicators and save them in another CSV file.
# 5: Test Indicator 

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import pandas as pd
from DBInitialize import Initialize
from scraper import AutoSpotValue, utility
from MainDriver import CreateCSVDataFile, ComputeIndicators
from MainDriver.IndicatorTester import ADXIndicatorTesting, MACDIndicatorTesting

class kAddingNewStock:

    def __init__(self):
        self.stockName = utility.stockName
        self.dbTableName = utility.dbTableName
        self.startYear = utility.startYear
        self.endYear = utility.endYear
        self.dbStartDate = utility.dbStartDate
        self.dbEndDate = utility.dbEndDate
        self.csvFileName = utility.csvFileName
        self.csvFileNameWithIndicators = utility.csvFileNameWithIndicators

    def __call__(self):
        # 1: Initialize db by creating table for given stock if it not present there.
        self.initializeDb()

        # 2: Scrape spot data of that stock and fill in db.
        self.scrapeSpotData()

        # 3: Create CSV file from db.
        self.createCSVFile()

        # 4: Create all Indicators and save them in another CSV file.
        self.createIndicators()

        # 5: Test Indicator 
        self.testIndicator()

    def initializeDb(self):
        print "==============================================="
        print "Creating database table :"
        dbInitialize = Initialize.kInitialize(self.dbTableName)
        dbInitialize()

    def scrapeSpotData(self):
        print "==============================================="
        print "Scraping data from NSE :"
        autoSpotValue = AutoSpotValue.kAutoSpotValue(self.stockName, self.startYear, self.endYear)
        autoSpotValue()

    def createCSVFile(self):
        print "==============================================="
        print "Creating CSV file :"
        createCSVFile = CreateCSVDataFile.kCreateCSVDataFile(self.dbTableName, self.dbStartDate, self.dbEndDate, self.csvFileName)
        createCSVFile()

    def createIndicators(self):
        print "==============================================="
        print "Creating indicator's CSV file :"
        computeIndicator = ComputeIndicators.kComputeIndicators(self.csvFileName, self.csvFileNameWithIndicators)
        computeIndicator()

    def testIndicator(self):
        print "==============================================="
        print "Testing indicator :"
        testIndicator = MACDIndicatorTesting.kMACDIndicatorTesting(self.csvFileNameWithIndicators, 3)
        testIndicator()

if __name__ == "__main__":
    addingNewStock = kAddingNewStock()
    # if you want to do all 5 steps, uncomment following line
    #addingNewStock()

    #addingNewStock.createCSVFile()
    #addingNewStock.createIndicators()
    addingNewStock.testIndicator()
