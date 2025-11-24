"""
Shock Score Engine - Main Processing Pipeline

Integrates all components for real-time facial emotion recognition
and Shock Score calculation in cinema environments.
"""

import cv2
import numpy as np
import argparse
import json
import time
from datetime import datetime
from typing import Optional, Dict

# Import custom modules
import config
from face_detector import CinemaFaceDetector
from emotion_analyzer import EmotionAnalyzer, EmotionAggregator
from shock_score_calculator import ShockScoreCalculator, ShockScoreReport
from anonymizer import DataAnonymizer


class ShockScoreEngine:
    """
    Main processing engine that orchestrates the entire FER pipeline.

    Pipeline:
    Video Input → Face Detection → Emotion Analysis → Anonymization →
    Shock Score Calculation → Aggregation → Report Generation
    """

    def __init__(self, realtime_display: bool = True):
        """
        Initialize all processing components.

        Args:
            realtime_display: Whether to show live visualization
        """
        print("Initializing Shock Score Engine...")

        # Initialize components
        self.face_detector = CinemaFaceDetector()
        self.emotion_analyzer = EmotionAnalyzer()
        self.emotion_aggregator = EmotionAggregator()
        self.shock_calculator = ShockScoreCalculator()
        self.report_generator = ShockScoreReport()
        self.anonymizer = DataAnonymizer()

        # Processing state
        self.frame_count = 0
        self.processed_count = 0
        self.shock_history = []
        self.realtime_display = realtime_display
        self.start_time = None

        # Performance metrics
        self.fps_history = []

        print("Engine initialized successfully")

    def process_video(
        self,
        video_source: str = 0,
        output_file: str = "shock_score_report.json"
    ):
        """
        Process video stream and generate Shock Score report.

        Args:
            video_source: Path to video file or camera index (0 for webcam)
            output_file: Path to save JSON report
        """
        print(f"\nStarting video processing...")
        print(f"Source: {video_source}")
        print(f"Output: {output_file}")

        # Open video capture
        cap = cv2.VideoCapture(video_source)

        if not cap.isOpened():
            raise ValueError(f"Cannot open video source: {video_source}")

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"Video FPS: {fps}")
        print(f"Total frames: {total_frames}")
        print("\nProcessing... Press 'q' to quit\n")

        self.start_time = time.time()

        try:
            while True:
                ret, frame = cap.read()

                if not ret:
                    print("\nEnd of video reached")
                    break

                self.frame_count += 1

                # Process frame (with frame skipping for performance)
                if self.frame_count % config.FRAME_SKIP == 0:
                    timestamp = self.frame_count / fps
                    annotated_frame = self._process_frame(frame, timestamp)

                    # Display if enabled
                    if self.realtime_display and annotated_frame is not None:
                        cv2.imshow('Shock Score Engine', annotated_frame)

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            print("\nProcessing interrupted by user")
                            break

                # Progress indicator
                if self.frame_count % 100 == 0:
                    self._print_progress(fps, total_frames)

        finally:
            # Cleanup
            cap.release()
            if self.realtime_display:
                cv2.destroyAllWindows()

        # Generate final report
        self._finalize_and_save_report(output_file)

    def _process_frame(self, frame: np.ndarray, timestamp: float) -> Optional[np.ndarray]:
        """
        Process a single video frame through the FER pipeline.

        Args:
            frame: Video frame (BGR format)
            timestamp: Frame timestamp in seconds

        Returns:
            Annotated frame for display (or None if display disabled)
        """
        frame_start_time = time.time()

        # Step 1: Detect faces
        detections = self.face_detector.detect_faces(frame)
        face_regions = self.face_detector.extract_face_regions(frame, detections)

        # Step 2: Analyze emotions
        emotion_results = self.emotion_analyzer.analyze_batch(face_regions)

        # Step 3: Anonymize (aggregate across all faces)
        anonymized_data = self.anonymizer.anonymize_emotion_data(
            emotion_results,
            timestamp
        )

        # Step 4: Calculate aggregate emotions
        self.emotion_aggregator.add_frame_emotions(emotion_results, timestamp)
        emotion_aggregate = self.emotion_aggregator.get_aggregate_emotions()

        # Step 5: Calculate Shock Score
        if self.processed_count < 30:  # Calibration phase
            calibration_data = []
            for result in emotion_results:
                if result:
                    calibration_data.append({'emotions': result['emotion_scores']})
            self.shock_calculator.calibrate_baseline(calibration_data)

        shock_score = self.shock_calculator.calculate_shock_score(emotion_aggregate)
        self.shock_history.append(shock_score)

        # Step 6: Detect scare events
        is_scare = False
        if len(self.shock_history) >= 5:
            is_scare = self.shock_calculator.detect_scare_event(
                self.shock_history[-10:]
            )

        # Step 7: Add to report
        self.report_generator.add_timestamp_data(
            timestamp,
            shock_score,
            emotion_aggregate,
            is_scare
        )

        self.processed_count += 1

        # Calculate FPS
        frame_time = time.time() - frame_start_time
        current_fps = 1.0 / frame_time if frame_time > 0 else 0
        self.fps_history.append(current_fps)

        # Visualize (if enabled)
        if self.realtime_display:
            annotated = self._create_visualization(
                frame,
                detections,
                emotion_aggregate,
                shock_score,
                is_scare,
                current_fps
            )
            return annotated

        return None

    def _create_visualization(
        self,
        frame: np.ndarray,
        detections: list,
        emotion_aggregate: Dict,
        shock_score: float,
        is_scare: bool,
        fps: float
    ) -> np.ndarray:
        """
        Create annotated frame with all metrics for display.

        Args:
            frame: Original video frame
            detections: Face detections
            emotion_aggregate: Aggregate emotion scores
            shock_score: Current Shock Score
            is_scare: Whether scare was detected
            fps: Current processing FPS

        Returns:
            Annotated frame
        """
        # Draw face detections
        vis_frame = self.face_detector.visualize_detections(frame, detections)

        # Create info panel
        panel_height = 200
        panel = np.zeros((panel_height, vis_frame.shape[1], 3), dtype=np.uint8)

        # Shock Score (large display)
        shock_text = f"SHOCK SCORE: {shock_score:.1f}"
        cv2.putText(
            panel,
            shock_text,
            (20, 50),
            cv2.FONT_HERSHEY_BOLD,
            1.2,
            (0, 0, 255) if is_scare else (255, 255, 255),
            3
        )

        # Scare indicator
        if is_scare:
            cv2.putText(
                panel,
                "*** SCARE DETECTED ***",
                (20, 90),
                cv2.FONT_HERSHEY_BOLD,
                0.8,
                (0, 0, 255),
                2
            )

        # Emotion breakdown
        emotions = emotion_aggregate.get('emotions', {})
        y_offset = 120
        for i, (emotion, score) in enumerate(sorted(
            emotions.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]):  # Top 3 emotions
            text = f"{emotion.upper()}: {score:.1f}%"
            cv2.putText(
                panel,
                text,
                (20, y_offset + i * 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1
            )

        # Performance metrics
        perf_text = f"FPS: {fps:.1f} | Faces: {len(detections)} | Frame: {self.frame_count}"
        cv2.putText(
            panel,
            perf_text,
            (vis_frame.shape[1] - 400, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1
        )

        # Combine frame and panel
        combined = np.vstack([vis_frame, panel])

        return combined

    def _print_progress(self, fps: float, total_frames: int):
        """Print processing progress."""
        if total_frames > 0:
            progress = (self.frame_count / total_frames) * 100
            avg_fps = np.mean(self.fps_history[-100:]) if self.fps_history else 0
            print(f"Progress: {progress:.1f}% | Processing FPS: {avg_fps:.1f}")

    def _finalize_and_save_report(self, output_file: str):
        """
        Generate final report and save to file.

        Args:
            output_file: Path to save JSON report
        """
        print("\nGenerating final report...")

        # Generate comprehensive report
        report = self.report_generator.generate_report()

        # Add processing metadata
        total_time = time.time() - self.start_time if self.start_time else 0
        avg_fps = np.mean(self.fps_history) if self.fps_history else 0

        report['processing_metadata'] = {
            'total_frames': self.frame_count,
            'processed_frames': self.processed_count,
            'processing_time_seconds': round(total_time, 2),
            'average_fps': round(avg_fps, 2),
            'session_id': self.anonymizer.session_id,
            'timestamp': datetime.now().isoformat()
        }

        # Add privacy report
        report['privacy_compliance'] = self.anonymizer.generate_privacy_report()

        # Save to file
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\nReport saved to: {output_file}")

        # Print summary
        self._print_summary(report)

    def _print_summary(self, report: Dict):
        """Print report summary to console."""
        print("\n" + "="*60)
        print("SHOCK SCORE ANALYSIS SUMMARY")
        print("="*60)

        metrics = report.get('overall_metrics', {})

        print(f"\nOverall EPM Score: {metrics.get('epm_score', 0)}/10")
        print(f"Average Shock Score: {metrics.get('average_shock_score', 0)}")
        print(f"Peak Shock Score: {metrics.get('peak_shock_score', 0)}")
        print(f"Total Scare Events: {metrics.get('total_scare_events', 0)}")
        print(f"Average Audience Size: {metrics.get('average_audience_size', 0)} people")

        print(f"\nTop 3 Scariest Moments:")
        for i, moment in enumerate(report.get('peak_moments', [])[:3], 1):
            print(f"  {i}. {moment['timestamp']} - Score: {moment['shock_score']}")

        print("\n" + "="*60)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Shock Score Engine - Real-Time Facial Emotion Recognition for Cinema'
    )
    parser.add_argument(
        '--input',
        type=str,
        default=0,
        help='Video file path or camera index (default: 0 for webcam)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='shock_score_report.json',
        help='Output JSON report path (default: shock_score_report.json)'
    )
    parser.add_argument(
        '--no-display',
        action='store_true',
        help='Disable real-time visualization (faster processing)'
    )

    args = parser.parse_args()

    # Convert camera index to int if it's a digit
    video_source = args.input
    if isinstance(video_source, str) and video_source.isdigit():
        video_source = int(video_source)

    # Initialize and run engine
    engine = ShockScoreEngine(realtime_display=not args.no_display)

    try:
        engine.process_video(video_source, args.output)
    except KeyboardInterrupt:
        print("\n\nProcessing interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        raise


if __name__ == "__main__":
    main()
