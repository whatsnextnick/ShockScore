"""
Shock Score Demo Script

Demonstrates the full FER pipeline with webcam or sample video.
Perfect for showcasing to B2B clients (Hollywood studios).
"""

import cv2
import numpy as np
import json
from datetime import datetime

# Import Shock Score modules
from shock_score_engine import ShockScoreEngine
import config


def print_welcome_banner():
    """Display welcome banner."""
    banner = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║                   SHOCK SCORE DEMO                         ║
    ║        Real-Time Facial Emotion Recognition Engine        ║
    ║                                                            ║
    ║        Powered by: OpenCV + DeepFace + Custom AI          ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝

    Cinema-Optimized Horror Film Analytics

    This demo showcases the Shock Score engine processing live video
    to detect fear, surprise, and other emotions in real-time.

    """
    print(banner)


def print_instructions():
    """Display usage instructions."""
    instructions = """
    DEMO MODES:
    -----------
    1. Webcam Demo (Real-time Processing)
       - Uses your webcam to demonstrate emotion detection
       - Shows live Shock Score calculation
       - Best for testing the system

    2. Video File Demo (Full Analysis)
       - Process a pre-recorded video
       - Generates comprehensive Shock Score report
       - Simulates cinema screening analysis

    CONTROLS:
    ---------
    - Press 'Q' to quit at any time
    - Press 'S' to take a screenshot (saves current frame)
    - Press 'P' to pause/resume processing

    """
    print(instructions)


def run_webcam_demo():
    """Run interactive webcam demo."""
    print("\n" + "="*60)
    print("STARTING WEBCAM DEMO")
    print("="*60)
    print("\nInitializing camera...")

    # Check if camera is available
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Cannot access webcam")
        print("Please ensure your camera is connected and not in use")
        return

    cap.release()

    print("Camera ready!")
    print("\nTIP: For best results:")
    print("  - Face the camera directly")
    print("  - Ensure good lighting")
    print("  - Try different expressions (surprise, fear, neutral)")
    print("\nStarting demo in 3 seconds...\n")

    import time
    time.sleep(3)

    # Initialize engine
    engine = ShockScoreEngine(realtime_display=True)

    # Process webcam (will run until user presses 'q')
    try:
        engine.process_video(
            video_source=0,
            output_file=f"demo_webcam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
    except Exception as e:
        print(f"\nDemo error: {e}")


def run_video_demo(video_path: str = None):
    """
    Run demo with video file.

    Args:
        video_path: Path to video file (if None, prompts user)
    """
    if video_path is None:
        video_path = input("\nEnter path to video file: ").strip()

    print("\n" + "="*60)
    print("STARTING VIDEO FILE DEMO")
    print("="*60)
    print(f"\nVideo: {video_path}")

    # Initialize engine
    engine = ShockScoreEngine(realtime_display=True)

    # Process video
    output_file = f"demo_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    try:
        engine.process_video(
            video_source=video_path,
            output_file=output_file
        )

        print(f"\nDemo complete! Report saved to: {output_file}")

        # Display report summary
        display_report_summary(output_file)

    except Exception as e:
        print(f"\nDemo error: {e}")


def display_report_summary(report_path: str):
    """
    Display formatted summary of Shock Score report.

    Args:
        report_path: Path to JSON report file
    """
    try:
        with open(report_path, 'r') as f:
            report = json.load(f)

        print("\n" + "="*60)
        print("SHOCK SCORE REPORT SUMMARY")
        print("="*60)

        metrics = report.get('overall_metrics', {})

        print(f"""
        Overall Performance:
        --------------------
        EPM Score: {metrics.get('epm_score', 0)}/10
        Average Shock Score: {metrics.get('average_shock_score', 0)}
        Peak Shock Score: {metrics.get('peak_shock_score', 0)}

        Audience Metrics:
        -----------------
        Total Scare Events: {metrics.get('total_scare_events', 0)}
        Average Audience Size: {metrics.get('average_audience_size', 0)} people
        Runtime: {metrics.get('total_runtime_seconds', 0):.1f} seconds

        Top 3 Scariest Moments:
        -----------------------
        """)

        for i, moment in enumerate(report.get('peak_moments', [])[:3], 1):
            print(f"        {i}. {moment['timestamp']} - Score: {moment['shock_score']}")

        print("\n" + "="*60)

    except Exception as e:
        print(f"Could not display report: {e}")


def generate_sample_video():
    """
    Generate a simple sample video for testing (if no video available).

    Creates a 10-second video with text simulating a horror film scene.
    """
    print("\nGenerating sample test video...")

    output_path = "sample_test_video.mp4"
    fps = 30
    duration = 10  # seconds
    width, height = 640, 480

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    scenes = [
        (0, 3, "Normal Scene", (255, 255, 255)),
        (3, 5, "BUILDING TENSION...", (200, 200, 0)),
        (5, 6, "*** JUMP SCARE! ***", (0, 0, 255)),
        (6, 10, "Relief / Resolution", (0, 255, 0))
    ]

    for frame_num in range(fps * duration):
        timestamp = frame_num / fps

        # Create black frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Determine current scene
        current_scene = None
        for start, end, text, color in scenes:
            if start <= timestamp < end:
                current_scene = (text, color)
                break

        if current_scene:
            text, color = current_scene

            # Add text
            cv2.putText(
                frame,
                text,
                (50, height // 2),
                cv2.FONT_HERSHEY_BOLD,
                1.5,
                color,
                3
            )

            # Add timestamp
            cv2.putText(
                frame,
                f"Time: {timestamp:.1f}s",
                (50, height - 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

        out.write(frame)

    out.release()
    print(f"Sample video created: {output_path}")
    return output_path


def main():
    """Main demo entry point."""
    print_welcome_banner()

    # Check for dependencies
    print("Checking dependencies...")
    try:
        import cv2
        import deepface
        import mtcnn
        print("✓ All dependencies installed\n")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nPlease install requirements:")
        print("  pip install -r requirements.txt\n")
        return

    print_instructions()

    # Demo mode selection
    while True:
        print("\nSELECT DEMO MODE:")
        print("  1. Webcam Demo (Real-time)")
        print("  2. Video File Demo")
        print("  3. Generate Sample Video (for testing)")
        print("  4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == '1':
            run_webcam_demo()
        elif choice == '2':
            run_video_demo()
        elif choice == '3':
            sample_path = generate_sample_video()
            print(f"\nSample video created: {sample_path}")
            use_it = input("Process this sample video now? (y/n): ").strip().lower()
            if use_it == 'y':
                run_video_demo(sample_path)
        elif choice == '4':
            print("\nThank you for using Shock Score!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
