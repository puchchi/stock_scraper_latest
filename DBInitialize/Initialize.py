import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import MySQLdb
from scraper import utility


class kInitialize():

	def __init__(self, tableName):
		self.tableName = tableName
		try:
			self.db = MySQLdb.connect(utility.databaseHost, utility.databaseUsername,
						    utility.databasePassword, utility.databaseName, charset="utf8", use_unicode=True)
			# Cursor will used in executing SQL query
			self.cursor = self.db.cursor()
		except Exception as e:
			print "Error in connecting Mysql db in initialize.py"

	def __call__(self):
		SQL = ""
		if utility.stockType == "Index" or utility.stockType == "Equity":
			SQL = """ CREATE TABLE %s ( Date INT NOT NULL,Open FLOAT NOT NULL
				    ,High FLOAT NOT NULL,Low FLOAT NOT NULL,Close FLOAT NOT NULL,
				    SharesTraded INT NOT NULL,Turnover FLOAT NULL,
				    PRIMARY KEY (Date)); """ % ( self.tableName)
		elif utility.stockType == "Option":
			SQL = """ CREATE TABLE %s ( Date INT NOT NULL,OptionType VARCHAR(3), 
                    StrikePrice INT NOT NULL, Open FLOAT NOT NULL
				    ,High FLOAT NOT NULL,Low FLOAT NOT NULL,Close FLOAT NOT NULL,
				    NoOfContracts INT NOT NULL,Turnover FLOAT NULL, OpenInterest INT NOT NULL,
                    ChangeInOI INT NOT NULL); """ % ( self.tableName)
		try:
			print SQL
			self.cursor.execute(SQL)
		except Exception as e:
			print "Error in Initialize Call function."


if __name__ == "__main__":
    tableName = "SpotValueOfNiftyBank"
    db = kInitialize(tableName);
    db()