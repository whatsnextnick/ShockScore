# Shock Score - System Architecture

Technical architecture documentation for the Shock Score FER system.

## Overview

Shock Score is a real-time Facial Emotion Recognition (FER) system designed specifically for cinema environments. It analyzes audience reactions to horror/thriller films and produces actionable analytics for Hollywood studios.

### Key Design Principles

1. **Privacy-First**: No facial data stored, only aggregate metrics
2. **Real-Time**: Low-latency processing suitable for live analysis
3. **Edge Computing**: Analysis occurs locally at cinema (not cloud)
4. **Scalability**: Handles 50+ simultaneous faces per frame
5. **Cinema-Optimized**: Works with low-light IR cameras

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CINEMA EDGE DEVICE                       │
│                                                                 │
│  ┌────────────┐    ┌──────────────┐    ┌─────────────────┐   │
│  │ IR Camera  │───▶│ Face Detector│───▶│ Emotion Analyzer│   │
│  └────────────┘    └──────────────┘    └─────────────────┘   │
│                                                  │              │
│                                                  ▼              │
│                                         ┌─────────────────┐    │
│                                         │  Anonymizer     │    │
│                                         │  (Privacy Layer)│    │
│                                         └─────────────────┘    │
│                                                  │              │
│                                                  ▼              │
│                                         ┌─────────────────┐    │
│                                         │ Shock Score     │    │
│                                         │ Calculator      │    │
│                                         └─────────────────┘    │
└─────────────────────────────────────────────┬───────────────────┘
                                              │
                                              │ Encrypted HTTPS
                                              ▼
                                    ┌──────────────────┐
                                    │  Node.js API     │
                                    │  (Cloud Backend) │
                                    └──────────────────┘
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │  React Dashboard │
                                    │  (B2B Frontend)  │
                                    └──────────────────┘
```

### Component Architecture

```
shock_score_engine.py (Main Orchestrator)
    │
    ├── face_detector.py (MTCNN-based detection)
    │   └── Uses: OpenCV, MTCNN
    │
    ├── emotion_analyzer.py (DeepFace emotion recognition)
    │   └── Uses: DeepFace, TensorFlow/Keras
    │
    ├── anonymizer.py (Privacy compliance)
    │   └── Aggregate-only data transformation
    │
    └── shock_score_calculator.py (Proprietary metrics)
        └── EPM calculation, scare detection, report generation
```

---

## Core Components

### 1. Face Detector (`face_detector.py`)

**Purpose**: Detect and localize faces in video frames.

**Technology**: MTCNN (Multi-task Cascaded Convolutional Networks)

**Key Features**:
- Handles multiple faces (up to 50 per frame)
- Works with IR camera input (940nm wavelength)
- Confidence-based filtering (>70% confidence)
- Facial landmark detection (eyes, nose, mouth)

**Performance**:
- Processing speed: 30-50ms per frame (CPU)
- Detection accuracy: 95%+ in cinema conditions

**Algorithm**:
```python
def detect_faces(frame):
    1. Convert BGR to RGB
    2. Run MTCNN face detection
    3. Filter by confidence threshold
    4. Extract face regions with padding
    5. Return bounding boxes + keypoints
```

### 2. Emotion Analyzer (`emotion_analyzer.py`)

**Purpose**: Classify facial expressions into 7 emotion categories.

**Technology**: DeepFace library with pre-trained CNN model

**Emotion Categories**:
- Fear (primary metric for horror films)
- Surprise (jump scares)
- Disgust (visceral reactions)
- Happy (nervous laughter, tension release)
- Sad (empathetic responses)
- Angry (negative reactions)
- Neutral (baseline)

**Model Architecture**:
- Input: 48x48 grayscale face image
- Convolutional layers for feature extraction
- Softmax output for 7 emotion probabilities
- Pre-trained on FER+ dataset

**Performance**:
- Inference time: 40-60ms per face (CPU)
- Accuracy: ~70% (state-of-the-art for FER)

**Batch Processing**:
```python
def analyze_batch(faces):
    results = []
    for face in faces:
        emotion_scores = model.predict(face)
        results.append(emotion_scores)
    return results
```

### 3. Anonymizer (`anonymizer.py`)

**Purpose**: Ensure GDPR/CCPA compliance through immediate data anonymization.

**Privacy Guarantees**:
- No video frames stored (deleted after processing)
- No facial images stored
- No face embeddings stored
- No demographic inference (age, gender, race)
- No individual tracking across frames

**Anonymization Process**:
```python
def anonymize_emotion_data(individual_emotions):
    # Aggregate across all faces
    aggregate = average_emotions(individual_emotions)

    # Output only population statistics
    return {
        'audience_size': len(individual_emotions),
        'emotions': aggregate,  # Averaged across all faces
        'contains_pii': False
    }
