import streamlit as st

def show():

    st.title("👤 User Dashboard")

    st.write("Welcome User")

    if st.button("Logout"):
        st.session_state.page = "home"
        st.rerun()