/**
 * Netlify Function: Analyze Frame
 *
 * Serverless function to analyze webcam frames and return emotion data
 * This is a simplified version that returns mock data for demo purposes
 */

const multipart = require('parse-multipart-data');

exports.handler = async (event, context) => {
  // Handle CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
      },
      body: ''
    };
  }

  // Only accept POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

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

    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        faceDetected: true,
        emotions: normalized,
        dominantEmotion,
        shockScore,
        _mode: 'mock',
        _platform: 'netlify'
      })
    };

  } catch (err) {
    console.error('Analysis error:', err);
    return {
      statusCode: 500,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        faceDetected: false,
        error: err.message
      })
    };
  }
};

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
