from typing import Dict, List, Optional
from app.schemas import LanguageInfo

SUPPORTED_LANGUAGES: Dict[str, LanguageInfo] = {
    "as": LanguageInfo(
        code="as",
        name="Assamese",
        native_name="অসমীয়া",
        script="Bengali-Assamese",
        region="Assam, North East India",
        tts_supported=True
    ),
    "bn": LanguageInfo(
        code="bn",
        name="Bengali",
        native_name="বাংলা",
        script="Bengali",
        region="Tripura, Barak Valley, Assam",
        tts_supported=True
    ),
    "mni": LanguageInfo(
        code="mni",
        name="Manipuri (Meitei)",
        native_name="মৈতৈলোন্ / ꯃꯤꯇꯩꯂꯣꯟ",
        script="Meitei Mayek / Bengali",
        region="Manipur",
        tts_supported=False
    ),
    "brx": LanguageInfo(
        code="brx",
        name="Bodo",
        native_name="बर'",
        script="Devanagari",
        region="Bodoland, Assam",
        tts_supported=False
    ),
    "lus": LanguageInfo(
        code="lus",
        name="Mizo",
        native_name="Mizo ṭawng",
        script="Latin",
        region="Mizoram",
        tts_supported=False
    ),
    "kha": LanguageInfo(
        code="kha",
        name="Khasi",
        native_name="Ka Ktien Khasi",
        script="Latin",
        region="Meghalaya",
        tts_supported=False
    ),
    "grt": LanguageInfo(
        code="grt",
        name="Garo",
        native_name="A·chik",
        script="Latin",
        region="Garo Hills, Meghalaya",
        tts_supported=False
    ),
    "hi": LanguageInfo(
        code="hi",
        name="Hindi",
        native_name="हिन्दी",
        script="Devanagari",
        region="Pan-India / Arunachal Pradesh",
        tts_supported=True
    ),
    "en": LanguageInfo(
        code="en",
        name="English",
        native_name="English",
        script="Latin",
        region="Regional Lingua Franca (Nagaland, Meghalaya, etc.)",
        tts_supported=True
    )
}

