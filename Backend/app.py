from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2
from deepface import DeepFace
import os
import csv
from datetime import datetime

app = Flask(__name__)
CORS(app)

THRESHOLD = 0.4


# ================= LOG FUNCTION =================
def save_log(name, role, status):

    file_path = "logs/login_log.csv"

    if not os.path.exists("logs"):
        os.makedirs("logs")

    if not os.path.exists(file_path):
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Role", "Date", "Time", "Status"])

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, role, date, time, status])


# ================= HOME =================
@app.route("/")
def home():
    return "Backend Running 🚀"


# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():

    cap = cv2.VideoCapture(0)

    frame_count = 0
    detected = False

    while True:
        ret, frame = cap.read()

        if not ret:
            return jsonify({"status": "camera_error"})

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

                if len(admin[0]) > 0 and admin[0].iloc[0]["distance"] < THRESHOLD:

                    name = admin[0].iloc[0]["identity"].split("\\")[-2]

                    save_log(name, "Admin", "Success")

                    cap.release()
                    cv2.destroyAllWindows()

                    return jsonify({
                        "status": "success",
                        "role": "admin",
                        "name": name
                    })

                # 🔵 User Check
                user = DeepFace.find(
                    img_path="test.jpg",
                    db_path="dataset/users",
                    enforce_detection=True
                )

                if len(user[0]) > 0 and user[0].iloc[0]["distance"] < THRESHOLD:

                    name = user[0].iloc[0]["identity"].split("\\")[-2]

                    save_log(name, "User", "Success")

                    cap.release()
                    cv2.destroyAllWindows()

                    return jsonify({
                        "status": "success",
                        "role": "user",
                        "name": name
                    })

            except:
                pass

        if frame_count > 200:
            break

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    save_log("Unknown", "Unknown", "Failed")

    return jsonify({
        "status": "failed",
        "message": "Face not matched"
    })


# ================= REGISTER =================
@app.route("/register", methods=["POST"])
def register():

    data = request.json
    name = data.get("name")
    role = data.get("role")

    if not name:
        return jsonify({"status": "error", "message": "Name required"})

    if role == "admin":
        path = f"dataset/admins/{name}"
    else:
        path = f"dataset/users/{name}"

    os.makedirs(path, exist_ok=True)

    cap = cv2.VideoCapture(0)

    count = 0

    while count < 10:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Register", frame)

        if cv2.waitKey(1) == 32:
            cv2.imwrite(f"{path}/{count}.jpg", frame)
            count += 1

    cap.release()
    cv2.destroyAllWindows()

    return jsonify({
        "status": "registered",
        "name": name
    })


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)