```

**Compliance**:
- GDPR Article 25: Privacy by Design
- CCPA Section 1798.100: Data minimization
- No PII collected or transmitted

### 4. Shock Score Calculator (`shock_score_calculator.py`)

**Purpose**: Calculate proprietary metrics for horror film effectiveness.

**Key Metrics**:

#### A. Instantaneous Shock Score (0-100)
Formula:
```
Shock Score = (Fear_Delta × 2.0) + (Surprise_Delta × 1.5) + Tension_Factor

Where:
- Fear_Delta = Current Fear - Baseline Fear
- Surprise_Delta = Current Surprise - Baseline Surprise
- Tension_Factor = (Current Fear + Disgust) / 2
```

#### B. EPM (Emotional Performance Metric) (0-10)
Aggregate metric over time windows:
```
EPM = (Avg_Shock × Peak_Factor × Consistency_Factor) / 10

Where:
- Peak_Factor = Max_Shock / 100
- Consistency_Factor = 1 - (StdDev / 50)
```

Higher EPM = better horror film performance

#### C. Scare Event Detection
Identifies jump scares based on rapid Shock Score spikes:
```
If (Current_Score - Recent_Avg) > 30:
    SCARE_DETECTED = True
```

**Baseline Calibration**:
- First 30 seconds establish "neutral" emotional state
- All subsequent measurements relative to baseline
- Accounts for audience predisposition

### 5. Main Engine (`shock_score_engine.py`)

**Purpose**: Orchestrate entire pipeline in real-time.

**Processing Pipeline**:
```python
for each frame in video:
    1. faces = detect_faces(frame)
    2. emotions = analyze_emotions(faces)
    3. anonymized = anonymize(emotions)
    4. shock_score = calculate_shock(anonymized)
    5. report.add_data(timestamp, shock_score)
    6. if realtime_display:
           show_visualization(frame, shock_score)
```

**Performance Optimizations**:
- Frame skipping (process every Nth frame)
- Batch emotion analysis
- GPU acceleration (if available)
- Asynchronous I/O for report writing

**Real-Time Constraints**:
- Target: 15-30 FPS processing
- Max latency: 100ms per frame
- Backpressure handling for slower systems

---

## Data Flow

### Input → Output Pipeline

```
1. INPUT: Video frame (640×480, BGR)
   │
   ▼
2. FACE DETECTION
   │ Output: List of face bounding boxes
   │ Format: [(x, y, w, h), confidence]
   ▼
3. FACE EXTRACTION
   │ Output: Cropped face images
   │ Format: [face1, face2, ..., faceN]
   ▼
4. EMOTION ANALYSIS
   │ Output: Emotion probabilities per face
   │ Format: [{fear: 0.65, surprise: 0.20, ...}, ...]
   ▼
5. ANONYMIZATION
   │ Output: Aggregate emotion scores
   │ Format: {audience_size: N, emotions: {fear: avg, ...}}
   ▼
6. SHOCK SCORE CALCULATION
   │ Output: Shock Score (0-100)
   │ Format: float
   ▼
7. REPORT GENERATION
   Output: JSON report
   Format: {
       overall_metrics: {...},
       peak_moments: [...],
       scare_events: [...],
       timeline_data: [...]
   }
