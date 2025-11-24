"""
Shock Score & EPM (Emotional Performance Metric) Calculator

Proprietary algorithm for quantifying horror/thriller film effectiveness
based on real-time audience emotional responses.
"""

import numpy as np
from typing import List, Dict, Tuple
from collections import deque
import config


class ShockScoreCalculator:
    """
    Calculates the proprietary Shock Score metric for horror films.

    The Shock Score combines:
    - Fear intensity (primary metric)
    - Surprise spikes (jump scares)
    - Sustained tension (fear duration)
    - Tension release patterns (relief indicators)
    """

    def __init__(self):
        """Initialize calculator with baseline calibration."""
        self.baseline_fear = 0.0
        self.baseline_surprise = 0.0
        self.baseline_established = False
        self.calibration_data = []

        # Rolling window for EPM calculation
        self.epm_window = deque(maxlen=config.EPM_WINDOW_SECONDS * 10)  # Assumes ~10 samples/sec

    def calibrate_baseline(self, emotion_data: List[Dict]):
        """
        Establish baseline emotional state from opening scenes.

        Args:
            emotion_data: List of aggregate emotion dictionaries
        """
        if len(emotion_data) < 5:
            # Need at least 5 samples for meaningful baseline
            return

        fear_values = [d['emotions'].get('fear', 0) for d in emotion_data]
        surprise_values = [d['emotions'].get('surprise', 0) for d in emotion_data]

        self.baseline_fear = np.mean(fear_values)
        self.baseline_surprise = np.mean(surprise_values)
        self.baseline_established = True

    def calculate_shock_score(self, emotion_aggregate: Dict) -> float:
        """
        Calculate instantaneous Shock Score for current moment.

        Formula:
        Shock Score = (Fear_Delta * 2.0) + (Surprise_Delta * 1.5) + Tension_Factor

        Args:
            emotion_aggregate: Current aggregate emotion scores

        Returns:
            Shock Score (0-100 scale)
        """
        emotions = emotion_aggregate.get('emotions', {})

        current_fear = emotions.get('fear', 0)
        current_surprise = emotions.get('surprise', 0)
        current_disgust = emotions.get('disgust', 0)

        # Calculate deltas from baseline
        if self.baseline_established:
            fear_delta = max(0, current_fear - self.baseline_fear)
            surprise_delta = max(0, current_surprise - self.baseline_surprise)
        else:
            # No baseline yet - use absolute values
            fear_delta = current_fear
            surprise_delta = current_surprise

        # Tension factor (combination of fear and disgust)
        tension_factor = (current_fear + current_disgust) / 2

        # Calculate weighted shock score
        shock_score = (
            fear_delta * config.FEAR_WEIGHT +
            surprise_delta * config.SURPRISE_WEIGHT +
            tension_factor * 0.5
        )

        # Normalize to 0-100 scale
        normalized = min(100, shock_score)

        return round(normalized, 2)

    def detect_scare_event(
        self,
        shock_history: List[float],
        threshold: float = 30.0
    ) -> bool:
        """
        Detect if a "scare event" (jump scare) just occurred.

        A scare event is characterized by a rapid spike in Shock Score.

        Args:
            shock_history: Recent Shock Score values (last 2-3 seconds)
            threshold: Minimum score increase to qualify as scare

        Returns:
            True if scare detected
        """
        if len(shock_history) < 3:
            return False

        # Check for sudden increase
        recent_avg = np.mean(shock_history[-5:-2]) if len(shock_history) >= 5 else shock_history[0]
        current = shock_history[-1]

        spike = current - recent_avg

        return spike >= threshold

    def calculate_epm(self, shock_scores: List[float]) -> float:
        """
        Calculate EPM (Emotional Performance Metric) over a time window.

        EPM is the proprietary B2B metric shown in Shock Score reports.
        It represents sustained emotional engagement, not just peaks.

        Formula:
        EPM = (Average_Shock_Score * Peak_Factor * Consistency_Factor) / 10

        Args:
            shock_scores: List of Shock Score values over time window

        Returns:
            EPM score (0-10 scale, where 10 is exceptional horror performance)
        """
        if not shock_scores:
            return 0.0

        # Average shock intensity
        avg_shock = np.mean(shock_scores)

        # Peak factor (how high did it get?)
        max_shock = np.max(shock_scores)
        peak_factor = max_shock / 100  # Normalize to 0-1

        # Consistency factor (sustained tension vs. sporadic scares)
        if len(shock_scores) > 1:
            std_dev = np.std(shock_scores)
            consistency = 1.0 - min(1.0, std_dev / 50)  # Lower variance = better
        else:
            consistency = 1.0

        # Calculate EPM
        epm = (avg_shock * peak_factor * consistency) / 10

        return round(min(10.0, epm), 2)


