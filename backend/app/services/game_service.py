import random
import uuid
from typing import Dict, List, Any, Optional
from app.utils.helpers import utc_now_iso
from app.schemas import CognitiveGameType, CognitiveDomain, GameInfo
from app.services.localization_service import LocalizationService

# 5 Games Information
GAMES_REGISTRY: Dict[CognitiveGameType, GameInfo] = {
    CognitiveGameType.MEMORY: GameInfo(
        id="memory",
        name="Smrithi Memory Recall",
        cognitive_domain=CognitiveDomain.MEMORY,
        description="Assesses short-term and working memory recall through culturally resonant North Eastern artifacts and symbols.",
        supported_difficulty_range=[1, 2, 3, 4, 5],
        ner_cultural_context="Uses traditional items like Bamboo Kula, Assamese Dhol, Bell Metal Bowl, and Japi Hat."
    ),
    CognitiveGameType.ATTENTION: GameInfo(
        id="attention",
        name="Target Motif Visual Search",
        cognitive_domain=CognitiveDomain.ATTENTION,
        description="Strengthens selective and sustained visual attention by finding target cultural symbols among distractors.",
        supported_difficulty_range=[1, 2, 3, 4, 5],
        ner_cultural_context="Features regional craft motifs and textile geometric symbols."
    ),
    CognitiveGameType.SEQUENCE: GameInfo(
        id="sequence",
        name="Daily Living & Cultural Sequence Recall",
        cognitive_domain=CognitiveDomain.REASONING_SEQUENCE,
        description="Stimulates executive functioning and procedural memory by ordering daily living routines and regional traditions.",
        supported_difficulty_range=[1, 2, 3, 4, 5],
        ner_cultural_context="Includes Assam orthodox tea brewing, traditional cooking, and morning routine steps."
    ),
    CognitiveGameType.PATTERN: GameInfo(
        id="pattern",
        name="Traditional Handloom Folk Motif Pattern",
        cognitive_domain=CognitiveDomain.PATTERN_RECOGNITION,
        description="Assesses pattern completion and inductive reasoning using North Eastern weaving and folk geometry.",
        supported_difficulty_range=[1, 2, 3, 4, 5],
        ner_cultural_context="Inspired by Eri, Muga, and tribal border weaving motifs."
    ),
    CognitiveGameType.RECOGNITION: GameInfo(
        id="recognition",
        name="Cultural Heritage & Object Recognition",
        cognitive_domain=CognitiveDomain.VISUAL_RECOGNITION,
        description="Enhances semantic memory and visual recognition of familiar North Eastern heritage artifacts.",
        supported_difficulty_range=[1, 2, 3, 4, 5],
        ner_cultural_context="Highlights iconic heritage items, musical instruments, and regional utensils."
    )
}

ITEM_POOL = ["japi", "dhol", "kula", "gamusa", "pepa", "tea", "rice_bowl", "sarai", "hornbill", "muga_silk"]

SEQUENCE_TEMPLATES = [
    {
        "title": "Assam Tea Preparation",
        "steps": [
            {"id": "s1", "label": "Boil fresh water in saucepan", "symbol": "♨"},
            {"id": "s2", "label": "Add fragrant Assam tea leaves", "symbol": "🍃"},
            {"id": "s3", "label": "Steep and add milk and ginger", "symbol": "☕"},
            {"id": "s4", "label": "Strain into bell-metal cup and serve", "symbol": "🍵"}
        ]
    },
    {
        "title": "Traditional Meal Routine",
        "steps": [
            {"id": "m1", "label": "Wash hands with clean water", "symbol": "💧"},
            {"id": "m2", "label": "Serve warm steamed rice in bowl", "symbol": "🍚"},
            {"id": "m3", "label": "Enjoy meal with family", "symbol": "🍲"},
            {"id": "m4", "label": "Take prescribed daily medication", "symbol": "💊"}
        ]
    },
    {
        "title": "Handloom Weaving Setup",
        "steps": [
            {"id": "w1", "label": "Spin pure golden Muga silk thread", "symbol": "🧶"},
            {"id": "w2", "label": "Set warp threads on traditional loom", "symbol": "🧵"},
            {"id": "w3", "label": "Weave geometric Gamusa floral border", "symbol": "🌸"},
            {"id": "w4", "label": "Complete and fold finished textile", "symbol": "🧣"}
        ]
    }
]

