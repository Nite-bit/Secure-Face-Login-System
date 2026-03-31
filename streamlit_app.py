import streamlit as st
import login_deepface
import register
import admin_dashboard
import user_dashboard

st.set_page_config(page_title="Secure Face Login System")

# Initialize states
if "page" not in st.session_state:
    st.session_state.page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

# 🔐 If logged in → go to dashboards
if st.session_state.logged_in:

    if st.session_state.role == "admin":
        admin_dashboard.show()

    elif st.session_state.role == "user":
        user_dashboard.show()

# 🏠 HOME PAGE
elif st.session_state.page == "home":

    st.title("🔐 Secure Face Login System")

    col1, col2 = st.columns(2)

    if col1.button("🔑 Login"):
        st.session_state.page = "login"
        st.rerun()

    if col2.button("📝 Register"):
        st.session_state.page = "register"
        st.rerun()

# 🔑 LOGIN PAGE
elif st.session_state.page == "login":
    login_deepface.show()

# 📝 REGISTER PAGE
elif st.session_state.page == "register":
    register.show()