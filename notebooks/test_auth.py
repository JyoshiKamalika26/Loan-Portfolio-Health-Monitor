import streamlit as st
from auth import *

require_login()

st.success("Login Successful")

st.write("User :", st.session_state.username)

st.write("Role :", st.session_state.role)

logout()