class GameService:
    @staticmethod
    def list_games() -> List[GameInfo]:
        return list(GAMES_REGISTRY.values())

    @staticmethod
    def get_game_info(game_type: CognitiveGameType) -> Optional[GameInfo]:
        return GAMES_REGISTRY.get(game_type)

    @staticmethod
    def generate_game_session(
        patient_id: str,
        game_type: CognitiveGameType,
        difficulty_level: int = 1,
        language: str = "as"
    ) -> Dict[str, Any]:
        """Generates dynamic game session data tailored to patient difficulty and language."""
        difficulty = max(1, min(5, difficulty_level))
        session_id = f"sess_{uuid.uuid4().hex[:10]}"
        game_meta = GAMES_REGISTRY[game_type]
        
        rounds_data = []
        instructions = LocalizationService.get_prompt(f"{game_type.value}_instruction", language)
        total_rounds = 3 if difficulty <= 2 else (4 if difficulty <= 4 else 5)

        if game_type == CognitiveGameType.MEMORY:
            # Memory Match / Recall
            # Level 1: 3 items, Level 2: 4 items, Level 3: 5 items, Level 4: 6 items, Level 5: 7 items
            item_count = min(len(ITEM_POOL), 2 + difficulty)
            for r in range(total_rounds):
                selected_ids = random.sample(ITEM_POOL, item_count)
                items = [LocalizationService.get_cultural_item(item_id, language) for item_id in selected_ids]
                target_item = random.choice(items)
                
                # Distractors for choice
                remaining_ids = [i for i in ITEM_POOL if i not in selected_ids]
                distractor_count = min(3, len(remaining_ids))
                distractor_ids = random.sample(remaining_ids, distractor_count)
                distractor_items = [LocalizationService.get_cultural_item(did, language) for did in distractor_ids]
                
                options = [target_item] + distractor_items
                random.shuffle(options)
                
                rounds_data.append({
                    "round_number": r + 1,
                    "stimulus_display_seconds": max(3, 7 - difficulty),
                    "items_to_remember": items,
                    "target_question": f"Which of the following items was in the displayed set?",
                    "target_id": target_item["id"],
                    "options": options
                })

        elif game_type == CognitiveGameType.ATTENTION:
            # Visual Search & Selective Attention
            for r in range(total_rounds):
                target_id = random.choice(ITEM_POOL)
                target_item = LocalizationService.get_cultural_item(target_id, language)
                
                distractor_ids = [i for i in ITEM_POOL if i != target_id]
                grid_size = 4 + (difficulty * 2)  # 6 to 14 items
                
                distractors = [LocalizationService.get_cultural_item(random.choice(distractor_ids), language) for _ in range(grid_size - 1)]
                grid_items = [target_item] + distractors
                random.shuffle(grid_items)
                
                rounds_data.append({
                    "round_number": r + 1,
                    "task": "Locate the target item in the grid",
                    "target_item": target_item,
                    "grid_items": grid_items,
                    "correct_target_id": target_id,
                    "time_limit_seconds": max(5, 20 - (difficulty * 2))
                })

        elif game_type == CognitiveGameType.SEQUENCE:
            # Chronological Routine Recall
            for r in range(total_rounds):
                template = random.choice(SEQUENCE_TEMPLATES)
                steps_count = min(len(template["steps"]), 2 + difficulty)
                ordered_steps = template["steps"][:steps_count]
                
                shuffled_steps = list(ordered_steps)
                random.shuffle(shuffled_steps)
                
                rounds_data.append({
                    "round_number": r + 1,
                    "activity_title": template["title"],
                    "shuffled_steps": shuffled_steps,
                    "correct_order_ids": [s["id"] for s in ordered_steps]
                })

        elif game_type == CognitiveGameType.PATTERN:
            # Folk Motif Weaving Pattern
            motifs = ["◇", "○", "△", "□", "✦", "⬡"]
            for r in range(total_rounds):
                m1, m2 = random.sample(motifs, 2)
                if difficulty <= 2:
                    pattern = [m1, m2, m1, m2, m1]
                    answer = m2
                    options = [m1, m2, random.choice([m for m in motifs if m not in [m1, m2]])]
                else:
                    m3 = random.choice([m for m in motifs if m not in [m1, m2]])
                    pattern = [m1, m2, m3, m1, m2]
                    answer = m3
                    options = [m1, m2, m3, random.choice([m for m in motifs if m not in [m1, m2, m3]])]
                
                random.shuffle(options)
                rounds_data.append({
                    "round_number": r + 1,
                    "motif_pattern": pattern,
                    "prompt": "Select the symbol that completes this weaving sequence:",
                    "options": options,
                    "correct_symbol": answer
                })

        elif game_type == CognitiveGameType.RECOGNITION:
            # Cultural Heritage Item Recognition
            for r in range(total_rounds):
                target_id = random.choice(ITEM_POOL)
                target_item = LocalizationService.get_cultural_item(target_id, language)
                
                other_ids = [i for i in ITEM_POOL if i != target_id]
                options_ids = [target_id] + random.sample(other_ids, min(3, len(other_ids)))
                options = [LocalizationService.get_cultural_item(oid, language) for oid in options_ids]
                random.shuffle(options)
                
                rounds_data.append({
                    "round_number": r + 1,
                    "question": f"Which of the following is {target_item['label']}?",
                    "symbol_hint": target_item["symbol"],
                    "category": target_item["category"],
                    "correct_id": target_id,
                    "options": options
                })

        return {
            "session_id": session_id,
            "patient_id": patient_id,
            "game_type": game_type,
            "game_name": game_meta.name,
            "cognitive_domain": game_meta.cognitive_domain.value,
            "difficulty_level": difficulty,
            "language": language,
            "instructions": instructions,
            "total_rounds": total_rounds,
            "rounds_data": rounds_data,
            "created_at": utc_now_iso()
        }
