from abc import ABC, abstractmethod

from src.dolphin.types import PromptConfig


class PromptBuilder(ABC):
    """Abstract base class for building prompts.

    Provides structured prompt building capabilities.
    Follows the builder pattern for complex prompt construction.
    """

    def __init__(self, config: PromptConfig):
        self._config = config

    @abstractmethod
    def build_system_prompt(self) -> str:
        """Builds the system prompt based on the configuration."""
        pass

    @abstractmethod
    def build_review_prompt(self) -> str:
        """Builds the code review prompt based on the configuration."""
        pass