class ShockScoreReport:
    """
    Generates comprehensive Shock Score analytics report for film studios.
    """

    def __init__(self):
        """Initialize report generator."""
        self.timeline_data = []
        self.scare_events = []
        self.calculator = ShockScoreCalculator()

    def add_timestamp_data(
        self,
        timestamp: float,
        shock_score: float,
        emotion_aggregate: Dict,
        is_scare_event: bool = False
    ):
        """
        Record data for a single timestamp.

        Args:
            timestamp: Time in seconds from film start
            shock_score: Calculated Shock Score
            emotion_aggregate: Full emotion breakdown
            is_scare_event: Whether this was a detected scare
        """
        data_point = {
            'timestamp': timestamp,
            'shock_score': shock_score,
            'emotions': emotion_aggregate['emotions'],
            'sample_size': emotion_aggregate.get('sample_size', 0)
        }

        self.timeline_data.append(data_point)

        if is_scare_event:
            self.scare_events.append({
                'timestamp': timestamp,
                'shock_score': shock_score,
                'type': 'jump_scare'
            })

    def generate_report(self) -> Dict:
        """
        Generate comprehensive analytics report.

        Returns:
            Report dictionary with all metrics and recommendations
        """
        if not self.timeline_data:
            return self._get_empty_report()

        # Extract shock scores
        shock_scores = [d['shock_score'] for d in self.timeline_data]

        # Calculate overall metrics
        avg_shock = np.mean(shock_scores)
        max_shock = np.max(shock_scores)
        overall_epm = self.calculator.calculate_epm(shock_scores)

        # Identify peak moments (top 5 scariest moments)
        sorted_moments = sorted(
            self.timeline_data,
            key=lambda x: x['shock_score'],
            reverse=True
        )[:5]

        # Identify weak moments (potential missed opportunities)
        weak_moments = sorted(
            self.timeline_data,
            key=lambda x: x['shock_score']
        )[:5]

        # Tension analysis
        tension_periods = self._analyze_tension_patterns(shock_scores)

        report = {
            'overall_metrics': {
                'total_runtime_seconds': self.timeline_data[-1]['timestamp'],
                'average_shock_score': round(avg_shock, 2),
                'peak_shock_score': round(max_shock, 2),
                'epm_score': overall_epm,
                'total_scare_events': len(self.scare_events),
                'average_audience_size': int(np.mean([
                    d['sample_size'] for d in self.timeline_data
                ]))
            },
            'peak_moments': [
                {
                    'timestamp': self._format_timestamp(m['timestamp']),
                    'shock_score': m['shock_score'],
                    'dominant_emotion': max(
                        m['emotions'].items(),
                        key=lambda x: x[1]
                    )[0]
                }
                for m in sorted_moments
            ],
            'scare_events': [
                {
                    'timestamp': self._format_timestamp(s['timestamp']),
                    'intensity': s['shock_score']
                }
                for s in self.scare_events
            ],
            'missed_opportunities': [
                {
                    'timestamp': self._format_timestamp(m['timestamp']),
                    'shock_score': m['shock_score'],
                    'recommendation': 'Consider enhancing tension in this segment'
                }
                for m in weak_moments
                if m['shock_score'] < 10
            ],
            'tension_analysis': tension_periods,
            'timeline_data': self.timeline_data
        }

        return report

    def _analyze_tension_patterns(self, shock_scores: List[float]) -> Dict:
        """
        Analyze sustained tension periods vs. isolated scares.

        Args:
            shock_scores: Full timeline of Shock Scores

        Returns:
            Tension pattern analysis
        """
        # Find sustained high-tension periods (shock > 20 for 30+ seconds)
        tension_threshold = 20
        sustained_periods = []

        current_period_start = None
        for i, score in enumerate(shock_scores):
            if score > tension_threshold:
                if current_period_start is None:
                    current_period_start = i
            else:
                if current_period_start is not None:
                    period_length = i - current_period_start
                    if period_length >= 30:  # At least 30 samples (~30 seconds)
                        sustained_periods.append({
                            'start_index': current_period_start,
                            'duration_samples': period_length
                        })
                    current_period_start = None

        return {
            'sustained_tension_periods': len(sustained_periods),
            'average_tension_duration': np.mean([
                p['duration_samples'] for p in sustained_periods
            ]) if sustained_periods else 0
        }

    def _format_timestamp(self, seconds: float) -> str:
        """Convert seconds to MM:SS format."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def _get_empty_report(self) -> Dict:
        """Return empty report structure."""
        return {
            'overall_metrics': {},
            'peak_moments': [],
            'scare_events': [],
            'missed_opportunities': [],
            'tension_analysis': {},
            'timeline_data': []
        }


if __name__ == "__main__":
    # Test the calculator
    print("Testing Shock Score Calculator...")

    calculator = ShockScoreCalculator()

    # Simulate emotion data
    test_emotions = [
        {'emotions': {'fear': 15, 'surprise': 10, 'neutral': 75}},
        {'emotions': {'fear': 20, 'surprise': 15, 'neutral': 65}},
        {'emotions': {'fear': 65, 'surprise': 20, 'neutral': 15}},  # Scare!
        {'emotions': {'fear': 40, 'surprise': 10, 'neutral': 50}},
        {'emotions': {'fear': 25, 'surprise': 5, 'neutral': 70}},
    ]

    # Calibrate baseline
    calculator.calibrate_baseline(test_emotions[:2])
    print(f"Baseline Fear: {calculator.baseline_fear}")
    print(f"Baseline Surprise: {calculator.baseline_surprise}")

    # Calculate shock scores
    shock_scores = []
    for i, emotions in enumerate(test_emotions):
        shock = calculator.calculate_shock_score(emotions)
        shock_scores.append(shock)
        print(f"Frame {i}: Shock Score = {shock}")

    # Detect scare
    is_scare = calculator.detect_scare_event(shock_scores)
    print(f"\nScare detected: {is_scare}")

    # Calculate EPM
    epm = calculator.calculate_epm(shock_scores)
    print(f"EPM Score: {epm}/10")