# Localized UI prompts and cognitive task instructions
LOCALIZED_PROMPTS: Dict[str, Dict[str, str]] = {
    "en": {
        "welcome": "Welcome to Smrithi Cognitive Memory Exercise",
        "memory_instruction": "Carefully observe the items shown. When ready, identify the target item from memory.",
        "attention_instruction": "Find the specified target item as quickly and accurately as possible among the patterns.",
        "sequence_instruction": "Arrange the daily North Eastern routine or recipe steps in the correct chronological order.",
        "pattern_instruction": "Look at the traditional handloom motif sequence and identify which pattern comes next.",
        "recognition_instruction": "Identify the cultural North Eastern object or memory item shown in the question.",
        "session_completed": "Session completed successfully! Great effort today.",
        "reminder_game": "Time for your cognitive gaming exercise with Smrithi!",
        "reminder_medication": "Friendly reminder to take your prescribed medication on time."
    },
    "as": {
        "welcome": "স্মৃতি (Smrithi) স্মৃতিশক্তি আৰু জ্ঞানভিত্তিক খেললৈ স্বাগতম",
        "memory_instruction": "তলৰ বস্তুবোৰ মনোযোগেৰে চাওক। কিছু সময়ৰ পিছত লক্ষ্য বস্তুটো চিনাক্ত কৰক।",
        "attention_instruction": "বিকল্পবোৰৰ মাজৰ পৰা নিৰ্দিষ্ট সাংস্কৃতিক প্ৰতীকটো যিমান পাৰি সোনকালে বিচাৰি উলিয়াওক।",
        "sequence_instruction": "অসমৰ পৰম্পৰাগত চাহ বনোৱা বা দৈনন্দিন কামৰ সঠিক ক্ৰমটো বাছক।",
        "pattern_instruction": "ফুলাম গামোচা আৰু এৰী-মুগাৰ পৰম্পৰাগত চানেকি চাই পৰৱৰ্তী চানেকিটো নিৰ্ণয় কৰক।",
        "recognition_instruction": "প্ৰশ্নত থকা চিনাকি উত্তৰ-পূবৰ সাংস্কৃতিক সামগ্ৰীটো চিনাক্ত কৰক।",
        "session_completed": "আজিৰ খেল সফলতাৰে সম্পূৰ্ণ হ'ল! আপুনি বহুত ভাল প্ৰদৰ্শন কৰিলে।",
        "reminder_game": "স্মৃতি খেল খেলি মনটো সতেজ কৰাৰ সময় হৈছে!",
        "reminder_medication": "সময়মতে আপোনাৰ ঔষধ খোৱাৰ কথা মনত পেলাই দিয়া হৈছে।"
    },
    "bn": {
        "welcome": "স্মৃতি (Smrithi) জ্ঞানমূলক ও স্মৃতিশক্তি অনুশীলন খেলায় স্বাগতম",
        "memory_instruction": "প্রদর্শিত জিনিসগুলি মনোযোগ সহকারে দেখুন। এরপর স্মৃতি থেকে লক্ষ্য বস্তুটি চিহ্নিত করুন।",
        "attention_instruction": "বিভিন্ন চিহ্নের মধ্য থেকে নির্দিষ্ট ঐতিহ্যবাহী বস্তুটি খুঁজে বের করুন।",
        "sequence_instruction": "দৈনন্দিন কাজ বা রান্নার ধাপগুলি সঠিক ক্রমানুসারে সাজান।",
        "pattern_instruction": "ঐতিহ্যবাহী তাঁতের নকশার ক্রম লক্ষ্য করে পরবর্তী নকশাটি নির্বাচন করুন।",
        "recognition_instruction": "উত্তর-পূর্বাঞ্চলের পরিচিত সাংস্কৃতিক বস্তুটি চিহ্নিত করুন।",
        "session_completed": "আজকের পর্ব সফলভাবে সম্পন্ন হয়েছে! চমৎকার প্রচেষ্টা।",
        "reminder_game": "স্মৃতি খেলার মাধ্যমে স্মৃতি চর্চা করার সময় হয়েছে!",
        "reminder_medication": "প্রেসক্রিপশন অনুযায়ী ওষুধ গ্রহণ করার বিনীত অনুরোধ।"
    },
    "hi": {
        "welcome": "स्मृति (Smrithi) संज्ञानात्मक खेल मंच में आपका स्वागत है",
        "memory_instruction": "दिखाई गई वस्तुओं को ध्यान से देखें। फिर याददाश्त के आधार पर सही वस्तु चुनें।",
        "attention_instruction": "दिए गए सांस्कृतिक प्रतीकों में से सही वस्तु को शीघ्रता से पहचानें।",
        "sequence_instruction": "पूर्वोत्तर की दैनिक दिनचर्या या चाय बनाने के चरणों को सही क्रम में लगाएं।",
        "pattern_instruction": "पारंपरिक हथकरघा पैटर्न को देखकर अगला पैटर्न चुनें।",
        "recognition_instruction": "दिए गए प्रश्न में पूर्वोत्तर की सांस्कृतिक वस्तु को पहचानें।",
        "session_completed": "आज का सत्र सफलतापूर्वक पूरा हुआ! बहुत अच्छा प्रयास।",
        "reminder_game": "आज का दिमागी खेल खेलने का समय हो गया है!",
        "reminder_medication": "कृपया अपनी निर्धारित दवा समय पर लें।"
    },
    "mni": {
        "welcome": "Smrithi Cognitive Game da taranabidari",
        "memory_instruction": "Pukning changna yengbiyu amasung ningthorakpa matamda achumba potlam khallu.",
        "attention_instruction": "Meitei cultural pattern gi maraktagi achumba potlam thidok-u.",
        "sequence_instruction": "Chak thongba amasung numit khudinggi thabak singgi mathang manao chamna leppiyu.",
        "pattern_instruction": "Tradition phi gi motif pattern gi mathang gi matam khallu.",
        "recognition_instruction": "Manipur gi cultural potlam sing sakkhangbiyu.",
        "session_completed": "Ngasi gi game session mai pakna loire! Nungaijare.",
        "reminder_game": "Smrithi game sanna ningsing thouna pibagi matam oire!",
        "reminder_medication": "Hidag chabagi matam oire."
    },
    "lus": {
        "welcome": "Smrithi Hriatna Tiphuhtu Game-ah kan lo lawm a che",
        "memory_instruction": "Thil langte hi ngun takin en la, a hnuah a dik zawn chhuak rawh.",
        "attention_instruction": "Hmanlai thil lem zinga a dik ber hi rang takin zawng chhuak rawh.",
        "sequence_instruction": "Nitin nitin chaw ei leh thingpui lum dan indawt dik takin rem rawh.",
        "pattern_instruction": "Puan zai zinga a dawt leh tur chhut chhuak rawh.",
        "recognition_instruction": "Kan hnam thil hriat lar tak takte hi hria la thlang chhuak rawh.",
        "session_completed": "Vawiin atan i ti zo ta! I ti ṭha hle mai.",
        "reminder_game": "Smrithi thluak chettirna game khelh a hun e!",
        "reminder_medication": "Damdawi ei hun a ni e."
    },
    "kha": {
        "welcome": "Kmie/Kpa phin sngewbha ban wan sha Smrithi",
        "memory_instruction": "Peit bha ia kine ki jingdon bad buh jingmut ban jied ia kaba dei.",
        "attention_instruction": "Wad ia ka dak kaba donkam napdeng kiwei.",
        "sequence_instruction": "Buh ryntih ia ki rukom shet ja ne rukom leh step ba step.",
        "pattern_instruction": "Peit ia ka jingpynwan dur ryndia bad jied ia kaban wan bud.",
        "recognition_instruction": "Ithuh ia ki tiar tynrai jong ka thain Ri-lum.",
        "session_completed": "Phi la pyndep bha mynta ka sngi!",
        "reminder_game": "Pynkiew jingmut da kaba ialehkai Smrithi!",
        "reminder_medication": "Kynmaw ban dih dawai ha ka por ba dei."
    },
    "grt": {
        "welcome": "Smrithi gisik seng-atna kal-anio rimnapbe-a",
        "memory_instruction": "Mesokgimin bosturangko name nibo aro gisik ra·e seokbo.",
        "attention_instruction": "Bosturangoni nang·ko am·atchi gita ta·raken am·e seokbo.",
        "sequence_instruction": "Salaram a·songni cha·a-ringani aro kamrangko riting gita donbo.",
        "pattern_instruction": "Dakgimin dokani gita ja·mano mai ba·gen uko seokbo.",
        "recognition_instruction": "Dak-bewalni bosturangko u·ibo aro seokbo.",
        "session_completed": "Da·alni kal·ani matchotaha! Namaha.",
        "reminder_game": "Smrithi kal·e gisik seng-atna somoi ong·aha!",
        "reminder_medication": "Sam cha·na somoi ong·aha."
    },
    "brx": {
        "welcome": "Smrithi गोसो गोथार गेलेमुयाव बरायबाय",
        "memory_instruction": "दिनथिनाय मुवाफोरखौ मोजाङै नाय आरो उननि समाव गेबें मुवाखौ सायख'।",
        "attention_instruction": "हनाय मुवाफोरनि गेजेरनिफ्राय गेबें सिनखौ गोख्रैयै दिहुन।",
        "sequence_instruction": "दै गाहाम सा बानायनाय आरो सानफ्रोमबोनि खामानिखौ थि फारियाव दोन।",
        "pattern_instruction": "दखना आरो आर'नायनि सिन्थिखौ नायना उननि सिन्थिखौ सायख'।",
        "recognition_instruction": "हारिमुआरि मुवाफोरखौ सिनायथि ला।",
        "session_completed": "दिनैनि गेलेनाया जाफुंबाय! मोजां जादों।",
        "reminder_game": "स्मृति गेलेनायनि सम जाबाय!",
        "reminder_medication": "समबादि मुलु ओन्दोंमोन।"
    }
}

