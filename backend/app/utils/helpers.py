from datetime import datetime, timezone

def utc_now() -> datetime:
    """Returns current timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)

def utc_now_iso() -> str:
    """Returns ISO 8601 formatted UTC timestamp string."""
    return datetime.now(timezone.utc).isoformat()
