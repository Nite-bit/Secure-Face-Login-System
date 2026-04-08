import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./register.css";

function Register() {
  const [name, setName] = useState("");
  const [role, setRole] = useState("user");
  const navigate = useNavigate();

  const handleRegister = async () => {
    await fetch("http://127.0.0.1:5000/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, role }),
    });

    alert("Registered Successfully!");
  };

  return (
    <div className="register-container">

      {/* LEFT IMAGE */}
      <div className="left-section">
        <div className="image-box"></div>
      </div>

      {/* RIGHT FORM */}
      <div className="right-section">

        <div className="form-box">

          <h1>Register</h1>

          <input
            type="text"
            placeholder="Enter Name"
            onChange={(e) => setName(e.target.value)}
          />

          <select onChange={(e) => setRole(e.target.value)}>
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>

          <button onClick={handleRegister}>Capture Face</button>

          <p onClick={() => navigate("/")} className="back-link">
            ⬅ Back to Home
          </p>

        </div>

      </div>
    </div>
  );
}

export default Register;