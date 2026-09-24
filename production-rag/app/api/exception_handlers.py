from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.llm.errors import LLMProviderError, LLMServiceError, LLMTimeoutError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(LLMTimeoutError)
    async def handle_llm_timeout(_: Request, exc: LLMTimeoutError) -> JSONResponse:
        return JSONResponse(status_code=504, content={"detail": str(exc)})

    @app.exception_handler(LLMServiceError)
    async def handle_llm_service_error(_: Request, exc: LLMServiceError) -> JSONResponse:
        if exc.status_code == 429:
            return JSONResponse(status_code=429, content={"detail": str(exc)})
        return JSONResponse(status_code=502, content={"detail": str(exc)})

    @app.exception_handler(LLMProviderError)
    async def handle_llm_provider_error(_: Request, exc: LLMProviderError) -> JSONResponse:
        return JSONResponse(status_code=502, content={"detail": str(exc)})
