import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
sys.path.append( path.dirname( path.abspath(__file__) ) )

import MySQLdb
import csv
from scraper import utility

class kCreateCSVDataFile():

    def __init__(self, tableName, startDate, endDate, filename):
        self.tableName = tableName
        self.startDate = startDate
        self.endDate = endDate
        self.fileName = filename
        try:
            self.db = MySQLdb.connect(utility.databaseHost, utility.databaseUsername,
						    utility.databasePassword, utility.databaseName, charset="utf8", use_unicode=True)
        except Exception as e:
            print "Error in connecting Mysql db in CreateCSVDataFile.py"

    def __call__(self):
        SQL = """select Date, Open, High, Low, Close, SharesTraded from %s where Date >= %s and Date <= %s
                """ %(self.tableName, self.startDate, self.endDate)
        # Cursor will used in executing SQL query
        cursor = self.db.cursor()  
        cursor.execute(SQL)
        row = cursor.fetchall()
        
        # adding headers to csv file
        header = "Date,Open,High,Low,Close,Volume\n"
        with open(self.fileName, 'wb') as fp:
            fp.write(header)

        with open(self.fileName, 'ab') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerows(row)

        cursor.close()


if __name__ == "__main__":
    createCSVDataFile = kCreateCSVDataFile(utility.dbTableName, utility.dbStartDate, utility.dbEndDate, utility.csvFileName)
    createCSVDataFile()
