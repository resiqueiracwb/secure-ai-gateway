from fastapi import APIRouter
from app.models.request_models import PromptRequest

router = APIRouter()

@router.post("/prompt")
def process_prompt(request: PromptRequest):
    return {
        "received": request.prompt
    }