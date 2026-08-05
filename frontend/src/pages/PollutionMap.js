import { useEffect, useState } from "react";
import { GoogleMap, Marker, InfoWindow, useLoadScript } from "@react-google-maps/api";
import API from "../services/api";

function PollutionMap() {
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);

  const { isLoaded } = useLoadScript({
    googleMapsApiKey: "AIzaSyAAnN31Q44nBrk_yKeOSNjDjf2-m293NwM",
  });

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const response = await API.get("reports/approved/");
      setReports(response.data);
    } catch (error) {
      console.error(error);
      alert("Failed to load map reports");
    }
  };

  if (!isLoaded) {
    return <div className="container mt-5">Loading map...</div>;
  }

  return (
    <div className="container mt-5">
      <h2>Pollution Location Map</h2>

      <GoogleMap
        zoom={7}
        center={{ lat: 9.9312, lng: 76.2673 }}
        mapContainerStyle={{
          width: "100%",
          height: "500px",
          borderRadius: "10px",
        }}
      >
        {reports.map((report) => (
          <Marker
            key={report.id}
            position={{
              lat: parseFloat(report.latitude),
              lng: parseFloat(report.longitude),
            }}
            onClick={() => setSelectedReport(report)}
          />
        ))}

        {selectedReport && (
          <InfoWindow
            position={{
              lat: parseFloat(selectedReport.latitude),
              lng: parseFloat(selectedReport.longitude),
            }}
            onCloseClick={() => setSelectedReport(null)}
          >
            <div>
              <h6>{selectedReport.pollution_type}</h6>
              <p>{selectedReport.description}</p>

              {selectedReport.image && (
                <img
                  src={
                    selectedReport.image.startsWith("http")
                      ? selectedReport.image
                      : `http://127.0.0.1:8000${selectedReport.image}`
                  }
                  alt="Pollution"
                  style={{
                    width: "150px",
                    height: "100px",
                    objectFit: "cover",
                  }}
                />
              )}
            </div>
          </InfoWindow>
        )}
      </GoogleMap>
    </div>
  );
}

export default PollutionMap;