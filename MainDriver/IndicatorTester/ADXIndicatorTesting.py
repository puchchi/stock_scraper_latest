import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import pandas as pd
from scraper import utility
from MainDriver.IndicatorTester.IndicatorTesterClass import kIndicatorTesterClass

class kADXIndicatorTesting(kIndicatorTesterClass):

    def __init__(self, filename, noOfDays):
        kIndicatorTesterClass.__init__(self, filename, noOfDays)
        self.noOfDays = noOfDays

    def __call__(self):
        startIndex = utility.startIndex
        endIndex = utility.endIndex
        df = self.getDataFrame()
        #self.df.drop(self.df.index[range(28)], inplace=True)
        plusDIs = df["+DI14"]
        minusDIs = df["-DI14"]
        adxs = df["ADX"]
        close = df["Close"]

        flag = True
        if minusDIs[startIndex] > plusDIs[startIndex]:
            flag = False

        for i in range(startIndex + 1, plusDIs.count() - endIndex):
            
            if flag:
                if minusDIs[i] > plusDIs[i] and adxs[i] > 20:
                    self.sellSignal(i)
                    flag = False
            else:
                if plusDIs[i] > minusDIs[i] and adxs[i] > 20:
                    self.buySignal(i)
                    flag = True
            
        print "====== Test result b/w +DI14 & -DI14 having ADX>20 ======"
        self.buySignalResult()
        print "===================================="
        self.sellSignalResult()

if __name__ == "__main__":

    adxTesting = kADXIndicatorTesting(utility.csvFileNameWithIndicators)
    adxTesting.testIndicator()
    