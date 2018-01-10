import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import pandas as pd
from scraper import utility

class kIndicatorTesterClass:

    def __init__(self, filename, noOfDays):
        self.noOfDays = noOfDays
        self.totBPass = 0
        self.totBFail = 0
        self.totBPassFromHigh = 0
        self.totBFailFromHigh = 0
        self.totSPass = 0
        self.totSFail = 0
        self.totSPassFromLow = 0
        self.totSFailFromLow = 0

        parser = lambda date: pd.datetime.strptime(date, '%Y-%m-%d')
        self.df = pd.read_csv(filename, parse_dates = [0], date_parser = parser, index_col = "Date")

    def getDataFrame(self):
        return self.df

    def sellSignal(self, index):
        minClose = min(self.df["Close"][index+1:index+self.noOfDays+1])
        minLow = min(self.df["Low"][index+1:index+self.noOfDays+1])
        print "--------------Sell Signal : " + str(self.df.index[index]) + " Current Close : " + str(self.df["Close"][index]) + " Lows in nxt " + str(self.noOfDays) + " days : " + str(self.df["Low"][index:index+self.noOfDays+1])
                    
        if minClose < self.df["Close"][index]:
            self.totSPass = self.totSPass + 1
        else:
            self.totSFail = self.totSFail + 1

        if minLow < self.df["Close"][index]:
            self.totSPassFromLow = self.totSPassFromLow + 1
        else:
            self.totSFailFromLow = self.totSFailFromLow + 1

        # Special case
        #if minClose > self.df["Close"][index] and minLow < self.df["Close"][index]:
        #    print "--------------Sell Signal : " + str(self.df.index[index]) + " Current Close : " + str(self.df["Close"][index]) + "Min Close in nxt " + str(self.noOfDays) + " days : " + str(self.df["Low"][index:index+self.noOfDays+1])

    def sellSignalResult(self):
        print "Total sell pass : " + str(self.totSPass)
        print "Total sell fail : " + str(self.totSFail)
        per = float(self.totSPass)/(self.totSPass + self.totSFail)*100
        print "Total sell pass percentage in nxt " + str(self.noOfDays) + " days : " + str(per)

        print "Total sell pass from low: " + str(self.totSPassFromLow)
        print "Total sell fail from low: " + str(self.totSFailFromLow)
        perFromLow = float(self.totSPassFromLow)/(self.totSPassFromLow + self.totSFailFromLow)*100
        print "Total sell pass percentage from low in nxt " + str(self.noOfDays) + " days : " + str(perFromLow)


    def buySignal(self, index):
        maxClose = max(self.df["Close"][index+1:index+self.noOfDays+1])
        maxHigh = max(self.df["High"][index+1:index+self.noOfDays+1])
        print "++++++++++++++Buy Signal : " + str(self.df.index[index]) + " Current Close : " + str(self.df["Close"][index]) + " Highs in nxt " + str(self.noOfDays) + " days : " + str(self.df["High"][index:index+self.noOfDays+1])
                    
        if maxClose > self.df["Close"][index]:
            self.totBPass = self.totBPass + 1
        else:
            self.totBFail = self.totBFail + 1
        if maxHigh > self.df["Close"][index]:
            self.totBPassFromHigh = self.totBPassFromHigh + 1
        else:
            self.totBFailFromHigh = self.totBFailFromHigh + 1
        
        # Special case
        #if maxClose < self.df["Close"][index] and maxHigh > self.df["Close"][index]:
        #    print "++++++++++++++Buy Signal : " + str(self.df.index[index]) + " Current Close : " + str(self.df["Close"][index]) + "Max Close in nxt " + str(self.noOfDays) + " days : " + str(self.df["High"][index:index+self.noOfDays+1])

    def buySignalResult(self):
        print "Total buy pass : " + str(self.totBPass)
        print "Total buy fail : " + str(self.totBFail)
        per = float(self.totBPass)/(self.totBPass + self.totBFail)*100
        print "Total buy pass percentage in nxt " + str(self.noOfDays) + " days : " + str(per)

        print "Total buy pass from high: " + str(self.totBPassFromHigh)
        print "Total buy fail from high: " + str(self.totBFailFromHigh)
        perFromHigh = float(self.totBPassFromHigh)/(self.totBPassFromHigh + self.totBFailFromHigh)*100
        print "Total buy pass percentage from high in nxt " + str(self.noOfDays) + " days : " + str(perFromHigh)

    def resetValue(self):
        self.totBPass = 0
        self.totBFail = 0
        self.totBPassFromHigh = 0
        self.totBFailFromHigh = 0
        self.totSPass = 0
        self.totSFail = 0
        self.totSPassFromLow = 0
        self.totSFailFromLow = 0