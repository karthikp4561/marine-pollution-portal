import { useState } from "react";
import API from "../services/api";

function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user");

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      await API.post("users/register/", {
        username,
        email,
        password,
        role,
      });

      alert("Registration Successful");
      window.location.href = "/login";
    } catch (error) {
      console.error(error.response?.data || error);
      alert("Registration Failed");
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Create Account</h2>
        <p>Register as a user or organization to access the portal.</p>

        <form onSubmit={handleRegister}>
          <input
            type="text"
            className="auth-input"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            type="email"
            className="auth-input"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            className="auth-input"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <select
            className="auth-input"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="user">User</option>
            <option value="organization">Organization</option>
          </select>

          <button className="auth-button">Register</button>
        </form>
      </div>
    </div>
  );
}

export default Register;