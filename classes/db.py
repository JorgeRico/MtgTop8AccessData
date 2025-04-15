import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

class Db:

    def __init__(self):
        load_dotenv()
        # ## database
        self.config = {
            'host'     : os.getenv('HOST_NAME'),
            'port'     : os.getenv('PORT_NAME'),
            'database' : os.getenv('DATABASE_NAME'),
            'user'     : os.getenv('USER_NAME'),
            'password' : os.getenv('PASSWORD')
        }

    def connection(self):
        connection = None

        try:
            connection = mysql.connector.connect(**self.getConfig())

            return connection
                
        except Error as e:
            print("Error while connecting to MySQL %s" %e)
        # finally:
        #     if connection.is_connected():
        #         self.endConnection(connection)

    def getConfig(self):
        return self.config

    def endConnection(self, connection):
        try:
            cursor = connection.cursor()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        except Error as e:
            print("Error while connecting to MySQL %s" %e)

    def executeQuery(self, connection, query):
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            # print(cursor.rowcount, "Record inserted successfully into table")
            cursor.close()
        except Error as e:
            print("Error while connecting to MySQL %s" %e)
    
    def executeInsertQuery(self, connection, query):
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            id = cursor.lastrowid
            cursor.close()
            
            return id
        except Error as e:
            print("Error while connecting to MySQL %s" %e)

    def selectQuery(self, connection, query):
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            final_result = [list(i) for i in result]
            cursor.close()

            return final_result
        except Error as e:
            print("Error while connecting to MySQL %s" %e)
    
    def getOneColumnResultSingleRow(self, result):
        for item in result:
            itemResult = item[0]
            break
        
        return itemResult

    def dropTable(self, connection, tableName):
        try:
            cursor = connection.cursor()
            delete_table_query = "DROP TABLE " + tableName
            cursor.execute(delete_table_query)
        except Error as e:
            print("Error while connecting to MySQL %s" %e)

    def truncateTable(self, connection, tableName):
        try:
            cursor = connection.cursor()
            delete_table_query = "TRUNCATE TABLE " + tableName
            cursor.execute(delete_table_query)
        except Error as e:
            print("Error while connecting to MySQL %s" %e)