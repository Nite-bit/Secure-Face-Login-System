import streamlit as st
import cv2
import os

def show():

    st.title("Register Face")

    name = st.text_input("Enter Name")
    role = st.selectbox("Select Role", ["Admin", "User"])

    if st.button("Start Registration"):

        if role == "Admin":
            path = f"dataset/admins/{name}"
        else:
            path = f"dataset/users/{name}"

        os.makedirs(path, exist_ok=True)

        cap = cv2.VideoCapture(0)

        st.info("Press SPACE in camera window")

        while True:
            ret, frame = cap.read()
            cv2.imshow("Register Face", frame)

            if cv2.waitKey(1) == 32:  # SPACE pressed
                break

        count = 0

        while count < 10:
            ret, frame = cap.read()

            img_path = f"{path}/{count}.jpg"
            cv2.imwrite(img_path, frame)

            count += 1
            cv2.waitKey(300)

        cap.release()
        cv2.destroyAllWindows()

        st.success("Registration Completed")
    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()