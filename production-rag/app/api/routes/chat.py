from fastapi import APIRouter, Depends

from app.api.schemas.chat import ChatRequest, ChatResponse
from app.dependencies import get_llm_provider
from app.llm import LLMMessage, LLMProvider, LLMRequest

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    llm_provider: LLMProvider = Depends(get_llm_provider),
) -> ChatResponse:
    llm_response = await llm_provider.generate(
        LLMRequest(
            messages=[
                LLMMessage(role=message.role, content=message.content)
                for message in request.messages
            ],
            model=request.model,
            temperature=request.temperature,
        )
    )

    return ChatResponse(
        answer=llm_response.content,
        model=llm_response.model,
        prompt_tokens=llm_response.prompt_tokens,
        completion_tokens=llm_response.completion_tokens,
    )
