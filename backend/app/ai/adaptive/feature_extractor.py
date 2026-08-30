import numpy as np
from typing import List, Dict, Any

class AdaptiveFeatureExtractor:
    """
    Data Preprocessing & Feature Extraction for Cognitive Performance.
    Extracts statistical features from raw game attempt history.
    """
    @staticmethod
    def extract_features(attempts: List[Dict[str, Any]], window_size: int = 5) -> Dict[str, float]:
        """
        Extracts performance features from the latest N attempts.
        Returns:
            Dictionary containing statistical features for decision engine.
        """
        if not attempts:
            return {
                "rolling_accuracy": 50.0,
                "average_response_time_ms": 5000.0,
                "mistake_rate": 0.0,
                "performance_streak": 0,
                "trend_slope": 0.0,
                "recent_attempts_count": 0,
                "latency_std_dev": 0.0
            }

        # Take latest window_size attempts
        recent = attempts[-window_size:]
        accuracies = [float(a.get("accuracy", (a.get("correct_answers", 0) / max(1, a.get("total_questions", 1))) * 100)) for a in recent]
        latencies = [float(a.get("response_time_ms", 5000)) for a in recent]
        mistakes = [float(a.get("mistakes", 0)) for a in recent]
        total_q = [float(a.get("total_questions", 1)) for a in recent]

        rolling_acc = float(np.mean(accuracies))
        avg_lat = float(np.mean(latencies))
        lat_std = float(np.std(latencies)) if len(latencies) > 1 else 0.0
        
        total_mistakes = sum(mistakes)
        total_questions = sum(total_q)
        mistake_rate = float(total_mistakes / max(1.0, total_questions))

        # Calculate streak (positive streak = consecutive high scores >= 80%, negative = consecutive low scores < 50%)
        streak = 0
        for a in reversed(recent):
            acc = float(a.get("accuracy", 0))
            if acc >= 80.0:
                if streak >= 0:
                    streak += 1
                else:
                    break
            elif acc < 50.0:
                if streak <= 0:
                    streak -= 1
                else:
                    break
            else:
                break

        # Calculate linear trend slope over time (rate of improvement or decline)
        if len(accuracies) >= 2:
            x = np.arange(len(accuracies))
            y = np.array(accuracies)
            # Linear fit: y = slope * x + intercept
            slope, _ = np.polyfit(x, y, 1)
            trend_slope = float(slope)
        else:
            trend_slope = 0.0

        return {
            "rolling_accuracy": round(rolling_acc, 2),
            "average_response_time_ms": round(avg_lat, 2),
            "mistake_rate": round(mistake_rate, 3),
            "performance_streak": streak,
            "trend_slope": round(trend_slope, 2),
            "recent_attempts_count": len(recent),
            "latency_std_dev": round(lat_std, 2)
        }
