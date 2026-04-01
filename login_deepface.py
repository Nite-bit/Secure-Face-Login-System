import streamlit as st
import cv2
from deepface import DeepFace
import csv
from datetime import datetime
import os

def save_log(name, role, status):

    file_path = "logs/login_log.csv"

    # Create file if not exists
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Role", "Date", "Time", "Status"])

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, role, date, time, status])

THRESHOLD = 0.4

def show():

    st.title("🔑 Face Login")

    if st.button("Start Camera"):

        cap = cv2.VideoCapture(0)

        status = st.empty()
        status.info("Look at camera for authentication...")

        frame_count = 0
        detected = False   # ✅ track match

        while True:
            ret, frame = cap.read()

            if not ret:
                status.error("Camera error ❌")
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

                            name = admin[0].iloc[0]["identity"].split("\\")[-2]

                            save_log(name, "Admin", "Success")

                            status.success(f"Admin Detected ✅ ({name})")

                            cap.release()
                            cv2.destroyAllWindows()

                            st.session_state.logged_in = True
                            st.session_state.role = "admin"

                            detected = True
                            break

                    # 🔵 User Check
                    user = DeepFace.find(
                        img_path="test.jpg",
                        db_path="dataset/users",
                        enforce_detection=True
                    )

                    if len(user[0]) > 0:
                        if user[0].iloc[0]["distance"] < THRESHOLD:

                            name = user[0].iloc[0]["identity"].split("\\")[-2]

                            save_log(name, "User", "Success")

                            status.success(f"User Detected ✅ ({name})")

                            cap.release()
                            cv2.destroyAllWindows()

                            st.session_state.logged_in = True
                            st.session_state.role = "user"

                            detected = True
                            break

                except:
                    # ❌ Face not detected
                    status.warning("Face not detected ⚠️ Please look at camera")

            # ❌ Stop after some time
            if frame_count > 200:
                break

            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

        # ✅ AFTER LOOP (IMPORTANT)
        if not detected:
            status.error("Face not matched ❌")

            save_log("Unknown", "Unknown", "Failed")

        st.rerun()