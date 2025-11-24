#!/usr/bin/env python3
"""
Real-Time Frame Analysis Script

Analyzes a single image frame for facial emotions.
Used by the webcam feature for live Shock Score detection.
"""

import sys
import json
import cv2
import numpy as np
from pathlib import Path

# Add parent directory to path to import our modules
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from emotion_analyzer import EmotionAnalyzer
    from face_detector import CinemaFaceDetector
except ImportError as e:
    print(json.dumps({
        "error": f"Failed to import modules: {e}",
        "faceDetected": False
    }))
    sys.exit(1)


def analyze_frame(image_path):
    """
    Analyze a single frame for emotions.

    Args:
        image_path: Path to image file

    Returns:
        dict: Analysis results
    """
    try:
        # Load image
        frame = cv2.imread(image_path)
        if frame is None:
            return {
                "faceDetected": False,
                "error": "Could not read image"
            }

        # Initialize components
        face_detector = CinemaFaceDetector()
        emotion_analyzer = EmotionAnalyzer()

        # Detect faces
        detections = face_detector.detect_faces(frame)

        if not detections:
            return {
                "faceDetected": False,
                "message": "No face detected"
            }

        # Use the first (most prominent) face
        face_regions = face_detector.extract_face_regions(frame, [detections[0]])

        if not face_regions:
            return {
                "faceDetected": False,
                "message": "Could not extract face"
            }

        # Analyze emotion
        result = emotion_analyzer.analyze_face(face_regions[0])

        if result is None:
            return {
                "faceDetected": False,
                "message": "Emotion analysis failed"
            }

        # Return results
        return {
            "faceDetected": True,
            "dominantEmotion": result['dominant_emotion'],
            "emotions": result['emotion_scores']
        }

    except Exception as e:
        return {
            "faceDetected": False,
            "error": str(e)
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "No image path provided",
            "faceDetected": False
        }))
        sys.exit(1)

    image_path = sys.argv[1]
    result = analyze_frame(image_path)
    print(json.dumps(result))
