import streamlit as st

def init_state():
    defaults = {
        "token":       None,
        "user":        None,
        "page":        "dashboard",
        "selected_id": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def is_logged_in():
    return st.session_state.get("token") is not None

def logout():
    st.session_state.token = None
    st.session_state.user  = None
    st.session_state.page  = "dashboard"
    st.rerun()

def go_to(page, selected_id=None):
    st.session_state.page = page
    if selected_id:
        st.session_state.selected_id = selected_id
    st.rerun()