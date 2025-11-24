"""
Quick Installation Test Script

Verifies that all Shock Score components are properly installed
and configured. Run this after installation to ensure everything works.
"""

import sys


def test_imports():
    """Test that all required packages can be imported."""
    print("Testing package imports...")
    tests = {
        'OpenCV': 'cv2',
        'NumPy': 'numpy',
        'DeepFace': 'deepface',
        'TensorFlow': 'tensorflow',
        'MTCNN': 'mtcnn',
        'Flask': 'flask',
        'Pandas': 'pandas',
        'Pillow': 'PIL'
    }

    failed = []
    for name, module in tests.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError as e:
            print(f"  ✗ {name} - {e}")
            failed.append(name)

    return len(failed) == 0, failed


def test_custom_modules():
    """Test that all Shock Score modules can be imported."""
    print("\nTesting Shock Score modules...")
    modules = [
        'config',
        'face_detector',
        'emotion_analyzer',
        'shock_score_calculator',
        'anonymizer',
        'shock_score_engine'
    ]

    failed = []
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}.py")
        except Exception as e:
            print(f"  ✗ {module}.py - {e}")
            failed.append(module)

    return len(failed) == 0, failed


def test_camera():
    """Test camera access."""
    print("\nTesting camera access...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)

        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()

            if ret and frame is not None:
                print(f"  ✓ Camera accessible (frame size: {frame.shape})")
                return True
            else:
                print("  ⚠ Camera opened but cannot read frames")
                return False
        else:
            print("  ✗ Cannot open camera (index 0)")
            print("    Try a different camera index or check permissions")
            return False

    except Exception as e:
        print(f"  ✗ Camera test failed - {e}")
        return False


def test_gpu():
    """Test GPU availability."""
    print("\nTesting GPU acceleration...")
    try:
        import tensorflow as tf

        gpus = tf.config.list_physical_devices('GPU')

        if gpus:
            print(f"  ✓ GPU detected: {len(gpus)} device(s)")
            for gpu in gpus:
                print(f"    - {gpu.name}")
            return True
        else:
            print("  ⚠ No GPU detected (CPU mode will be used)")
            print("    For faster processing, install CUDA and cuDNN")
            return False

    except Exception as e:
        print(f"  ⚠ GPU test failed - {e}")
        return False


def test_model_download():
    """Test DeepFace model availability."""
    print("\nTesting DeepFace model...")
    try:
        from deepface import DeepFace
        import numpy as np

        # Create dummy image
        dummy_img = np.zeros((48, 48, 3), dtype=np.uint8)

        print("  Attempting model load (this may take a minute on first run)...")

        # This will download the model if not present
        result = DeepFace.analyze(
            dummy_img,
            actions=['emotion'],
            detector_backend='skip',
            enforce_detection=False,
            silent=True
        )

        print("  ✓ Emotion recognition model loaded successfully")
        return True

    except Exception as e:
        print(f"  ✗ Model test failed - {e}")
        print("    Try manually downloading: python -c \"from deepface import DeepFace; DeepFace.build_model('Emotion')\"")
        return False


def test_face_detection():
    """Test face detection with MTCNN."""
    print("\nTesting face detection (MTCNN)...")
    try:
        from mtcnn import MTCNN
        import numpy as np
        import cv2

        detector = MTCNN()

        # Create simple test image with a face-like region
        test_img = np.zeros((200, 200, 3), dtype=np.uint8)

        # Draw a simple face-like pattern
        cv2.circle(test_img, (100, 100), 50, (255, 255, 255), -1)  # Face
        cv2.circle(test_img, (85, 90), 5, (0, 0, 0), -1)  # Left eye
        cv2.circle(test_img, (115, 90), 5, (0, 0, 0), -1)  # Right eye

        detections = detector.detect_faces(test_img)

        print(f"  ✓ Face detector initialized")
        return True

    except Exception as e:
        print(f"  ✗ Face detection test failed - {e}")
        return False


def print_summary(results):
    """Print test summary."""
    print("\n" + "="*60)
    print("INSTALLATION TEST SUMMARY")
    print("="*60)

    all_passed = all(results.values())

    if all_passed:
        print("\n✓ All tests passed! Shock Score is ready to use.")
        print("\nNext steps:")
        print("  1. Run demo: python demo.py")
        print("  2. Test webcam: python shock_score_engine.py --input 0")
        print("  3. Read documentation: README.md")
    else:
        print("\n⚠ Some tests failed. Please review the output above.")
        print("\nFailed tests:")
        for test_name, passed in results.items():
            if not passed:
                print(f"  - {test_name}")

        print("\nRefer to INSTALLATION.md for troubleshooting steps.")

    print("\n" + "="*60)

    return all_passed


def main():
    """Run all tests."""
    print("="*60)
    print("SHOCK SCORE - INSTALLATION TEST")
    print("="*60)
    print("\nThis script will verify your installation.\n")

    results = {}

    # Run tests
    results['Package Imports'], failed_imports = test_imports()
    results['Custom Modules'], failed_modules = test_custom_modules()
    results['Camera Access'] = test_camera()
    results['GPU Acceleration'] = test_gpu()  # Warning only, not critical
    results['Face Detection'] = test_face_detection()
    results['Emotion Model'] = test_model_download()

    # Print summary
    all_passed = print_summary(results)

    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
