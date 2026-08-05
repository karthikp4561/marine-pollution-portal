import { useEffect, useState } from "react";
import API from "../services/api";

function Reports() {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const response = await API.get("reports/approved/");
      setReports(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="marine-page">
      <div className="reports-panel">
        <h2>Pollution Reports</h2>
        <p className="form-subtitle">
          View approved marine pollution reports submitted by users.
        </p>

        {reports.map((report) => (
          <div className="report-glass-card" key={report.id}>
            <h4>{report.pollution_type}</h4>

            <p>{report.description}</p>

            <p>
              <strong>Latitude:</strong> {report.latitude}
            </p>

            <p>
              <strong>Longitude:</strong> {report.longitude}
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
          </div>
        ))}
      </div>
    </div>
  );
}

export default Reports;