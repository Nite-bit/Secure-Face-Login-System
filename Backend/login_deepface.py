from flask import request, jsonify
from flask_cors import CORS
import cv2
from deepface import DeepFace
import base64
import numpy as np
import csv
from datetime import datetime
import os
from app import app

# ================= CONFIG =================
CORS(app, resources={r"/*": {"origins": "*"}})
THRESHOLD = 0.6

# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ADMIN_PATH = os.path.join(BASE_DIR, "Dataset", "admins")
USER_PATH = os.path.join(BASE_DIR, "Dataset", "users")
TEST_IMAGE_PATH = os.path.join(BASE_DIR, "test.jpg")

print("ADMIN PATH:", ADMIN_PATH, os.path.exists(ADMIN_PATH))
print("USER PATH:", USER_PATH, os.path.exists(USER_PATH))


# ================= LOG =================
def save_log(name, role, status):
    log_dir = os.path.join(BASE_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)

    file_path = os.path.join(log_dir, "login_log.csv")

    if not os.path.exists(file_path):
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Role", "Date", "Time", "Status"])

    now = datetime.now()

    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            name,
            role,
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            status
        ])


# ================= IMAGE DECODE =================
def decode_image(base64_string):
    try:
        image_data = base64_string.split(",")[1]
        image_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return img
    except:
        return None


# ================= MATCH FUNCTION =================
def match_face(test_img, db_path):
    try:
        for person in os.listdir(db_path):
            person_path = os.path.join(db_path, person)

            for img_name in os.listdir(person_path):
                db_img = os.path.join(person_path, img_name)

                result = DeepFace.verify(
                    img1_path=test_img,
                    img2_path=db_img,
                    model_name="Facenet512",
                    enforce_detection=False
                )

                print(f"Compare with {person}/{img_name} →", result["distance"])

                if result["verified"] and result["distance"] < THRESHOLD:
                    return True, person

        return False, None

    except Exception as e:
        print("ERROR:", e)
        return False, None


# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():
    print("\n🔥 LOGIN API HIT")

    try:
        data = request.json
        image_data = data.get("image")

        if not image_data:
            return jsonify({"status": "error"})

        img = decode_image(image_data)

        if img is None:
            return jsonify({"status": "error"})

        # Save image
        cv2.imwrite(TEST_IMAGE_PATH, img)

        # ================= ADMIN =================
        found, name = match_face(TEST_IMAGE_PATH, ADMIN_PATH)

        if found:
            save_log(name, "Admin", "Success")
            return jsonify({
                "status": "success",
                "role": "admin",
                "name": name
            })

        # ================= USER =================
        found, name = match_face(TEST_IMAGE_PATH, USER_PATH)

        if found:
            save_log(name, "User", "Success")
            return jsonify({
                "status": "success",
                "role": "user",
                "name": name
            })

        # ================= FAIL =================
        save_log("Unknown", "Unknown", "Failed")

        return jsonify({"status": "fail"})

    except Exception as e:
        print("SERVER ERROR:", e)
        return jsonify({"status": "error"})