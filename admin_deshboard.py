import streamlit as st
import pandas as pd

def show():

    st.title("📊 Admin Dashboard")

    if st.button("Logout"):
        st.session_state.page = "login"
        st.rerun()

    df = pd.read_csv("logs/login_log.csv")

    st.subheader("Login History")
    st.dataframe(df)

    st.subheader("Login Statistics")
    df.columns = df.columns
    st.bar_chart(df["Status"].value_counts())