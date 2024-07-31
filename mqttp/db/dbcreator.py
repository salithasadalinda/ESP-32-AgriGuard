import mysql.connector
from cryptography.fernet import Fernet

config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': 3308,
    'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# Handle error
try:
    cursor.execute("""
        CREATE DATABASE IF NOT EXISTS agriguard
        DEFAULT CHARACTER SET utf8mb4
        DEFAULT COLLATE utf8mb4_unicode_ci
    """)
except mysql.connector.Error as err:
    print("Error: {}".format(err))
    if err.errno == 6:
        print("Database 'agriguard' already exists.")

cnx.database = 'agriguard'

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        userid INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        sensorid VARCHAR(255),
        name VARCHAR(255),
        date DATE,
        time TIME,
        userid INT,
        FOREIGN KEY (userid) REFERENCES users(userid)
    )
""")

cursor.close()
cnx.close()
