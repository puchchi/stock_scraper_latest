import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import pandas as pd

class kMACD():

    def __init__(self):
        #do nothing
        print "In kMACD class"

    def Calculate (self, dataFrame):
        ##### FORMULA #####
        # MACD Line: (12-day EMA - 26-day EMA)
        #Signal Line: 9-day EMA of MACD Line
        #MACD Histogram: MACD Line - Signal Line

        close = dataFrame["Close"]

        _12DaysEMA = pd.ewma(close, span=12)
        _26DaysEMA = pd.ewma(close, span=26)
        macdLine = _12DaysEMA - _26DaysEMA

        signalLine = pd.ewma(macdLine, span=9)

        macdHistogram = macdLine - signalLine

        macdDataframe = pd.DataFrame()
        macdDataframe.insert(loc=0, column="MACD Line", value=macdLine)
        macdDataframe.insert(loc=1, column="Signal Line", value=signalLine)
        macdDataframe.insert(loc=2, column="MACD Histogram", value=macdHistogram)

        #print macdDataframe
        return macdDataframe