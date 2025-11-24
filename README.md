# Shock Score - Real-Time Facial Emotion Recognition Engine

A high-performance Python-based FER system designed for cinema environments, capable of processing IR camera feeds to quantify audience emotional responses in real-time.

## Features

- **Real-Time Processing**: Optimized for 15-30 FPS on edge devices
- **Cinema-Optimized**: Handles low-light IR camera input and challenging viewing angles
- **Privacy-First**: Immediate anonymization - no facial data stored
- **Emotion Metrics**: Tracks fear, surprise, happiness, sadness, anger, disgust, neutral
- **Shock Score Algorithm**: Proprietary EPM (Emotional Performance Metric) calculation

## Architecture

```
IR Camera → Frame Capture → Face Detection → Emotion Analysis → Anonymization → Aggregated Metrics
```

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```bash
# Process a video file
python shock_score_engine.py --input sample_video.mp4 --output results.json

# Real-time camera processing
python shock_score_engine.py --camera 0

# Demo mode (generates visualizations)
python demo.py
```

## Components

- `shock_score_engine.py` - Core FER processing engine
- `face_detector.py` - Optimized face detection module
- `emotion_analyzer.py` - Emotion classification using DeepFace
- `shock_score_calculator.py` - EPM metric calculation
- `anonymizer.py` - Privacy-preserving data transformation
- `config.py` - System configuration

## Technical Specifications

- **Face Detection**: MTCNN (Multi-task Cascaded CNN)
- **Emotion Model**: Custom fine-tuned model on FER+ dataset
- **Processing**: OpenCV for frame manipulation
- **Inference**: TensorFlow backend with GPU acceleration support

## Privacy Guarantee

The system processes facial expressions in real-time and immediately converts them to anonymized emotional metrics. No facial images, video frames, or personally identifiable information is ever stored.
# ShockScore
