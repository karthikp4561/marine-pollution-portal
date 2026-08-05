import { useEffect, useState } from "react";
import API from "../services/api";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

import { Line, Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function Dashboard() {
  const [sensorData, setSensorData] = useState([]);

  const fetchSensorData = async () => {
    try {
      const response = await API.get("sensors/");
      setSensorData(response.data.slice().reverse());
    } catch (error) {
      console.error(error);
      alert("Failed to load sensor data");
    }
  };

  useEffect(() => {
    fetchSensorData();

    const interval = setInterval(() => {
      fetchSensorData();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const labels = sensorData.map((item) =>
    new Date(item.created_at).toLocaleTimeString()
  );

  const phData = {
    labels,
    datasets: [
      {
        label: "pH Level",
        data: sensorData.map((item) => item.ph),
        tension: 0.4,
      },
    ],
  };

  const turbidityData = {
    labels,
    datasets: [
      {
        label: "Turbidity",
        data: sensorData.map((item) => item.turbidity),
      },
    ],
  };

  const salinityData = {
    labels,
    datasets: [
      {
        label: "Salinity",
        data: sensorData.map((item) => item.salinity),
        tension: 0.4,
      },
    ],
  };

  const latest = sensorData[sensorData.length - 1];

  const getTurbidityStatus = (value) => {
    if (value > 70) {
      return {
        title: "High Pollution Alert",
        message: "Water turbidity is very high. Immediate attention is required.",
        className: "alert-danger-box",
        icon: "🚨",
      };
    } else if (value >= 55) {
      return {
        title: "Moderate Turbidity Warning",
        message: "Water quality is slightly affected. Continuous monitoring is recommended.",
        className: "alert-warning-box",
        icon: "⚠️",
      };
    } else {
      return {
        title: "Water Quality Normal",
        message: "Turbidity level is within the safe range.",
        className: "alert-success-box",
        icon: "✅",
      };
    }
  };

  const alertStatus = latest ? getTurbidityStatus(latest.turbidity) : null;

  return (
    <div className="dashboard-page">
      <h1 className="dashboard-title">IoT Sensor Dashboard</h1>

      <p className="dashboard-subtitle">
        Real-time water quality monitoring from smart buoys.
      </p>

      {alertStatus && (
        <div className={`smart-alert ${alertStatus.className}`}>
          <h3>
            {alertStatus.icon} {alertStatus.title}
          </h3>

          <p>{alertStatus.message}</p>

          <strong>Latest Turbidity:</strong> {latest.turbidity}
        </div>
      )}

      {latest && (
        <div className="stats-grid">
          <div className="stat-card">
            <h3>{latest.ph}</h3>
            <p>Latest pH</p>
          </div>

          <div className="stat-card">
            <h3>{latest.turbidity}</h3>
            <p>Turbidity</p>
          </div>

          <div className="stat-card">
            <h3>{latest.salinity}</h3>
            <p>Salinity</p>
          </div>

          <div className="stat-card">
            <h3>{latest.oil_detected ? "Yes" : "No"}</h3>
            <p>Oil Detected</p>
          </div>
        </div>
      )}

      <div className="chart-card">
        <h3>pH Level Trend</h3>
        <Line data={phData} />
      </div>

      <div className="chart-card">
        <h3>Turbidity Readings</h3>
        <Bar data={turbidityData} />
      </div>

      <div className="chart-card">
        <h3>Salinity Trend</h3>
        <Line data={salinityData} />
      </div>
    </div>
  );
}

export default Dashboard;