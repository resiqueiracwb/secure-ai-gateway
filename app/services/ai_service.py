from app.exceptions.custom_exceptions import (
    ProviderNotSupportedException
)


class AIService:

    SUPPORTED_PROVIDERS = [
        "openai",
        "claude",
        "gemini"
    ]

    @staticmethod
    def process_prompt(
        prompt: str,
        provider: str
    ):

        if provider not in AIService.SUPPORTED_PROVIDERS:
            raise ProviderNotSupportedException(
                provider
            )

        return prompt.strip().upper()