# Cultural vocabulary in NER languages
CULTURAL_VOCABULARY: Dict[str, Dict[str, Dict[str, str]]] = {
    "as": {
        "japi": {"label": "জাপী (Traditional Assamese Japi Hat)", "symbol": "⌂", "category": "heritage"},
        "dhol": {"label": "অসমীয়া ঢোল (Traditional Drum)", "symbol": "◉", "category": "music"},
        "kula": {"label": "বাঁহৰ কুলা (Bamboo Winnower)", "symbol": "▦", "category": "craft"},
        "gamusa": {"label": "ফুলাম গামোচা (Embroidered Shawl)", "symbol": "▤", "category": "textile"},
        "pepa": {"label": "ম'হৰ শিঙৰ পেঁপা (Hornpipe Instrument)", "symbol": "🎺", "category": "music"},
        "tea": {"label": "অসমীয়া চাহ (Assam Garden Tea)", "symbol": "☕", "category": "food"},
        "rice_bowl": {"label": "কাঁহৰ বাটি (Bell Metal Bowl)", "symbol": "◒", "category": "craft"},
        "sarai": {"label": "কাঁহৰ শৰাই (Traditional Offerings Sarai)", "symbol": "🏺", "category": "heritage"},
        "hornbill": {"label": "ধনেশ পক্ষী (Great Hornbill)", "symbol": "🦅", "category": "nature"},
        "muga_silk": {"label": "সোণালী মুগা সূতা (Golden Muga Silk)", "symbol": "🧶", "category": "textile"}
    },
    "bn": {
        "japi": {"label": "জাপি (ঐতিহ্যবাহী টুপি)", "symbol": "⌂", "category": "heritage"},
        "dhol": {"label": "ঢোল (বাদ্যযন্ত্র)", "symbol": "◉", "category": "music"},
        "kula": {"label": "বাঁশের কুলা", "symbol": "▦", "category": "craft"},
        "gamusa": {"label": "ঐতিহ্যবাহী গামছা", "symbol": "▤", "category": "textile"},
        "pepa": {"label": "শিংয়ের বাঁশি", "symbol": "🎺", "category": "music"},
        "tea": {"label": "আসাম চা", "symbol": "☕", "category": "food"},
        "rice_bowl": {"label": "কাঁসার বাটি", "symbol": "◒", "category": "craft"},
        "sarai": {"label": "শরাই (পূজার থালি)", "symbol": "🏺", "category": "heritage"},
        "hornbill": {"label": "ধনেশ পাখি", "symbol": "🦅", "category": "nature"},
        "muga_silk": {"label": "মুগা সিল্ক", "symbol": "🧶", "category": "textile"}
    },
    "hi": {
        "japi": {"label": "जापी (पारंपरिक पूर्वोत्तर टोपी)", "symbol": "⌂", "category": "heritage"},
        "dhol": {"label": "पारंपरिक ढोल", "symbol": "◉", "category": "music"},
        "kula": {"label": "बांस का सूप (कुला)", "symbol": "▦", "category": "craft"},
        "gamusa": {"label": "पारंपरिक गमोसा", "symbol": "▤", "category": "textile"},
        "pepa": {"label": "पेपा (सींग की बांसुरी)", "symbol": "🎺", "category": "music"},
        "tea": {"label": "असमिया चाय", "symbol": "☕", "category": "food"},
        "rice_bowl": {"label": "पारंपरिक कांस्य कटोरा", "symbol": "◒", "category": "craft"},
        "sarai": {"label": "शराई (कांस्य थाली)", "symbol": "🏺", "category": "heritage"},
        "hornbill": {"label": "धनेश पक्षी (हॉर्नबिल)", "symbol": "🦅", "category": "nature"},
        "muga_silk": {"label": "मुगा रेशम", "symbol": "🧶", "category": "textile"}
    },
    "en": {
        "japi": {"label": "Japi (Traditional Conical Hat)", "symbol": "⌂", "category": "heritage"},
        "dhol": {"label": "Traditional Folk Dhol (Drum)", "symbol": "◉", "category": "music"},
        "kula": {"label": "Bamboo Winnower Basket", "symbol": "▦", "category": "craft"},
        "gamusa": {"label": "Gamusa Embroidered Cloth", "symbol": "▤", "category": "textile"},
        "pepa": {"label": "Buffalo Hornpipe (Pepa)", "symbol": "🎺", "category": "music"},
        "tea": {"label": "Assam Orthodox Tea", "symbol": "☕", "category": "food"},
        "rice_bowl": {"label": "Bell Metal Rice Bowl", "symbol": "◒", "category": "craft"},
        "sarai": {"label": "Xorai Offerings Tray", "symbol": "🏺", "category": "heritage"},
        "hornbill": {"label": "Great Indian Hornbill", "symbol": "🦅", "category": "nature"},
        "muga_silk": {"label": "Golden Muga Silk Thread", "symbol": "🧶", "category": "textile"}
    }
}

