import streamlit as st
import mysql.connector
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

def login():
    # Create a title for your page
    st.title("Login Page")
    session_state = st.session_state

    # Check if the user is already logged in
    if 'logged_in' in session_state and session_state['logged_in']:
        st.success(f"Logged in as {session_state['username']}")

        # Add a logout button
        if st.button("Logout"):
            session_state['logged_in'] = False
            session_state['username'] = ""
            st.experimental_rerun()

        return

    # Create a text input for the user to enter their username
    username = st.text_input("Username")

    # Create a password input for the user to enter their password
    password = st.text_input("Password", type="password")

    # Create a submit button for the user to press to authenticate
    if st.button("Login"):
        if username and password:
            try:
                # Create a new connection for each login attempt
                cnx = mysql.connector.connect(**db_config)
                cursor = cnx.cursor(dictionary=True)

                # Fetch the user details from the database
                cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()

                if user and 'password' in user:
                    stored_password = user['password']
                    
                    # Verify the password
                    if decrypt_message(stored_password.encode(), key) == password:
                        session_state['logged_in'] = True
                        session_state['username'] = username
                        st.success("Login successful!")
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Invalid username or password")

                cursor.close()
                cnx.close()

            except mysql.connector.Error as err:
                st.error(f"Database error: {err}")
        else:
            st.error("Please enter both username and password")

login()
