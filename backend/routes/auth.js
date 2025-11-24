/**
 * Authentication Routes (Placeholder)
 *
 * For now, simplified auth. In production, implement full JWT authentication.
 */

const express = require('express');
const router = express.Router();

// POST /api/auth/login
router.post('/login', async (req, res) => {
  const { email, password } = req.body;

  // Mock authentication - replace with real auth in production
  if (email && password) {
    res.json({
      success: true,
      token: 'mock-jwt-token-' + Date.now(),
      user: {
        id: 1,
        email,
        name: 'Demo Studio',
        role: 'studio'
      }
    });
  } else {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});

// POST /api/auth/register
router.post('/register', async (req, res) => {
  const { email, password, studioName } = req.body;

  res.json({
    success: true,
    message: 'Registration successful',
    user: {
      id: Date.now(),
      email,
      studioName
    }
  });
});

module.exports = router;
