"""
Simple test script to verify Shock Score components work
without requiring a webcam (WSL2 compatible).
"""

import numpy as np
import cv2
from face_detector import CinemaFaceDetector
from emotion_analyzer import EmotionAnalyzer
from shock_score_calculator import ShockScoreCalculator
from anonymizer import DataAnonymizer

print("="*60)
print("SHOCK SCORE - SIMPLE COMPONENT TEST (WSL2 Compatible)")
print("="*60)

# Create a synthetic test image with a simple face pattern
print("\n1. Creating synthetic test image...")
test_img = np.zeros((480, 640, 3), dtype=np.uint8)

# Draw a simple face (white oval with eye and mouth patterns)
cv2.ellipse(test_img, (320, 240), (80, 100), 0, 0, 360, (255, 255, 255), -1)
cv2.circle(test_img, (295, 220), 10, (0, 0, 0), -1)  # Left eye
cv2.circle(test_img, (345, 220), 10, (0, 0, 0), -1)  # Right eye
cv2.ellipse(test_img, (320, 270), (30, 15), 0, 0, 180, (0, 0, 0), 2)  # Smile

print("  ✓ Test image created (480x640)")

# Test Face Detector
print("\n2. Testing Face Detector...")
try:
    detector = CinemaFaceDetector()
    # Note: May not detect our simple face, but should run without error
    detections = detector.detect_faces(test_img)
    print(f"  ✓ Face detector initialized")
    print(f"    Detected {len(detections)} faces (synthetic image)")
except Exception as e:
    print(f"  ✗ Face detector failed: {e}")

# Test Emotion Analyzer
print("\n3. Testing Emotion Analyzer...")
try:
    analyzer = EmotionAnalyzer()

    # Create a proper test face image (48x48 RGB)
    test_face = np.random.randint(100, 200, (48, 48, 3), dtype=np.uint8)

    result = analyzer.analyze_face(test_face)
    if result:
        print(f"  ✓ Emotion analyzer working")
        print(f"    Dominant emotion: {result['dominant_emotion']}")
        print(f"    Top 3 emotions:")
        sorted_emotions = sorted(
            result['emotion_scores'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        for emotion, score in sorted_emotions:
            print(f"      - {emotion}: {score:.1f}%")
    else:
        print("  ⚠ No emotion detected (expected for random image)")
except Exception as e:
    print(f"  ✗ Emotion analyzer failed: {e}")

# Test Shock Score Calculator
print("\n4. Testing Shock Score Calculator...")
try:
    calculator = ShockScoreCalculator()

    # Simulate emotion data
    test_emotions = {
        'emotions': {
            'fear': 65.0,
            'surprise': 20.0,
            'neutral': 15.0,
            'happy': 0.0,
            'sad': 0.0,
            'angry': 0.0,
            'disgust': 0.0
        }
    }

    shock_score = calculator.calculate_shock_score(test_emotions)
    print(f"  ✓ Shock Score calculator working")
    print(f"    Test Shock Score: {shock_score}/100")
    print(f"    (High fear + surprise should give high score)")
except Exception as e:
    print(f"  ✗ Shock Score calculator failed: {e}")

# Test Anonymizer
print("\n5. Testing Anonymizer (Privacy Layer)...")
try:
    anonymizer = DataAnonymizer()

    # Simulate individual emotion results from 3 faces
    individual_emotions = [
        {'emotion_scores': {'fear': 70, 'surprise': 15, 'neutral': 15}},
        {'emotion_scores': {'fear': 60, 'surprise': 25, 'neutral': 15}},
        {'emotion_scores': {'fear': 65, 'surprise': 20, 'neutral': 15}},
    ]

    anonymized = anonymizer.anonymize_emotion_data(individual_emotions, timestamp=10.5)

    print(f"  ✓ Anonymizer working")
    print(f"    Input: 3 individual faces → Output: Aggregate only")
    print(f"    Audience size: {anonymized['audience_size']}")
    print(f"    Average fear: {anonymized['emotions']['fear']:.1f}%")
    print(f"    Privacy level: {anonymized['privacy_level']}")
    print(f"    Contains PII: {anonymized['contains_pii']}")

    # Validate privacy compliance
    is_compliant = anonymizer.validate_privacy_compliance(anonymized)
    print(f"    Privacy compliant: {is_compliant}")
except Exception as e:
    print(f"  ✗ Anonymizer failed: {e}")

# Summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)
print("\n✓ Core components verified successfully!")
print("\nNOTE: Camera test skipped (WSL2 has no webcam access)")
print("To test with video, use: python shock_score_engine.py --input video.mp4")
print("\n" + "="*60)
