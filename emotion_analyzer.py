"""
Emotion Recognition Module

Uses DeepFace for emotion classification optimized for cinema environments.
Analyzes facial expressions to detect fear, surprise, and other emotions.
"""

import cv2
import numpy as np
from deepface import DeepFace
from typing import List, Dict, Optional
import config
import warnings
warnings.filterwarnings('ignore')


class EmotionAnalyzer:
    """
    Emotion recognition engine using DeepFace.

    Designed for real-time processing of multiple faces with focus on
    horror/thriller-relevant emotions (fear, surprise, disgust).
    """

    def __init__(self, model_name: str = 'Facenet', detector_backend: str = 'skip'):
        """
        Initialize emotion analyzer.

        Args:
            model_name: DeepFace model to use ('VGG-Face', 'Facenet', 'OpenFace', etc.)
            detector_backend: 'skip' since we're using our own face detector
        """
        self.model_name = model_name
        self.detector_backend = detector_backend
        self.analysis_count = 0

        # Warm up the model (load weights into memory)
        print("Warming up emotion recognition model...")
        self._warm_up_model()
        print("Model ready for real-time analysis")

    def _warm_up_model(self):
        """Pre-load model weights by running a dummy prediction."""
        try:
            dummy_frame = np.zeros((48, 48, 3), dtype=np.uint8)
            DeepFace.analyze(
                dummy_frame,
                actions=['emotion'],
                detector_backend='skip',
                enforce_detection=False,
                silent=True
            )
        except Exception as e:
            print(f"Model warm-up warning: {e}")

    def analyze_face(self, face_image: np.ndarray) -> Optional[Dict]:
        """
        Analyze a single face image for emotions.

        Args:
            face_image: Cropped face region (BGR format from OpenCV)

        Returns:
            Dictionary with emotion probabilities or None if analysis fails:
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
        """
        try:
            # Ensure face image is valid
            if face_image is None or face_image.size == 0:
                return None

            # Resize if too small (DeepFace requires minimum size)
            if face_image.shape[0] < 48 or face_image.shape[1] < 48:
                face_image = cv2.resize(face_image, (48, 48))

            # Run emotion analysis
            result = DeepFace.analyze(
                face_image,
                actions=['emotion'],
                detector_backend='skip',  # We already detected faces
                enforce_detection=False,
                silent=True
            )

            # Handle result format (DeepFace may return list or dict)
            if isinstance(result, list):
                result = result[0]

            self.analysis_count += 1

            return {
                'dominant_emotion': result['dominant_emotion'],
                'emotion_scores': result['emotion']
            }

        except Exception as e:
            # Silently handle analysis failures (poor lighting, extreme angles, etc.)
            return None

    def analyze_batch(self, face_images: List[np.ndarray]) -> List[Optional[Dict]]:
        """
        Analyze multiple faces in sequence.

        Args:
            face_images: List of cropped face regions

        Returns:
            List of emotion analysis results (same order as input)
        """
        results = []
        for face_img in face_images:
            result = self.analyze_face(face_img)
            results.append(result)
        return results

    def get_shock_relevant_score(self, emotion_result: Dict) -> float:
        """
        Calculate a single "shock relevance" score for horror/thriller content.

        This score emphasizes fear and surprise while accounting for other emotions.

        Args:
            emotion_result: Output from analyze_face()

        Returns:
            Float score between 0-100 indicating shock/scare intensity
        """
        if emotion_result is None:
            return 0.0

        scores = emotion_result['emotion_scores']

        # Weighted combination of emotions
        shock_score = (
            scores.get('fear', 0) * config.FEAR_WEIGHT +
            scores.get('surprise', 0) * config.SURPRISE_WEIGHT +
            scores.get('disgust', 0) * config.DISGUST_WEIGHT +
            scores.get('happy', 0) * config.HAPPY_WEIGHT +  # Nervous laughter
            scores.get('angry', 0) * config.ANGRY_WEIGHT +
            scores.get('sad', 0) * config.SAD_WEIGHT +
            scores.get('neutral', 0) * config.NEUTRAL_WEIGHT
        )

        # Normalize to 0-100 scale
        max_possible_score = 100 * (
            config.FEAR_WEIGHT + config.SURPRISE_WEIGHT
        )
        normalized_score = min(100, (shock_score / max_possible_score) * 100)

        return round(normalized_score, 2)


class EmotionAggregator:
    """
    Aggregates emotion data across multiple faces and time windows.
    """

    def __init__(self):
        """Initialize aggregator with empty state."""
        self.emotion_history = []
        self.timestamp_history = []

    def add_frame_emotions(
        self,
        frame_results: List[Optional[Dict]],
        timestamp: float
    ):
        """
        Store emotion results from a single frame.

        Args:
            frame_results: List of emotion analysis results
            timestamp: Frame timestamp in seconds
        """
        # Filter out None results
        valid_results = [r for r in frame_results if r is not None]

        self.emotion_history.append(valid_results)
        self.timestamp_history.append(timestamp)

    def get_aggregate_emotions(
        self,
        window_seconds: float = config.EPM_WINDOW_SECONDS
    ) -> Dict:
        """
        Calculate aggregate emotion scores over a time window.

        Args:
            window_seconds: Time window for aggregation

        Returns:
            Dictionary with averaged emotion scores across all faces
        """
        if not self.emotion_history:
            return self._get_empty_aggregate()

        # Get recent frames within time window
        current_time = self.timestamp_history[-1]
        cutoff_time = current_time - window_seconds

        # Collect all emotion scores within window
        all_emotions = []
        for timestamp, frame_emotions in zip(
            self.timestamp_history,
            self.emotion_history
        ):
            if timestamp >= cutoff_time:
                all_emotions.extend(frame_emotions)

        if not all_emotions:
            return self._get_empty_aggregate()

        # Calculate average for each emotion
        emotion_sums = {emotion: 0.0 for emotion in config.EMOTION_LABELS}
        count = len(all_emotions)

        for emotion_result in all_emotions:
            for emotion, score in emotion_result['emotion_scores'].items():
                emotion_sums[emotion] += score

        # Average and round
        emotion_averages = {
            emotion: round(total / count, 2)
            for emotion, total in emotion_sums.items()
        }

        return {
            'emotions': emotion_averages,
            'sample_size': count,
            'window_seconds': window_seconds
        }

    def _get_empty_aggregate(self) -> Dict:
        """Return empty aggregate structure."""
        return {
            'emotions': {emotion: 0.0 for emotion in config.EMOTION_LABELS},
            'sample_size': 0,
            'window_seconds': 0
        }


if __name__ == "__main__":
    # Quick test
    print("Testing Emotion Analyzer...")
    analyzer = EmotionAnalyzer()

    # Test with webcam
    cap = cv2.VideoCapture(0)
    print("Show different emotions! Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Simple face detection for testing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_roi = frame[y:y+h, x:x+w]
            result = analyzer.analyze_face(face_roi)

            if result:
                emotion = result['dominant_emotion']
                shock_score = analyzer.get_shock_relevant_score(result)

                # Draw results
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"{emotion} (Shock: {shock_score})",
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        cv2.imshow('Emotion Analysis Test', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Analyzed {analyzer.analysis_count} faces")
