from abc import ABC, abstractmethod
from pathlib import Path

from dolphin.types import CodeBlock, ExplorationQuery, GitDiff


class CodeExplorer(ABC):
    """Abstract base class for code exploration.

    Handles discovery and retrieval of code blocks or git diff based on various queries.
    """

    def __init__(self, project_root: Path) -> None:
        """Initialize the code explorer with a project root directory.

        Args:
            project_root (Path): The root directory of the project to explore.

        Raises:
            ValueError: If the project root is not a valid directory.
        """
        if not project_root.is_dir():
            msg = f"Project root ({project_root}) is not a valid directory."
            raise ValueError(msg)
        self._project_root = project_root

    @abstractmethod
    def get_git_diff(self, base_bracnh: str = "main") -> list[GitDiff]:
        """Get git diff information for the current branch.

        Args:
            base_bracnh (str): The base branch to compare against. Defaults to "main".

        Returns:
            list[GitDiff]: A list of GitDiff objects containing the diff information.

        Raises:
            GitError: If git operations fails.
        """
        ...

    @abstractmethod
    def find_code_blocks(self, query: ExplorationQuery) -> list[CodeBlock]:
        """Find code blocks matching the given query.

        Args:
            query (ExplorationQuery): The query to search for code blocks.

        Returns:
            list[CodeBlock]: A list of CodeBlock objects matching the query.

        Raises:
            ExplorationError: If exploration fails.
        """
        ...
        ...

    @abstractmethod
    def get_related_code(self, file_path: Path, context_lines: int = 5) -> list[CodeBlock]:
        """Get code blocks related to a specific file.

        Args:
            file_path (Path): The path to the file to explore.
            context_lines (int): Number of context lines to include around the code block.

        Returns:
            list[CodeBlock]: A list of CodeBlock objects related to the file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        ...

    @abstractmethod
    def get_file_dependencies(self, file_path: Path) -> list[Path]:
        """Get dependencies for a specific file.

        Args:
            file_path (Path): The path to the file to analyze.

        Returns:
            list[Path]: A list of Paths representing the dependencies of the file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        ...
