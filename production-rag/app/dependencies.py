from functools import lru_cache

from fastapi import Depends, HTTPException, status

from app.llm import LLMProvider, OpenAIProvider
from app.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_llm_provider(settings: Settings = Depends(get_settings)) -> LLMProvider:
    if not settings.openai_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OPENAI_API_KEY is not configured",
        )

    return OpenAIProvider(
        api_key=settings.openai_api_key,
        default_model=settings.openai_model,
        timeout_seconds=settings.llm_timeout_seconds,
    )
