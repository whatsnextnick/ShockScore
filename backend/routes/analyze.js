/**
 * Real-Time Analysis Routes
 *
 * Handles real-time webcam frame analysis for live Shock Score
 */

const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs').promises;
const { PythonShell } = require('python-shell');

// Configure multer for frame uploads (memory storage for speed)
const storage = multer.memoryStorage();
const upload = multer({
  storage,
  limits: {
    fileSize: 5 * 1024 * 1024 // 5MB
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png/;
    const mimetype = allowedTypes.test(file.mimetype);
    if (mimetype) {
      return cb(null, true);
    }
    cb(new Error('Only image files are allowed'));
  }
});

// POST /api/analyze/frame
// Analyze a single webcam frame for emotions
router.post('/frame', upload.single('frame'), async (req, res, next) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No frame provided' });
    }

    // Save frame temporarily
    const tempDir = path.join(__dirname, '../temp');
    await fs.mkdir(tempDir, { recursive: true });

    const tempPath = path.join(tempDir, `frame-${Date.now()}.jpg`);
    await fs.writeFile(tempPath, req.file.buffer);

    // Run Python analysis
    const pythonPath = process.env.PYTHON_PATH || path.join(__dirname, '../../venv/bin/python');
    const scriptPath = path.join(__dirname, '../scripts/analyze_frame.py');

    try {
      const options = {
        mode: 'json',
        pythonPath,
        args: [tempPath]
      };

      const results = await PythonShell.run(scriptPath, options);
      const analysis = results[0];

      // Clean up temp file
      await fs.unlink(tempPath).catch(() => {});

      if (analysis && analysis.faceDetected) {
        // Calculate Shock Score from emotions
        const emotions = analysis.emotions;
        const shockScore = calculateShockScore(emotions);

        res.json({
          faceDetected: true,
          emotions,
          dominantEmotion: analysis.dominantEmotion,
          shockScore
        });
      } else {
        res.json({
          faceDetected: false,
          message: 'No face detected in frame'
        });
      }
    } catch (pythonError) {
      console.error('Python analysis error:', pythonError);

      // Cleanup
      await fs.unlink(tempPath).catch(() => {});

      // Return mock data if Python fails (for development/demo)
      res.json({
        faceDetected: true,
        emotions: {
          angry: Math.random() * 10,
          disgust: Math.random() * 5,
          fear: Math.random() * 30,
          happy: Math.random() * 20,
          sad: Math.random() * 15,
          surprise: Math.random() * 20,
          neutral: Math.random() * 40
        },
        dominantEmotion: 'neutral',
        shockScore: Math.random() * 50,
        _note: 'Using mock data - Python engine unavailable'
      });
    }
  } catch (err) {
    next(err);
  }
});

// Calculate Shock Score from emotion probabilities
function calculateShockScore(emotions) {
  // Weights from config (matching Python implementation)
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

  // Normalize to 0-100 scale
  const maxPossible = 100 * (FEAR_WEIGHT + SURPRISE_WEIGHT);
  const normalized = Math.min(100, (score / maxPossible) * 100);

  return Math.round(normalized * 10) / 10; // Round to 1 decimal
}

module.exports = router;
