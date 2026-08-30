import os
import io
import base64
import hashlib
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger("smrithi.voice")

# Map NER languages to gTTS language codes
GTTS_LANG_MAP = {
    "as": "bn",   # Bengali script/phonetics is closest available in standard gTTS for Assamese
    "bn": "bn",
    "hi": "hi",
    "en": "en",
    "mni": "hi",  # Fallback
    "brx": "hi",
    "lus": "en",
    "kha": "en",
    "grt": "en"
}

class VoiceService:
    @staticmethod
    def synthesize_speech(text: str, language: str = "as", speed_rate: float = 1.0) -> Dict[str, Any]:
        """
        Synthesizes speech from text using Google TTS (gTTS) with local caching and base64 streaming.
        Handles offline/missing external service gracefully.
        """
        lang_code = language.lower()
        gtts_code = GTTS_LANG_MAP.get(lang_code, "en")
        fallback_used = (lang_code != gtts_code and lang_code not in ["bn", "hi", "en"])
        
        # Create audio cache dir
        cache_dir = Path(settings.AUDIO_CACHE_DIR)
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Deterministic cache filename based on text + language
        text_hash = hashlib.md5(f"{text}_{lang_code}_{speed_rate}".encode('utf-8')).hexdigest()
        file_path = cache_dir / f"{text_hash}.mp3"

        duration_estimate = max(1.0, round(len(text.split()) * 0.45, 1))

        if file_path.exists():
            try:
                with open(file_path, "rb") as f:
                    audio_bytes = f.read()
                audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
                return {
                    "audio_url": f"/api/voice/stream/{file_path.name}",
                    "audio_base64": audio_b64,
                    "format": "mp3",
                    "duration_estimate_seconds": duration_estimate,
                    "language_used": gtts_code,
                    "fallback_used": fallback_used,
                    "status": "cached",
                    "message": "Audio retrieved from local cache."
                }
            except Exception as e:
                logger.warning(f"Failed to read cached audio: {e}")

        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang=gtts_code, slow=(speed_rate < 0.9))
            
            # Save to cache
            tts.save(str(file_path))
            
            with open(file_path, "rb") as f:
                audio_bytes = f.read()
            audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            return {
                "audio_url": f"/api/voice/stream/{file_path.name}",
                "audio_base64": audio_b64,
                "format": "mp3",
                "duration_estimate_seconds": duration_estimate,
                "language_used": gtts_code,
                "fallback_used": fallback_used,
                "status": "synthesized",
                "message": f"Speech synthesized successfully using voice code '{gtts_code}'{' (phonetic fallback)' if fallback_used else ''}."
            }
        except Exception as err:
            logger.error(f"Voice synthesis error: {err}")
            # Mock / Standby response when offline or network unavailable
            return {
                "audio_url": None,
                "audio_base64": None,
                "format": "mp3",
                "duration_estimate_seconds": duration_estimate,
                "language_used": gtts_code,
                "fallback_used": fallback_used,
                "status": "service_unavailable",
                "message": f"External TTS service is currently unreachable or offline. Text '{text}' queued for client synthesis."
            }

    @staticmethod
    def get_supported_voices() -> Dict[str, Any]:
        return {
            "supported_engines": ["gTTS", "IndicTTS_Hook", "WebAudio_Fallback"],
            "language_mappings": GTTS_LANG_MAP,
            "sample_rate_hz": 24000,
            "output_formats": ["mp3", "base64_stream"]
        }
