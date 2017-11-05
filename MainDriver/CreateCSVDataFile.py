import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
sys.path.append( path.dirname( path.abspath(__file__) ) )


import panda as pd
import MySQLdb
import csv
from scraper import utility

class kCreateCSVDataFile():

    def __init__(self):
        try:
            self.db = MySQLdb.connect(utility.databaseHost, utility.databaseUsername,
						    utility.databasePassword, utility.databaseName, charset="utf8", use_unicode=True)
        except Exception as e:
            print "Error in connecting Mysql db in CreateCSVDataFile.py"

    def __call__(self, tableName, startDate, endDate, filename):
        SQL = """select Date, Open, High, Low, Close, SharesTraded from %s where Date >= %s and Date <= %s
                """ %(tableName, startDate, endDate)
        # Cursor will used in executing SQL query
        cursor = self.db.cursor()  
        cursor.execute(SQL)
        row = cursor.fetchall()
        with open(filename, 'w') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerows(row)

        cursor.close()



if __name__ == "__main__":
    createCSVDataFile = kCreateCSVDataFile()
    createCSVDataFile("spotValueOfNifty", 20100101, 20170101, "data/nifty.csv")
