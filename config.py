"""
Shock Score System Configuration

Cinema-optimized settings for facial emotion recognition in low-light environments.
"""

# Video Processing Settings
FRAME_RATE = 30  # Target FPS for processing
FRAME_SKIP = 2   # Process every Nth frame (15 FPS effective rate for performance)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Face Detection Settings
MIN_FACE_SIZE = 40  # Minimum face size in pixels (cinema audiences may be far from camera)
DETECTION_CONFIDENCE = 0.7  # Threshold for face detection (lower for challenging IR conditions)
MAX_FACES_PER_FRAME = 50  # Maximum audience members to track per frame

# Emotion Recognition Settings
EMOTION_LABELS = [
    'angry',
    'disgust',
    'fear',
    'happy',
    'sad',
    'surprise',
    'neutral'
]

# Shock Score Calculation Parameters
FEAR_WEIGHT = 2.0      # Fear has highest impact on Shock Score
SURPRISE_WEIGHT = 1.5  # Surprise indicates successful scare
HAPPY_WEIGHT = 0.3     # Nervous laughter (tension release)
DISGUST_WEIGHT = 0.8   # Visceral reaction
ANGRY_WEIGHT = 0.2     # Negative but not target emotion
SAD_WEIGHT = 0.1       # Low impact
NEUTRAL_WEIGHT = 0.0   # No emotional engagement

# EPM (Emotional Performance Metric) Settings
EPM_WINDOW_SECONDS = 5  # Calculate EPM over 5-second rolling windows
BASELINE_CALIBRATION_SECONDS = 30  # Use first 30s to establish neutral baseline

# Privacy & Anonymization
STORE_FRAMES = False  # NEVER store video frames
STORE_FACE_EMBEDDINGS = False  # NEVER store facial feature vectors
AGGREGATE_ONLY = True  # Only output aggregate emotional scores

# Performance Optimization
USE_GPU = True  # Enable GPU acceleration if available
BATCH_SIZE = 8  # Process multiple faces in batch for efficiency

# Output Settings
OUTPUT_FORMAT = 'json'  # Options: 'json', 'csv'
REALTIME_DISPLAY = True  # Show live visualization during processing
SAVE_REPORT = True  # Generate detailed report at end of session
