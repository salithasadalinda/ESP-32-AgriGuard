
import mysql.connector

# Define the database configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': 3308,
    'database': 'agriguard',
    'raise_on_warnings': True
}
try:
    connection = mysql.connector.connect(**db_config)

except mysql.connector.Error as err:
    print(f"Error: {err}")