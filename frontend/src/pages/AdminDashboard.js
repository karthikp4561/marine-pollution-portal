import { useEffect, useState } from "react";
import API from "../services/api";

function AdminDashboard() {
  const [reports, setReports] = useState([]);
  const [users, setUsers] = useState([]);

  const fetchReports = async () => {
    try {
      const response = await API.get("reports/");
      setReports(response.data);
    } catch (error) {
      console.error(error);
      alert("Failed to load reports");
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await API.get("users/manage/");
      setUsers(response.data);
    } catch (error) {
      console.error(error);
      alert("Failed to load users");
    }
  };

  useEffect(() => {
    fetchReports();
    fetchUsers();
  }, []);

  const approveReport = async (id) => {
    try {
      await API.patch(`reports/${id}/approve/`);
      alert("Report approved");
      fetchReports();
    } catch (error) {
      console.error(error);
      alert("Approval failed");
    }
  };

  const rejectReport = async (id) => {
    try {
      await API.patch(`reports/${id}/reject/`);
      alert("Report rejected");
      fetchReports();
    } catch (error) {
      console.error(error);
      alert("Rejection failed");
    }
  };

  const deleteUser = async (id, role) => {
    if (role === "admin") {
      alert("Admin users cannot be deleted from here");
      return;
    }

    const confirmDelete = window.confirm(
      "Are you sure you want to delete this user?"
    );

    if (!confirmDelete) {
      return;
    }

    try {
      await API.delete(`users/manage/${id}/`);
      alert("User deleted");
      fetchUsers();
    } catch (error) {
      console.error(error);
      alert("User deletion failed");
    }
  };

  return (
    <div className="dashboard-page">
      <h1 className="dashboard-title">Admin Dashboard</h1>

      <p className="dashboard-subtitle">
        Review, approve and manage pollution reports.
      </p>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>{reports.length}</h3>
          <p>Total Reports</p>
        </div>

        <div className="stat-card">
          <h3>{reports.filter((report) => report.status === "approved").length}</h3>
          <p>Approved Reports</p>
        </div>

        <div className="stat-card">
          <h3>{reports.filter((report) => report.status === "pending").length}</h3>
          <p>Pending Reports</p>
        </div>

        <div className="stat-card">
          <h3>{users.length}</h3>
          <p>Registered Users</p>
        </div>
      </div>

      <h2 className="section-heading">Report Management</h2>

      {reports.map((report) => (
        <div className="glass-card mb-4" key={report.id}>
          <h4>{report.pollution_type}</h4>

          <p>{report.description}</p>

          <p>
            <strong>Location:</strong> {report.latitude}, {report.longitude}
          </p>

          <p>
            <strong>Status:</strong>{" "}
            <span
              className={
                report.status === "approved"
                  ? "text-success"
                  : report.status === "rejected"
                  ? "text-danger"
                  : "text-warning"
              }
            >
              {report.status}
            </span>
          </p>

          {report.image && (
            <img
              src={
                report.image.startsWith("http")
                  ? report.image
                  : `http://127.0.0.1:8000${report.image}`
              }
              alt="Pollution"
              style={{
                width: "300px",
                height: "200px",
                objectFit: "cover",
                borderRadius: "10px",
                marginBottom: "15px",
              }}
            />
          )}

          <div>
            <button
              className="btn btn-success me-2"
              onClick={() => approveReport(report.id)}
              disabled={report.status === "approved"}
            >
              Approve
            </button>

            <button
              className="btn btn-danger"
              onClick={() => rejectReport(report.id)}
              disabled={report.status === "rejected"}
            >
              Reject
            </button>
          </div>
        </div>
      ))}

      <hr className="my-5 text-light" />

      <h2 className="section-heading">User Management</h2>

      {users.map((user) => (
        <div className="glass-card mb-4" key={user.id}>
          <h5>{user.username}</h5>

          <p>
            <strong>Email:</strong> {user.email}
          </p>

          <p>
            <strong>Role:</strong> {user.role}
          </p>

          {user.role !== "admin" && (
            <button
              className="btn btn-danger"
              onClick={() => deleteUser(user.id, user.role)}
            >
              Delete User
            </button>
          )}
        </div>
      ))}
    </div>
  );
}

export default AdminDashboard;