```

### Data Structures

**Face Detection Output**:
```python
{
    'box': [x, y, width, height],
    'confidence': 0.95,
    'keypoints': {
        'left_eye': (x1, y1),
        'right_eye': (x2, y2),
        'nose': (x3, y3),
        'mouth_left': (x4, y4),
        'mouth_right': (x5, y5)
    }
}
```

**Emotion Analysis Output**:
```python
{
    'dominant_emotion': 'fear',
    'emotion_scores': {
        'angry': 0.05,
        'disgust': 0.02,
        'fear': 0.65,
        'happy': 0.01,
        'sad': 0.03,
        'surprise': 0.20,
        'neutral': 0.04
    }
}
```

**Anonymized Data**:
```python
{
    'session_id': 'abc123...',
    'timestamp': 125.5,
    'audience_size': 32,
    'emotions': {
        'fear': 45.2,  # Averaged across all 32 faces
        'surprise': 12.3,
        ...
    },
    'privacy_level': 'anonymized',
    'contains_pii': False
}
```

**Final Report**:
```json
{
    "overall_metrics": {
        "epm_score": 7.8,
        "average_shock_score": 42.5,
        "peak_shock_score": 89.3,
        "total_scare_events": 12,
        "average_audience_size": 35
    },
    "peak_moments": [
        {"timestamp": "12:45", "shock_score": 89.3},
        {"timestamp": "23:12", "shock_score": 85.7},
        ...
    ],
    "scare_events": [
        {"timestamp": "05:23", "intensity": 78.5},
        ...
    ],
    "timeline_data": [
        {"timestamp": 0.0, "shock_score": 12.3, ...},
        {"timestamp": 0.5, "shock_score": 15.7, ...},
        ...
    ]
}
```

---

## Performance Characteristics

### Latency Breakdown (Per Frame)

| Component | CPU Time | GPU Time | % of Total |
|-----------|----------|----------|------------|
| Face Detection | 30-50ms | 10-15ms | 40% |
| Emotion Analysis | 40-60ms | 15-20ms | 50% |
| Anonymization | 1-2ms | 1-2ms | 2% |
| Shock Calculation | 3-5ms | 3-5ms | 5% |
| Visualization | 5-10ms | N/A | 3% |
| **Total** | **80-130ms** | **30-45ms** | **100%** |

**Throughput**:
- CPU: 8-12 FPS
- GPU: 20-30 FPS
- With frame skip (2x): 15-30 FPS effective

### Resource Requirements

**CPU Mode**:
- CPU: 60-80% utilization (Intel i5/i7)
- RAM: 1-2 GB
- Disk I/O: Minimal (report writing only)

**GPU Mode**:
- CPU: 20-30% utilization
- GPU: 40-60% utilization
- RAM: 2-3 GB (includes GPU memory)

### Scalability

**Faces Per Frame**:
- 1-10 faces: Real-time (30 FPS)
- 11-30 faces: Near real-time (15-20 FPS)
- 31-50 faces: Reduced rate (10-15 FPS)
- 50+ faces: Frame skipping required

**Video Length**:
- No limit (streaming processing)
- Memory usage constant (no buffering)

---

## Deployment Models

### 1. Edge Device (Cinema)

**Hardware**: Raspberry Pi 4 or NVIDIA Jetson Nano

**Configuration**:
```python
FRAME_SKIP = 3  # 10 FPS effective
MAX_FACES_PER_FRAME = 30
USE_GPU = True  # Jetson only
REALTIME_DISPLAY = False  # Headless
```

**Network**: Send aggregated data to cloud API every 5 seconds

### 2. Development/Testing

**Hardware**: Standard laptop/desktop

**Configuration**:
```python
FRAME_SKIP = 1  # 30 FPS
MAX_FACES_PER_FRAME = 10
REALTIME_DISPLAY = True
```

### 3. Cloud Processing (Future)

**Not recommended** due to privacy concerns, but possible:
- Upload anonymized features only (not raw video)
- Higher-compute models for better accuracy
- Batch processing of multiple screenings

---

## Security Considerations

### Privacy Protection

1. **Data Minimization**: Only emotion scores transmitted
2. **No Persistent Storage**: Frames deleted immediately
3. **Encryption**: HTTPS for API transmission
4. **Access Control**: B2B dashboard requires authentication
5. **Audit Logging**: All data access logged

### Attack Surface

**Potential Vulnerabilities**:
- Camera feed interception → Use encrypted connection
- Edge device compromise → Secure boot, TPM
- API man-in-the-middle → Certificate pinning
- Report tampering → Digital signatures

### Compliance

- **GDPR**: Article 25 (Privacy by Design)
- **CCPA**: Data minimization, no sale of data
- **HIPAA**: Not applicable (emotions not health data)
- **COPPA**: Not applicable (no children tracking)

---

## Future Enhancements

### Short-Term (3-6 months)

1. **Enhanced Models**:
   - Fine-tune on cinema-specific dataset
   - Add "anticipation" emotion category
   - Improve low-light performance

2. **Real-Time Streaming**:
   - WebSocket API for live dashboards
   - Server-Sent Events for updates

3. **Multi-Camera Support**:
   - Aggregate across multiple camera angles
   - Avoid double-counting same person

### Long-Term (6-12 months)

1. **Advanced Analytics**:
   - Scene-by-scene comparison across films
   - A/B testing for director's cuts
   - Demographic segmentation (opt-in only)

2. **Edge Optimization**:
   - Custom TensorFlow Lite models
   - Hardware-accelerated inference
   - 60 FPS real-time processing

3. **B2B Features**:
   - RESTful API for studio integration
   - Webhook notifications for scare events
   - Export to industry-standard formats

---

## References

### Papers & Research

- **FER+**: Training Deep Networks for Facial Expression Recognition (Microsoft Research)
- **MTCNN**: Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks
- **DeepFace**: Closing the Gap to Human-Level Performance in Face Verification (Facebook AI)

### Libraries & Frameworks

- OpenCV: https://opencv.org/
- DeepFace: https://github.com/serengil/deepface
- TensorFlow: https://tensorflow.org/
- MTCNN: https://github.com/ipazc/mtcnn

### Standards

- GDPR: https://gdpr.eu/
- CCPA: https://oag.ca.gov/privacy/ccpa
- ISO/IEC 27001: Information Security Management
