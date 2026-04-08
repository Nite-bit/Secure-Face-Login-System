import { useNavigate } from "react-router-dom";
import "./home.css";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">

      {/* NAVBAR */}
      <nav className="navbar">
        <h2 className="logo">🔐 Security</h2>

        <ul className="nav-links">
          <li>Home</li>
          <li>About</li>
          <li>Features</li>
          <li>Contact</li>
        </ul>

        <div className="nav-buttons">
          <button onClick={() => navigate("/login")} className="login-btn">
            Login
          </button>

          <button onClick={() => navigate("/register")} className="register-btn">
            Register
          </button>
        </div>
      </nav>

      {/* HERO SECTION */}
      <div className="hero">

        <h1 className="hero-title">
          Secure Face Login System
        </h1>

        <p className="hero-subtitle">
          AI Powered Authentication using Face Recognition
        </p>

      </div>

    </div>
  );
}

export default Home;