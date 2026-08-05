import { useState } from "react";

import API from "../services/api";

function ReportPollution() {

  const [pollutionType, setPollutionType] = useState("");

  const [description, setDescription] = useState("");

  const [latitude, setLatitude] = useState("");

  const [longitude, setLongitude] = useState("");

  const [image, setImage] = useState(null);

  const handleSubmit = async (e) => {

    e.preventDefault();

    const formData = new FormData();

    formData.append("pollution_type", pollutionType);

    formData.append("description", description);

    formData.append("latitude", latitude);

    formData.append("longitude", longitude);

    if (image) {

      formData.append("image", image);
    }

    try {

      await API.post("reports/", formData, {

        headers: {

          "Content-Type": "multipart/form-data",
        },
      });

      alert("Pollution Report Submitted");

    } catch (error) {

      console.error(error);

      alert("Submission Failed");
    }
  };

  const getLocation = () => {

    navigator.geolocation.getCurrentPosition(

      (position) => {

        setLatitude(position.coords.latitude);

        setLongitude(position.coords.longitude);
      },

      () => {

        alert("Location access denied");
      }
    );
  };

  return (
  <div className="marine-page">
    <div className="marine-form-card">
      <h2>Report Pollution</h2>
      <p className="form-subtitle">
        Submit pollution details with location and image evidence.
      </p>

      <form onSubmit={handleSubmit}>
        <select
          className="marine-input"
          value={pollutionType}
          onChange={(e) => setPollutionType(e.target.value)}
        >
          <option value="">Select Pollution Type</option>
          <option>Oil Spill</option>
          <option>Plastic Waste</option>
          <option>Chemical Waste</option>
        </select>

        <textarea
          className="marine-input marine-textarea"
          placeholder="Describe the pollution incident"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <div className="location-grid">
          <input
            type="text"
            className="marine-input"
            placeholder="Latitude"
            value={latitude}
            onChange={(e) => setLatitude(e.target.value)}
          />

          <input
            type="text"
            className="marine-input"
            placeholder="Longitude"
            value={longitude}
            onChange={(e) => setLongitude(e.target.value)}
          />
        </div>

        <input
          type="file"
          className="marine-input"
          onChange={(e) => setImage(e.target.files[0])}
        />

        <button type="button" className="location-btn" onClick={getLocation}>
          📍 Use Current Location
        </button>

        <button className="submit-btn">
          Submit Report
        </button>
      </form>
    </div>
  </div>
);
}

export default ReportPollution;