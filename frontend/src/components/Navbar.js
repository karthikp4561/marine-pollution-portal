import { Link } from "react-router-dom";

function Navbar() {
  const role = localStorage.getItem("role");
  const isLoggedIn = localStorage.getItem("access");

  const logout = () => {
    localStorage.clear();
    window.location.href = "/";
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <div className="container">
        <Link className="navbar-brand" to="/">
          Marine Pollution Portal
        </Link>

        <div>
          <Link className="btn btn-light me-2" to="/">
            Home
          </Link>

          {!isLoggedIn && (
            <>
              <Link className="btn btn-light me-2" to="/login">
                Login
              </Link>

              <Link className="btn btn-light me-2" to="/register">
                Register
              </Link>
            </>
          )}

          {isLoggedIn && role === "user" && (
            <>
              <Link className="btn btn-warning me-2" to="/report">
                Report Pollution
              </Link>

              <Link className="btn btn-light me-2" to="/reports">
                Reports
              </Link>

              <Link className="btn btn-info me-2" to="/map">
                Map
              </Link>
            </>
          )}

          {isLoggedIn && role === "organization" && (
            <>
              <Link className="btn btn-light me-2" to="/reports">
                Reports
              </Link>

              <Link className="btn btn-light me-2" to="/dashboard">
                Sensor Dashboard
              </Link>

              <Link className="btn btn-info me-2" to="/map">
                Map
              </Link>
            </>
          )}

          {isLoggedIn && role === "admin" && (
            <>
              <Link className="btn btn-danger me-2" to="/admin-dashboard">
                Admin Dashboard
              </Link>

              <Link className="btn btn-info me-2" to="/map">
                Map
              </Link>
            </>
          )}

          {isLoggedIn && (
            <button className="btn btn-dark" onClick={logout}>
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;