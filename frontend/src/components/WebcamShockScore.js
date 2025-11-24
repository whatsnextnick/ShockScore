import React, { useState, useRef, useEffect } from 'react';
import './WebcamShockScore.css';

const WebcamShockScore = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isActive, setIsActive] = useState(false);
  const [currentShockScore, setCurrentShockScore] = useState(0);
  const [dominantEmotion, setDominantEmotion] = useState('neutral');
  const [emotionScores, setEmotionScores] = useState({
    angry: 0,
    disgust: 0,
    fear: 0,
    happy: 0,
    sad: 0,
    surprise: 0,
    neutral: 0
  });
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [faceDetected, setFaceDetected] = useState(false);
  const intervalRef = useRef(null);

  // Start webcam
  const startWebcam = async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 }
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setIsActive(true);

        // Start capturing frames for analysis
        startFrameCapture();
      }
    } catch (err) {
      console.error('Webcam error:', err);
      setError('Cannot access webcam. Please ensure camera permissions are granted.');
    }
  };

  // Stop webcam
  const stopWebcam = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    setIsActive(false);
    stopFrameCapture();
    resetScores();
  };

  // Start capturing and analyzing frames
  const startFrameCapture = () => {
    intervalRef.current = setInterval(() => {
      captureAndAnalyze();
    }, 1000); // Analyze every 1 second
  };

  // Stop frame capture
  const stopFrameCapture = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  // Capture frame and send for analysis
  const captureAndAnalyze = async () => {
    if (!videoRef.current || !canvasRef.current || isProcessing) return;

    const canvas = canvasRef.current;
    const video = videoRef.current;
    const context = canvas.getContext('2d');

    // Set canvas size to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw current video frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to blob
    canvas.toBlob(async (blob) => {
      if (!blob) return;

      setIsProcessing(true);

      try {
        // Send frame to backend for emotion analysis
        const formData = new FormData();
        formData.append('frame', blob, 'frame.jpg');

        const response = await fetch('/api/analyze/frame', {
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          const data = await response.json();

          if (data.faceDetected) {
            setFaceDetected(true);
            setEmotionScores(data.emotions);
            setDominantEmotion(data.dominantEmotion);
            setCurrentShockScore(data.shockScore);
          } else {
            setFaceDetected(false);
          }
        }
      } catch (err) {
        console.error('Analysis error:', err);
      } finally {
        setIsProcessing(false);
      }
    }, 'image/jpeg', 0.8);
  };

  // Reset scores
  const resetScores = () => {
    setCurrentShockScore(0);
    setDominantEmotion('neutral');
    setEmotionScores({
      angry: 0,
      disgust: 0,
      fear: 0,
      happy: 0,
      sad: 0,
      surprise: 0,
      neutral: 0
    });
    setFaceDetected(false);
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopWebcam();
    };
  }, []);

  // Get shock score color
  const getShockScoreColor = (score) => {
    if (score < 20) return '#10b981'; // Green
    if (score < 40) return '#f59e0b'; // Orange
    if (score < 60) return '#f97316'; // Deep orange
    if (score < 80) return '#ef4444'; // Red
    return '#dc2626'; // Dark red
  };

  // Get emotion emoji
  const getEmotionEmoji = (emotion) => {
    const emojis = {
      angry: '😠',
      disgust: '🤢',
      fear: '😨',
      happy: '😊',
      sad: '😢',
      surprise: '😲',
      neutral: '😐'
    };
    return emojis[emotion] || '😐';
  };

  return (
    <div className="webcam-shock-score">
      <div className="webcam-header">
        <h3>Try It Yourself!</h3>
        <p>Use your webcam to test your real-time Shock Score</p>
      </div>

      <div className="webcam-container">
        {/* Video Feed */}
        <div className="video-wrapper">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className={`webcam-video ${isActive ? 'active' : ''}`}
          />
          <canvas ref={canvasRef} style={{ display: 'none' }} />

          {!isActive && !error && (
            <div className="video-placeholder">
              <div className="placeholder-icon">📹</div>
              <p>Click "Start Camera" to begin</p>
            </div>
          )}

          {error && (
            <div className="video-error">
              <div className="error-icon">⚠️</div>
              <p>{error}</p>
            </div>
          )}

          {isActive && !faceDetected && (
            <div className="no-face-overlay">
              <p>Position your face in frame</p>
            </div>
          )}

          {isActive && faceDetected && (
            <div className="face-detected-indicator">
              ✓ Face Detected
            </div>
          )}
        </div>

        {/* Controls */}
        <div className="webcam-controls">
          {!isActive ? (
            <button onClick={startWebcam} className="btn btn-primary btn-large">
              🎥 Start Camera
            </button>
          ) : (
            <button onClick={stopWebcam} className="btn btn-secondary btn-large">
              ⏹️ Stop Camera
            </button>
          )}
        </div>

        {/* Live Shock Score Display */}
        {isActive && faceDetected && (
          <div className="live-results">
            <div className="shock-score-display">
              <div className="score-label">Your Shock Score</div>
              <div
                className="score-value"
                style={{ color: getShockScoreColor(currentShockScore) }}
              >
                {currentShockScore.toFixed(1)}
              </div>
              <div className="score-max">/100</div>
            </div>

            <div className="emotion-display">
              <div className="emotion-emoji">
                {getEmotionEmoji(dominantEmotion)}
              </div>
              <div className="emotion-label">
                {dominantEmotion.charAt(0).toUpperCase() + dominantEmotion.slice(1)}
              </div>
            </div>

            {/* Emotion Breakdown */}
            <div className="emotion-bars">
              {Object.entries(emotionScores).map(([emotion, score]) => (
                <div key={emotion} className="emotion-bar-item">
                  <div className="emotion-bar-label">
                    {getEmotionEmoji(emotion)} {emotion}
                  </div>
                  <div className="emotion-bar-container">
                    <div
                      className="emotion-bar-fill"
                      style={{
                        width: `${score}%`,
                        backgroundColor: emotion === 'fear' || emotion === 'surprise'
                          ? '#dc2626'
                          : '#666'
                      }}
                    />
                  </div>
                  <div className="emotion-bar-value">
                    {score.toFixed(0)}%
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Info Box */}
        <div className="webcam-info">
          <h4>How It Works</h4>
          <ul>
            <li>✓ Real-time facial emotion recognition</li>
            <li>✓ Instant Shock Score calculation</li>
            <li>✓ 7 emotion categories detected</li>
            <li>✓ No data stored - 100% private</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default WebcamShockScore;
