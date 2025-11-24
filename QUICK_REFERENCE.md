# Shock Score - Quick Reference Card

## 🚀 Installation (3 Steps)

```bash
# 1. Create virtual environment
python3 -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test installation
python test_installation.py
```

---

## 🎮 Common Commands

### Run Interactive Demo
```bash
python demo.py
```

### Process Webcam (Real-time)
```bash
python shock_score_engine.py --input 0
```

### Process Video File
```bash
python shock_score_engine.py --input movie.mp4 --output report.json
```

### Headless Mode (No Display)
```bash
python shock_score_engine.py --input movie.mp4 --no-display
```

### Test Individual Modules
```bash
python face_detector.py        # Test face detection
python emotion_analyzer.py     # Test emotion recognition
python shock_score_calculator.py  # Test metrics
python anonymizer.py           # Test privacy layer
```

---

## 📊 Key Metrics Explained

### Shock Score (0-100)
Instantaneous scare intensity at each moment
- **0-20**: Low/No fear response
- **20-40**: Mild tension
- **40-60**: Moderate scare
- **60-80**: Strong fear reaction
- **80-100**: Extreme terror (jump scare)

### EPM Score (0-10)
Emotional Performance Metric - Overall film rating
- **0-3**: Poor horror effectiveness
- **3-5**: Average
- **5-7**: Good (commercial success likely)
- **7-9**: Excellent (cult classic potential)
- **9-10**: Exceptional (genre-defining)

### Scare Events
Jump scares detected via rapid Shock Score spikes (>30 point increase)

---

## ⚙️ Configuration (config.py)

### Performance Tuning
```python
FRAME_SKIP = 2          # Process every Nth frame (2 = 15 FPS)
USE_GPU = True          # Enable GPU acceleration
MAX_FACES_PER_FRAME = 50  # Maximum faces to track
```

### Cinema Optimization
```python
MIN_FACE_SIZE = 40      # Smaller = detect distant faces
DETECTION_CONFIDENCE = 0.7  # Lower = more detections (noisier)
```

### Emotion Weights (Shock Score Formula)
```python
FEAR_WEIGHT = 2.0       # Fear impact (highest)
SURPRISE_WEIGHT = 1.5   # Surprise impact
DISGUST_WEIGHT = 0.8    # Disgust impact
HAPPY_WEIGHT = 0.3      # Nervous laughter
```

---

## 📁 File Structure

```
ShockScore/
│
├── 🚀 ENTRY POINTS
│   ├── shock_score_engine.py    # Main processing pipeline
│   ├── demo.py                   # Interactive demo
│   └── test_installation.py     # Installation verification
│
├── 🧠 CORE MODULES
│   ├── face_detector.py          # MTCNN face detection
│   ├── emotion_analyzer.py       # DeepFace emotion AI
│   ├── shock_score_calculator.py # EPM metrics
│   └── anonymizer.py             # Privacy layer
│
├── ⚙️ CONFIGURATION
│   ├── config.py                 # System settings
│   └── requirements.txt          # Dependencies
│
└── 📚 DOCUMENTATION
    ├── README.md                 # Quick start
    ├── INSTALLATION.md           # Setup guide (6,000+ words)
    ├── ARCHITECTURE.md           # Technical deep-dive (8,000+ words)
    ├── PROJECT_SUMMARY.md        # Overview
    └── QUICK_REFERENCE.md        # This file
```

---

## 🐛 Troubleshooting

### "Cannot open camera"
```bash
# Try different camera index
python shock_score_engine.py --input 1

# Check camera permissions (Linux/macOS)
ls /dev/video*
```

### "ImportError: No module named cv2"
```bash
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python==4.8.1.78 opencv-contrib-python==4.8.1.78
```

### Slow Processing
```python
# In config.py, increase frame skip:
FRAME_SKIP = 5  # Process every 5th frame (6 FPS)

# Enable GPU if available
USE_GPU = True

# Reduce max faces
MAX_FACES_PER_FRAME = 20
```

### Model Download Fails
```bash
# Manually download DeepFace models
python -c "from deepface import DeepFace; DeepFace.build_model('Emotion')"
```

---

## 📈 Report Output Format

