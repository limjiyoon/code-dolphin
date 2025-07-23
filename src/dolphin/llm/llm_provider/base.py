from abc import ABC, abstractmethod

from dolphin.types import LLMResponse

class LLMProviders(ABC):
    """Abstract base class for LLM providers implementations."""

    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        *,
        max_tokens: int = 4000,
        temperature: float = 0.1,
        system_prompt: str | None = None,
    ) -> LLMResponse:
        """Generate response from LLM.

        Args:
            prompt (str): The input prompt for the LLM.
            max_tokens (int): Maximum number of tokens in response.
            temperature ( float ): Sampling temperature for response generation.
            system_prompt (str | None): Optional system prompt to set context.

        Returns:
            LLMResponse: containing the generated content and metadata.

        Raises:
            LLMClientError: If the LLM request fails.
        """
        ...

    @abstractmethod
    async def is_available(self) -> bool:
        """Check if the LLM provider is available.

        Returns:
            bool: True if the provider is available, False otherwise.
        """
        ...

    @abstractmethod
    def get_model_info(self) -> dict[str, str]:
        """Get information about the LLM model being used.

        Returns:
            dict[str, str]: Dictionary containing model information.
        """
        ...

