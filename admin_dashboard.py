import streamlit as st
import pandas as pd

def show():

    st.title("📊 Admin Dashboard")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()

    df = pd.read_csv("logs/login_log.csv")

    st.subheader("Login History")
    st.dataframe(df)

    st.subheader("Login Statistics")
    df.columns = df.columns
    st.bar_chart(df["Status"].value_counts())

    st.subheader("Login Distribution")
    st.pyplot(df["Role"].value_counts().plot.pie(autopct='%1.1f%%').figure)

    date = st.selectbox("Select Date", df["Date"].unique())
    filtered = df[df["Date"] == date]
    st.dataframe(filtered)

    name = st.text_input("Search User")
    if name:
        st.dataframe(df[df["Name"].str.contains(name)])