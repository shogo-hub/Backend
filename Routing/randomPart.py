from Database.MySQLWrapper import MySQLWrapper
from mysql.connector import Error


db = MySQLWrapper()

def returnRandomParts():
    try:
        statement = "SELECT * FROM computer_parts ORDER BY RAND() LIMIT 1"

        result = db.query(sql=statement)
        part = result.fetch_assoc()
        return part

    except Error as e:
        print(f"Error fetching random part: {e}")
        return None