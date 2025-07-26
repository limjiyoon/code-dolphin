from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Protocol


class ReviewStatus(Enum):
    """Status of code review process."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True)
class CodeBlock:
    """Represents a block of code with metadata."""

    file_path: Path
    content: str
    start_line: int
    end_line: int
    class_name: str | None = None
    function_name: str | None = None

    def __str__(self) -> str:
        file_info = f"{self.file_path}:{self.start_line}-{self.end_line}"
        class_info = f"{self.class_name}" if self.class_name else ""
        function_info = f".{self.function_name}" if self.function_name else ""
        return f"{file_info} ({class_info}{function_info})\ncontent:\n{self.content}"

    def __repr__(self) -> str:
        return (
            f"CodeBlock(file_path={self.file_path}, "
            f"start_line={self.start_line}, "
            f"end_line={self.end_line}, "
            f"class_name={self.class_name}, "
            f"function_name={self.function_name})"
            f"content={self.content[:50]}..."  # Show first 50 characters of content
        )


@dataclass(frozen=True)
class GitDiff:
    """Represents a Git diff with metadata."""

    file_path: Path
    diff_content: str
    added_lines: list[int]
    removed_lines: list[int]
    modified_lines: list[int]


@dataclass(frozen=True)
class ReviewResult:
    """Result of code review analysis."""

    status: ReviewStatus
    issues: list[str]
    suggestions: list[str]
    score: float
    summary: str
    reviewed_files: list[Path]
    # focus: ReviewFocus


@dataclass(frozen=True)
class ExplorationQuery:
    """Query for code exploration."""

    file_pattern: str | None = None
    module_path: str | None = None
    class_name: str | None = None
    function_name: str | None = None
    keywords: list[str] | None = None


@dataclass(frozen=True)
class PromptConfig:
    """Configuration for prompt generation."""

    # focus: ReviewFocus
    max_context_lines: int = 50
    include_file_trees: bool = True
    include_commit_messages: bool = False
    custom_instructions: str = ""


class LLMResponse(Protocol):
    """Protocol for LLM response."""

    content: str
    metadata: dict[str, Any]
