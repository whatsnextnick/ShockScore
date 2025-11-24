"""
Face Detection Module - Optimized for Cinema Environments

Handles face detection in low-light IR camera feeds with multiple audience members.
Uses MTCNN for robust detection in challenging conditions.
"""

import cv2
import numpy as np
from mtcnn import MTCNN
from typing import List, Tuple, Dict
import config


class CinemaFaceDetector:
    """
    High-performance face detector optimized for cinema audience analysis.

    Features:
    - IR camera compatibility
    - Multi-face detection (up to 50 faces per frame)
    - Confidence-based filtering for noisy conditions
    """

    def __init__(self):
        """Initialize MTCNN detector with cinema-optimized settings."""
        self.detector = MTCNN(
            min_face_size=config.MIN_FACE_SIZE,
            steps_threshold=[0.6, 0.7, config.DETECTION_CONFIDENCE]
        )
        self.frame_count = 0

    def detect_faces(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect all faces in the current frame.

        Args:
            frame: BGR image from OpenCV (numpy array)

        Returns:
            List of face dictionaries with keys:
                - 'box': [x, y, width, height]
                - 'confidence': detection confidence score
                - 'keypoints': facial landmarks (eyes, nose, mouth)
        """
        self.frame_count += 1

        # Convert BGR to RGB (MTCNN expects RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        detections = self.detector.detect_faces(rgb_frame)

        # Filter low-confidence detections
        filtered_detections = [
            face for face in detections
            if face['confidence'] >= config.DETECTION_CONFIDENCE
        ]

        # Limit to max faces (performance optimization)
        if len(filtered_detections) > config.MAX_FACES_PER_FRAME:
            # Sort by confidence and take top N
            filtered_detections = sorted(
                filtered_detections,
                key=lambda x: x['confidence'],
                reverse=True
            )[:config.MAX_FACES_PER_FRAME]

        return filtered_detections

    def extract_face_regions(
        self,
        frame: np.ndarray,
        detections: List[Dict]
    ) -> List[np.ndarray]:
        """
        Extract individual face regions from frame for emotion analysis.

        Args:
            frame: Full video frame
            detections: List of face detections from detect_faces()

        Returns:
            List of cropped face images (BGR format)
        """
        face_regions = []
        height, width = frame.shape[:2]

        for detection in detections:
            x, y, w, h = detection['box']

            # Add padding around face (10% on each side)
            padding = int(min(w, h) * 0.1)
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(width, x + w + padding)
            y2 = min(height, y + h + padding)

            # Extract face region
            face_roi = frame[y1:y2, x1:x2]

            # Ensure face region is valid
            if face_roi.size > 0:
                face_regions.append(face_roi)

        return face_regions

    def visualize_detections(
        self,
        frame: np.ndarray,
        detections: List[Dict]
    ) -> np.ndarray:
        """
        Draw bounding boxes on frame for debugging/demo purposes.

        Args:
            frame: Original video frame
            detections: List of face detections

        Returns:
            Frame with bounding boxes drawn
        """
        annotated_frame = frame.copy()

        for detection in detections:
            x, y, w, h = detection['box']
            confidence = detection['confidence']

            # Draw bounding box (green)
            cv2.rectangle(
                annotated_frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # Draw confidence score
            label = f"{confidence:.2f}"
            cv2.putText(
                annotated_frame,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

            # Draw keypoints (facial landmarks)
            keypoints = detection['keypoints']
            for key, point in keypoints.items():
                cv2.circle(
                    annotated_frame,
                    point,
                    2,
                    (0, 0, 255),
                    -1
                )

        # Add frame info
        info_text = f"Faces: {len(detections)} | Frame: {self.frame_count}"
        cv2.putText(
            annotated_frame,
            info_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        return annotated_frame


if __name__ == "__main__":
    # Quick test with webcam
    print("Testing Face Detector...")
    detector = CinemaFaceDetector()
    cap = cv2.VideoCapture(0)

    print("Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detector.detect_faces(frame)
        annotated = detector.visualize_detections(frame, detections)

        cv2.imshow('Face Detection Test', annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Processed {detector.frame_count} frames")
