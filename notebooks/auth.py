import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

USERS = {
    os.getenv("ADMIN_USERNAME"): {
        "password": os.getenv("ADMIN_PASSWORD"),
        "role": "Admin"
    },
    os.getenv("ANALYST_USERNAME"): {
        "password": os.getenv("ANALYST_PASSWORD"),
        "role": "Risk Analyst"
    },
    os.getenv("MANAGER_USERNAME"): {
        "password": os.getenv("MANAGER_PASSWORD"),
        "role": "Manager"
    }
}


def init_session():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = ""

    if "role" not in st.session_state:
        st.session_state.role = ""


def login():

    st.title("🔐 Loan Portfolio Health Monitor System")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username in USERS:

            if USERS[username]["password"] == password:

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = USERS[username]["role"]

                st.rerun()

            else:
                st.error("Invalid Password")

        else:
            st.error("Invalid Username")


def require_login():

    init_session()

    if not st.session_state.logged_in:
        login()
        st.stop()


def logout():

    st.sidebar.markdown("---")

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()