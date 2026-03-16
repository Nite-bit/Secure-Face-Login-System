import streamlit as st
import cv2
from deepface import DeepFace

def show():

    st.title("🔑 Face Login")

    if st.button("Scan Face"):

        cap = cv2.VideoCapture(0)

        st.write("Press SPACE in camera window")

        while True:
            ret, frame = cap.read()
            cv2.imshow("Camera", frame)

            if cv2.waitKey(1) == 32:
                cv2.imwrite("test.jpg", frame)
                break

        cap.release()
        cv2.destroyAllWindows()

        # Check Admin Dataset
        admin_result = DeepFace.find(
            img_path="test.jpg",
            db_path="dataset/admins",
            enforce_detection=False
        )

        if len(admin_result[0]) > 0:
            st.success("Admin Login Successful")
            st.session_state.page = "admin"
            st.rerun()

        # Check User Dataset
        user_result = DeepFace.find(
            img_path="test.jpg",
            db_path="dataset/users",
            enforce_detection=False
        )

        if len(user_result[0]) > 0:
            st.success("User Login Successful")
            st.session_state.page = "user"
            st.rerun()

        st.error("Access Denied")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()