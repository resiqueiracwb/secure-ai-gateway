from app.security.authorization import (
    require_admin
)

from fastapi import APIRouter, status, Depends
from app.utils.logger import logger
from app.security.dependencies import (
    get_current_user
)

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
def process_prompt(
    request: PromptRequest,
    current_user: dict = Depends(
        require_admin
    )
):

    logger.info(
        f"Received prompt request "
        f"using provider={request.provider}"
    )

    normalized = AIService.process_prompt(
        request.prompt,
        request.provider.value
    )

    logger.info(
        "Prompt processed successfully"
    )

    return PromptResponse(
        message="Prompt processed successfully",
        provider=request.provider,
        normalized_prompt=normalized
    )