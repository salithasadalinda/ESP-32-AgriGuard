import mysql.connector
import streamlit as st
import pandas as pd

# Define the database configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': 3308,
    'database': 'agriguard',
    'raise_on_warnings': True
}

# Function to create a connection
def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Streamlit app
session_state = st.session_state
user = session_state['username']

if 'logged_in' not in session_state or not session_state['logged_in']:
    st.error('Please login first!')
else:
    cnx = create_connection()
    if cnx:
        cursor = cnx.cursor()
        query = 'SELECT * FROM agriguard.log'
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        st.dataframe(df)
        cursor.close()
        cnx.close()
    else:
        st.error('Database connection failed.')
