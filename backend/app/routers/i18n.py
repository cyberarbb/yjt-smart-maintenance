"""다국어(i18n) API 라우터"""
from fastapi import APIRouter
from app.services.i18n_service import (
    SUPPORTED_LANGUAGES, get_all_translations, get_translation
)

router = APIRouter()


@router.get("/languages")
def list_languages():
    """지원 언어 목록"""
    return SUPPORTED_LANGUAGES


@router.get("/translations/{lang}")
def get_translations(lang: str):
    """특정 언어의 전체 번역 데이터"""
    if lang not in SUPPORTED_LANGUAGES:
        lang = "en"
    return {
        "language": lang,
        "dir": SUPPORTED_LANGUAGES[lang]["dir"],
        "translations": get_all_translations(lang),
    }
