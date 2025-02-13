import argparse
from mysql.connector import Error
from .Helpers.Setting import Settings  # Assuming you have a Settings class to handle environment variables
from .Database.MySQLWrapper import MySQLWrapper

def migrate():
    """Handles the database migration."""
    print("Database migration enabled.")
    # Simulating the inclusion of a setup script
    print("Including database setup...")
    # Here you would typically run setup scripts or migrations
    print("Database migration ended.")

def main():
    # Parsing command-line arguments
    parser = argparse.ArgumentParser(description="Database Setup Script")
    parser.add_argument('--migrate', action='store_true', help="Run database migration")
    args = parser.parse_args()

    # Handle migration option
    if args.migrate:
        migrate()

    try:
        # Creating an instance of MySQLWrapper and checking the charset
        mysql_wrapper = MySQLWrapper()

        # Retrieve the charset info
        charset_info = mysql_wrapper.get_charset()
        if not charset_info:
            raise Exception("Charset could not be read.")

        # Print the charset and collation info
        print(f"{mysql_wrapper.get_database_name()}'s charset: {charset_info[0][1]}")
        print(f"Collation: {charset_info[1][1]}")

        # Close the connection
        mysql_wrapper.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
