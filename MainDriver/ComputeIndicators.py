import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import pandas as pd
from Indicators import AccumulationNDistributionLine, OnBalanceVolume, AverageDirectionalIndex, MACD, RSI

class kComputeIndicators:
    def __init__(self, filename):
        parser = lambda date: pd.datetime.strptime(date, '%Y%m%d')
        self.df = pd.read_csv(filename, parse_dates = [0], date_parser = parser, index_col = "Date")

    def GetDataFrame(self):
        return self.df

    def CalculateAllIndicators(self):
        dataframe = self.df

        # Calculating ADL
        adl = AccumulationNDistributionLine.kAccumulationNDistributionLine()
        adlSeries = adl.calculate(dataframe)
        adlDataframe = pd.DataFrame(adlSeries, columns=["ADL"])

        # Calculating OBV
        obv = OnBalanceVolume.kOnBalanceVolume()
        obvSeries = obv.calculate(dataframe)
        obvDataframe = pd.DataFrame(obvSeries, columns=["OBV"])

        # Calculating ADX
        adx = AverageDirectionalIndex.kAverageDirectionalIndex()
        adxDataframe = adx.calculate(dataframe)

        # Calculating MACD
        macd = MACD.kMACD()
        macdDataframe = macd.Calculate(dataframe)

        # Calculating RSI
        rsi = RSI.kRSI()
        rsiSeries = rsi.Calculate(dataframe)
        rsiDataframe = pd.DataFrame(rsiSeries, columns=["RSI"])

        dataframe = dataframe.merge(adlDataframe, left_index=True, right_index=True)
        dataframe = dataframe.merge(obvDataframe, left_index=True, right_index=True)
        dataframe = dataframe.merge(adxDataframe, left_index=True, right_index=True)
        dataframe = dataframe.merge(macdDataframe, left_index=True, right_index=True)
        dataframe = dataframe.merge(rsiDataframe, left_index=True, right_index=True)

        return dataframe


if __name__ == "__main__":

    computeIndicator = kComputeIndicators("data/nifty.csv")
    dataframe = computeIndicator.CalculateAllIndicators()
    dataframe.to_csv("data/niftyWithIndicators.csv")
