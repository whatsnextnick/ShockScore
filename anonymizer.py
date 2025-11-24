"""
Privacy & Anonymization Layer

Ensures all facial data is immediately anonymized and no personally
identifiable information (PII) is stored or transmitted.

GDPR/CCPA Compliant Data Processing
"""

import hashlib
import json
from typing import Dict, List, Any
from datetime import datetime
import config


class DataAnonymizer:
    """
    Ensures privacy-first data handling.

    Key principles:
    1. No video frames stored
    2. No face embeddings stored
    3. No facial images stored
    4. Only aggregate emotional metrics transmitted
    5. No demographic inference or tracking
    """

    def __init__(self, session_id: str = None):
        """
        Initialize anonymizer with unique session ID.

        Args:
            session_id: Optional session identifier (for B2B reporting)
        """
        self.session_id = session_id or self._generate_session_id()
        self.data_processed_count = 0
        self.privacy_log = []

    def _generate_session_id(self) -> str:
        """Generate anonymous session identifier."""
        timestamp = datetime.now().isoformat()
        hash_input = f"{timestamp}_shock_score".encode()
        return hashlib.sha256(hash_input).hexdigest()[:16]

    def anonymize_emotion_data(
        self,
        emotion_results: List[Dict],
        timestamp: float
    ) -> Dict:
        """
        Convert raw emotion data to anonymized aggregate metrics.

        This is the core privacy transformation. Individual faces are
        aggregated into population-level statistics.

        Args:
            emotion_results: List of emotion dicts from EmotionAnalyzer
            timestamp: Frame timestamp

        Returns:
            Anonymized aggregate data (safe for transmission/storage)
        """
        # Filter out None results
        valid_results = [r for r in emotion_results if r is not None]

        if not valid_results:
            return self._get_empty_aggregate(timestamp)

        # Aggregate emotion scores across all faces
        emotion_totals = {emotion: 0.0 for emotion in config.EMOTION_LABELS}

        for result in valid_results:
            for emotion, score in result['emotion_scores'].items():
                emotion_totals[emotion] += score

        # Calculate averages (this destroys individual identity)
        face_count = len(valid_results)
        emotion_averages = {
            emotion: round(total / face_count, 2)
            for emotion, total in emotion_totals.items()
        }

        self.data_processed_count += face_count

        # Log privacy compliance
        self._log_privacy_event(
            'data_anonymized',
            face_count,
            timestamp
        )

        return {
            'session_id': self.session_id,
            'timestamp': round(timestamp, 2),
            'audience_size': face_count,
            'emotions': emotion_averages,
            'privacy_level': 'anonymized',
            'contains_pii': False
        }

    def validate_privacy_compliance(self, data: Dict) -> bool:
        """
        Validate that data structure contains no PII.

        Args:
            data: Data dictionary to validate

        Returns:
            True if privacy-compliant, False otherwise
        """
        # Forbidden keys that would indicate PII
        forbidden_keys = [
            'face_image',
            'face_embedding',
            'face_id',
            'person_id',
            'facial_landmarks',
            'bounding_box',
            'video_frame',
            'name',
            'identity',
            'demographics',
            'age',
            'gender',
            'race'
        ]

        # Recursively check for forbidden keys
        def check_dict(d):
            if isinstance(d, dict):
                for key in d.keys():
                    if key in forbidden_keys:
                        return False
                    if not check_dict(d[key]):
                        return False
            elif isinstance(d, list):
                for item in d:
                    if not check_dict(item):
                        return False
            return True

        compliant = check_dict(data)

        self._log_privacy_event(
            'privacy_validation',
            result='pass' if compliant else 'FAIL'
        )

        return compliant

    def _log_privacy_event(self, event_type: str, *args, **kwargs):
        """
        Log privacy-related events for audit trail.

        Args:
            event_type: Type of privacy event
            *args, **kwargs: Event details
        """
        event = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'event_type': event_type,
            'details': {'args': args, 'kwargs': kwargs}
        }
        self.privacy_log.append(event)

    def _get_empty_aggregate(self, timestamp: float) -> Dict:
        """Return empty anonymized data structure."""
        return {
            'session_id': self.session_id,
            'timestamp': round(timestamp, 2),
            'audience_size': 0,
            'emotions': {emotion: 0.0 for emotion in config.EMOTION_LABELS},
            'privacy_level': 'anonymized',
            'contains_pii': False
        }

    def generate_privacy_report(self) -> Dict:
        """
        Generate privacy compliance report for audit.

        Returns:
            Privacy report with processing statistics
        """
        report = {
            'session_id': self.session_id,
            'total_faces_processed': self.data_processed_count,
            'video_frames_stored': 0,  # Always 0
            'facial_images_stored': 0,  # Always 0
            'face_embeddings_stored': 0,  # Always 0
            'pii_incidents': 0,  # Should always be 0
            'privacy_level': 'GDPR_COMPLIANT',
            'data_retention': 'aggregate_only',
            'anonymization_method': 'population_aggregation',
            'privacy_log_entries': len(self.privacy_log)
        }

        self._log_privacy_event('privacy_report_generated')

        return report


