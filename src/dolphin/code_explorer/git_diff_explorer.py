import subprocess
from pathlib import Path

from dolphin.code_explorer.base import CodeExplorer
from dolphin.types import CodeBlock


class GitDiffExplorer(CodeExplorer):
    def __init__(self, project_root: str, target_branch: str = "main") -> None:
        super().__init__(Path(project_root))
        self._target_branch = target_branch

    def explore(self) -> list[CodeBlock]:
        """Get git diff information for the current branch.

        Returns:
            list[CodeBlock]: A list of GitDiff objects containing the diff information.

        Raises:
            GitError: If git operations fails.
        """
        name_only_option = ["--name-only", "*.py"]
        diff_python_files = self._execute_git_diff_cmd(name_only_option).splitlines()

        diffs = []
        for file_path in diff_python_files:
            if file_path:
                diff_file_option = ["--", file_path, "--ignore-space-at-eol"]
                diff_result = self._execute_git_diff_cmd(diff_file_option)
                start_line, end_line = -1, -1
                for line in diff_result.splitlines():
                    if line.startswith("@@"):
                        # Diff hunk header format: @@ -start_line,delta_line +start_line,delta_line @@
                        # Extract later start and end lines from the hunk header
                        # Example: @@ -10,6 +10,7 @@
                        # Uses: start_line=10, end_line=17
                        start_line, delta_line = map(int, line.strip().strip("@").strip().split()[1].split(","))
                        end_line = start_line + delta_line
                        break

                diffs.append(
                    CodeBlock(
                        file_path=Path(file_path),
                        content=diff_result,
                        start_line=start_line,  # Placeholder, as we don't have line numbers in git diff
                        end_line=end_line,  # Placeholder, as we don't have line numbers in git diff
                        class_name=None,  # Placeholder, as we don't extract class names from git diff
                        function_name=None,
                    )
                )
        return diffs

    def _execute_git_diff_cmd(self, options: list[str]) -> str:
        """Execute a git command and return the output.

        Args:
            options (list[str]): The git command options to execute.

        Returns:
            str: The output of the git command.

        Raises:
            subprocess.CalledProcessError: If the git command fails.
        """
        git_cmd = ["git", "--no-pager", "diff", self._target_branch] + options
        result = subprocess.run(
            cwd=self._project_root,
            args=git_cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
