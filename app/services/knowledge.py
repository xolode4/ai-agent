import os
from pathlib import Path
from git import Repo, GitCommandError
import yaml
from typing import Dict, List

def load_knowledge_sources() -> Dict:
    """Загрузка конфигурации репозиториев из YAML"""
    with open("knowledge_sources.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def setup_ssh_wrapper(repo_path: Path):
    """Создаем SSH wrapper для корректной работы Git в Docker"""
    wrapper = repo_path / "git_ssh_wrapper.sh"
    wrapper.write_text("""#!/bin/sh
exec ssh -o StrictHostKeyChecking=no -i /root/.ssh/id_ed25519 "$@"
""")
    os.chmod(wrapper, 0o755)
    return wrapper

def clone_repo(repo_url: str, repo_path: Path, branch: str):
    """Клонирование репозитория через SSH"""
    wrapper = setup_ssh_wrapper(repo_path.parent)
    env = {
        'GIT_SSH': str(wrapper),
        'GIT_TERMINAL_PROMPT': '0'
    }
    Repo.clone_from(
        repo_url,
        str(repo_path),
        branch=branch,
        env=env
    )

def update_repo(repo: Repo):
    """Обновление существующего репозитория"""
    wrapper = setup_ssh_wrapper(Path(repo.working_dir).parent)
    with repo.git.custom_environment(GIT_SSH=str(wrapper)):
        repo.remotes.origin.pull()

def load_repo(env: str, repo_url: str, branch: str) -> Repo:
    """Загрузка или обновление репозитория"""
    safe_env = env.replace(" ", "_")
    repo_path = Path("knowledge") / safe_env
    
    try:
        if repo_path.exists():
            repo = Repo(repo_path)
            update_repo(repo)
        else:
            # Преобразуем HTTPS URL в SSH, если нужно
            if repo_url.startswith("https://"):
                repo_url = repo_url.replace("https://", "git@").replace("/", ":", 1)
            clone_repo(repo_url, repo_path, branch)
            repo = Repo(repo_path)
        return repo
    except GitCommandError as e:
        raise Exception(f"Git operation failed for {env}: {str(e)}")

def load_combined_knowledge(selected_envs: List[str]) -> Dict[str, str]:
    """Загрузка знаний из всех выбранных репозиториев"""
    sources = load_knowledge_sources()
    knowledge = {}
    
    for env in selected_envs:
        if env not in sources:
            continue
            
        conf = sources[env]
        try:
            repo = load_repo(env, conf["репозиторий"], conf["ветка"])
            for file in Path(repo.working_dir).rglob("*"):
                if file.is_file() and not any(p in str(file) for p in [".git", "__pycache__"]):
                    try:
                        knowledge[str(file.relative_to(repo.working_dir))] = file.read_text(encoding="utf-8")
                    except Exception as e:
                        print(f"Error reading {file}: {e}")
        except Exception as e:
            print(f"Failed to process {env}: {e}")
    
    return knowledge