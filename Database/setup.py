from mysql.connector import Error
from .MySQLWrapper import MySQLWrapper
from ..Helpers.Setting import Settings



# Using MySQLWrapper to run the query

try:
    # Create an instance of MySQLWrapper (this connects to the database)
    mysql_wrapper = MySQLWrapper()

    # SQL query to create the table if it doesn't exist
    sql_query = """
        CREATE TABLE IF NOT EXISTS cars (
            id INT PRIMARY KEY AUTO_INCREMENT,
            make VARCHAR(50),
            model VARCHAR(50),
            year INT,
            color VARCHAR(20),
            price FLOAT,
            mileage FLOAT,
            transmission VARCHAR(20),
            engine VARCHAR(20),
            status VARCHAR(10)
        );
    """

    # Run the query
    result = mysql_wrapper.query(sql_query)

    if not result:
        raise Exception('Could not execute query.')
    else:
        print("Successfully ran all SQL setup queries.")

except Exception as e:
    print(f"An error occurred: {e}")
