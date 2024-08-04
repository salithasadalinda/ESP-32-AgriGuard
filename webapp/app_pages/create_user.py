import mysql.connector
import streamlit as st
from db import decrypt_message, encrypt_message, key

# Define the database configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': 3308,
    'database': 'agriguard',
    'raise_on_warnings': True
}

def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def close_connection(connection):
    if connection:
        connection.close()

def create_user():
    st.title("Create User Page")

    # Create a text input for the user to enter their username
    username = st.text_input("Username")
    
    email = st.text_input("Email")

    # Create a password input for the user to enter their password
    password = st.text_input("Password", type="password")
    password = encrypt_message(password, key)
    
    # Create a submit button for the user to press to create user
    if st.button("Create User"):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()

                query = "INSERT INTO agriguard.users (username, email, password) VALUES (%s, %s, %s)"
                cursor.execute(query, (username, email, password))
                conn.commit()
                st.success(f"User {username} created successfully!")
                
                cursor.close()
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
            finally:
                close_connection(conn)
        else:
            st.error("Failed to connect to the database.")

create_user()
