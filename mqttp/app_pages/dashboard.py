
import streamlit as st
import pandas as pd


from db import cnx_pool
session_state = st.session_state
user = session_state['username']
if 'logged_in' not in session_state or not session_state['logged_in']:
    st.error('Please login first!')

if 'logged_in' in st.session_state or session_state['logged_in']:
    if user is None:
        cnx = cnx_pool.get_connection()
        cursor = cnx.cursor()

        query = 'SELECT * FROM agriguard.log'

        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        
        st.dataframe(df)
