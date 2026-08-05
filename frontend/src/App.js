import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Navbar from "./components/Navbar";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import ReportPollution from "./pages/ReportPollution";
import Reports from "./pages/Reports";
import UserDashboard from "./pages/UserDashboard";
import OrganizationDashboard from "./pages/OrganizationDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import PollutionMap from "./pages/PollutionMap";

function App() {

  return (

    <BrowserRouter>

      <Navbar />

      <Routes>

        <Route path="/" element={<Home />} />

        <Route path="/login" element={<Login />} />

        <Route path="/register" element={<Register />} />

        <Route path="/dashboard" element={<Dashboard />} />

        <Route path="/report" element={<ReportPollution />} />

        <Route path="/reports" element={<Reports />} />

        <Route path="/user-dashboard" element={<UserDashboard />} />
        
        <Route path="/organization-dashboard" element={<OrganizationDashboard />} />
        
        <Route path="/admin-dashboard" element={<AdminDashboard />} />

        <Route path="/map" element={<PollutionMap />} />

      </Routes>

    </BrowserRouter>

  );
}

export default App;