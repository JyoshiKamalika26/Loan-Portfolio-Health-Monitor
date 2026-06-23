import streamlit as st

USERS = {
    "admin": {
        "password": "admin123",
        "role": "Admin"
    },
    "analyst": {
        "password": "analyst123",
        "role": "Risk Analyst"
    },
    "manager": {
        "password": "manager123",
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