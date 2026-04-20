from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import base64
import numpy as np

app = Flask(__name__)
CORS(app)

# Load Haarcascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

@app.route("/detect", methods=["POST"])
def detect_face():

    data = request.json
    image_data = data.get("image")

    if not image_data:
        return jsonify({"status": "error", "message": "No image received"})

    try:
        # 🔄 Decode base64 image
        image_data = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_data)

        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            return jsonify({
                "status": "success",
                "faces_detected": len(faces)
            })
        else:
            return jsonify({
                "status": "fail",
                "message": "No face detected"
            })

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error"})
        

if __name__ == "__main__":
    app.run(debug=True)