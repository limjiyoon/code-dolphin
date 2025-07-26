from dataclasses import dataclass
from typing import Any

import ollama
from loguru import logger

from dolphin.llm.llm_provider.base import LLMProvider
from dolphin.types import LLMResponse


@dataclass
class OllamaResponse:
    """Response class for Ollama LLM responses."""

    content: str
    metadata: dict[str, Any]


class OllamaProvider(LLMProvider):
    """LLM provider for Ollama.

    This class implements the LLMProvider interface for Ollama.
    It provides methods to interact with the Ollama API for code review tasks.
    """

    def __init__(
        self,
        model_name: str,
        base_url: str = "http://localhost:11434",  # Default Ollama API URL
    ):
        self._base_url = base_url
        self._model_name = model_name
        self._client = ollama.Client(
            host=self._base_url,
        )

    @property
    def provider_info(self) -> dict[str, Any]:
        """Returns provider information."""
        return {
            "name": "Ollama",
            "model_name": self._model_name,
            "base_url": self._base_url,
        }

    def generate_response(
        self,
        prompt: str,
        *,
        temperature: float = 0.1,
        system_prompt: str | None = None,
    ) -> LLMResponse:
        """Generate responses."""
        logger.debug(f"Generating response using Ollama model: {self._model_name}")
        response = self._client.generate(
            model=self._model_name,
            prompt=prompt,
            system=system_prompt,
            options={
                "temperature": temperature,
            },
        )
        response = response.model_dump()

        return OllamaResponse(content=response.pop("content", ""), metadata=response)

    def is_available(self) -> bool:
        """Check if the Ollama model is available."""
        # TODO: Implement a more robust availability check
        return True
