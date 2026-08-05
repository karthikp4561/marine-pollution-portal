import { useState } from "react";
import API from "../services/api";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await API.post("login/", {
        username,
        password,
      });

      localStorage.setItem("access", response.data.access);
      localStorage.setItem("refresh", response.data.refresh);
      localStorage.setItem("username", response.data.username);
      localStorage.setItem("role", response.data.role);

      alert("Login Successful");

      if (response.data.role === "admin") {
        window.location.href = "/admin-dashboard";
      } else if (response.data.role === "organization") {
        window.location.href = "/organization-dashboard";
      } else {
        window.location.href = "/user-dashboard";
      }
    } catch (error) {
      console.error(error.response?.data || error);
      alert("Login Failed");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Welcome Back</h2>
        <p>Login to access your marine monitoring dashboard.</p>

        <form onSubmit={handleLogin}>
          <input
            type="text"
            className="auth-input"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            type="password"
            className="auth-input"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button className="auth-button">Login</button>
        </form>
      </div>
    </div>
  );
}

export default Login;