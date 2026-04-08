import { useNavigate } from "react-router-dom";
import { useRef, useEffect } from "react";
import "./login.css";

function Login() {
  const navigate = useNavigate();
  const videoRef = useRef(null);

  // 🎥 Start Camera Automatically
  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        videoRef.current.srcObject = stream;
      })
      .catch(() => {
        alert("Camera not accessible ❌");
      });
  }, []);

  const handleLogin = async () => {
  try {
    const res = await fetch("http://127.0.0.1:5000/login", {
      method: "POST"
    });

    const data = await res.json();

    console.log(data);  // 👈 DEBUG

    if (data.status === "success") {
      if (data.role === "admin") navigate("/admin");
      else navigate("/user");
    } else {
      alert(data.message || "Face not matched ❌");
    }

  } catch (err) {
    console.error(err);
    alert("Server error ❌");
  }
};

  return (
    <div className="login-container">

      <div className="scanner-box">

        {/* CAMERA */}
        <div className="scanner-circle">

          <video ref={videoRef} autoPlay className="camera"></video>

          <div className="scan-line"></div>

          <div className="face-text">
            FACE SCAN ACTIVE
          </div>

        </div>

        <button className="scan-btn" onClick={handleLogin}>
          Start Scan
        </button>

        <button className="back-btn" onClick={() => navigate("/")}>
          ⬅ Back
        </button>

      </div>

    </div>
  );
}

export default Login;