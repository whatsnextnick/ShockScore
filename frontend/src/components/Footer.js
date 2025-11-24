import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h4>Shock Score</h4>
            <p>Real-time cinema audience emotion analytics</p>
          </div>

          <div className="footer-section">
            <h5>Privacy Guarantee</h5>
            <p className="privacy-badge">
              ✓ GDPR Compliant | ✓ Zero PII Stored | ✓ Aggregate Data Only
            </p>
          </div>

          <div className="footer-section">
            <p className="copyright">
              &copy; 2025 Shock Score. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
