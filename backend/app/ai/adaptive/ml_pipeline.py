"""
Machine Learning Pipeline Architecture for SMRITHI Adaptive Difficulty.

This module provides the decoupled architectural scaffold for future ML classifiers
(e.g., Logistic Regression, Gradient Boosted Trees, or Deep Q-Networks for Cognitive State Estimation).

Architecture Components:
1. Data Preprocessing (Cleaning, normalizing, and structuring attempt records)
2. Feature Extraction (Extracting rolling statistics, z-score latencies, streak lengths)
3. Model Interface (Base class for ML/RL models)
4. Prediction & Decision Boundary (Translating model outputs to difficulty increments)
5. Evaluation (Offline validation and accuracy scoring against caregiver/clinical benchmarks)
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple
import numpy as np
from app.schemas import AdaptiveAction
from app.ai.adaptive.feature_extractor import AdaptiveFeatureExtractor

class BaseAdaptiveModel(ABC):
    """Abstract Base Class for Adaptive Cognitive Difficulty Models."""
    @abstractmethod
    def fit(self, X: np.ndarray, y: np.ndarray):
        """Train or calibrate the model on historical sessions."""
        pass

    @abstractmethod
    def predict(self, feature_vector: np.ndarray) -> Tuple[AdaptiveAction, float]:
        """Predict the optimal action and return confidence score."""
        pass


class StatisticalLinearAdaptiveModel(BaseAdaptiveModel):
    """
    Parametric Linear Evaluation Model utilizing normalized weighted scoring.
    Combines cognitive accuracy weight (0.60), latency speed index (0.25), and streak multiplier (0.15).
    """
    def __init__(self):
        # Default cognitive scoring weights
        self.w_acc = 0.60
        self.w_lat = 0.25
        self.w_streak = 0.15

    def fit(self, X: np.ndarray, y: np.ndarray):
        # Placeholder for supervised training against clinician-annotated difficulty transitions
        pass

    def predict(self, feature_vector: np.ndarray) -> Tuple[AdaptiveAction, float]:
        """
        Input feature vector: [accuracy (0-100), latency_ms, streak, trend_slope]
        """
        acc = float(feature_vector[0])
        lat = float(feature_vector[1])
        streak = float(feature_vector[2])

        # Normalized scores (0 to 1)
        norm_acc = min(1.0, max(0.0, acc / 100.0))
        norm_speed = min(1.0, max(0.0, 1.0 - (lat / 10000.0)))
        norm_streak = min(1.0, max(-1.0, streak / 3.0))

        composite_score = (self.w_acc * norm_acc) + (self.w_lat * norm_speed) + (self.w_streak * (norm_streak * 0.5 + 0.5))

        if composite_score >= 0.75:
            action = AdaptiveAction.INCREASE
            confidence = min(0.95, composite_score)
        elif composite_score <= 0.40:
            action = AdaptiveAction.DECREASE
            confidence = min(0.95, 1.0 - composite_score)
        else:
            action = AdaptiveAction.MAINTAIN
            confidence = 0.80

        return action, round(float(confidence), 2)


class AdaptivePipeline:
    """
    Full pipeline coordinating Preprocessing, Feature Extraction, Model Prediction, and Post-Evaluation.
    """
    def __init__(self, use_ml_model: bool = False):
        self.use_ml_model = use_ml_model
        self.ml_model = StatisticalLinearAdaptiveModel()
        self.feature_extractor = AdaptiveFeatureExtractor()

    def process(self, attempts: List[Dict[str, Any]], current_difficulty: int) -> Dict[str, Any]:
        # Step 1: Preprocessing & Feature Extraction
        features = self.feature_extractor.extract_features(attempts)

        # Step 2: Model Prediction
        if self.use_ml_model:
            vector = np.array([
                features["rolling_accuracy"],
                features["average_response_time_ms"],
                features["performance_streak"],
                features["trend_slope"]
            ])
            action, confidence = self.ml_model.predict(vector)
            
            if action == AdaptiveAction.INCREASE:
                recommended_difficulty = min(5, current_difficulty + 1)
                rationale = f"[Statistical ML Pipeline] High composite engagement score. Increasing to Level {recommended_difficulty}."
            elif action == AdaptiveAction.DECREASE:
                recommended_difficulty = max(1, current_difficulty - 1)
                rationale = f"[Statistical ML Pipeline] Low composite score detected. Adjusting to Level {recommended_difficulty}."
            else:
                recommended_difficulty = current_difficulty
                rationale = f"[Statistical ML Pipeline] Balanced cognitive stability. Maintaining Level {recommended_difficulty}."
            
            engine_type = "Statistical_ML_Composite_Pipeline"
        else:
            from app.ai.adaptive.adaptive_rules import HeuristicAdaptiveEngine
            action, recommended_difficulty, confidence, rationale = HeuristicAdaptiveEngine.evaluate(
                current_difficulty=current_difficulty,
                features=features
            )
            engine_type = "Heuristic_Cognitive_Rule_Engine"

        return {
            "current_difficulty": current_difficulty,
            "recommended_difficulty": recommended_difficulty,
            "action": action,
            "confidence_score": confidence,
            "metrics": features,
            "rationale": rationale,
            "engine_type": engine_type
        }
