import mysql.connector
from db import cnx_pool

# Obtain a connection from the connection pool once and reuse it
cnx = cnx_pool.get_connection()

def create_log(sensorid, name, date, log_time, userid):
    cursor = cnx.cursor(prepared=True)  # Use prepared statements for better performance
    try:
        cursor.execute("""
            INSERT INTO log (sensorid, name, date, time, userid)
            VALUES (%s, %s, %s, %s, %s)
        """, (sensorid, name, date, log_time, userid))
        cnx.commit()
    except mysql.connector.Error as err:  # Correct the exception handling
        print(f"Error creating log entry: {err}")
    finally:
        cursor.close()
        # Don't close the connection here if you plan to reuse it for other operations
        # cnx.close()

# If you need to close the connection at the end of your script or after a batch of operations
# def close_connection():
#     cnx.close()

# # Example usage
# create_log(1, 'Temperature Sensor', '2024-08-01', '12:00:00', 101)
# create_log(2, 'Humidity Sensor', '2024-08-01', '12:05:00', 102)
# # Close the connection after all operations
# close_connection()
