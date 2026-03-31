import streamlit as st
import cv2
import os

def show():

    st.title("📝 Registration")

    name = st.text_input("Enter Name")
    role = st.selectbox("Select Role", ["Admin", "User"])

    if st.button("Start Capture") and name:

        if role == "Admin":
            path = f"dataset/admins/{name}"
        else:
            path = f"dataset/users/{name}"

        os.makedirs(path, exist_ok=True)

        cap = cv2.VideoCapture(0)

        st.write("Press SPACE to capture images")

        count = 0

        while count < 10:
            ret, frame = cap.read()
            cv2.imshow("Register", frame)

            key = cv2.waitKey(1)

            if key == 32:  # SPACE
                cv2.imwrite(f"{path}/{count}.jpg", frame)
                count += 1
                print(f"Captured {count}")

        cap.release()
        cv2.destroyAllWindows()

        st.success("Registration Successful!")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()