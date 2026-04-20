import { useNavigate } from "react-router-dom";
import { useRef, useState } from "react";
import "./login.css";

function Login() {
  const navigate = useNavigate();
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const [cameraOn, setCameraOn] = useState(false);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  // 🎥 START CAMERA
  const startScan = async () => {
    try {
      // prevent multiple starts
      if (streamRef.current) return;

      const stream = await navigator.mediaDevices.getUserMedia({ video: true });

      streamRef.current = stream;
      setCameraOn(true);
      setStatus("scanning");
      setLoading(true);

      // wait for DOM render
      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      }, 200);

      startScanning();

    } catch (err) {
      console.error(err);
      alert("Camera permission denied ❌");
    }
  };

  // 🔍 SCANNING LOOP
  const startScanning = () => {
    let attempts = 0;
    let failCount = 0;
    let isProcessing = false;

    const scanInterval = setInterval(async () => {

      if (isProcessing) return;
      isProcessing = true;

      try {
        attempts++;

        const video = videoRef.current;

        if (!video || !video.videoWidth) {
          isProcessing = false;
          return;
        }

        // 📸 CAPTURE FRAME
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0);

        const image = canvas.toDataURL("image/jpeg");

        // 📡 SEND TO BACKEND
        const res = await fetch("http://127.0.0.1:5000/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ image })
        });

        const data = await res.json();
        console.log("Response:", data);

        // ✅ SUCCESS
        if (data.status === "success") {
          clearInterval(scanInterval);
          stopCamera();

          setStatus("granted");

          setTimeout(() => {
            if (data.role === "admin") navigate("/admin");
            else navigate("/user");
          }, 1000);
        }

        // ⚠ NO FACE
        else if (data.status === "no_face") {
          setStatus("no_face");

          clearInterval(scanInterval);
          stopCamera();
        }

        // ❌ FAIL
        else {
          failCount++;
          setStatus("denied");

          if (failCount >= 3) {
            clearInterval(scanInterval);
            stopCamera();
          }
        }

        // ⏱ TIMEOUT
        if (attempts >= 10) {
          clearInterval(scanInterval);
          stopCamera();
          setStatus("timeout");
        }

      } catch (err) {
        console.error(err);
      } finally {
        isProcessing = false;
      }

    }, 2000); // 🔥 delay to avoid overload
  };

  // ❌ STOP CAMERA
  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }

    setCameraOn(false);
    setLoading(false);
  };

  return (
    <div className="login-container">

      <div className="scanner-box">

        {/* CAMERA CIRCLE */}
        <div className={`scanner-circle ${loading ? "active" : ""}`}>
          {cameraOn && (
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="camera"
            />
          )}
        </div>

        {/* START BUTTON */}
        <div className="center-btn">
          {!cameraOn && (
            <button className="scan-btn" onClick={startScan}>
              Start Scan
            </button>
          )}
        </div>

        {/* NAVIGATION */}
        <div className="nav-row">
          <button className="nav-btn" onClick={() => navigate("/")}>
            ⬅ Back
          </button>

          <button className="nav-btn" onClick={() => navigate("/register")}>
            Register ➡
          </button>
        </div>

        {/* STATUS */}
        {status === "scanning" && <h3 className="info">Scanning...</h3>}
        {status === "granted" && <h2 className="granted">✔ ACCESS GRANTED</h2>}
        {status === "denied" && <h2 className="denied">❌ ACCESS DENIED</h2>}
        {status === "no_face" && <h2 className="warning">⚠ No Face Detected</h2>}
        {status === "timeout" && <h2 className="denied">⏱ Timeout</h2>}

      </div>

    </div>
  );
}

export default Login;