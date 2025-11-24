import React from 'react';
import './Analytics.css';

const Analytics = () => {
  return (
    <div className="analytics-page fade-in">
      <div className="container">
        <h1>Analytics</h1>
        <p>Advanced analytics and insights (Coming Soon)</p>

        <div className="card">
          <h3>Multi-Film Comparison</h3>
          <p className="placeholder-text">Compare EPM scores across multiple films</p>
        </div>

        <div className="card">
          <h3>Genre Benchmarking</h3>
          <p className="placeholder-text">See how your film ranks against genre averages</p>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
