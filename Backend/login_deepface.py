from flask import Flask, jsonify
from flask_cors import CORS
import cv2
from deepface import DeepFace
import csv
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

THRESHOLD = 0.4


def save_log(name, role, status):

    if not os.path.exists("logs"):
        os.makedirs("logs")

    file_path = "logs/login_log.csv"

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


@app.route("/login", methods=["POST"])
def login():

    cap = cv2.VideoCapture(0)

    frame_count = 0

    while frame_count < 200:
        ret, frame = cap.read()

        if not ret:
            return jsonify({"status": "error", "message": "Camera error"})

        frame_count += 1

        if frame_count % 20 == 0:
            cv2.imwrite("test.jpg", frame)

            try:
                # 🔴 Admin
                admin = DeepFace.find(
                    img_path="test.jpg",
                    db_path="Dataset/admins",
                    enforce_detection=True
                )

                if len(admin[0]) > 0 and admin[0].iloc[0]["distance"] < THRESHOLD:
                    name = admin[0].iloc[0]["identity"].split("\\")[-2]

                    save_log(name, "Admin", "Success")

                    cap.release()
                    return jsonify({"status": "success", "role": "admin", "name": name})

                # 🔵 User
                user = DeepFace.find(
                    img_path="test.jpg",
                    db_path="Dataset/users",
                    enforce_detection=True
                )

                if len(user[0]) > 0 and user[0].iloc[0]["distance"] < THRESHOLD:
                    name = user[0].iloc[0]["identity"].split("\\")[-2]

                    save_log(name, "User", "Success")

                    cap.release()
                    return jsonify({"status": "success", "role": "user", "name": name})

            except Exception as e:
                print("Error:", e)

    cap.release()

    save_log("Unknown", "Unknown", "Failed")

    return jsonify({"status": "fail", "message": "Face not matched"})