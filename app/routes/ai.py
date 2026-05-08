from fastapi import APIRouter
from app.models.request_models import PromptRequest

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.post(
    "/prompt",
    summary="Process AI prompt",
    description="Receives and validates an AI prompt request"
)
def process_prompt(request: PromptRequest):

    return {
        "message": "Prompt processed successfully",
        "provider": request.provider,
        "temperature": request.temperature,
        "prompt": request.prompt
    }