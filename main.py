import os
import random
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Smrithi Cognitive Gaming Engine",
    description="Unified localized config and rule-based adaptive backend for all 5 games.",
    version="1.1.0"
)

# Enable CORS so your React Frontend teammates can connect to your local backend server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================================
# 1. LOCAL DATA MOCK (Allows instant testing in VS Code without Firebase setup)
# =====================================================================
MOCK_PATIENTS_DB = {
    "patient123": {
        "profile": {"name": "Pranab Gogoi", "age": 74},
        "settings": {
            "difficulty_level": 1,
            "lock_difficulty": False,
            "personalization_facts": [
                {
                    "relation": "daughter",
                    "name": "Priya",
                    "img_url": "/assets/mock/daughter_priya.png"
                },
                {
                    "relation": "grandson",
                    "name": "Arjun",
                    "img_url": "/assets/mock/grandson_arjun.png"
                }
            ]
        }
    }
}

MOCK_SESSIONS_DATABASE = []

# =====================================================================
# 2. DATA SCHEMAS (Pydantic validation layers)
# =====================================================================
class GameConfigRequest(BaseModel):
    patient_id: str = Field(..., example="patient123")
    game_type: str = Field(..., description="memory_match | recognition | sequence_recall | motif_weaver | regional_kitchen", example="memory_match")
    language: str = Field(default="as", description="Preferred language: 'as' (Assamese) or 'kha' (Khasi)", example="as")

class GameSessionPayload(BaseModel):
    patient_id: str = Field(..., example="patient123")
    game_type: str = Field(..., example="memory_match")
    difficulty_level: int = Field(..., ge=1, le=3, example=1)
    total_taps: int = Field(..., ge=0, example=8)
    correct_taps: int = Field(..., ge=0, example=6)
    mistakes: int = Field(..., ge=0, example=2)
    duration_seconds: float = Field(..., ge=0.0, example=18.4)

