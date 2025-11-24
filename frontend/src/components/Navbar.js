import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();

  const isActive = (path) => location.pathname === path ? 'active' : '';

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-content">
          <Link to="/" className="navbar-brand">
            <span className="brand-icon">🎬</span>
            <span className="brand-text">SHOCK SCORE</span>
          </Link>

          <div className="navbar-links">
            <Link to="/" className={`nav-link ${isActive('/')}`}>
              Dashboard
            </Link>
            <Link to="/upload" className={`nav-link ${isActive('/upload')}`}>
              Upload
            </Link>
            <Link to="/analytics" className={`nav-link ${isActive('/analytics')}`}>
              Analytics
            </Link>
          </div>

          <div className="navbar-actions">
            <button className="btn btn-secondary btn-sm">
              Demo Studio
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
