import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


# ============================================================
# Firebase Admin SDK — service account credentials
# ============================================================

# Primary: path to serviceAccountKey.json
FIREBASE_CRED_PATH = os.getenv(
    "FIREBASE_CRED_PATH",
    str(BASE_DIR / "serviceAccountKey.json")
)

# Fallback: individual environment variables
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")
FIREBASE_CLIENT_EMAIL = os.getenv("FIREBASE_CLIENT_EMAIL", "")
FIREBASE_PRIVATE_KEY = os.getenv(
    "FIREBASE_PRIVATE_KEY",
    ""
).replace("\\n", "\n")

# Firebase Web API Key — used by smoke_test.py
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY", "")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


# ============================================================
# Application Settings
# ============================================================

class Settings(BaseSettings):
    APP_NAME: str = "SPARSH — Smrithi API"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Storage for Voice Synthesis Cache
    AUDIO_CACHE_DIR: str = str(BASE_DIR / "audio_cache")

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()