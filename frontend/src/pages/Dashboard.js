import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import WebcamShockScore from '../components/WebcamShockScoreSimple';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalFilms: 127,
    avgEPM: 6.8,
    totalAudience: 54231,
    totalScreenings: 1543
  });

  const [recentFilms, setRecentFilms] = useState([
    { id: 1, title: 'The Haunting Hour', epm: 8.2, date: '2025-11-20', status: 'completed' },
    { id: 2, title: 'Midnight Terror', epm: 7.5, date: '2025-11-19', status: 'completed' },
    { id: 3, title: 'Dark Corridors', epm: 6.9, date: '2025-11-18', status: 'completed' }
  ]);

  // Mock EPM trend data
  const epmTrendData = [
    { month: 'Jun', avgEPM: 6.2 },
    { month: 'Jul', avgEPM: 6.5 },
    { month: 'Aug', avgEPM: 6.8 },
    { month: 'Sep', avgEPM: 7.1 },
    { month: 'Oct', avgEPM: 7.4 },
    { month: 'Nov', avgEPM: 6.8 }
  ];

  return (
    <div className="dashboard fade-in">
      <div className="container">
        {/* Header */}
        <div className="dashboard-header">
          <div>
            <h1>Dashboard</h1>
            <p>Real-time cinema emotion analytics overview</p>
          </div>
          <Link to="/upload" className="btn btn-primary">
            + Upload New Film
          </Link>
        </div>

        {/* Live Webcam Shock Score Demo */}
        <WebcamShockScore />

        {/* Stats Grid */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">🎬</div>
            <div className="stat-content">
              <div className="stat-value">{stats.totalFilms}</div>
              <div className="stat-label">Films Analyzed</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-content">
              <div className="stat-value">{stats.avgEPM}/10</div>
              <div className="stat-label">Average EPM Score</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">👥</div>
            <div className="stat-content">
              <div className="stat-value">{stats.totalAudience.toLocaleString()}</div>
              <div className="stat-label">Total Audience</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🎥</div>
            <div className="stat-content">
              <div className="stat-value">{stats.totalScreenings}</div>
              <div className="stat-label">Screenings</div>
            </div>
          </div>
        </div>

        {/* Charts */}
        <div className="charts-grid">
          <div className="card chart-card">
            <h3>EPM Trend (Last 6 Months)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={epmTrendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="month" stroke="#a3a3a3" />
                <YAxis stroke="#a3a3a3" domain={[0, 10]} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1a1a1a',
                    border: '1px solid #333',
                    borderRadius: '0.5rem'
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="avgEPM"
                  stroke="#dc2626"
                  strokeWidth={3}
                  name="Average EPM"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="card chart-card">
            <h3>Top Performing Films</h3>
            <div className="top-films-list">
              {[
                { title: 'Scream Factory', epm: 9.1, shock: 95.3 },
                { title: 'Dark Corners', epm: 8.9, shock: 92.7 },
                { title: 'The Ritual', epm: 8.5, shock: 89.4 }
              ].map((film, index) => (
                <div key={index} className="top-film-item">
                  <div className="film-rank">#{index + 1}</div>
                  <div className="film-details">
                    <div className="film-title">{film.title}</div>
                    <div className="film-stats">
                      EPM: <span className="highlight">{film.epm}</span> |
                      Peak Shock: <span className="highlight">{film.shock}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recent Analyses */}
        <div className="card">
          <h3>Recent Analyses</h3>
          <div className="table-container">
            <table className="films-table">
              <thead>
                <tr>
                  <th>Film Title</th>
                  <th>EPM Score</th>
                  <th>Upload Date</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {recentFilms.map(film => (
                  <tr key={film.id}>
                    <td className="film-title-cell">{film.title}</td>
                    <td>
                      <span className={`epm-badge ${film.epm >= 7 ? 'high' : ''}`}>
                        {film.epm}/10
                      </span>
                    </td>
                    <td>{film.date}</td>
                    <td>
                      <span className="status-badge completed">
                        {film.status}
                      </span>
                    </td>
                    <td>
                      <Link to={`/report/${film.id}`} className="btn btn-secondary btn-sm">
                        View Report
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
