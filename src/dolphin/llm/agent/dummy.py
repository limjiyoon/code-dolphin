from dolphin.llm.agent.base import ReviewAgent
from dolphin.types import CodeBlock


class DummyAgent(ReviewAgent):
    """Dummy agent for testing purposes.

    This agent does not perform any actual code review but serves as a placeholder.
    It can be used to test the integration of the review process without requiring a real LLM or code explorer.
    """

    def _explore_git_diff(self, is_staged_only: bool) -> list:
        """Returns an empty list to simulate no git diffs."""
        return self._code_explorer.explore()

    def _explore_related_code(self, git_diffs: list[CodeBlock], depth: int = -1) -> list:
        """Returns an empty list to simulate no related code."""
        return []

    def _review(self, git_diffs: list, related_code: list) -> dict:
        """Returns a dummy review result."""
        response = self._llm_provider.generate_response(
            prompt=f"Review the code in this project. Code diffs: {str(git_diffs)}",
            temperature=0.1,
            system_prompt="You are an expert code reviewer.",
        )
        return {
            "review": response.content,
        }
        # return {
        #     "status": "success",
        #     "issues": [],
        #     "suggestions": [],
        #     "score": 1.0,
        #     "summary": "Dummy review completed successfully.",
        #     "reviewed_files": [],
        # }