# =====================================================================
# 3. ENDPOINT 1: LOCALIZED CONFIGURATION GENERATION
# =====================================================================
@app.post("/api/games/config", status_code=status.HTTP_200_OK)
async def get_game_configuration(payload: GameConfigRequest) -> Dict[str, Any]:
    """
    Unified configuration endpoint. Serves localized asset layouts and 
    audio prompts for all 5 games based on language and difficulty.
    """
    patient = MOCK_PATIENTS_DB.get(payload.patient_id)
    if not patient:
        raise HTTPException(
            status_code=404, 
            detail=f"Patient '{payload.patient_id}' not found. Use 'patient123' to test!"
        )

    settings = patient.get("settings", {})
    difficulty = settings.get("difficulty_level", 1)
    lang = payload.language.lower() if payload.language.lower() in ["as", "kha"] else "as"

    # GAME 1: MEMORY MATCH (Remember -> Find -> Match)
    if payload.game_type == "memory_match":
        card_pairs_count = 2 + difficulty  # Level 1 = 3 pairs, Level 3 = 5 pairs
        items_pool = [
            {"id": "tea_cup", "emoji": "☕"},
            {"id": "rickshaw", "emoji": "🛺"},
            {"id": "dhol", "emoji": "🥁"},
            {"id": "hornbill", "emoji": "🦅"},
            {"id": "bamboo", "emoji": "🧺"},
            {"id": "fish", "emoji": "🐟"}
        ]
        selected_items = random.sample(items_pool, card_pairs_count)
        game_cards = selected_items + selected_items
        random.shuffle(game_cards)
        
        return {
            "game_type": "memory_match",
            "difficulty_level": difficulty,
            "audio_prompt": f"/audio/{lang}/memory_match_intro_lvl{difficulty}.mp3",
            "cards": [{"unique_id": f"card_{idx}", "item_id": card["id"], "emoji": card["emoji"]} for idx, card in enumerate(game_cards)],
            "rules": {"required_pairs_to_win": card_pairs_count}
        }

    # GAME 2: RECOGNITION (See -> Recognize -> Select)
    elif payload.game_type == "recognition":
        facts = settings.get("personalization_facts", [])
        if facts and difficulty > 1:
            target = random.choice(facts)
            question_text = f"Find your {target['relation']}, {target['name']}!"
            correct_id = target["relation"]
            options = [
                {"id": correct_id, "label": target["name"], "img_url": target["img_url"]},
                {"id": "stranger_1", "label": "Neighbor", "img_url": "/assets/mock/stranger_1.png"},
                {"id": "stranger_2", "label": "Doctor", "img_url": "/assets/mock/stranger_2.png"}
            ]
        else:
            question_text = "Select the Traditional Assamese Japi!" if lang == "as" else "Select the Traditional Khasi Ryndia!"
            correct_id = "japi" if lang == "as" else "ryndia"
            options = [
                {"id": correct_id, "label": "Japi" if lang == "as" else "Ryndia", "emoji": "👒"},
                {"id": "umbrella", "label": "Umbrella", "emoji": "☂️"},
                {"id": "cap", "label": "Cap", "emoji": "🧢"}
            ]
        random.shuffle(options)
        
        return {
            "game_type": "recognition",
            "difficulty_level": difficulty,
            "audio_prompt": f"/audio/{lang}/recognition_intro.mp3",
            "question_text": question_text,
            "correct_id": correct_id,
            "options": options
        }

    # GAME 3: SEQUENCE RECALL (Observe -> Remember -> Reproduce)
    elif payload.game_type == "sequence_recall":
        sequence_length = 2 + difficulty  # Level 1 = 3 beats, Level 3 = 5 beats
        beats_pool = ["Dhol_Low", "Dhol_High", "Pepa_Short", "Pepa_Long"]
        generated_sequence = [random.choice(beats_pool) for _ in range(sequence_length)]
        
        return {
            "game_type": "sequence_recall",
            "difficulty_level": difficulty,
            "audio_prompt": f"/audio/{lang}/sequence_recall_intro.mp3",
            "target_sequence": generated_sequence,
            "instrument_buttons": [
                {"id": "Dhol_Low", "label": "Dhol (Bass)", "emoji": "🥁"},
                {"id": "Dhol_High", "label": "Dhol (Treble)", "emoji": "🎵"},
                {"id": "Pepa_Short", "label": "Pepa (Short)", "emoji": "🎷"},
                {"id": "Pepa_Long", "label": "Pepa (Long)", "emoji": "🎺"}
            ]
        }

    # GAME 4: FOLK MOTIF WEAVER (Observe Pattern -> Remember -> Complete)
    elif payload.game_type == "motif_weaver":
        pattern_id = f"gamosa_pattern_{difficulty}"
        correct_index = {"gamosa_pattern_1": 0, "gamosa_pattern_2": 2, "gamosa_pattern_3": 1}
        
        return {
            "game_type": "motif_weaver",
            "difficulty_level": difficulty,
            "audio_prompt": f"/audio/{lang}/motif_intro.mp3",
            "incomplete_pattern_visual": "◈ ◈ ◈ ? ◈ ◈" if difficulty == 1 else "◈ ⧓ ◈ ⧓ ? ⧓",
            "options": [
                {"index": 0, "emoji": "◈", "label": "Diamond"},
                {"index": 1, "emoji": "⧓", "label": "Hourglass"},
                {"index": 2, "emoji": "⬡", "label": "Hexagon"}
            ],
            "correct_index": correct_index.get(pattern_id, 0)
        }

    # GAME 5: REGIONAL KITCHEN (Observe Ingredients -> Remember Order -> Recreate)
    elif payload.game_type == "regional_kitchen":
        recipes = {
            "as": {
                "name": "Khar",
                "steps": ["water", "mustard_oil", "raw_papaya", "kol_khar"]
            },
            "kha": {
                "name": "Jadoh",
                "steps": ["pork", "local_onion", "turmeric", "black_sesame"]
            }
        }
        recipe = recipes.get(lang, recipes["as"])
        sequence_limit = max(2, min(difficulty + 1, len(recipe["steps"])))
        correct_order = recipe["steps"][:sequence_limit]

        return {
            "game_type": "regional_kitchen",
            "difficulty_level": difficulty,
            "recipe_name": recipe["name"],
            "audio_prompt": f"/audio/{lang}/kitchen_intro_lvl{difficulty}.mp3",
            "correct_sequence": correct_order,
            "ingredients_pool": [
                {"id": "water", "name": "Water", "emoji": "💧"},
                {"id": "mustard_oil", "name": "Mustard Oil", "emoji": "🍯"},
                {"id": "raw_papaya", "name": "Raw Papaya", "emoji": "🍈"},
                {"id": "kol_khar", "name": "Kol Khar", "emoji": "🥣"},
                {"id": "pork", "name": "Pork", "emoji": "🥩"},
                {"id": "chili", "name": "Bhut Jolokia", "emoji": "🌶️"}
            ]
        }

    raise HTTPException(status_code=400, detail="Unknown game type requested.")

