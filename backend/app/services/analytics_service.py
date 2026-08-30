from typing import Dict, List, Any, Optional
from app.utils.helpers import utc_now_iso
import numpy as np
from app.database.db import db
from app.schemas import CognitiveGameType, CognitiveDomain, PatientAnalyticsResponse, DomainScore

DOMAIN_MAPPING = {
    CognitiveGameType.MEMORY.value: CognitiveDomain.MEMORY.value,
    CognitiveGameType.ATTENTION.value: CognitiveDomain.ATTENTION.value,
    CognitiveGameType.SEQUENCE.value: CognitiveDomain.REASONING_SEQUENCE.value,
    CognitiveGameType.PATTERN.value: CognitiveDomain.PATTERN_RECOGNITION.value,
    CognitiveGameType.RECOGNITION.value: CognitiveDomain.VISUAL_RECOGNITION.value
}

class AnalyticsService:
    @staticmethod
    def calculate_patient_analytics(patient_id: str) -> Dict[str, Any]:
        """
        Calculates comprehensive multi-domain cognitive analytics for a patient.
        """
        patient = db.patients.find_one({"id": patient_id}) or {
            "name": "Unknown Patient",
            "dementia_stage": "Not Recorded",
            "current_difficulty_levels": {}
        }

        attempts = db.game_attempts.find(query={"patient_id": patient_id}, sort_by="timestamp", reverse=False)

        if not attempts:
            # Return baseline schema when no sessions exist yet
            empty_domains = {}
            for g_type, d_name in DOMAIN_MAPPING.items():
                empty_domains[d_name] = {
                    "domain_name": d_name,
                    "game_type": g_type,
                    "total_sessions": 0,
                    "average_accuracy": 0.0,
                    "average_response_time_ms": 0.0,
                    "current_difficulty_level": patient.get("current_difficulty_levels", {}).get(g_type, 1),
                    "status": "not_started",
                    "recent_trend_slope": 0.0
                }

            return {
                "patient_id": patient_id,
                "patient_name": patient.get("name", "Unknown"),
                "dementia_stage": str(patient.get("dementia_stage", "Not Recorded")),
                "total_games_played": 0,
                "total_play_time_minutes": 0.0,
                "overall_accuracy_percentage": 0.0,
                "overall_avg_response_time_ms": 0.0,
                "domain_breakdown": empty_domains,
                "accuracy_history": [],
                "response_time_history": [],
                "difficulty_progression": {g: [] for g in DOMAIN_MAPPING.keys()},
                "improvement_indicators": {
                    "overall_trajectory": "baseline_pending",
                    "consistency_index": 100.0,
                    "fatigue_risk": "low"
                },
                "generated_at": utc_now_iso()
            }

        total_sessions = len(attempts)
        total_time_sec = sum(a.get("session_duration_seconds", 60) for a in attempts)
        all_accuracies = [float(a.get("accuracy", 0)) for a in attempts]
        all_latencies = [float(a.get("response_time_ms", 0)) for a in attempts]

        overall_accuracy = round(float(np.mean(all_accuracies)), 2)
        overall_latency = round(float(np.mean(all_latencies)), 2)

        # Domain breakdown
        domain_breakdown = {}
        for g_type, d_name in DOMAIN_MAPPING.items():
            g_attempts = [a for a in attempts if a.get("game_type") == g_type]
            if g_attempts:
                g_accs = [float(a.get("accuracy", 0)) for a in g_attempts]
                g_lats = [float(a.get("response_time_ms", 0)) for a in g_attempts]
                avg_acc = float(np.mean(g_accs))
                avg_lat = float(np.mean(g_lats))

                # Trend slope
                slope = 0.0
                if len(g_accs) >= 2:
                    slope = float(np.polyfit(np.arange(len(g_accs)), np.array(g_accs), 1)[0])

                status = "stable"
                if slope > 2.0 or avg_acc >= 80.0:
                    status = "improving"
                elif slope < -3.0 or avg_acc < 50.0:
                    status = "needs_attention"

                curr_diff = patient.get("current_difficulty_levels", {}).get(g_type, g_attempts[-1].get("difficulty_level", 1))

                domain_breakdown[d_name] = {
                    "domain_name": d_name,
                    "game_type": g_type,
                    "total_sessions": len(g_attempts),
                    "average_accuracy": round(avg_acc, 2),
                    "average_response_time_ms": round(avg_lat, 2),
                    "current_difficulty_level": curr_diff,
                    "status": status,
                    "recent_trend_slope": round(slope, 2)
                }
            else:
                domain_breakdown[d_name] = {
                    "domain_name": d_name,
                    "game_type": g_type,
                    "total_sessions": 0,
                    "average_accuracy": 0.0,
                    "average_response_time_ms": 0.0,
                    "current_difficulty_level": patient.get("current_difficulty_levels", {}).get(g_type, 1),
                    "status": "not_started",
                    "recent_trend_slope": 0.0
                }

        # History arrays
        accuracy_history = [
            {"session_id": a.get("session_id", a.get("id")), "game_type": a.get("game_type"), "accuracy": a.get("accuracy"), "timestamp": a.get("timestamp")}
            for a in attempts[-30:]
        ]
        response_time_history = [
            {"session_id": a.get("session_id", a.get("id")), "game_type": a.get("game_type"), "response_time_ms": a.get("response_time_ms"), "timestamp": a.get("timestamp")}
            for a in attempts[-30:]
        ]

        difficulty_progression = {}
        for g_type in DOMAIN_MAPPING.keys():
            difficulty_progression[g_type] = [
                {"difficulty_level": a.get("difficulty_level"), "accuracy": a.get("accuracy"), "timestamp": a.get("timestamp")}
                for a in attempts if a.get("game_type") == g_type
            ]

        # Overall trajectory & consistency index (std dev based)
        acc_std = float(np.std(all_accuracies)) if len(all_accuracies) > 1 else 5.0
        consistency_index = round(max(10.0, 100.0 - (acc_std * 1.5)), 1)

        overall_slope = 0.0
        if len(all_accuracies) >= 2:
            overall_slope = float(np.polyfit(np.arange(len(all_accuracies)), np.array(all_accuracies), 1)[0])

        if overall_slope > 1.5:
            trajectory = "improving"
        elif overall_slope < -2.0:
            trajectory = "declining"
        else:
            trajectory = "stable"

        # Check for sudden decline to generate an alert
        if len(all_accuracies) >= 3 and all_accuracies[-1] < (overall_accuracy - 25.0):
            # Check if alert already created recently
            existing = db.alerts.find_one({
                "patient_id": patient_id,
                "alert_type": "performance_drop",
                "is_read": False
            })
            if not existing:
                db.alerts.insert_one({
                    "patient_id": patient_id,
                    "caregiver_id": patient.get("caregiver_id"),
                    "alert_type": "performance_drop",
                    "severity": "warning",
                    "message": f"Notice: Patient {patient.get('name', 'Patient')} experienced a significant accuracy drop to {all_accuracies[-1]}% in recent session.",
                    "created_at": utc_now_iso(),
                    "is_read": False
                })

        return {
            "patient_id": patient_id,
            "patient_name": patient.get("name", "Unknown"),
            "dementia_stage": str(patient.get("dementia_stage", "Not Recorded")),
            "total_games_played": total_sessions,
            "total_play_time_minutes": round(total_time_sec / 60.0, 1),
            "overall_accuracy_percentage": overall_accuracy,
            "overall_avg_response_time_ms": overall_latency,
            "domain_breakdown": domain_breakdown,
            "accuracy_history": accuracy_history,
            "response_time_history": response_time_history,
            "difficulty_progression": difficulty_progression,
            "improvement_indicators": {
                "overall_trajectory": trajectory,
                "trend_slope": round(overall_slope, 2),
                "consistency_index": consistency_index,
                "fatigue_risk": "moderate" if overall_latency > 7000 else "low"
            },
            "generated_at": utc_now_iso()
        }
