/**
 * Video Processing Routes
 *
 * Handles video upload, processing, and status checking
 */

const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs').promises;
const pythonBridge = require('../services/pythonBridge');

// Configure multer for video uploads
const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    const uploadDir = path.join(__dirname, '../uploads');
    await fs.mkdir(uploadDir, { recursive: true });
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, `video-${uniqueSuffix}${path.extname(file.originalname)}`);
  }
});

const upload = multer({
  storage,
  limits: {
    fileSize: 500 * 1024 * 1024 // 500MB
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = /mp4|avi|mov|mkv|webm/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);

    if (extname && mimetype) {
      return cb(null, true);
    }
    cb(new Error('Only video files are allowed (mp4, avi, mov, mkv, webm)'));
  }
});

// POST /api/videos/upload
// Upload a new video for processing
router.post('/upload', upload.single('video'), async (req, res, next) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No video file uploaded' });
    }

    const { filmTitle, genre, studoName } = req.body;

    res.json({
      message: 'Video uploaded successfully',
      video: {
        id: req.file.filename,
        originalName: req.file.originalname,
        size: req.file.size,
        path: req.file.path,
        uploadedAt: new Date().toISOString()
      },
      metadata: {
        filmTitle: filmTitle || 'Untitled',
        genre: genre || 'Horror',
        studioName: studoName || 'Unknown'
      }
    });
  } catch (err) {
    next(err);
  }
});

// POST /api/videos/:id/process
// Start processing a video
router.post('/:id/process', async (req, res, next) => {
  try {
    const videoId = req.params.id;
    const videoPath = path.join(__dirname, '../uploads', videoId);
    const outputPath = path.join(__dirname, '../uploads', `${videoId}-report.json`);

    // Check if video exists
    try {
      await fs.access(videoPath);
    } catch (err) {
      return res.status(404).json({ error: 'Video not found' });
    }

    // Get Socket.IO instance
    const io = req.app.get('io');

    // Start processing in background
    setImmediate(async () => {
      try {
        await pythonBridge.processVideo(
          videoPath,
          outputPath,
          (progress) => {
            // Emit real-time progress to connected clients
            io.to(`session-${videoId}`).emit('processing-progress', {
              videoId,
              ...progress
            });
          }
        );

        // Emit completion event
        io.to(`session-${videoId}`).emit('processing-complete', {
          videoId,
          outputPath
        });
      } catch (err) {
        io.to(`session-${videoId}`).emit('processing-error', {
          videoId,
          error: err.message
        });
      }
    });

    res.json({
      message: 'Processing started',
      videoId,
      status: 'processing'
    });
  } catch (err) {
    next(err);
  }
});

// GET /api/videos/:id/status
// Get processing status
router.get('/:id/status', async (req, res, next) => {
  try {
    const videoId = req.params.id;
    const reportPath = path.join(__dirname, '../uploads', `${videoId}-report.json`);

    try {
      await fs.access(reportPath);
      res.json({
        videoId,
        status: 'completed',
        reportAvailable: true
      });
    } catch (err) {
      res.json({
        videoId,
        status: 'processing',
        reportAvailable: false
      });
    }
  } catch (err) {
    next(err);
  }
});

// GET /api/videos/:id/report
// Get the Shock Score report for a processed video
router.get('/:id/report', async (req, res, next) => {
  try {
    const videoId = req.params.id;
    const reportPath = path.join(__dirname, '../uploads', `${videoId}-report.json`);

    const reportData = await fs.readFile(reportPath, 'utf8');
    const report = JSON.parse(reportData);

    res.json({
      videoId,
      report
    });
  } catch (err) {
    if (err.code === 'ENOENT') {
      return res.status(404).json({ error: 'Report not found. Video may still be processing.' });
    }
    next(err);
  }
});

// DELETE /api/videos/:id
// Delete a video and its report
router.delete('/:id', async (req, res, next) => {
  try {
    const videoId = req.params.id;
    const videoPath = path.join(__dirname, '../uploads', videoId);
    const reportPath = path.join(__dirname, '../uploads', `${videoId}-report.json`);

    await fs.unlink(videoPath).catch(() => {});
    await fs.unlink(reportPath).catch(() => {});

    res.json({
      message: 'Video and report deleted successfully',
      videoId
    });
  } catch (err) {
    next(err);
  }
});

module.exports = router;