# =====================================================================
# 4. ENDPOINT 2: GAMEPLAY LOGGING & ADAPTIVE DIFFICULTY TUNER
# =====================================================================
@app.post("/api/games/session", status_code=status.HTTP_201_CREATED)
async def process_game_session(payload: GameSessionPayload) -> Dict[str, Any]:
    """
    Computes game accuracy, logs sessions, and implements automatic difficulty adjustments:
    - Downward Hook (Frustration Prevention): Lower level if mistakes >= 3 or accuracy < 60%
    - Upward Hook (Challenge Progression): Raise level if accuracy >= 85% and mistakes < 2
    """
    patient = MOCK_PATIENTS_DB.get(payload.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found.")

    # Calculate metrics
    total = payload.total_taps
    accuracy = (payload.correct_taps / total * 100) if total > 0 else 0.0
    avg_latency = (payload.duration_seconds / total) if total > 0 else 0.0

    # Save gameplay session
    session_id = f"sess_{len(MOCK_SESSIONS_DATABASE) + 1:03d}"
    MOCK_SESSIONS_DATABASE.append({
        "session_id": session_id,
        "patient_id": payload.patient_id,
        "game_type": payload.game_type,
        "difficulty_level": payload.difficulty_level,
        "accuracy": round(accuracy, 2),
        "mistakes": payload.mistakes,
        "avg_latency": round(avg_latency, 2)
    })

    # Rule-Based Adaptive Logic (Downward/Upward Hooks)
    settings = patient.get("settings", {})
    current_difficulty = settings.get("difficulty_level", 1)
    lock_active = settings.get("lock_difficulty", False)

    new_difficulty = current_difficulty
    status_msg = "Stable performance. Level maintained."
    adapted = False

    if not lock_active:
        # Downward Hook (Frustration Prevention Rule)
        if payload.mistakes >= 3 or accuracy < 60.0:
            if current_difficulty > 1:
                new_difficulty = current_difficulty - 1
                adapted = True
                status_msg = f"Frustration detected: Decreased level {current_difficulty} -> {new_difficulty}"
        # Upward Hook (Challenge Progression Rule)
        elif accuracy >= 85.0 and payload.mistakes < 2:
            if current_difficulty < 3:
                new_difficulty = current_difficulty + 1
                adapted = True
                status_msg = f"Challenge progressed: Increased level {current_difficulty} -> {new_difficulty}"

        if adapted:
            MOCK_PATIENTS_DB[payload.patient_id]["settings"]["difficulty_level"] = new_difficulty

    return {
        "status": "success",
        "session_id": session_id,
        "metrics": {"accuracy": round(accuracy, 2), "avg_latency_seconds": round(avg_latency, 2)},
        "difficulty_state": {
            "adaptation_triggered": adapted,
            "previous_level": current_difficulty,
            "active_database_level": new_difficulty,
            "feedback": status_msg
        }
    }

# =====================================================================
# 5. ENDPOINT 3: PATIENT SUMMARY & SESSION HISTORY
# =====================================================================
@app.get("/api/patients/{patient_id}/summary", status_code=status.HTTP_200_OK)
async def get_patient_summary(patient_id: str) -> Dict[str, Any]:
    """
    Fetches profile, current active difficulty settings, and past session history.
    """
    patient = MOCK_PATIENTS_DB.get(patient_id)
    if not patient:
        raise HTTPException(
            status_code=404, 
            detail=f"Patient '{patient_id}' not found."
        )
    
    # Filter sessions for this specific patient
    patient_sessions = [
        sess for sess in MOCK_SESSIONS_DATABASE 
        if sess["patient_id"] == patient_id
    ]

    return {
        "status": "success",
        "patient_id": patient_id,
        "profile": patient.get("profile", {}),
        "current_settings": patient.get("settings", {}),
        "total_sessions_played": len(patient_sessions),
        "session_history": patient_sessions
    }