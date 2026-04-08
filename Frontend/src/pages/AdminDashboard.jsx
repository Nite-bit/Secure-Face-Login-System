import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function AdminDashboard() {
  const [logs, setLogs] = useState([]);
  const [filteredLogs, setFilteredLogs] = useState([]);
  const [search, setSearch] = useState("");
  const [date, setDate] = useState("");
  const [statusStats, setStatusStats] = useState({});
  const [roleStats, setRoleStats] = useState({});
  const navigate = useNavigate();

  // Load logs
  useEffect(() => {
    fetch("http://127.0.0.1:5000/admin/logs")
      .then(res => res.json())
      .then(data => {
        setLogs(data);
        setFilteredLogs(data);
        calculateStats(data);
      });
  }, []);

  // Calculate stats
  const calculateStats = (data) => {
    const statusCount = {};
    const roleCount = {};

    data.forEach(item => {
      statusCount[item.Status] = (statusCount[item.Status] || 0) + 1;
      roleCount[item.Role] = (roleCount[item.Role] || 0) + 1;
    });

    setStatusStats(statusCount);
    setRoleStats(roleCount);
  };

  // Search filter
  const handleSearch = () => {
    const result = logs.filter(log =>
      log.Name.toLowerCase().includes(search.toLowerCase())
    );
    setFilteredLogs(result);
  };

  // Date filter
  const handleDateFilter = () => {
    const result = logs.filter(log => log.Date === date);
    setFilteredLogs(result);
  };

  return (
    <div className="bg-dashboard" style={{ padding: "20px" }}>

      <h1 style={{ fontSize: "28px", marginBottom: "20px" }}>
        📊 Admin Dashboard
      </h1>

      {/* Logout */}
      <button
        className="btn btn-danger"
        onClick={() => navigate("/")}
      >
        Logout
      </button>

      <hr />

      {/* Search */}
      <h3>🔍 Search User</h3>
      <input
        className="input"
        placeholder="Enter name"
        onChange={(e) => setSearch(e.target.value)}
      />
      <button className="btn btn-primary" onClick={handleSearch}>
        Search
      </button>

      {/* Date Filter */}
      <h3>📅 Filter by Date</h3>
      <input
        className="input"
        placeholder="YYYY-MM-DD"
        onChange={(e) => setDate(e.target.value)}
      />
      <button className="btn btn-primary" onClick={handleDateFilter}>
        Filter
      </button>

      <hr />

      {/* Stats */}
      <h3>📊 Login Statistics</h3>
      <div>
        {Object.entries(statusStats).map(([key, val]) => (
          <p key={key}>{key}: {val}</p>
        ))}
      </div>

      <h3>👥 Role Distribution</h3>
      <div>
        {Object.entries(roleStats).map(([key, val]) => (
          <p key={key}>{key}: {val}</p>
        ))}
      </div>

      <hr />

      {/* Table */}
      <h3>📋 Login History</h3>

      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Role</th>
            <th>Date</th>
            <th>Time</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {filteredLogs.map((log, index) => (
            <tr key={index}>
              <td>{log.Name}</td>
              <td>{log.Role}</td>
              <td>{log.Date}</td>
              <td>{log.Time}</td>
              <td>{log.Status}</td>
            </tr>
          ))}
        </tbody>
      </table>

    </div>
  );
}

export default AdminDashboard;