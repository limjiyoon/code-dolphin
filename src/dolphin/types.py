from enum import Enum
from dataclasses import dataclass
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


@dataclass(frozen=True)
class ExplorationQuery:
    """Query for code exploration."""

    file_pattern: str | None = None
    module_path: str | None = None
    class_name: str | None = None
    function_name: str | None = None
    keywords: list[str] | None = None


class LLMResponse(Protocol):
    """Protocol for LLM response."""

    content: str
    metadata: dict[str, Any]

