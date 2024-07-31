# login page
import streamlit as st

def login():
    # Create a title for your page
    st.title("Login Page")

    # Create a text input for the user to enter their username
    username = st.text_input("Username")

    # Create a password input for the user to enter their password
    password = st.text_input("Password", type="password")

    # Create a submit button for the user to press to authenticate
    if st.button("Login"):
        # Check if the username and password are correct
        if username == "admin" and password == "admin":
            session_state = st.session_state
            if 'logged_in' not in session_state:
                session_state['logged_in'] = True
                session_state['username'] = username
                st.session_state = session_state
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

login()