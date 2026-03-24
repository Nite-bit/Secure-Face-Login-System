import streamlit as st
import cv2
from deepface import DeepFace
import pandas as pd
from datetime import datetime
import os


# ---------- Function to Store Login ----------
def store_login(name, role):

    file = "logs/login_log.csv"

    now = datetime.now()

    data = {
        "Name": name,
        "Role": role,
        "Date": now.strftime("%Y-%m-%d"),
        "Time": now.strftime("%H:%M:%S"),
        "Status": "Success"
    }

    if os.path.exists(file):
        df = pd.read_csv(file)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])

    df.to_csv(file, index=False)


# ---------- Login Page ----------
def show():

    st.title("🔑 Face Login")

    if st.button("Scan Face"):

        cap = cv2.VideoCapture(0)

        st.write("Scanning Face...")

        # Capture automatically
        ret, frame = cap.read()

        cv2.imwrite("test.jpg", frame)

        cap.release()

# -------- Check Admin Dataset --------
try:
    admin_result = DeepFace.find(
        img_path="test.jpg",
        db_path="dataset/admins",
        enforce_detection=False
    )

    if len(admin_result[0]) > 0:
        identity_path = admin_result[0].iloc[0]["identity"]
        name = os.path.basename(os.path.dirname(identity_path))

        store_login(name, "Admin")

        st.success(f"Admin Login Successful : {name}")
        st.session_state.page = "admin"
        st.rerun()

except:
    pass


# -------- Check User Dataset --------
try:
    user_result = DeepFace.find(
        img_path="test.jpg",
        db_path="dataset/users",
        enforce_detection=False
    )

    if len(user_result[0]) > 0:
        identity_path = user_result[0].iloc[0]["identity"]
        name = os.path.basename(os.path.dirname(identity_path))

        store_login(name, "User")

        st.success(f"User Login Successful : {name}")
        st.session_state.page = "user"
        st.rerun()

except:
    pass

# -------- If not found --------
st.error("Access Denied")

if st.button("⬅ Back"):
    st.session_state.page = "home"
    st.rerun()