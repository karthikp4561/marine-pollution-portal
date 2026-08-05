function Home() {
  return (
    <div className="home-page">
      <div className="hero-section">
        <div className="hero-content">
          <h1>Marine Pollution Reporting Portal</h1>
          <p>
            Monitor marine pollution and water quality using IoT smart buoys.
          </p>
        </div>

        <div className="feature-cards">
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>View Reports</h3>
            <p>See detailed pollution and water quality data.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🛟</div>
            <h3>IoT Buoy Status</h3>
            <p>Check the status of your networked smart buoys.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🔔</div>
            <h3>Report Incidents</h3>
            <p>Submit reports about marine pollution incidents.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;