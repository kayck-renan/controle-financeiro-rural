import os
import json
import subprocess
from django.conf import settings

def git_info(request):
    """
    Context processor para injetar o Código da Última Atualização no GitHub
    em todas as telas da aplicação, conforme solicitação do professor e do aluno.
    """
    commit_hash = "99bb372"
    commit_date = "2026-10-13"
    repo_url = "https://github.com/kayck-renan/controle-financeiro-rural"

    version_file = os.path.join(settings.BASE_DIR, "version.json")
    if os.path.exists(version_file):
        try:
            with open(version_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                commit_hash = data.get("commit_hash", commit_hash)
                commit_date = data.get("commit_date", commit_date)
                repo_url = data.get("repo_url", repo_url)
        except Exception:
            pass

    # Tenta atualizar dinamicamente se o comando git estiver disponível
    try:
        git_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(settings.BASE_DIR),
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        if git_hash:
            commit_hash = git_hash
    except Exception:
        pass

    try:
        git_date = subprocess.check_output(
            ["git", "log", "-1", "--format=%cd", "--date=format:%d/%m/%Y %H:%M"],
            cwd=str(settings.BASE_DIR),
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        if git_date:
            commit_date = git_date
    except Exception:
        pass

    return {
        "git_commit_hash": commit_hash,
        "git_commit_date": commit_date,
        "git_repo_url": repo_url,
        "git_commit_url": f"{repo_url}/commit/{commit_hash}",
    }
