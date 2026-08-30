import os
import uuid
import logging
from typing import Dict, Any, List, Optional
from datetime import timedelta
import requests
from app.utils.helpers import utc_now, utc_now_iso
from app.core.config import settings
from app.database.db import db
from app.services.analytics_service import AnalyticsService

logger = logging.getLogger("smrithi.ai_report")

class AIReportService:
    @staticmethod
    def generate_progress_report(patient_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Synthesizes actual stored game attempts, latency metrics, and domain breakdowns
        into a structured, doctor-ready progress report with AI narrative generation.
        """
        # Fetch patient profile
        patient = db.patients.find_one({"id": patient_id})
        if not patient:
            patient = {
                "id": patient_id,
                "name": "Patient",
                "age": "Unknown",
                "dementia_stage": "Not Recorded"
            }

        # Fetch analytics
        analytics = AnalyticsService.calculate_patient_analytics(patient_id)
        
        # Query recent attempts
        cutoff_date = (utc_now() - timedelta(days=days)).isoformat()
        attempts = db.game_attempts.find(query={"patient_id": patient_id}, sort_by="timestamp", reverse=True)
        recent_in_period = [a for a in attempts if a.get("timestamp", "") >= cutoff_date]
        if not recent_in_period:
            recent_in_period = attempts[:10]

        total_sessions = len(recent_in_period)
        overall_acc = analytics.get("overall_accuracy_percentage", 0.0)
        overall_lat = analytics.get("overall_avg_response_time_ms", 0.0)
        domains = analytics.get("domain_breakdown", {})
        trajectory = analytics.get("improvement_indicators", {}).get("overall_trajectory", "stable")
        consistency = analytics.get("improvement_indicators", {}).get("consistency_index", 100.0)

        # Identify strengths and areas to watch based on actual domain data
        observed_strengths = []
        areas_to_watch = []

        for d_name, d_data in domains.items():
            if d_data["total_sessions"] > 0:
                avg_acc = d_data["average_accuracy"]
                slope = d_data["recent_trend_slope"]
                if avg_acc >= 75.0 or slope > 1.5:
                    observed_strengths.append(f"{d_name}: Strong engagement with {avg_acc}% mean accuracy (Difficulty Level {d_data['current_difficulty_level']}).")
                elif avg_acc < 55.0 or slope < -2.0:
                    areas_to_watch.append(f"{d_name}: Noted lower accuracy ({avg_acc}%) and higher cognitive effort. Recommended for gentle repetition.")

        if not observed_strengths:
            observed_strengths.append("Consistent willingness to participate in regular daily cognitive sessions.")
        if not areas_to_watch:
            areas_to_watch.append("Continue monitoring response time latency during late evening sessions.")

        caregiver_suggestions = [
            f"Schedule cognitive sessions during morning hours when alertness is peak.",
            f"Use familiar cultural cues (e.g. Assamese tea preparation, regional folk motifs) to trigger positive autobiographical recall.",
            f"Maintain daily gentle 10-minute game sessions rather than long infrequent sessions."
        ]

        # Clinical narrative generation (LLM with local clinical heuristic fallback)
        clinical_summary = ""
        is_ai_generated = False
        ai_engine = "Smrithi_Deterministic_Clinical_Rules"

        # Attempt LLM generation if GEMINI_API_KEY is available
        if settings.GEMINI_API_KEY:
            try:
                prompt_text = (
                    f"Generate a concise, professional 3-sentence progress summary for a dementia caregiver and doctor. "
                    f"Patient Name: {patient.get('name')}, Dementia Stage: {patient.get('dementia_stage')}. "
                    f"Total sessions in period: {total_sessions}, Overall Accuracy: {overall_acc}%, Average Latency: {overall_lat}ms. "
                    f"Trajectory: {trajectory}, Consistency: {consistency}%. "
                    f"Strengths: {'; '.join(observed_strengths)}. "
                    f"Areas to watch: {'; '.join(areas_to_watch)}. "
                    f"Important: Do not provide a diagnosis. Provide an objective progress description."
                )
                
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
                payload = {
                    "contents": [{"parts": [{"text": prompt_text}]}]
                }
                resp = requests.post(url, json=payload, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    clinical_summary = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    is_ai_generated = True
                    ai_engine = "Google_Gemini_1.5_Flash"
            except Exception as e:
                logger.warning(f"External LLM API call failed or timed out ({e}). Utilizing deterministic clinical fallback.")

        # Fallback deterministic summary if no API key or network call failed
        if not clinical_summary:
            if total_sessions == 0:
                clinical_summary = (
                    f"Baseline monitoring period initiated for {patient.get('name', 'the patient')}. "
                    f"No completed gaming sessions recorded yet. Please complete initial cognitive baseline exercises."
                )
            else:
                clinical_summary = (
                    f"Over the recorded period, {patient.get('name', 'the patient')} completed {total_sessions} cognitive exercise sessions "
                    f"with an overall accuracy of {overall_acc}% and an average response time of {overall_lat}ms. "
                    f"Performance trajectory is currently assessed as '{trajectory}' with a consistency rating of {consistency}/100. "
                    f"Highest engagement was noted in {observed_strengths[0].split(':')[0]}."
                )

        report_doc = {
            "report_id": f"rep_{uuid.uuid4().hex[:10]}",
            "patient_id": patient_id,
            "patient_name": patient.get("name", "Unknown"),
            "dementia_stage": str(patient.get("dementia_stage", "Not Recorded")),
            "reporting_period": f"Past {days} days (from {cutoff_date[:10]} to {utc_now_iso()[:10]})",
            "total_sessions_analyzed": total_sessions,
            "cognitive_domains": domains,
            "clinical_summary": clinical_summary,
            "observed_strengths": observed_strengths,
            "areas_to_watch": areas_to_watch,
            "performance_trend": trajectory.capitalize(),
            "adherence_and_consistency": {
                "consistency_score": consistency,
                "adherence_status": "Regular" if total_sessions >= 7 else "Needs Encouragement",
                "recommended_weekly_target_sessions": 7
            },
            "caregiver_actionable_suggestions": caregiver_suggestions,
            "recent_activity": [
                {
                    "game_type": a.get("game_type"),
                    "difficulty_level": a.get("difficulty_level"),
                    "score": a.get("score"),
                    "accuracy": a.get("accuracy"),
                    "response_time_ms": a.get("response_time_ms"),
                    "timestamp": a.get("timestamp")
                }
                for a in recent_in_period[:5]
            ],
            "is_ai_generated": is_ai_generated,
            "ai_engine": ai_engine,
            "disclaimer": "This progress-assistance report is generated for caregivers and healthcare facilitators to monitor cognitive engagement. It is NOT a medical diagnosis or replacement for clinical neuropsychological assessment.",
            "created_at": utc_now_iso()
        }

        # Store in database
        db.reports.insert_one(report_doc)
        return report_doc
