import streamlit as st
import login_deepface
import register
import admin_deshboard
import user_dashboard

st.set_page_config(page_title="Secure Face Login System")

if "page" not in st.session_state:
    st.session_state.page = "home"

st.title("🔐 Secure Face Login System")

# HOME PAGE
if st.session_state.page == "home":

    col1, col2 = st.columns(2)

    if col1.button("🔑 Login"):
        st.session_state.page = "login"
        st.rerun()

    if col2.button("📝 Register"):
        st.session_state.page = "register"
        st.rerun()

# REGISTER PAGE
elif st.session_state.page == "register":
    register.show()

# LOGIN PAGE
elif st.session_state.page == "login":
    login_deepface.show()

# ADMIN PAGE
elif st.session_state.page == "admin":
    admin_deshboard.show()

# USER PAGE
elif st.session_state.page == "user":
    user_dashboard.show()