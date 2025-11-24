import React, { useState, useRef, useEffect } from 'react';
import './WebcamShockScore.css';

const WebcamShockScoreSimple = () => {
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
  const [debugLog, setDebugLog] = useState([]);
  const intervalRef = useRef(null);

  // Add debug message
  const addDebug = (message) => {
    console.log('🔍', message);
    setDebugLog(prev => [...prev.slice(-4), `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  // Start webcam
  const startWebcam = async () => {
    try {
      addDebug('Requesting camera access...');
      setError(null);

      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 }
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        addDebug('✓ Camera started');
        setIsActive(true);
        setFaceDetected(true);  // Assume face is detected for demo

        // Start capturing frames for analysis
        addDebug('Starting frame capture...');
        startFrameCapture();
      }
    } catch (err) {
      console.error('Webcam error:', err);
      const errorMsg = 'Cannot access webcam. Please allow camera permissions.';
      setError(errorMsg);
      addDebug(`✗ Error: ${errorMsg}`);
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
    addDebug('Camera stopped');
  };

  // Start capturing and analyzing frames
  const startFrameCapture = () => {
    addDebug('Frame capture started (every 1.5s)');
    intervalRef.current = setInterval(() => {
      captureAndAnalyze();
    }, 1500); // Every 1.5 seconds
  };

  // Stop frame capture
  const stopFrameCapture = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
      addDebug('Frame capture stopped');
    }
  };

  // Capture frame and send for analysis
  const captureAndAnalyze = async () => {
    if (!videoRef.current || !canvasRef.current || isProcessing) {
      return;
    }

    addDebug('Capturing frame...');
    setIsProcessing(true);

    const canvas = canvasRef.current;
    const video = videoRef.current;
    const context = canvas.getContext('2d');

    // Set canvas size
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;

    // Draw video frame
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert to blob
    canvas.toBlob(async (blob) => {
      if (!blob) {
        addDebug('✗ Failed to create blob');
        setIsProcessing(false);
        return;
      }

      try {
        addDebug(`Sending frame (${(blob.size / 1024).toFixed(1)}KB)...`);

        const formData = new FormData();
        formData.append('frame', blob, 'frame.jpg');

        const response = await fetch('/api/analyze/frame', {
          method: 'POST',
          body: formData
        });

        addDebug(`Response: ${response.status}`);

        if (response.ok) {
          const data = await response.json();
          addDebug(`✓ Got data: Shock=${data.shockScore?.toFixed(1)}`);

          setFaceDetected(true);
          setEmotionScores(data.emotions);
          setDominantEmotion(data.dominantEmotion);
          setCurrentShockScore(data.shockScore);
        } else {
          const errorText = await response.text();
          addDebug(`✗ Error ${response.status}: ${errorText}`);
        }
      } catch (err) {
        addDebug(`✗ Network error: ${err.message}`);
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

  // Cleanup
  useEffect(() => {
    return () => {
      stopWebcam();
    };
  }, []);

  const getShockScoreColor = (score) => {
    if (score < 20) return '#10b981';
    if (score < 40) return '#f59e0b';
    if (score < 60) return '#f97316';
    if (score < 80) return '#ef4444';
    return '#dc2626';
  };

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
        {/* Debug Panel */}
        {isActive && (
          <div style={{
            background: '#1a1a1a',
            padding: '1rem',
            borderRadius: '0.5rem',
            marginBottom: '1rem',
            fontSize: '0.75rem',
            fontFamily: 'monospace',
            color: '#10b981'
          }}>
            <div style={{ marginBottom: '0.5rem', fontWeight: 'bold' }}>Debug Log:</div>
            {debugLog.map((log, i) => (
              <div key={i} style={{ opacity: 0.8 }}>{log}</div>
            ))}
            <div style={{ marginTop: '0.5rem', color: isProcessing ? '#f59e0b' : '#10b981' }}>
              Status: {isProcessing ? '⏳ Processing...' : '✓ Ready'}
            </div>
          </div>
        )}

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

          {isActive && faceDetected && (
            <div className="face-detected-indicator">
              ✓ Active - Analyzing every 1.5s
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

        {/* Live Results */}
        {isActive && faceDetected && currentShockScore > 0 && (
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
            <li>✓ Instant Shock Score calculation (demo mode)</li>
            <li>✓ 7 emotion categories detected</li>
            <li>✓ No data stored - 100% private</li>
          </ul>
          <p style={{ marginTop: '1rem', fontSize: '0.875rem', color: '#f59e0b' }}>
            📊 Currently using mock data for demo. Full Python FER integration coming soon.
          </p>
        </div>
      </div>
    </div>
  );
};

export default WebcamShockScoreSimple;
