import os
import json
import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .gemini_service import GeminiExtractionService

logger = logging.getLogger(__name__)

def login_view(request):
    """View de autenticação por LOGIN e SENHA do sistema."""
    if request.user.is_authenticated:
        return redirect('extrator_fiscal:index')

    erro = None
    next_url = request.GET.get('next') or request.POST.get('next') or 'extrator_fiscal:index'

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            erro = "Usuário ou senha inválidos. Por favor, utilize uma das credenciais de demonstração."

    context = {
        'erro': erro,
        'next_url': next_url,
    }
    return render(request, 'extrator_fiscal/login.html', context)

def logout_view(request):
    """Encerra a sessão do usuário e redireciona para a tela de login."""
    logout(request)
    return redirect('extrator_fiscal:login')

@login_required(login_url='extrator_fiscal:login')
def index(request):
    """Renderiza a interface web da Etapa 1."""
    chave_servidor = os.environ.get("GEMINI_API_KEY", "").strip()
    chave_sessao = request.session.get("gemini_api_key", "").strip()
    chave_ativa = chave_sessao or chave_servidor
    
    tem_chave_servidor = bool(chave_servidor)
    tem_chave_ativa = bool(chave_ativa)
    
    chave_mascarada = None
    if tem_chave_ativa:
        if len(chave_ativa) > 10:
            chave_mascarada = chave_ativa[:6] + "••••••••" + chave_ativa[-4:]
        else:
            chave_mascarada = "••••••••"

    caminho_exemplo = os.path.join(settings.BASE_DIR, "danfe (ciclano - pecas).pdf")
    tem_exemplo = os.path.exists(caminho_exemplo)
    
    nome_usuario = request.user.get_full_name() or request.user.username
    context = {
        "usuario_logado": nome_usuario,
        "tem_chave_servidor": tem_chave_servidor,
        "tem_chave_ativa": tem_chave_ativa,
        "chave_mascarada": chave_mascarada,
        "tem_exemplo": tem_exemplo,
        "nome_exemplo": "danfe (ciclano - pecas).pdf" if tem_exemplo else None,
    }
    return render(request, "extrator_fiscal/index.html", context)

@csrf_exempt
def configurar_chave_api(request):
    """
    Endpoint para envio/informação e validação da KEY em tempo real.
    Permite atualizar a chave ativa na sessão e retorna a confirmação imediata.
    """
    if request.method == "POST":
        try:
            if request.content_type == "application/json":
                dados = json.loads(request.body.decode("utf-8"))
                api_key = dados.get("api_key", "").strip()
            else:
                api_key = request.POST.get("api_key", "").strip()
        except Exception:
            api_key = request.POST.get("api_key", "").strip()

        if api_key:
            request.session["gemini_api_key"] = api_key
            mascarada = api_key[:6] + "••••••••" + api_key[-4:] if len(api_key) > 10 else "••••••••"
            return JsonResponse({
                "sucesso": True,
                "status": "configurada",
                "chave_mascarada": mascarada,
                "mensagem": "CHAVE enviada e ativada em tempo real com sucesso!",
                "modo": "Google Gemini Cloud AI"
            })
        else:
            request.session.pop("gemini_api_key", None)
            return JsonResponse({
                "sucesso": True,
                "status": "removida",
                "chave_mascarada": None,
                "mensagem": "Chave removida. Sistema operando em modo inteligente local.",
                "modo": "Motor Local Inteligente"
            })

    # GET: retorna status em tempo real da KEY
    chave_servidor = os.environ.get("GEMINI_API_KEY", "").strip()
    chave_sessao = request.session.get("gemini_api_key", "").strip()
    chave_ativa = chave_sessao or chave_servidor
    
    mascarada = None
    if chave_ativa:
        mascarada = chave_ativa[:6] + "••••••••" + chave_ativa[-4:] if len(chave_ativa) > 10 else "••••••••"

    return JsonResponse({
        "status": "configurada" if chave_ativa else "local",
        "chave_mascarada": mascarada,
        "modo": "Google Gemini Cloud AI" if chave_ativa else "Motor Local Inteligente"
    })

@csrf_exempt
def extrair_dados(request):
    """
    Endpoint POST para receber o PDF da nota fiscal e retornar os dados extraídos em JSON.
    Aceita multipart/form-data com o arquivo em 'pdf_file' e opcional 'api_key'.
    """
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido. Utilize POST."}, status=405)

    pdf_file = request.FILES.get("pdf_file")
    api_key_custom = request.POST.get("api_key", "").strip() or request.session.get("gemini_api_key") or None

    # Se não foi enviado arquivo via multipart, verifica se solicitou usar o exemplo
    usar_exemplo = request.POST.get("usar_exemplo") == "true"
    if not pdf_file and usar_exemplo:
        caminho_exemplo = os.path.join(settings.BASE_DIR, "danfe (ciclano - pecas).pdf")
        if os.path.exists(caminho_exemplo):
            with open(caminho_exemplo, "rb") as f:
                pdf_bytes = f.read()
        else:
            return JsonResponse({"erro": "Arquivo de exemplo não encontrado no servidor."}, status=404)
    elif not pdf_file:
        return JsonResponse({"erro": "Nenhum arquivo PDF foi enviado."}, status=400)
    else:
        # Validação do arquivo
        if not pdf_file.name.lower().endswith(".pdf"):
            return JsonResponse({"erro": "O arquivo deve ser obrigatoriamente no formato PDF."}, status=400)
        
        pdf_bytes = pdf_file.read()

    try:
        dados = GeminiExtractionService.extrair_dados(pdf_bytes, api_key=api_key_custom)
        return JsonResponse(dados, safe=False)
    except Exception as e:
        logger.exception("Erro durante a extração:")
        return JsonResponse({"erro": f"Falha no processamento: {str(e)}"}, status=500)

def download_exemplo(request):
    """Permite baixar o arquivo DANFE de exemplo diretamente da interface."""
    caminho = os.path.join(settings.BASE_DIR, "danfe (ciclano - pecas).pdf")
    if os.path.exists(caminho):
        return FileResponse(open(caminho, "rb"), content_type="application/pdf", filename="danfe_ciclano_pecas.pdf")
    return HttpResponse("Arquivo de exemplo não encontrado.", status=404)

def status_api(request):
    """Retorna o status dos serviços e integrações."""
    tem_chave = bool(os.environ.get("GEMINI_API_KEY") or request.session.get("gemini_api_key"))
    return JsonResponse({
        "status": "online",
        "framework": "Django 6.1.1",
        "linguagem": "Python 3.14.5",
        "etapa": "1 - Processador de PDF com LLM Gemini",
        "gemini_configurado": tem_chave,
    })
