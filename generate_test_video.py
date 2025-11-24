"""
Generate a sample test video for Shock Score testing.

Creates a 15-second video simulating different horror film scenes
with text overlays to demonstrate the Shock Score pipeline.
"""

import cv2
import numpy as np

print("Generating sample horror scene video...")

output_path = 'sample_horror_test.mp4'
fps = 30
duration = 15  # 15 seconds
width, height = 640, 480

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

if not out.isOpened():
    print("Error: Could not create video file")
    print("Trying alternative codec...")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_path = 'sample_horror_test.avi'
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

scenes = [
    (0, 3, 'CALM OPENING', (200, 200, 200)),
    (3, 6, 'Building Tension...', (150, 150, 0)),
    (6, 7, '!!! JUMP SCARE !!!', (0, 0, 255)),
    (7, 10, 'High Fear State', (255, 100, 0)),
    (10, 12, 'Relief Period', (0, 200, 0)),
    (12, 15, 'Final Tension', (100, 0, 100))
]

for frame_num in range(fps * duration):
    timestamp = frame_num / fps

    # Create black frame
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Determine current scene
    for start, end, text, color in scenes:
        if start <= timestamp < end:
            # Add flashing effect for jump scare
            if 'SCARE' in text:
                intensity = int(200 + 55 * np.sin(frame_num * 0.8))
                color = (0, 0, intensity)

            # Draw scene text
            cv2.putText(
                frame,
                text,
                (50, height//2),
                cv2.FONT_HERSHEY_SIMPLEX,  # Standard font
                1.2,
                color,
                3
            )

            # Draw timestamp
            time_text = f'Time: {timestamp:.1f}s'
            cv2.putText(
                frame,
                time_text,
                (50, height - 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            # Add emotion hint
            emotion_hints = {
                'CALM': 'Expected: Neutral/Happy',
                'Tension': 'Expected: Fear Rising',
                'SCARE': 'Expected: Fear + Surprise',
                'Fear': 'Expected: High Fear',
                'Relief': 'Expected: Happy/Neutral',
                'Final': 'Expected: Fear'
            }

            for key, hint in emotion_hints.items():
                if key in text:
                    cv2.putText(
                        frame,
                        hint,
                        (50, height - 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (100, 100, 100),
                        1
                    )
                    break

            break

    out.write(frame)

out.release()

print(f'\n✓ Successfully created: {output_path}')
print(f'  Duration: {duration} seconds')
print(f'  Frame rate: {fps} FPS')
print(f'  Resolution: {width}x{height}')
print(f'  Total frames: {fps * duration}')
print(f'\nNow process it with:')
print(f'  python shock_score_engine.py --input {output_path} --output results.json')
