import streamlit as st
import cv2
from deepface import DeepFace

def show():

    st.title("🔑 Face Login")

    if st.button("Login with Face"):

        cap = cv2.VideoCapture(0)

        st.write("Capturing face...")

        while True:
            ret, frame = cap.read()
            cv2.imshow("Login", frame)

            if cv2.waitKey(1) == 32:
                cv2.imwrite("test.jpg", frame)
                break

        cap.release()
        cv2.destroyAllWindows()

        # Check Admin
        admin = DeepFace.find(
            img_path="test.jpg",
            db_path="dataset/admins",
            enforce_detection=False
        )

        if len(admin[0]) > 0:
            st.success("Admin Login Successful")
            st.session_state.page = "admin"
            st.rerun()

        # Check User
        user = DeepFace.find(
            img_path="test.jpg",
            db_path="dataset/users",
            enforce_detection=False
        )

        if len(user[0]) > 0:
            st.success("User Login Successful")
            st.session_state.page = "user"
            st.rerun()

        st.error("Access Denied ❌")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()