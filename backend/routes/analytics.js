/**
 * Analytics Routes
 *
 * Provides aggregated analytics and insights
 */

const express = require('express');
const router = express.Router();

// GET /api/analytics/dashboard
// Get dashboard overview statistics
router.get('/dashboard', async (req, res, next) => {
  try {
    // Mock data for now - would query database in production
    res.json({
      overview: {
        totalFilmsAnalyzed: 127,
        totalScreenings: 1543,
        totalAudienceMembers: 54231,
        averageEPM: 6.8
      },
      recentAnalyses: [
        {
          id: 1,
          filmTitle: 'The Haunting Hour',
          uploadDate: '2025-11-20',
          epmScore: 8.2,
          status: 'completed'
        },
        {
          id: 2,
          filmTitle: 'Midnight Terror',
          uploadDate: '2025-11-19',
          epmScore: 7.5,
          status: 'completed'
        }
      ],
      topPerformers: [
        { filmTitle: 'Scream Factory', epmScore: 9.1, peakShock: 95.3 },
        { filmTitle: 'Dark Corners', epmScore: 8.9, peakShock: 92.7 },
        { filmTitle: 'The Ritual', epmScore: 8.5, peakShock: 89.4 }
      ]
    });
  } catch (err) {
    next(err);
  }
});

// GET /api/analytics/compare
// Compare multiple films
router.get('/compare', async (req, res, next) => {
  try {
    const { filmIds } = req.query;

    // Mock comparison data
    res.json({
      comparison: {
        films: [
          {
            id: 1,
            title: 'Film A',
            epmScore: 8.2,
            avgShockScore: 42.5,
            totalScareEvents: 12
          },
          {
            id: 2,
            title: 'Film B',
            epmScore: 7.1,
            avgShockScore: 35.2,
            totalScareEvents: 8
          }
        ]
      }
    });
  } catch (err) {
    next(err);
  }
});

module.exports = router;