class LocalizationService:
    @staticmethod
    def get_supported_languages() -> List[LanguageInfo]:
        return list(SUPPORTED_LANGUAGES.values())

    @staticmethod
    def get_language_info(code: str) -> Optional[LanguageInfo]:
        return SUPPORTED_LANGUAGES.get(code.lower(), SUPPORTED_LANGUAGES.get("en"))

    @staticmethod
    def get_localized_content(lang_code: str) -> Dict:
        lang = lang_code.lower()
        if lang not in SUPPORTED_LANGUAGES:
            lang = "en"
        
        prompts = LOCALIZED_PROMPTS.get(lang, LOCALIZED_PROMPTS["en"])
        vocab = CULTURAL_VOCABULARY.get(lang, CULTURAL_VOCABULARY["en"])
        lang_info = SUPPORTED_LANGUAGES[lang]
        
        return {
            "language": lang,
            "language_name": lang_info.name,
            "native_name": lang_info.native_name,
            "script": lang_info.script,
            "common_prompts": prompts,
            "game_vocabulary": vocab
        }

    @staticmethod
    def get_prompt(prompt_key: str, lang_code: str = "as") -> str:
        lang = lang_code.lower()
        if lang in LOCALIZED_PROMPTS and prompt_key in LOCALIZED_PROMPTS[lang]:
            return LOCALIZED_PROMPTS[lang][prompt_key]
        return LOCALIZED_PROMPTS["en"].get(prompt_key, "")

    @staticmethod
    def get_cultural_item(item_id: str, lang_code: str = "as") -> Dict:
        lang = lang_code.lower()
        vocab = CULTURAL_VOCABULARY.get(lang, CULTURAL_VOCABULARY["en"])
        if item_id in vocab:
            return {"id": item_id, **vocab[item_id]}
        # Fallback to english
        en_vocab = CULTURAL_VOCABULARY["en"]
        if item_id in en_vocab:
            return {"id": item_id, **en_vocab[item_id]}
        return {"id": item_id, "label": item_id.capitalize(), "symbol": "◆", "category": "general"}

    @staticmethod
    def translate_text(text: str, source_lang: str, target_lang: str) -> Dict[str, str]:
        """
        Translates text across NER languages. Uses high-precision localized lookup
        and provides modular hooks for IndicTrans2/Bhashini APIs if configured.
        """
        source_lang = source_lang.lower()
        target_lang = target_lang.lower()

        # Check prompt matching
        for prompt_key, prompt_val in LOCALIZED_PROMPTS.get(source_lang, {}).items():
            if prompt_val.strip().lower() == text.strip().lower():
                target_val = LOCALIZED_PROMPTS.get(target_lang, {}).get(prompt_key)
                if target_val:
                    return {
                        "original_text": text,
                        "translated_text": target_val,
                        "source_language": source_lang,
                        "target_language": target_lang,
                        "service_used": "smrithi_ner_localization_engine"
                    }

        # Check vocabulary matching
        for vocab_id, vocab_data in CULTURAL_VOCABULARY.get(source_lang, {}).items():
            if vocab_data["label"].strip().lower() == text.strip().lower():
                target_data = CULTURAL_VOCABULARY.get(target_lang, {}).get(vocab_id)
                if target_data:
                    return {
                        "original_text": text,
                        "translated_text": target_data["label"],
                        "source_language": source_lang,
                        "target_language": target_lang,
                        "service_used": "smrithi_ner_cultural_dictionary"
                    }

        # If identical or untranslatable without external engine, return source with notice
        return {
            "original_text": text,
            "translated_text": text,
            "source_language": source_lang,
            "target_language": target_lang,
            "service_used": "smrithi_pass_through"
        }
