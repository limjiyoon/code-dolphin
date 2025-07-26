
from dolphin.code_explorer.git_diff_explorer import GitDiffExplorer
from dolphin.llm.agent.dummy import DummyAgent
from dolphin.llm.llm_provider.ollama_provider import OllamaProvider


def review_code() -> None:
    project_root = "/Users/jiyoonlim/study/side_project/gemini-project/code-dolphin"
    target_branch = "main"
    model = "devstral:latest"
    ollama_url = "http://localhost:11434"

    llm_provider = OllamaProvider(
        model_name=model,
        base_url=ollama_url,
    )
    code_explorer = GitDiffExplorer(project_root=project_root, target_branch=target_branch)
    agent = DummyAgent(
        llm_provider=llm_provider,
        code_explorer=code_explorer,
    )
    print(agent.review_code())


if __name__ == "__main__":
    review_code()
    print("Code review process initiated.")
