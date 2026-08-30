from typing import Dict, Any, Optional
from app.utils.helpers import utc_now_iso
from app.database.db import db
from app.schemas import CognitiveGameType, AdaptiveEvaluationResponse, AdaptiveMetricsAnalyzed
from app.ai.adaptive.ml_pipeline import AdaptivePipeline

class AdaptiveService:
    @staticmethod
    def evaluate_patient_difficulty(
        patient_id: str,
        game_type: CognitiveGameType,
        explicit_current_difficulty: Optional[int] = None,
        use_ml_pipeline: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluates historical attempts for a patient and specific game type,
        determining whether to increase, maintain, or decrease difficulty.
        """
        # Fetch patient profile
        patient = db.patients.find_one({"id": patient_id})
        
        current_diff = 1
        if explicit_current_difficulty is not None:
            current_diff = explicit_current_difficulty
        elif patient and "current_difficulty_levels" in patient:
            current_diff = patient["current_difficulty_levels"].get(game_type.value, 1)

        # Query recent attempts for this patient and game type
        query = {"patient_id": patient_id, "game_type": game_type.value}
        attempts = db.game_attempts.find(query=query, sort_by="timestamp", reverse=False)

        # Run pipeline
        pipeline = AdaptivePipeline(use_ml_model=use_ml_pipeline)
        result = pipeline.process(attempts=attempts, current_difficulty=current_diff)

        # Check if we should automatically update patient's current difficulty level
        if patient and result["recommended_difficulty"] != current_diff:
            diff_levels = patient.get("current_difficulty_levels", {})
            diff_levels[game_type.value] = result["recommended_difficulty"]
            db.patients.update_one({"id": patient_id}, {"$set": {"current_difficulty_levels": diff_levels}})

        return {
            "patient_id": patient_id,
            "game_type": game_type,
            "current_difficulty": result["current_difficulty"],
            "recommended_difficulty": result["recommended_difficulty"],
            "action": result["action"],
            "confidence_score": result["confidence_score"],
            "metrics": result["metrics"],
            "rationale": result["rationale"],
            "evaluated_at": utc_now_iso()
        }
