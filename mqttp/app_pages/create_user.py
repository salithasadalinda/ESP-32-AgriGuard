import streamlit as st
from db import cnx_pool,decrypt_message,encrypt_message,key

def create_user():
    st.title("Create User Page")

    # Create a text input for the user to enter their username
    username = st.text_input("Username")
    
    email = st.text_input("Email")

    # Create a password input for the user to enter their password
    password = st.text_input("Password", type="password")
    password = encrypt_message(password,key)
    # password = decrypt_message(password)
    # Create a submit button for the user to press to create user
    if st.button("Create User"):
        with cnx_pool.get_connection() as cnx:
            cursor = cnx.cursor()

            query = "INSERT INTO agriguard.users (username,email, password) VALUES (%s, %s,%s)"
            cursor.execute(query, (username,email, password))
            cnx.commit()
            st.success(f"User {username} created successfully!")
            
create_user()


