import streamlit as st
import cv2
from deepface import DeepFace

THRESHOLD = 0.4

def show():

    st.title("🔑 Face Login (Auto Mode)")

    if st.button("Start Camera"):

        cap = cv2.VideoCapture(0)

        status = st.empty()
        status.info("Look at camera for authentication...")

        frame_count = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            cv2.imshow("Login", frame)

            frame_count += 1

            if frame_count % 20 == 0:

                cv2.imwrite("test.jpg", frame)

                try:
                    # 🔴 Admin Check
                    admin = DeepFace.find(
                        img_path="test.jpg",
                        db_path="dataset/admins",
                        enforce_detection=True
                    )

                    if len(admin[0]) > 0:
                        if admin[0].iloc[0]["distance"] < THRESHOLD:

                            status.success("Admin Detected ✅")

                            cap.release()
                            cv2.destroyAllWindows()

                            st.session_state.logged_in = True
                            st.session_state.role = "admin"

                            break   # 🔥 VERY IMPORTANT

                    # 🔵 User Check
                    user = DeepFace.find(
                        img_path="test.jpg",
                        db_path="dataset/users",
                        enforce_detection=True
                    )

                    if len(user[0]) > 0:
                        if user[0].iloc[0]["distance"] < THRESHOLD:

                            status.success("User Detected ✅")

                            cap.release()
                            cv2.destroyAllWindows()

                            st.session_state.logged_in = True
                            st.session_state.role = "user"

                            break   # 🔥 VERY IMPORTANT

                except:
                    pass

            if cv2.waitKey(1) == 27:
                break

        # 🔥 AFTER LOOP → FORCE RERUN
        st.rerun()