from typing import List
from fastapi import APIRouter, HTTPException, status
from app.schemas import LanguageInfo, LocalizedContentResponse, TranslationRequest, TranslationResponse
from app.services.localization_service import LocalizationService, SUPPORTED_LANGUAGES

router = APIRouter(tags=["Multilingual & NER Languages"])

@router.get("/api/languages", response_model=List[LanguageInfo])
@router.get("/languages", response_model=List[LanguageInfo])
def list_supported_languages():
    """Lists all supported North Eastern languages with metadata and voice support flags."""
    return LocalizationService.get_supported_languages()

@router.get("/api/languages/content/{language_code}", response_model=LocalizedContentResponse)
@router.get("/content/{language_code}", response_model=LocalizedContentResponse)
def get_localized_content(language_code: str):
    """Retrieves localized prompts, instructions, and cultural object dictionary for a language."""
    if language_code.lower() not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Language '{language_code}' is not supported. Supported codes: {list(SUPPORTED_LANGUAGES.keys())}"
        )
    return LocalizationService.get_localized_content(language_code)

@router.post("/api/languages/translate", response_model=TranslationResponse)
@router.post("/translate", response_model=TranslationResponse)
def translate_phrase(req: TranslationRequest):
    """Translates text across NER languages using the cultural dictionary and localization layer."""
    res = LocalizationService.translate_text(
        text=req.text,
        source_lang=req.source_language,
        target_lang=req.target_language
    )
    return TranslationResponse(**res)
