from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class Provider(str, Enum):
    OPENAI = "openai"
    CLAUDE = "claude"
    GEMINI = "gemini"


class Metadata(BaseModel):
    source: str
    priority: int = Field(ge=1, le=5)


class PromptRequest(BaseModel):
    prompt: str = Field(
        min_length=5,
        max_length=500,
        description="User prompt input"
    )

    provider: Provider

    temperature: float = Field(
        default=0.7,
        ge=0,
        le=1
    )

    max_tokens: int = Field(
        default=200,
        ge=10,
        le=4000
    )

    tags: Optional[List[str]] = None

    metadata: Optional[Metadata] = None