from flask import Flask, request, jsonify
import cv2
import os
from app import app

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    role = data.get("role")

    if not name:
        return jsonify({"status": "error", "message": "Name is required"})

    # SAME LOGIC (unchanged)
    if role == "Admin":
        path = f"Dataset/admins/{name}"
    else:
        path = f"Dataset/users/{name}"

    os.makedirs(path, exist_ok=True)

    cap = cv2.VideoCapture(0)

    count = 0

    print("Press SPACE to capture images")

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

    return jsonify({
        "status": "success",
        "message": "Registration Successful"
    })