### JSON Structure
```json
{
  "overall_metrics": {
    "epm_score": 7.8,
    "average_shock_score": 42.5,
    "peak_shock_score": 89.3,
    "total_scare_events": 12,
    "average_audience_size": 35,
    "total_runtime_seconds": 6480
  },
  "peak_moments": [
    {"timestamp": "12:45", "shock_score": 89.3, "dominant_emotion": "fear"},
    {"timestamp": "23:12", "shock_score": 85.7, "dominant_emotion": "fear"}
  ],
  "scare_events": [
    {"timestamp": "05:23", "intensity": 78.5, "type": "jump_scare"}
  ],
  "missed_opportunities": [
    {"timestamp": "34:12", "shock_score": 8.2, "recommendation": "Consider enhancing tension"}
  ],
  "tension_analysis": {
    "sustained_tension_periods": 5,
    "average_tension_duration": 45.3
  },
  "timeline_data": [
    {"timestamp": 0.0, "shock_score": 12.3, "emotions": {...}, "sample_size": 32}
  ],
  "privacy_compliance": {
    "video_frames_stored": 0,
    "facial_images_stored": 0,
    "privacy_level": "GDPR_COMPLIANT"
  }
}
```

---

## 🔐 Privacy Compliance

### What is NEVER Stored
- ❌ Video frames
- ❌ Facial images
- ❌ Face embeddings
- ❌ Individual identity
- ❌ Demographics (age, gender, race)
- ❌ Any PII

### What IS Stored
- ✅ Aggregate emotion scores (population average)
- ✅ Audience count
- ✅ Timestamp
- ✅ Session ID (anonymous)

### Compliance Standards
- ✅ GDPR Article 25 (Privacy by Design)
- ✅ CCPA Section 1798.100 (Data Minimization)
- ✅ No PII collected or transmitted

---

## 💻 Hardware Requirements

### Minimum (Testing)
- CPU: Intel Core i5 / AMD Ryzen 5
- RAM: 8 GB
- Webcam: Any USB camera
- Storage: 2 GB

### Recommended (Production)
- CPU: Intel Core i7 / ARM (Raspberry Pi 4)
- RAM: 16 GB
- GPU: NVIDIA GTX 1650+ (optional but 2-3x faster)
- Camera: IR camera (940nm) for cinema
- Storage: 10 GB

### Edge Device (Cinema)
- Raspberry Pi 4 (4GB+ RAM) or NVIDIA Jetson Nano
- IR camera module
- 32GB+ microSD card
- Network connection (for data upload)

---

## 🎯 Performance Targets

| Metric | Target | Typical |
|--------|--------|---------|
| Processing FPS | 15-30 | 20 |
| Latency per frame | <100ms | 50-80ms |
| Face detection accuracy | >90% | 95% |
| Emotion accuracy | >65% | 70% |
| RAM usage | <3GB | 1-2GB |
| CPU usage (no GPU) | <80% | 60-70% |

---

## 📚 Additional Resources

### Documentation
- **README.md** - Quick start (5 min read)
- **INSTALLATION.md** - Detailed setup (15 min read)
- **ARCHITECTURE.md** - Technical deep-dive (30 min read)
- **PROJECT_SUMMARY.md** - Overview (10 min read)

### Code References
- All modules have built-in tests: `python module_name.py`
- Docstrings in every function
- Inline comments for complex logic

### External Links
- OpenCV: https://opencv.org/
- DeepFace: https://github.com/serengil/deepface
- MTCNN Paper: https://arxiv.org/abs/1604.02878
- FER+ Dataset: https://github.com/microsoft/FERPlus

---

## 🎬 Quick Demo Script

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Run webcam demo
python demo.py
# Select option 1 (Webcam Demo)

# 3. Show different emotions:
#    - Neutral (baseline)
#    - Wide eyes + mouth open (surprise)
#    - Scared expression (fear)
#    - Smile (happy/relief)

# 4. Press 'q' to quit

# 5. Check generated report
ls -lh demo_webcam_*.json
```

---

## 📞 Getting Help

1. **Check logs**: Most errors have descriptive messages
2. **Read INSTALLATION.md**: Comprehensive troubleshooting section
3. **Test individual modules**: Isolate the problem
4. **Review config.py**: Ensure settings match your hardware
5. **Check dependencies**: `python test_installation.py`

---

## ✅ Pre-Launch Checklist

Before production deployment:

- [ ] Installation test passes: `python test_installation.py`
- [ ] Camera accessible: `python face_detector.py`
- [ ] Emotion model loaded: `python emotion_analyzer.py`
- [ ] Config optimized for hardware: `config.py`
- [ ] Demo runs successfully: `python demo.py`
- [ ] Sample video processed: `python shock_score_engine.py --input test.mp4`
- [ ] Report generated: Check `.json` output file
- [ ] Privacy validation passes: Review `privacy_compliance` in report

---

**Last Updated**: November 2025
**Version**: 1.0.0 (Phase 1 - Edge Processing Complete)
