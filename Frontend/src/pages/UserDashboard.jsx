import { useNavigate } from "react-router-dom";

function UserDashboard() {
  const navigate = useNavigate();

  return (
    <div className="container bg-dashboard">
      <div className="card">
        <h1>User Dashboard</h1>

        <button className="btn btn-danger" onClick={() => navigate("/")}>
          Logout
        </button>
      </div>
    </div>
  );
}

export default UserDashboard;