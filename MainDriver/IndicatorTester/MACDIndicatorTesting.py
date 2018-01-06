import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import pandas as pd
from scraper import utility
from MainDriver.IndicatorTester.IndicatorTesterClass import kIndicatorTesterClass

class kMACDIndicatorTesting(kIndicatorTesterClass):

    def __init__(self, filename, noOfDays):
        kIndicatorTesterClass.__init__(self, filename, noOfDays)
        self.noOfDays = noOfDays

    def __call__(self):
        startIndex = utility.startIndex
        endIndex = utility.endIndex
        #self.df.drop(self.df.index[range(28)], inplace=True)
        df = self.getDataFrame()
        macdLine = df["MACD Line"]
        signalLine = df["Signal Line"]
        macd = df["MACD Histogram"]
        close = df["Close"]

        flag = True
        if macdLine[startIndex] < 0:
            flag = False

        # Test b/w MACD line & centerline(0)
        for i in range(startIndex+1, macdLine.count() - endIndex):
            if flag:
                if macdLine[i] <= 0:
                    self.sellSignal(i)
                    flag = False
            else:
                if macdLine[i] >= 0:
                    self.buySignal(i)
                    flag = True
        
        print "====== Test result b/w MACD line & centerline ======"  
        self.buySignalResult()
        print "===================================="
        self.sellSignalResult()

        # Test b/w MACD Line and Signal Line
        self.resetValue()
        flag = True
        if macdLine[startIndex] < signalLine[startIndex]:
            flag = False

        for i in range(startIndex+1, macdLine.count() - endIndex):
            if flag:
                if macdLine[i] < signalLine[i]:
                    self.sellSignal(i)
                    flag = False
            else:
                if macdLine[i] > signalLine[i]:
                    self.buySignal(i)
                    flag = True
        
        print "\n\n"
        print "====== Test result b/w MACD line & Signal line ====="
        self.buySignalResult()
        print "===================================="
        self.sellSignalResult()

if __name__ == "__main__":

    macdTesting = kMACDIndicatorTesting(utility.csvFileNameWithIndicators)
    macdTesting()
    