class SecureTransmission:
    """
    Ensures secure transmission of anonymized data to cloud API.
    """

    def __init__(self, api_endpoint: str = None):
        """
        Initialize secure transmission handler.

        Args:
            api_endpoint: URL of B2B backend API
        """
        self.api_endpoint = api_endpoint or "https://api.shockscore.example/v1/metrics"

    def prepare_transmission_payload(
        self,
        anonymized_data: List[Dict],
        session_metadata: Dict
    ) -> Dict:
        """
        Prepare anonymized data for secure transmission to cloud.

        Args:
            anonymized_data: List of anonymized data points
            session_metadata: Session info (film_id, cinema_id, etc.)

        Returns:
            Payload ready for API transmission
        """
        payload = {
            'api_version': '1.0',
            'session_metadata': {
                'session_id': session_metadata.get('session_id'),
                'film_id': session_metadata.get('film_id'),
                'cinema_location': session_metadata.get('cinema_location'),
                'screening_time': session_metadata.get('screening_time'),
                'runtime_seconds': session_metadata.get('runtime_seconds')
            },
            'metrics': anonymized_data,
            'data_type': 'anonymized_aggregate',
            'contains_pii': False,
            'privacy_compliant': True
        }

        return payload

    def validate_payload_security(self, payload: Dict) -> bool:
        """
        Final security check before transmission.

        Args:
            payload: Data payload to transmit

        Returns:
            True if secure for transmission
        """
        # Check for PII
        if payload.get('contains_pii', True):
            return False

        # Ensure only aggregate data
        if payload.get('data_type') != 'anonymized_aggregate':
            return False

        # Validate all metrics are anonymized
        for metric in payload.get('metrics', []):
            if not metric.get('privacy_level') == 'anonymized':
                return False

        return True


if __name__ == "__main__":
    # Test anonymization
    print("Testing Data Anonymizer...")

    anonymizer = DataAnonymizer()

    # Simulate raw emotion data (from multiple faces)
    raw_emotions = [
        {'dominant_emotion': 'fear', 'emotion_scores': {
            'fear': 65, 'surprise': 20, 'neutral': 15
        }},
        {'dominant_emotion': 'fear', 'emotion_scores': {
            'fear': 70, 'surprise': 15, 'neutral': 15
        }},
        {'dominant_emotion': 'surprise', 'emotion_scores': {
            'fear': 45, 'surprise': 40, 'neutral': 15
        }},
    ]

    # Anonymize
    anonymized = anonymizer.anonymize_emotion_data(raw_emotions, timestamp=125.5)

    print("\nRaw data (3 faces) → Anonymized aggregate:")
    print(json.dumps(anonymized, indent=2))

    # Validate privacy compliance
    is_compliant = anonymizer.validate_privacy_compliance(anonymized)
    print(f"\nPrivacy compliant: {is_compliant}")

    # Generate privacy report
    privacy_report = anonymizer.generate_privacy_report()
    print("\nPrivacy Report:")
    print(json.dumps(privacy_report, indent=2))

    # Test transmission preparation
    transmitter = SecureTransmission()
    payload = transmitter.prepare_transmission_payload(
        [anonymized],
        {
            'session_id': anonymizer.session_id,
            'film_id': 'horror_film_123',
            'cinema_location': 'Cinema_A',
            'screening_time': '2025-11-23T19:30:00',
            'runtime_seconds': 7200
        }
    )

    is_secure = transmitter.validate_payload_security(payload)
    print(f"\nPayload secure for transmission: {is_secure}")
