class LLMClientError(Exception):
    """Raised when LLM client operations fails."""


class CodeExplorationError(Exception):
    """Raised when code exploration fails."""


class GitError(Exception):
    """Raised when Git operations fail."""


class ReviewError(Exception):
    """Raised when code review operations fail."""


class PromptBuilderError(Exception):
    """Raised when prompt building operations fail."""


class CodeAnalysisError(Exception):
    """Raised when code analysis operations fail."""


class ReportGenerationError(Exception):
    """Raised when report generation operations fail."""
