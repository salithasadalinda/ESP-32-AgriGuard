import db
import time

def create_log(sensorid, name, date, time, userid):
    """
    This function creates a log entry in the database.

    Args:
        sensorid (str): The ID of the sensor.
        name (str): The name of the sensor.
        date (str): The date of the log entry.
        time (str): The time of the log entry.
        userid (int): The ID of the user associated with the log entry.

    Returns:
        None
    """
    # Initialize the connection pool
    cnx_pool = db.cnx_pool
    cnx = cnx_pool.get_connection()

    try:
        cnx.start_transaction()

        # Get the current time to use as a unique identifier
        current_time = int(time.time())

        # Insert the log entry into the database
        cursor = cnx.cursor()
        sql = """
            INSERT INTO logs (id, sensorid, name, date, time, userid)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        val = (current_time, sensorid, name, date, time, userid)
        cursor.execute(sql, val)

        # Commit the transaction
        cnx.commit()
        
        # Print a success message
        print("Log entry created successfully.")

    except db.mysql.connector.Error as err:
        # Rollback the transaction
        cnx.rollback()

        # Print an error message
        print("Error creating log entry: {}".format(err))

    finally:
        # Close the cursor and connection
        if cursor is not None:
            cursor.close()
        if cnx is not None:
            cnx.close()
