import sqlite3
from typing import Set

class SQLStore:
    '''
        SQL Store class to create and save stocks and portfolio
        data in a sqlite3 database.
    '''
    def __init__(self, db_file) -> None:
        try:
            self.conn = sqlite3.connect(db_file)
            self.createTable()
        except Exception as e:
            print(e)
            return -1
        
    def createTable(self) -> None:
        '''
            Creates required tables in sqlite3 database.
        '''
        try:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS stocks_db
                (
                    scrip_Code INT PRIMARY KEY NOT NULL,
                    short_name TEXT NOT NULL,
                    Long_Name TEXT NOT NULL,
                    meeting_date TEXT NOT NULL,
                    URL TEXT NOT NULL
                );'''
            )

            print("Database stocks_db initialized")

        except Exception as e:
            print("Initialization for stocks_db failed!")
            print(e)
            return -1

        try:    
            self.conn.execute('''CREATE TABLE IF NOT EXISTS portfolio_db
                (
                    scrip_Code INT PRIMARY KEY NOT NULL,
                    short_name TEXT NOT NULL,
                    calendar_event_id TEXT,
                    FOREIGN KEY(scrip_Code) REFERENCES stocks_db(scrip_Code)
                );'''
            )

            print("Database portfolio_db initialized")

        except Exception as e:
            print("Initialization for portfolio_db failed!")
            print(e)
            return -1

        try:    
            self.conn.execute('''CREATE TABLE IF NOT EXISTS meta_db
                (
                    last_updated TIMESTAMP NOT NULL
                );'''
            )

            print("Database meta_db initialized")

        except Exception as e:
            print("Initialization for meta_db failed!")
            print(e)
            return -1

    def insertIntoTable(self, table_name, num_cols, entries=[]) -> None:
        '''
            Inserts data into a given sqlite table.
            entries must be an array of sets.
        '''
        try:
            cursor = self.conn.cursor()
            sql_query_prefix = "INSERT INTO " + table_name + " VALUES " + "(" + (num_cols-1) * "?," + "?)"
            print(sql_query_prefix)
            cursor.executemany(sql_query_prefix, entries)
            self.conn.commit()

        except Exception as e:
            print(e)

    def testQuery(self) -> None:
        '''
            Sample test query to check if DB is working.
            Will be changed to something generic in future.
        '''
        try:
            cursor = self.conn.cursor()
        except Exception as e:
            print(e)
            return -1

        for row in cursor.execute("SELECT * FROM stocks_db LIMIT 10;"):
            print(row)

    def getScripDetails(self, scrip_code) -> Set:
        '''
            Returns Details for a script for SQLlite DB
        ''' 
        try:
            cursor = self.conn.cursor()
        except Exception as e:
            print(e)
            return -1

        cursor.execute("SELECT * FROM stocks_db where short_name is '%s';" % scrip_code)
        res = cursor.fetchall()
        print(res)
        return res[0]

    def checkScripInPortfolioDB(self, scrip_code) -> bool:
        try:
            cursor = self.conn.cursor()
        except Exception as e:
            print(e)
            return -1

        cursor.execute("SELECT calendar_event_id FROM portfolio_db where short_name is '%s';" % scrip_code)
        res = cursor.fetchall()
        print(res)
        if len(res) == 0:
            return False
        elif res[0] == "":
            return False
        else:
            return True

    def addScripInPortfolioDB(self, scrip: set, num_cols) -> None:
        try:
            cursor = self.conn.cursor()
        except Exception as e:
            print(e)
            return -1

        try:
            sql_query_prefix = "INSERT INTO portfolio_db VALUES (" + (num_cols-1) * "?," + "?)"
            cursor.execute(sql_query_prefix, scrip)
            self.conn.commit()

        except Exception as e:
            print(e)
