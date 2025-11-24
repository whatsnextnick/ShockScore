import React from 'react';
import { useParams } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import './Report.css';

const Report = () => {
  const { id } = useParams();

  // Mock report data
  const mockData = {
    filmTitle: 'The Haunting Hour',
    overall: {
      epmScore: 8.2,
      avgShockScore: 45.3,
      peakShockScore: 92.7,
      totalScareEvents: 15,
      avgAudienceSize: 42,
      runtime: '1h 48m'
    },
    timeline: [
      { time: '00:00', shock: 12 }, { time: '05:00', shock: 18 },
      { time: '10:00', shock: 32 }, { time: '15:00', shock: 25 },
      { time: '20:00', shock: 48 }, { time: '25:00', shock: 38 },
      { time: '30:00', shock: 67 }, { time: '35:00', shock: 45 },
      { time: '40:00', shock: 92 }, { time: '45:00', shock: 35 },
      { time: '50:00', shock: 28 }, { time: '55:00', shock: 72 },
      { time: '01:00', shock: 55 }, { time: '01:05', shock: 40 },
      { time: '01:10', shock: 85 }, { time: '01:15', shock: 62 }
    ],
    peakMoments: [
      { timestamp: '40:23', score: 92.7, emotion: 'fear' },
      { timestamp: '01:10:15', score: 85.3, emotion: 'fear' },
      { timestamp: '55:42', score: 72.1, emotion: 'surprise' }
    ],
    scareEvents: [
      { timestamp: '12:30', intensity: 68.5 },
      { timestamp: '25:15', intensity: 72.3 },
      { timestamp: '40:23', intensity: 92.7 }
    ]
  };

  return (
    <div className="report-page fade-in">
      <div className="container">
        {/* Header */}
        <div className="report-header">
          <div>
            <h1>{mockData.filmTitle}</h1>
            <p>Comprehensive Shock Score Analysis Report</p>
          </div>
          <button className="btn btn-secondary">
            📥 Export PDF
          </button>
        </div>

        {/* Overall Metrics */}
        <div className="metrics-grid">
          <div className="metric-card highlight">
            <div className="metric-label">EPM Score</div>
            <div className="metric-value large">{mockData.overall.epmScore}/10</div>
            <div className="metric-subtitle">Exceptional Performance</div>
          </div>

          <div className="metric-card">
            <div className="metric-label">Avg Shock Score</div>
            <div className="metric-value">{mockData.overall.avgShockScore}</div>
          </div>

          <div className="metric-card">
            <div className="metric-label">Peak Shock Score</div>
            <div className="metric-value">{mockData.overall.peakShockScore}</div>
          </div>

          <div className="metric-card">
            <div className="metric-label">Total Scare Events</div>
            <div className="metric-value">{mockData.overall.totalScareEvents}</div>
          </div>

          <div className="metric-card">
            <div className="metric-label">Avg Audience Size</div>
            <div className="metric-value">{mockData.overall.avgAudienceSize}</div>
          </div>

          <div className="metric-card">
            <div className="metric-label">Runtime</div>
            <div className="metric-value">{mockData.overall.runtime}</div>
          </div>
        </div>

        {/* Timeline Chart */}
        <div className="card">
          <h3>Shock Score Timeline</h3>
          <p className="chart-subtitle">Minute-by-minute emotional intensity throughout the film</p>
          <ResponsiveContainer width="100%" height={400}>
            <AreaChart data={mockData.timeline}>
              <defs>
                <linearGradient id="colorShock" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#dc2626" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#dc2626" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="time" stroke="#a3a3a3" />
              <YAxis stroke="#a3a3a3" domain={[0, 100]} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1a1a1a',
                  border: '1px solid #333',
                  borderRadius: '0.5rem'
                }}
              />
              <Area
                type="monotone"
                dataKey="shock"
                stroke="#dc2626"
                fillOpacity={1}
                fill="url(#colorShock)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Peak Moments & Scare Events */}
        <div className="two-column-grid">
          <div className="card">
            <h3>Top 3 Scariest Moments</h3>
            <div className="moments-list">
              {mockData.peakMoments.map((moment, index) => (
                <div key={index} className="moment-item">
                  <div className="moment-rank">#{index + 1}</div>
                  <div className="moment-details">
                    <div className="moment-time">{moment.timestamp}</div>
                    <div className="moment-score">Shock Score: {moment.score}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <h3>Scare Events Detected</h3>
            <div className="scares-list">
              {mockData.scareEvents.map((scare, index) => (
                <div key={index} className="scare-item">
                  <div className="scare-icon">⚡</div>
                  <div className="scare-details">
                    <div className="scare-time">{scare.timestamp}</div>
                    <div className="scare-intensity">
                      Intensity: <span className="highlight">{scare.intensity}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Insights */}
        <div className="card insights-card">
          <h3>Key Insights & Recommendations</h3>
          <ul className="insights-list">
            <li>✓ Strong opening with gradual tension build-up (0-30 minutes)</li>
            <li>✓ Excellent jump scare placement at 40:23 (Peak Shock: 92.7)</li>
            <li>⚠ Consider enhancing tension in the 45-50 minute range</li>
            <li>✓ Sustained high fear response in final act (01:00-01:15)</li>
            <li>💡 Audience engagement above industry average (EPM: 8.2 vs 6.5 avg)</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Report;
