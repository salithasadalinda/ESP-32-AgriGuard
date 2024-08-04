import streamlit as st

login=st.Page("app_pages/login.py", title="login", icon="🔥")
dashboard=st.Page("app_pages/dashboard.py", title="dashboard", icon=":material/favorite:")
createuser=st.Page("app_pages/create_user.py", title="createuser", icon=":material/favorite:")
camerasetup=st.Page("app_pages/camera_setup.py", title="camerasetup", icon=":material/favorite:")
pages=[
    login,
    createuser
]

#check if user is logged in
session_state = st.session_state
print(session_state)
if 'logged_in'in session_state:
    pages.append(dashboard)
    pages.append(camerasetup)
    
elif 'logged_in' not in session_state or not session_state['logged_in']:
    if dashboard in pages:
        pages.remove(dashboard)
        pages.remove(camerasetup)
st.session_state = session_state

pg = st.navigation(pages)

pg.run()