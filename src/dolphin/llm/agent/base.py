from abc import ABC, abstractmethod

from loguru import logger

from dolphin.code_explorer.base import CodeExplorer
from dolphin.llm.llm_provider.base import LLMProvider
from dolphin.types import CodeBlock, ReviewResult


class ReviewAgent(ABC):
    """Abstract base class for code review agents.

    Orchestrates the review process by coordinating code exploration, and analysis pahses.
    Follows the template method pattern for consistent review workflows.
    """

    def __init__(self, llm_provider: LLMProvider, code_explorer: CodeExplorer):
        self._llm_provider = llm_provider
        self._code_explorer = code_explorer

    def review_code(self, is_staged_only: bool = False, depth: int = -1) -> ReviewResult:
        """Execute the code review process.

        This is the main entry point for the review process.

        Args:
            base_branch (str): Branch to compare changes against, defaults to "main".
            is_staged_only (bool, optional): If true, only staged changes are compared.

        Returns:
            ReviewResult: Result of the code review process.

        Raises:
            ReviewError: Fails if any step in the review process fails.
        """
        logger.info("Starting code review process...")

        git_diffs = self._explore_git_diff(is_staged_only=is_staged_only)
        related_code = self._explore_related_code(git_diffs, depth=depth)
        try:
            review_result = self._review(git_diffs, related_code)
            logger.info(f"Code review completed with status: {review_result.status}")
            return review_result
        except Exception as e:
            logger.error(f"Code review failed with exception: {e}")
            # TODO: Create Faield ReviewResult by factory method
            return ReviewResult(
                status="failed",
                issues=[f"Review process failed: {str(e)}"],
                suggestions=[],
                score=0.0,
                summary="Code review process failed due to an system error.",
                reviewed_files=[],
            )

    @abstractmethod
    def _explore_git_diff(self, is_staged_only: bool) -> list[CodeBlock]:
        """Explore git diff context.

        Args:
            is_staged_only (bool): If true, only staged changes are compared.

        Returns:
            list[CodeBlock]: List of Git diffs representing changes.
        """
        ...

    @abstractmethod
    def _explore_related_code(self, git_diffs: list[CodeBlock], depth: int) -> list[CodeBlock]:
        """Explore related code based on Git diffs.

        Args:
            git_diffs (list[CodeBlock]): List of Git diffs to explore.
            depth (int): Depth to explore. if -1, explore all related code.

        Returns:
            list[str]: List of related code snippets.
        """
        ...

    @abstractmethod
    def _review(
        self,
        git_diffs: list[CodeBlock],
        related_code: list[CodeBlock],
    ) -> ReviewResult:
        """Perform code review analysis.

        Args:
            git_diffs (list[CodeBlock]): List of Git diffs to review.
            related_code (list[CodeBlock]): List of related code snippets.

        Returns:
            ReviewResult: Result of the code review analysis.
        """
        ...
