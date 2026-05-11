from enum import Enum

from fastapi import APIRouter, status
from app.utils.logger import logger

from app.models.prompt_models import (
    PromptRequest,
    PromptResponse
)
from app.services.ai_service import AIService
router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.post(
    "/prompt",
    response_model=PromptResponse,
    status_code=status.HTTP_200_OK,
    summary="Process AI prompt",
    description="Receives and validates AI prompt requests"
)
def process_prompt(request: PromptRequest):
    logger.info(
        f"Received prompt request using provider={request.provider}"
    )
    normalized = AIService.process_prompt(
        request.prompt
    )

    logger.info(
        "Prompt processed successfully"
    )

    return PromptResponse(
        message="Prompt processed successfully",
        provider=request.provider,
        normalized_prompt=normalized
    )