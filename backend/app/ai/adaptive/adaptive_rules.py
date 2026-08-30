from typing import Dict, Any, Tuple
from app.schemas import AdaptiveAction

class HeuristicAdaptiveEngine:
    """
    Transparent Rule-Based Adaptive Difficulty Engine for Dementia Patients.
    Applies geriatric cognitive psychology guidelines:
    - High accuracy (>80%) + consistent response latency -> Increase challenge to stimulate neuroplasticity.
    - Low accuracy (<50%) or high mistake rate / distress latency -> Decrease difficulty to avoid frustration.
    - Balanced accuracy (50%-80%) -> Maintain difficulty to consolidate cognitive mastery.
    """
    @staticmethod
    def evaluate(
        current_difficulty: int,
        features: Dict[str, Any],
        min_level: int = 1,
        max_level: int = 5
    ) -> Tuple[AdaptiveAction, int, float, str]:
        """
        Evaluates extracted features and returns:
        (AdaptiveAction, recommended_difficulty, confidence_score, rationale)
        """
        curr = max(min_level, min(max_level, current_difficulty))
        acc = features.get("rolling_accuracy", 50.0)
        streak = features.get("performance_streak", 0)
        avg_lat = features.get("average_response_time_ms", 5000.0)
        trend = features.get("trend_slope", 0.0)
        attempts_count = features.get("recent_attempts_count", 0)

        # Base case: Very first session
        if attempts_count == 0:
            return AdaptiveAction.MAINTAIN, curr, 0.70, "Initial baseline session; maintaining default starting level."

        # Condition 1: High performance mastery
        if (acc >= 85.0 or (acc >= 75.0 and streak >= 2)) and curr < max_level:
            next_diff = curr + 1
            confidence = min(0.95, 0.75 + (streak * 0.05) + (0.1 if avg_lat < 4000 else 0.0))
            rationale = (
                f"Patient achieved high rolling accuracy of {acc}% (positive streak: {streak}) "
                f"with stable latency ({avg_lat}ms). Escalating difficulty from level {curr} to {next_diff} "
                f"to support cognitive stimulation."
            )
            return AdaptiveAction.INCREASE, next_diff, round(confidence, 2), rationale

        # Condition 2: Performance struggle / Cognitive fatigue
        elif (acc < 50.0 or streak <= -2 or (acc < 60.0 and trend < -5.0)) and curr > min_level:
            next_diff = curr - 1
            confidence = min(0.95, 0.70 + (abs(streak) * 0.06))
            rationale = (
                f"Patient encountered difficulty with rolling accuracy of {acc}% (negative streak: {streak}) "
                f"and declining trend ({trend}). Adjusting difficulty from level {curr} to {next_diff} "
                f"to prevent cognitive frustration and support memory reinforcement."
            )
            return AdaptiveAction.DECREASE, next_diff, round(confidence, 2), rationale

        # Condition 3: Consolidation zone / Balanced mastery
        else:
            confidence = 0.85
            if curr == max_level and acc >= 85.0:
                rationale = f"Patient is excelling at maximum difficulty level {max_level} with {acc}% accuracy. Maintaining peak mastery level."
            elif curr == min_level and acc < 50.0:
                rationale = f"Patient is at foundational level {min_level} with {acc}% accuracy. Maintaining level with focused repetition."
            else:
                rationale = (
                    f"Patient demonstrates stable performance with rolling accuracy of {acc}% "
                    f"and average latency {avg_lat}ms. Maintaining difficulty level {curr}."
                )
            return AdaptiveAction.MAINTAIN, curr, round(confidence, 2), rationale
