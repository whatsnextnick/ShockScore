/**
 * Simplified Real-Time Analysis Routes (For Testing)
 *
 * Returns mock emotion data to verify the UI is working
 * Before connecting the full Python engine
 */

const express = require('express');
const router = express.Router();
const multer = require('multer');

const upload = multer({ storage: multer.memoryStorage() });

// POST /api/analyze/frame
router.post('/frame', upload.single('frame'), async (req, res) => {
  try {
    console.log('📸 Frame received for analysis');

    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 300));

    // Generate realistic mock emotion data
    const mockEmotions = {
      angry: Math.random() * 15,
      disgust: Math.random() * 10,
      fear: 20 + Math.random() * 40,        // Higher for demo
      happy: Math.random() * 25,
      sad: Math.random() * 15,
      surprise: 10 + Math.random() * 30,    // Higher for demo
      neutral: 10 + Math.random() * 30
    };

    // Normalize to 100%
    const total = Object.values(mockEmotions).reduce((a, b) => a + b, 0);
    const normalized = {};
    for (const [emotion, value] of Object.entries(mockEmotions)) {
      normalized[emotion] = (value / total) * 100;
    }

    // Find dominant emotion
    const dominantEmotion = Object.entries(normalized)
      .reduce((a, b) => a[1] > b[1] ? a : b)[0];

    // Calculate shock score
    const shockScore = calculateShockScore(normalized);

    console.log(`✓ Analysis complete - Shock Score: ${shockScore.toFixed(1)}`);

    res.json({
      faceDetected: true,
      emotions: normalized,
      dominantEmotion,
      shockScore,
      _mode: 'mock'  // Indicates this is mock data
    });

  } catch (err) {
    console.error('Analysis error:', err);
    res.status(500).json({
      faceDetected: false,
      error: err.message
    });
  }
});

function calculateShockScore(emotions) {
  const FEAR_WEIGHT = 2.0;
  const SURPRISE_WEIGHT = 1.5;
  const DISGUST_WEIGHT = 0.8;
  const HAPPY_WEIGHT = 0.3;
  const ANGRY_WEIGHT = 0.2;
  const SAD_WEIGHT = 0.1;

  const score = (
    (emotions.fear || 0) * FEAR_WEIGHT +
    (emotions.surprise || 0) * SURPRISE_WEIGHT +
    (emotions.disgust || 0) * DISGUST_WEIGHT +
    (emotions.happy || 0) * HAPPY_WEIGHT +
    (emotions.angry || 0) * ANGRY_WEIGHT +
    (emotions.sad || 0) * SAD_WEIGHT
  );

  const maxPossible = 100 * (FEAR_WEIGHT + SURPRISE_WEIGHT);
  const normalized = Math.min(100, (score / maxPossible) * 100);

  return Math.round(normalized * 10) / 10;
}

module.exports = router;
