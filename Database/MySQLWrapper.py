import mysql.connector
from mysql.connector import Error
from Helpers.Setting import Settings  # Assuming you have a Settings class similar to the one described earlier.

class MySQLWrapper:
    def __init__(self, hostname='localhost', username=None, password=None, database=None, port=None, socket=None):
        """
        MySQLに接続し、もしデータベースが存在しない場合は作成する。
        """
        try:
            databaseSetting = Settings.env()["DATABASE"]
            username = username or databaseSetting['DATABASE_USER']
            password = password or databaseSetting['DATABASE_USER_PASSWORD']
            database = database or databaseSetting['DATABASE_NAME']
            port = port or databaseSetting["DATABASE_PORT"]

            # MySQLに接続（データベース指定なし）
            self.connection = mysql.connector.connect(
                host=hostname,
                user=username,
                password=password,
                port=port,
                unix_socket=socket
            )
            self.cursor = self.connection.cursor()

            # データベースが存在するかチェック
            self.cursor.execute(f"SHOW DATABASES LIKE '{database}'")
            result = self.cursor.fetchone()

            # データベースが存在しない場合は作成
            if not result:
                print(f"Database '{database}' not found. Creating...")
                self.cursor.execute(f"CREATE DATABASE `{database}`")
                print(f"Database '{database}' created successfully.")

            # 一度切断し、指定したデータベースで再接続
            self.cursor.close()
            self.connection.close()

            self.connection = mysql.connector.connect(
                host=hostname,
                user=username,
                password=password,
                database=database,
                port=port,
                unix_socket=socket
            )
            self.cursor = self.connection.cursor()

            if self.connection.is_connected():
                print(f"Connected to MySQL database: {database}")

        except Error as e:
            print(f"Error: {e}")
            raise
        

    def getDatabaseName(self):
        """
        Retrieves the name of the default database.
        """
        try:
            self.cursor.execute("SELECT DATABASE() AS the_db")
            result = self.cursor.fetchone()
            if result and result[0]:
                return result[0]
            else:
                raise Exception("Couldn't get database name")
        except Exception as e:
            print(f"Error retrieving database name: {e}")
            raise


    def query(self, sql, params=None):
        """Executes an SQL query and returns results for SELECT statements."""
        try:
            self.cursor.execute(sql, params)  # Execute query with params
            if sql.strip().lower().startswith("select"):  # For SELECT queries
                return self.cursor.fetchall()  # Fetch all rows
            else:  # For INSERT, UPDATE, DELETE queries
                self.connection.commit()  # Commit changes
                return self.cursor.rowcount  # Return number of affected rows
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            self.connection.rollback()  # Rollback on error
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.connection.rollback()
            return False
