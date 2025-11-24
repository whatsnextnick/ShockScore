# Shock Score - Installation Guide

Complete setup instructions for the Shock Score FER Engine.

## System Requirements

### Hardware Requirements

**Minimum (Development/Testing):**
- CPU: Intel Core i5 or equivalent
- RAM: 8 GB
- Webcam: Any USB camera or built-in laptop camera
- Storage: 2 GB free space

**Recommended (Production/Cinema Edge Device):**
- CPU: Intel Core i7 or ARM-based edge processor (e.g., Raspberry Pi 4)
- RAM: 16 GB
- GPU: NVIDIA GPU with CUDA support (GTX 1650 or better)
- Camera: IR camera (940nm wavelength) for low-light cinema environments
- Storage: 10 GB free space

### Software Requirements

- **Operating System**: Linux (Ubuntu 20.04+), macOS (10.15+), or Windows 10+
- **Python**: 3.8, 3.9, or 3.10 (3.11+ not yet fully tested)
- **Pip**: Latest version

---

## Installation Steps

### 1. Clone or Download Repository

```bash
cd /path/to/your/projects
# If using git:
git clone <repository-url>
cd ShockScore

# Or simply navigate to the extracted folder
```

### 2. Create Virtual Environment

It's strongly recommended to use a virtual environment to avoid dependency conflicts.

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` prefix in your terminal prompt.

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

This will install:
- OpenCV (computer vision)
- DeepFace (emotion recognition)
- TensorFlow (deep learning backend)
- MTCNN (face detection)
- Flask (for future API integration)

**Note**: TensorFlow installation may take several minutes depending on your internet speed.

### 4. Verify Installation

Test that all components are installed correctly:

```bash
python -c "import cv2; import deepface; import mtcnn; print('All dependencies OK')"
```

You should see: `All dependencies OK`

### 5. Test Webcam Access

```bash
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error'); cap.release()"
```

---

## Quick Start

### Run Demo

The easiest way to test the system:

```bash
python demo.py
```

This launches an interactive menu with multiple demo modes:
1. **Webcam Demo** - Real-time processing with your camera
2. **Video File Demo** - Process a video file
3. **Generate Sample Video** - Create a test video

### Process a Video File

```bash
python shock_score_engine.py --input /path/to/video.mp4 --output results.json
```

### Real-Time Webcam Processing

```bash
python shock_score_engine.py --input 0 --output webcam_results.json
```

### Headless Mode (No Visualization)

For faster processing on edge devices:

```bash
python shock_score_engine.py --input video.mp4 --output results.json --no-display
```

---

## Troubleshooting

### Issue: "ImportError: No module named cv2"

**Solution**: Reinstall OpenCV
```bash
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python==4.8.1.78 opencv-contrib-python==4.8.1.78
```

### Issue: "Cannot open camera"

**Possible causes**:
1. Camera is in use by another application (close Zoom, Teams, etc.)
2. Permission denied (Linux/macOS may require camera permissions)
3. Wrong camera index

**Solution**: Try different camera indices:
```bash
python shock_score_engine.py --input 1  # Try camera index 1
python shock_score_engine.py --input 2  # Try camera index 2
```

### Issue: DeepFace model download fails

**Solution**: Manually download models:
```bash
python -c "from deepface import DeepFace; DeepFace.build_model('Emotion')"
```

This will download the emotion recognition model to `~/.deepface/weights/`

### Issue: TensorFlow GPU not detected

**Solution**: Install CUDA-enabled TensorFlow (for NVIDIA GPUs):
```bash
pip uninstall tensorflow
pip install tensorflow-gpu==2.16.1
```

**Note**: Requires NVIDIA CUDA Toolkit and cuDNN to be installed on your system.

### Issue: "Illegal instruction" error on Raspberry Pi

**Solution**: Use TensorFlow Lite instead:
```bash
pip uninstall tensorflow
pip install tensorflow-lite
```

You'll need to modify `emotion_analyzer.py` to use TFLite models.

---

## Advanced Configuration

### Optimize for Your Environment

Edit `config.py` to adjust settings:

```python
# For cinema with distant audience (increase detection range)
MIN_FACE_SIZE = 30  # Smaller minimum face size
MAX_FACES_PER_FRAME = 100  # More faces

# For close-up testing (faster processing)
MIN_FACE_SIZE = 60
MAX_FACES_PER_FRAME = 10

# For IR cameras (adjust detection confidence)
DETECTION_CONFIDENCE = 0.6  # Lower threshold for low-light

# Performance tuning
FRAME_SKIP = 3  # Process every 3rd frame (10 FPS effective)
USE_GPU = True  # Enable GPU acceleration
```

### GPU Acceleration Setup

For NVIDIA GPUs:

1. Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads
2. Install cuDNN: https://developer.nvidia.com/cudnn
3. Verify GPU detection:
   ```bash
   python -c "import tensorflow as tf; print('GPU Available:', tf.test.is_gpu_available())"
   ```

### Edge Device Deployment (Raspberry Pi)

For cinema edge devices:

1. Use lighter model: Edit `emotion_analyzer.py` to use `model_name='OpenFace'` (faster)
2. Enable frame skipping: Set `FRAME_SKIP = 5` in `config.py`
3. Disable display: Run with `--no-display` flag
4. Use hardware acceleration:
   ```bash
   # Install OpenCV with hardware acceleration
   pip uninstall opencv-python
   # Build from source with NEON/GPU support
   ```

---

## Testing Installation

### Unit Tests

Test individual components:

```bash
# Test face detector
python face_detector.py

# Test emotion analyzer
python emotion_analyzer.py

# Test shock score calculator
python shock_score_calculator.py

# Test anonymizer
python anonymizer.py
```

Each module has built-in tests that run when executed directly.

### Integration Test

Run the full pipeline:

```bash
python shock_score_engine.py --input 0
```

Press 'q' after a few seconds. Check that `shock_score_report.json` is generated.

---

## Next Steps

1. **Run Demo**: `python demo.py` to see the system in action
2. **Process Videos**: Test with your own video files
3. **Customize Settings**: Modify `config.py` for your environment
4. **Deploy**: Set up on edge device for cinema testing

For B2B integration (connecting to the Node.js backend), see `API_INTEGRATION.md` (coming soon).

---

## Support

For issues or questions:
- Check the troubleshooting section above
- Review `README.md` for architecture details
- Open an issue on GitHub

## Privacy Note

This system is designed with privacy-first principles:
- No video frames are stored
- No facial images are saved
- Only anonymized aggregate metrics are processed
- GDPR/CCPA compliant by design

See `anonymizer.py` for implementation details.
