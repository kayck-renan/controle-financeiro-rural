import os
import json
import logging
import subprocess
import urllib.request
from datetime import datetime, timezone, timedelta
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

CACHE_KEY_GITHUB_COMMIT = "github_latest_commit_cache_v2"
CACHE_TTL_SUCCESS = 180  # 3 minutos de cache para sucesso
CACHE_TTL_ERROR = 30     # 30 segundos de cache em caso de erro/rate-limit

def obter_info_commit_github(forcar_atualizacao=False):
    """
    Busca as informações do último commit da branch principal diretamente do GitHub.
    Utiliza cache para evitar requisições desnecessárias e rate-limit.
    Caso a consulta falhe, utiliza o fallback local (version.json ou git local)
    sem travar ou prejudicar o sistema.
    """
    if not forcar_atualizacao:
        cached = cache.get(CACHE_KEY_GITHUB_COMMIT)
        if cached:
            return cached

    repo_owner = "kayck-renan"
    repo_name = "controle-financeiro-rural"
    repo_url = f"https://github.com/{repo_owner}/{repo_name}"

    # Valores padrão de fallback
    commit_hash = "1e38504"
    commit_date = "13/10/2026"
    commit_message = "Atualização recente no sistema"
    commit_url = f"{repo_url}/commit/{commit_hash}"
    sucesso = False
    erro_msg = ""

    # 1. Tenta carregar fallback inicial de version.json
    version_file = os.path.join(settings.BASE_DIR, "version.json")
    if os.path.exists(version_file):
        try:
            with open(version_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                commit_hash = data.get("commit_hash", commit_hash)
                commit_date = data.get("commit_date", commit_date)
                commit_message = data.get("commit_message", commit_message)
                repo_url = data.get("repo_url", repo_url)
                commit_url = f"{repo_url}/commit/{commit_hash}"
        except Exception as e:
            logger.debug(f"Falha ao ler version.json: {e}")

    # 2. Tenta carregar do git local se disponível
    try:
        git_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(settings.BASE_DIR),
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        if git_hash:
            commit_hash = git_hash
            commit_url = f"{repo_url}/commit/{commit_hash}"
    except Exception:
        pass

    try:
        git_msg = subprocess.check_output(
            ["git", "log", "-1", "--format=%s"],
            cwd=str(settings.BASE_DIR),
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        if git_msg:
            commit_message = git_msg
    except Exception:
        pass

    try:
        git_date = subprocess.check_output(
            ["git", "log", "-1", "--format=%cd", "--date=format:%d/%m/%Y às %H:%M"],
            cwd=str(settings.BASE_DIR),
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        if git_date:
            commit_date = git_date
    except Exception:
        pass

    # 3. Consulta a API oficial do GitHub (sem necessidade de token para repositório público)
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/main"
    headers = {
        "User-Agent": "ControleFinanceiroRural/2.0",
        "Accept": "application/vnd.github.v3+json"
    }

    # Se houver um token configurado no ambiente, utiliza para ampliar rate-limit
    github_token = os.environ.get("GITHUB_TOKEN", "").strip()
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            if resp.status == 200:
                raw = resp.read().decode("utf-8")
                commit_data = json.loads(raw)

                full_sha = commit_data.get("sha", "")
                if full_sha:
                    commit_hash = full_sha[:7]
                    commit_url = commit_data.get("html_url") or f"{repo_url}/commit/{full_sha}"

                commit_detail = commit_data.get("commit", {})
                msg_full = commit_detail.get("message", "").strip()
                if msg_full:
                    commit_message = msg_full.split("\n")[0].strip()

                author_info = commit_detail.get("author", {})
                raw_iso_date = author_info.get("date", "")
                if raw_iso_date:
                    try:
                        dt = datetime.fromisoformat(raw_iso_date.replace("Z", "+00:00"))
                        dt_br = dt.astimezone(timezone(timedelta(hours=-3)))
                        commit_date = dt_br.strftime("%d/%m/%Y às %H:%M")
                    except Exception:
                        commit_date = raw_iso_date[:10]

                sucesso = True
                erro_msg = ""
    except Exception as err:
        logger.warning(f"Não foi possível consultar a API do GitHub: {err}. Utilizando fallback local.")
        sucesso = False
        erro_msg = "Não foi possível carregar os dados em tempo real do GitHub no momento."

    resultado = {
        "git_commit_hash": commit_hash,
        "git_commit_date": commit_date,
        "git_commit_message": commit_message,
        "git_commit_url": commit_url,
        "git_repo_url": repo_url,
        "git_sucesso": sucesso,
        "git_erro_msg": erro_msg,
    }

    # Armazena em cache
    ttl = CACHE_TTL_SUCCESS if sucesso else CACHE_TTL_ERROR
    try:
        cache.set(CACHE_KEY_GITHUB_COMMIT, resultado, timeout=ttl)
    except Exception:
        pass

    return resultado


def git_info(request):
    """
    Context processor para injetar as informações do último commit do GitHub
    em todos os templates da aplicação de forma transparente e segura.
    """
    return obter_info_commit_github(forcar_atualizacao=False)
