import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from frontend.utils.state import init_state, is_logged_in, logout, go_to
from frontend.utils.api_client import login, register

st.set_page_config(page_title="Prediction Tracker",
                   layout="wide", initial_sidebar_state="expanded")
init_state()

def show_login():
    st.title("Prediction Tracker")
    st.caption("Track your predictions. Measure your confidence. Know your biases.")
    st.divider()
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        with st.form("login_form"):
            email    = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit   = st.form_submit_button("Login", use_container_width=True)
        if submit:
            data, code = login(email, password)
            if code == 200:
                st.session_state.token = data["access_token"]
                st.session_state.user  = data["user"]
                st.rerun()
            else: st.error(data.get("detail", "Login failed"))
    with tab2:
        with st.form("register_form"):
            name     = st.text_input("Full name")
            email    = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit   = st.form_submit_button("Create account", use_container_width=True)
        if submit:
            data, code = register(name, email, password)
            if code == 201:
                st.session_state.token = data["access_token"]
                st.session_state.user  = data["user"]
                st.rerun()
            else: st.error(data.get("detail", "Registration failed"))

def show_sidebar():
    with st.sidebar:
        user = st.session_state.user
        st.markdown(f"### Hi, {user['name']}")
        st.caption(user["email"])
        st.divider()
        if st.button("Dashboard",  use_container_width=True): go_to("dashboard")
        if st.button("Calibration", use_container_width=True): go_to("calibration")
        st.divider()
        if st.button("Logout", use_container_width=True): logout()

def main():
    if not is_logged_in():
        show_login()
        return
    show_sidebar()
    page = st.session_state.page
    if   page == "dashboard":   from frontend.pages.dashboard import show; show()
    elif page == "detail":      from frontend.pages.prediction_detail import show; show()
    elif page == "calibration": from frontend.pages.calibration import show; show()

if __name__ == "__main__": main()