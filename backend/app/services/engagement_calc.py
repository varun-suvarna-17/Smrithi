from datetime import datetime, timezone, timedelta
from app.services import firestore_service as fs
from app.models.engagement import EngagementSummary


def recompute_engagement(caregiver_id: str, patient_id: str) -> EngagementSummary:
    """
    Recomputes all three dashboard metrics from raw session + reminder data,
    writes the result to engagementSummary/current, and returns the summary.

    Called synchronously inside session POST and reminder PATCH so the dashboard
    listener gets a fresh doc within the same request.
    """
    now = datetime.now(timezone.utc)
    seven_days_ago = now - timedelta(days=7)

    # ── Weekly session count & last session ──────────────────────────────────
    recent_sessions = fs.get_all_sessions_since(caregiver_id, patient_id, seven_days_ago)
    weekly_session_count = len(recent_sessions)

    last_session_at = None
    if recent_sessions:
        # sessions are returned newest-first
        raw_ts = recent_sessions[0].get("startedAt") or recent_sessions[0].get("endedAt")
        if raw_ts is not None:
            if hasattr(raw_ts, "timestamp"):           # Firestore Timestamp
                last_session_at = datetime.fromtimestamp(raw_ts.timestamp(), tz=timezone.utc)
            elif isinstance(raw_ts, datetime):
                last_session_at = raw_ts if raw_ts.tzinfo else raw_ts.replace(tzinfo=timezone.utc)

    # ── Streak (consecutive calendar days with >= 1 completed session) ───────
    # Collect unique dates with a completed session in the last 7 days
    completed_days: set[str] = set()
    for s in recent_sessions:
        if not s.get("completed"):
            continue
        ts = s.get("startedAt") or s.get("endedAt")
        if ts is None:
            continue
        if hasattr(ts, "timestamp"):
            dt = datetime.fromtimestamp(ts.timestamp(), tz=timezone.utc)
        elif isinstance(ts, datetime):
            dt = ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc)
        else:
            continue
        completed_days.add(dt.date().isoformat())

    streak = 0
    check_date = now.date()
    while check_date.isoformat() in completed_days:
        streak += 1
        check_date -= timedelta(days=1)

    # ── Reminder adherence rate (trailing 7 days) ────────────────────────────
    recent_reminders = fs.get_reminders_since(caregiver_id, patient_id, seven_days_ago)
    if recent_reminders:
        completed_reminders = sum(1 for r in recent_reminders if r.get("status") == "completed")
        adherence = completed_reminders / len(recent_reminders)
    else:
        adherence = 0.0

    summary = EngagementSummary(
        streakCount=streak,
        weeklySessionCount=weekly_session_count,
        reminderAdherenceRate=round(adherence, 4),
        lastSessionAt=last_session_at,
        updatedAt=now,
    )

    # Persist to Firestore so dashboard listeners pick it up immediately
    fs.upsert_engagement_summary(
        caregiver_id,
        patient_id,
        summary.model_dump(),
    )

    return summary

