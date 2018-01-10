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
from scraper import utility, AutoEquitySpotValue, AutoIndexSpotValue, AutoOptionValue
from MainDriver import ComputeIndicators, OptionRelatedTesting
from MainDriver.CSVCreator import CreateSpotCSVDataFile, CreateOptionCSVDataFile
from MainDriver.IndicatorTester import ADXIndicatorTesting, MACDIndicatorTesting

class kAddingNewStock:

    def __init__(self):
        self.stockName = utility.stockName
        self.stockType = utility.stockType
        self.dbTableName = utility.dbTableName
        self.dbTableNameOption = utility.dbTableNameOption
        self.startYear = utility.startYear
        self.endYear = utility.endYear
        self.dbStartDate = utility.dbStartDate
        self.dbEndDate = utility.dbEndDate
        self.csvFileName = utility.csvFileName
        self.csvFileNameOption = utility.csvFileNameOption
        self.csvFileNameWithIndicators = utility.csvFileNameWithIndicators
        self.expiries = utility.expiries
        self.instrumentType = utility.instrumentType
        self.expiry = ""

    def __call__(self):
        self.callInternal()

    def callInternal(self):

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

        if self.stockType == "Index" or self.stockType == "Equity":
            dbInitialize = Initialize.kInitialize(tableName)
            dbInitialize()
        elif self.stockType == "Option":
            for expiry in self.expiries:
                tableName = self.dbTableNameOption + expiry
                dbInitialize = Initialize.kInitialize(tableName)
                dbInitialize()

    def scrapeSpotData(self):
        print "==============================================="
        print "Scraping data from NSE :"

        if self.stockType == "Index":
            autoSpotValue = AutoIndexSpotValue.kAutoIndexSpotValue(self.stockName, self.startYear, self.endYear)
            autoSpotValue()
        elif self.stockType == "Equity":
            autoSpotValue = AutoEquitySpotValue.kAutoEquitySpotValue(self.stockName, self.startYear, self.endYear)
            autoSpotValue()
        elif self.stockType == "Option":
            autoOptionValue = AutoOptionValue.kAutoOptionValue(self.stockName, self.expiries, self.instrumentType)
            autoOptionValue()

    def createCSVFile(self):
        print "==============================================="
        print "Creating CSV file :"

        if self.stockType == "Index" or self.stockType == "Equity":
            createCSVFile = CreateSpotCSVDataFile.kCreateSpotCSVDataFile(self.dbTableName, self.dbStartDate, self.dbEndDate, self.csvFileName)
        elif self.stockType == "Option":
            tableNames = []
            fileNames = []
            for expiry in self.expiries:
                tableNames.append(self.dbTableNameOption + expiry)
                fileNames.append(self.csvFileNameOption + expiry + ".CSV")
            createCSVFile = CreateOptionCSVDataFile.kCreateOptionCSVDataFile(tableNames, fileNames)
        createCSVFile()

    def createIndicators(self):
        if self.stockType == "Index" or self.stockType == "Equity":
            print "==============================================="
            print "Creating indicator's CSV file :"
            computeIndicator = ComputeIndicators.kComputeIndicators(self.csvFileName, self.csvFileNameWithIndicators)
            computeIndicator()

    def testIndicator(self):
        print "==============================================="
        print "Testing indicator :"
        if self.stockType == "Index" or self.stockType == "Equity":
            testIndicator = ADXIndicatorTesting.kADXIndicatorTesting(self.csvFileNameWithIndicators, 3)
            testIndicator()
        elif self.stockType == "Option":
            optionTesting = OptionRelatedTesting.kOptionRelatedTesting(utility.optionCSVFileForTesting)
            optionTesting()

if __name__ == "__main__":
    addingNewStock = kAddingNewStock()
    # if you want to do all 5 steps, uncomment following line
    #addingNewStock()

    #addingNewStock.scrapeSpotData()
    #addingNewStock.createCSVFile()
    #addingNewStock.createIndicators()
    addingNewStock.testIndicator()
