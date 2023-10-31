from enum import Enum
import sqlite3
import mysql.connector
from mysql.connector import errorcode
import psycopg2


class DBTypes(Enum):
    MYSQL = "mysql"
    PSQL = "psql"
    SQLITE = "sqlite"

class DBAdapter:
    def __init__(
        self,
        db_type: DBTypes,
        db_name: str = None,
        db_username: str = None,
        db_password: str = None,
        db_host: str = None,
    ):
        self.db_type = db_type
        self.db_name = db_name
        self.db_username = db_username
        self.db_password = db_password
        self.db_host = db_host
        self.connection = None

    def connect(self):
        connection = None
        match self.db_type:
            case DBTypes.MYSQL.value:
                try:
                    connection = mysql.connector.connect(
                        host=self.db_host,
                        database=self.db_name,
                        user=self.db_username,
                        password=self.db_password,
                    )
                except mysql.connector.Error as e:
                    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                        print("Something is wrong with your user name or password")
                    elif e.errno == errorcode.ER_BAD_DB_ERROR:
                        print("Database does not exist")
                    else:
                        print(e)

            case DBTypes.PSQL.value:
                connection = psycopg2.connect(
                    host=self.db_host,
                    database=self.db_name,
                    user=self.db_username,
                    password=self.db_password,
                )
            case DBTypes.SQLITE.value:
                connection = sqlite3.connect(self.db_name)

        self.connection = connection
    
    def execute_query(self, query_text: str):
        cursor = self.connection.cursor()
        cursor.execute(query_text)
        results = cursor.fetchall() 
        cursor.close()
        return results
