import streamlit as st
import login_deepface
import register
import admin_deshboard
import user_dashboard

st.set_page_config(
    page_title="Secure Face login",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded"
)

if "page" not in st.session_state:
    st.session_state.page = "home"

st.title("🔐 Secure Face Login System")

if st.session_state.page == "home":

    st.subheader("Select Option")

    col1, col2 = st.columns(2)

    if col1.button("Login"):
        st.session_state.page = "login"
        st.rerun()

    if col2.button("Register"):
        st.session_state.page = "register"
        st.rerun()

elif st.session_state.page == "login":
    login_deepface.show()

elif st.session_state.page == "register":
    register.show()

elif st.session_state.page == "admin":
    admin_deshboard.show()

elif st.session_state.page == "user":
    user_dashboard.show()