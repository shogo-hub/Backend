import mysql.connector
from mysql.connector import Error
from ..Helpers.Setting import Settings  # Assuming you have a Settings class similar to the one described earlier.

class MySQLWrapper:
    def __init__(self, hostname='localhost', username=None, password=None, database=None, port=None, socket=None):
        """
        Initializes the MySQL connection. If connection fails, an exception is raised.
        Before initializing the database connection, ensure that error reporting is configured.
        For testing, you can input incorrect information in the .env settings.
        """
        try:
            username = username or Settings.env('DATABASE_USER')
            password = password or Settings.env('DATABASE_USER_PASSWORD')
            database = database or Settings.env('DATABASE_NAME')

            # Establish the connection
            self.connection = mysql.connector.connect(
                host=hostname,
                user=username,
                password=password,
                database=database,
                port=port,
                unix_socket=socket
            )

            if self.connection.is_connected():
                print("Connection to MySQL database established.")
        except Error as e:
            print(f"Error: {e}")
            raise

    def get_database_name(self):
        """
        Retrieves the name of the default database.
        Will raise an error if the query fails (e.g., if the query returns false or no rows are retrieved).
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT DATABASE() AS the_db")
        result = cursor.fetchone()
        return result[0] if result else None
