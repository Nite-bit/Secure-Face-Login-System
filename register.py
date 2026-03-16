import streamlit as st
import cv2
import os

def show():

    st.title("📝 Register")

    role = st.selectbox("Select Role", ["Admin", "User"])

    name = st.text_input("Enter Name")

    if st.button("Capture Face") and name:

        if role == "Admin":
            path = f"dataset/admins/{name}"
        else:
            path = f"dataset/users/{name}"

        os.makedirs(path, exist_ok=True)

        cap = cv2.VideoCapture(0)

        count = 0

        st.write("Capturing images...")

        while count < 20:
            ret, frame = cap.read()
            cv2.imshow("Register", frame)

            cv2.imwrite(f"{path}/{count}.jpg", frame)
            count += 1

            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

        st.success("Registration Successful")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()