import os
import json
import logging
from decimal import Decimal
from datetime import datetime, date

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.db.models import Q, Sum, Count
from django.utils import timezone

from .gemini_service import GeminiExtractionService
from .models import Pessoas, Classificacao, MovimentoContas, ParcelaContas
from .sync_manager import registrar_mutacao

logger = logging.getLogger(__name__)


# ==============================================================================
# AUTENTICAÇÃO
# ==============================================================================

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


# ==============================================================================
# GESTÃO SEGURA DA CHAVE GEMINI (OCULTA E PROTEGIDA)
# ==============================================================================

@csrf_exempt
def configurar_chave_api(request):
    """
    Endpoint para ativação/gestão segura da KEY Gemini.
    Por questões de segurança, a chave NUNCA é exposta em texto plano nas respostas.
    """
    if request.method == "POST":
        api_key = ""
        try:
            if request.content_type == "application/json":
                dados = json.loads(request.body.decode("utf-8"))
                api_key = dados.get("api_key", "").strip()
            else:
                api_key = request.POST.get("api_key", "").strip()
        except Exception:
            api_key = request.POST.get("api_key", "").strip()

        # Suporte a ativação da chave demo internamente sem exposição
        if request.POST.get("usar_demo") == "true" or (request.content_type == "application/json" and dados.get("usar_demo")):
            api_key = os.environ.get("GEMINI_API_KEY", "").strip() or "AIzaSyDemoUniRV2026RuralFinancasKey99"

        if api_key:
            request.session["gemini_api_key"] = api_key
            return JsonResponse({
                "sucesso": True,
                "status": "configurada",
                "chave_mascarada": "••••••••••••••••",
                "mensagem": "Chave da API ativada e protegida com sucesso!",
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

    # GET: Retorna se a chave está configurada sem revelar seus caracteres
    chave_servidor = os.environ.get("GEMINI_API_KEY", "").strip()
    chave_sessao = request.session.get("gemini_api_key", "").strip()
    chave_ativa = bool(chave_sessao or chave_servidor)

    return JsonResponse({
        "status": "configurada" if chave_ativa else "local",
        "chave_mascarada": "••••••••••••••••" if chave_ativa else None,
        "modo": "Google Gemini Cloud AI" if chave_ativa else "Motor Local Inteligente"
    })


# ==============================================================================
# TELA PRINCIPAL (EXTRATOR FISCAL COM ANÁLISE DA ETAPA 2)
# ==============================================================================

@login_required(login_url='extrator_fiscal:login')
def index(request):
    """
    Renderiza a interface principal do Sistema de Controle Financeiro Rural,
    com o Extrator Fiscal, Consulta de Entidades (Etapa 2) e Lançamento Automático.
    """
    chave_servidor = os.environ.get("GEMINI_API_KEY", "").strip()
    chave_sessao = request.session.get("gemini_api_key", "").strip()
    tem_chave = bool(chave_sessao or chave_servidor)

    caminho_exemplo = os.path.join(settings.BASE_DIR, "danfe (ciclano - pecas).pdf")
    tem_exemplo = os.path.exists(caminho_exemplo)

    nome_usuario = request.user.get_full_name() or request.user.username

    context = {
        "pagina_ativa": "extrator",
        "usuario_logado": nome_usuario,
        "tem_chave_ativa": tem_chave,
        "tem_exemplo": tem_exemplo,
        "nome_exemplo": "danfe (ciclano - pecas).pdf" if tem_exemplo else None,
    }
    return render(request, "extrator_fiscal/index.html", context)


# ==============================================================================
# EXTRAÇÃO DE DADOS (ETAPA 1)
# ==============================================================================

@csrf_exempt
def extrair_dados(request):
    """
    Endpoint POST para extração de dados do PDF da DANFE com Gemini / Motor Local.
    """
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido. Utilize POST."}, status=405)

    pdf_file = request.FILES.get("pdf_file")
    api_key_custom = request.POST.get("api_key", "").strip() or request.session.get("gemini_api_key") or None

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


# ==============================================================================
# ATIVIDADE 2ª ETAPA: CONSULTA DE EXISTÊNCIA E LANÇAMENTO NO BANCO DE DADOS
# ==============================================================================

def normalizar_doc(doc):
    if not doc:
        return ""
    return "".join(c for c in str(doc) if c.isdigit())


@csrf_exempt
def consultar_entidades_api(request):
    """
    ATIVIDADE 2ª ETAPA:
    Após a extração dos dados da DANFE, consulta no Banco de Dados e informa:
    - FORNECEDOR: existe ou não (com ID se existir)
    - FATURADO: existe ou não (com ID se existir)
    - DESPESA: existe na classificação ou não (com ID se existir)
    """
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        dados = json.loads(request.body.decode("utf-8")) if request.content_type == "application/json" else request.POST
    except Exception:
        dados = request.POST

    fornecedor_razao = (dados.get("fornecedor_razao") or dados.get("fornecedor", {}).get("razaoSocial") or "").strip()
    fornecedor_cnpj = (dados.get("fornecedor_cnpj") or dados.get("fornecedor", {}).get("cnpj") or "").strip()

    faturado_nome = (dados.get("faturado_nome") or dados.get("faturado", {}).get("nomeCompleto") or "").strip()
    faturado_cpf = (dados.get("faturado_cpf") or dados.get("faturado", {}).get("cpf") or "").strip()

    despesa_desc = (dados.get("despesa_descricao") or dados.get("classificacaoDespesa") or "").strip()

    # 1. Consulta Fornecedor
    forn_obj = None
    cnpj_limpo = normalizar_doc(fornecedor_cnpj)
    if cnpj_limpo:
        forn_obj = Pessoas.objects.filter(
            Q(cpf_cnpj__icontains=cnpj_limpo) | Q(cpf_cnpj=fornecedor_cnpj)
        ).first()

    if not forn_obj and fornecedor_razao:
        forn_obj = Pessoas.objects.filter(
            razao_social__icontains=fornecedor_razao
        ).first()

    fornecedor_resultado = {
        "nome": fornecedor_razao or (forn_obj.razao_social if forn_obj else "Não informado"),
        "documento": fornecedor_cnpj or (forn_obj.cpf_cnpj if forn_obj else ""),
        "existe": bool(forn_obj),
        "status_texto": f"EXISTE – ID: {forn_obj.id}" if forn_obj else "NÃO EXISTE",
        "id": forn_obj.id if forn_obj else None,
    }

    # 2. Consulta Faturado
    fat_obj = None
    cpf_limpo = normalizar_doc(faturado_cpf)
    if cpf_limpo:
        fat_obj = Pessoas.objects.filter(
            Q(cpf_cnpj__icontains=cpf_limpo) | Q(cpf_cnpj=faturado_cpf)
        ).first()

    if not fat_obj and faturado_nome:
        fat_obj = Pessoas.objects.filter(
            razao_social__icontains=faturado_nome
        ).first()

    faturado_resultado = {
        "nome": faturado_nome or (fat_obj.razao_social if fat_obj else "Não informado"),
        "documento": faturado_cpf or (fat_obj.cpf_cnpj if fat_obj else ""),
        "existe": bool(fat_obj),
        "status_texto": f"EXISTE – ID: {fat_obj.id}" if fat_obj else "NÃO EXISTE",
        "id": fat_obj.id if fat_obj else None,
    }

    # 3. Consulta Despesa
    desp_obj = None
    if despesa_desc:
        desp_obj = Classificacao.objects.filter(
            descricao__iexact=despesa_desc,
            tipo='DESPESA'
        ).first()
        if not desp_obj:
            # Tenta busca parcial
            desp_obj = Classificacao.objects.filter(
                descricao__icontains=despesa_desc.split()[0],
                tipo='DESPESA'
            ).first()

    despesa_resultado = {
        "descricao": despesa_desc or (desp_obj.descricao if desp_obj else "Não informada"),
        "existe": bool(desp_obj),
        "status_texto": f"EXISTE – ID: {desp_obj.id}" if desp_obj else "NÃO EXISTE",
        "id": desp_obj.id if desp_obj else None,
    }

    return JsonResponse({
        "fornecedor": fornecedor_resultado,
        "faturado": faturado_resultado,
        "despesa": despesa_resultado,
    })


@never_cache
@csrf_exempt
def lancar_movimento_etapa2(request):
    """
    ATIVIDADE 2ª ETAPA:
    Executa rigorosamente os 5 passos solicitados após a análise:
    1. CRIAR O NOVO FORNECEDOR (se for o caso)
    2. CRIAR O NOVO FATURADO (se for o caso)
    3. CRIAR NOVA DESPESA (se for o caso)
    4. CRIAR UM NOVO REGISTRO DO MOVIMENTO E SUA PARCELA
    5. INFORMAR AO USUÁRIO QUE REGISTRO FOI LANÇADO COM SUCESSO.
    """
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        dados = json.loads(request.body.decode("utf-8")) if request.content_type == "application/json" else request.POST
    except Exception as e:
        return JsonResponse({"erro": f"Dados inválidos: {str(e)}"}, status=400)

    try:
        # Extração de campos
        fornecedor_data = dados.get("fornecedor", {})
        faturado_data = dados.get("faturado", {})

        forn_razao = (fornecedor_data.get("razaoSocial") or dados.get("fornecedor_razao") or "FORNECEDOR DIVERSO").strip()
        forn_fantasia = (fornecedor_data.get("fantasia") or dados.get("fornecedor_fantasia") or "").strip()
        forn_cnpj = (fornecedor_data.get("cnpj") or dados.get("fornecedor_cnpj") or "").strip()

        fat_nome = (faturado_data.get("nomeCompleto") or dados.get("faturado_nome") or "PRODUTOR RURAL").strip()
        fat_cpf = (faturado_data.get("cpf") or dados.get("faturado_cpf") or "").strip()

        desp_desc = (dados.get("classificacaoDespesa") or dados.get("despesa_descricao") or "MANUTENÇÃO E OPERAÇÃO").strip()

        num_nf = str(dados.get("numero") or dados.get("documento_numero") or "000.000.000").strip()
        serie_nf = str(dados.get("serie") or "1").strip()

        data_emissao_str = dados.get("dataEmissao") or dados.get("data_emissao") or str(date.today())
        try:
            data_emissao = datetime.strptime(data_emissao_str[:10], "%Y-%m-%d").date()
        except Exception:
            data_emissao = date.today()

        data_venc_str = dados.get("dataVencimento") or dados.get("data_vencimento") or str(date.today())
        try:
            data_venc = datetime.strptime(data_venc_str[:10], "%Y-%m-%d").date()
        except Exception:
            data_venc = data_emissao

        valor_raw = dados.get("valorTotal") or dados.get("valor_total") or 0
        try:
            if isinstance(valor_raw, str):
                valor_clean = valor_raw.replace("R$", "").replace(".", "").replace(",", ".").strip()
                valor_total = Decimal(valor_clean)
            else:
                valor_total = Decimal(str(valor_raw))
        except Exception:
            valor_total = Decimal("0.00")

        qtd_parcelas = int(dados.get("quantidadeParcelas") or dados.get("qtd_parcelas") or 1)
        descricao_prod = (dados.get("descricaoProdutos") or dados.get("descricao") or "Aquisição de peças e insumos").strip()

        # =========================================================================
        # PASSO 1: CRIAR O NOVO FORNECEDOR (se for o caso)
        # =========================================================================
        cnpj_limpo = normalizar_doc(forn_cnpj)
        fornecedor = None
        if cnpj_limpo:
            fornecedor = Pessoas.objects.filter(Q(cpf_cnpj__icontains=cnpj_limpo) | Q(cpf_cnpj=forn_cnpj)).first()
        if not fornecedor and forn_razao:
            fornecedor = Pessoas.objects.filter(razao_social__iexact=forn_razao).first()

        criou_fornecedor = False
        if not fornecedor:
            fornecedor = Pessoas.objects.create(
                razao_social=forn_razao,
                nome_fantasia=forn_fantasia,
                cpf_cnpj=forn_cnpj,
                tipo='CLIENTE-FORNECEDOR',
                status='ATIVO'
            )
            criou_fornecedor = True

        # =========================================================================
        # PASSO 2: CRIAR O NOVO FATURADO (se for o caso)
        # =========================================================================
        cpf_limpo = normalizar_doc(fat_cpf)
        faturado = None
        if cpf_limpo:
            faturado = Pessoas.objects.filter(Q(cpf_cnpj__icontains=cpf_limpo) | Q(cpf_cnpj=fat_cpf)).first()
        if not faturado and fat_nome:
            faturado = Pessoas.objects.filter(razao_social__iexact=fat_nome).first()

        criou_faturado = False
        if not faturado:
            faturado = Pessoas.objects.create(
                razao_social=fat_nome,
                cpf_cnpj=fat_cpf,
                tipo='FATURADO',
                status='ATIVO'
            )
            criou_faturado = True

        # =========================================================================
        # PASSO 3: CRIAR NOVA DESPESA (se for o caso)
        # =========================================================================
        despesa = Classificacao.objects.filter(descricao__iexact=desp_desc, tipo='DESPESA').first()
        criou_despesa = False
        if not despesa:
            despesa = Classificacao.objects.create(
                descricao=desp_desc,
                tipo='DESPESA',
                status='ATIVO',
                observacoes="Criada automaticamente pelo Extrator Fiscal"
            )
            criou_despesa = True

        # =========================================================================
        # PASSO 4: CRIAR UM NOVO REGISTRO DO MOVIMENTO E SUA PARCELA
        # =========================================================================
        movimento = MovimentoContas.objects.create(
            tipo='APAGAR',
            pessoa=fornecedor,
            faturado=faturado,
            documento_numero=num_nf,
            serie=serie_nf,
            data_emissao=data_emissao,
            valor_total=valor_total,
            descricao=descricao_prod,
            status='ATIVO'
        )
        movimento.classificacoes.add(despesa)

        # Criação das parcelas
        parcelas_criadas = []
        valor_parcela = (valor_total / Decimal(qtd_parcelas)).quantize(Decimal("0.01")) if qtd_parcelas > 0 else valor_total

        if qtd_parcelas <= 1:
            p = ParcelaContas.objects.create(
                movimento=movimento,
                identificacao='ÚNICA',
                numero_parcela=1,
                data_vencimento=data_venc,
                valor=valor_total,
                status='ATIVO',
                status_pagamento='PENDENTE'
            )
            parcelas_criadas.append({"identificacao": "ÚNICA", "valor": str(p.valor), "vencimento": str(p.data_vencimento)})
        else:
            for i in range(1, qtd_parcelas + 1):
                p = ParcelaContas.objects.create(
                    movimento=movimento,
                    identificacao=f"{i}/{qtd_parcelas}",
                    numero_parcela=i,
                    data_vencimento=data_venc,
                    valor=valor_parcela,
                    status='ATIVO',
                    status_pagamento='PENDENTE'
                )
                parcelas_criadas.append({"identificacao": p.identificacao, "valor": str(p.valor), "vencimento": str(p.data_vencimento)})

        # =========================================================================
        # PASSO 5: INFORMAR AO USUÁRIO QUE REGISTRO FOI LANÇADO COM SUCESSO
        # =========================================================================
        if criou_fornecedor:
            registrar_mutacao(request, 'PESSOA', fornecedor)
        if criou_faturado:
            registrar_mutacao(request, 'PESSOA', faturado)
        if criou_despesa:
            registrar_mutacao(request, 'CLASSIFICACAO', despesa)
        registrar_mutacao(request, 'MOVIMENTO', movimento)

        return JsonResponse({
            "sucesso": True,
            "mensagem": "Registro de Movimento e Parcela(s) lançado com sucesso no Banco de Dados!",
            "detalhes": {
                "movimento_id": movimento.id,
                "tipo": "APAGAR",
                "fornecedor": {
                    "id": fornecedor.id,
                    "razao_social": fornecedor.razao_social,
                    "recem_criado": criou_fornecedor
                },
                "faturado": {
                    "id": faturado.id,
                    "razao_social": faturado.razao_social,
                    "recem_criado": criou_faturado
                },
                "despesa": {
                    "id": despesa.id,
                    "descricao": despesa.descricao,
                    "recem_criada": criou_despesa
                },
                "documento_numero": movimento.documento_numero,
                "valor_total": str(movimento.valor_total),
                "parcelas": parcelas_criadas
            }
        })

    except Exception as e:
        logger.exception("Erro ao lançar movimento:")
        return JsonResponse({"sucesso": False, "erro": f"Falha ao lançar movimento: {str(e)}"}, status=500)


# ==============================================================================
# DASHBOARD
# ==============================================================================

@never_cache
@login_required(login_url='extrator_fiscal:login')
def dashboard_view(request):
    """Exibe o Dashboard executivo com estatísticas do agronegócio."""
    total_pessoas = Pessoas.objects.filter(status='ATIVO').count()
    total_classificacoes = Classificacao.objects.filter(status='ATIVO').count()

    total_pagar = MovimentoContas.objects.filter(tipo='APAGAR', status='ATIVO').aggregate(Sum('valor_total'))['valor_total__sum'] or Decimal("0.00")
    total_receber = MovimentoContas.objects.filter(tipo='ARECEBER', status='ATIVO').aggregate(Sum('valor_total'))['valor_total__sum'] or Decimal("0.00")

    ultimos_movimentos = MovimentoContas.objects.filter(status='ATIVO').select_related('pessoa', 'faturado').prefetch_related('classificacoes')[:8]

    context = {
        "pagina_ativa": "dashboard",
        "usuario_logado": request.user.get_full_name() or request.user.username,
        "total_pessoas": total_pessoas,
        "total_classificacoes": total_classificacoes,
        "total_pagar": total_pagar,
        "total_receber": total_receber,
        "saldo": total_receber - total_pagar,
        "ultimos_movimentos": ultimos_movimentos,
    }
    return render(request, "extrator_fiscal/dashboard.html", context)


# ==============================================================================
# CRUD: MANTER PESSOAS (FORNECEDOR, CLIENTE, FATURADO)
# ==============================================================================

@never_cache
@login_required(login_url='extrator_fiscal:login')
def pessoas_view(request):
    """Renderiza a tela de gestão de Pessoas com filtros e busca."""
    context = {
        "pagina_ativa": "pessoas",
        "usuario_logado": request.user.get_full_name() or request.user.username,
    }
    return render(request, "extrator_fiscal/pessoas.html", context)


def _filtrar_por_status(qs, status_param, todos_param=False):
    """
    Aplica filtro por status suportando 3 opções:
    - 'TODOS' ou todos_param=True: exibe registros ativos e inativos
    - 'ATIVO': exibe exclusivamente os registros ativos
    - 'INATIVO': exibe exclusivamente os registros inativos
    - Padrão (se não informado): exibe todos para garantir localização e usabilidade
    """
    st = (status_param or "").strip().upper()
    if st == "ATIVO":
        return qs.filter(status="ATIVO")
    elif st == "INATIVO":
        return qs.filter(status="INATIVO")
    elif st == "TODOS" or todos_param:
        return qs
    return qs


@never_cache
@login_required(login_url='extrator_fiscal:login')
def api_pessoas_listar(request):
    """
    Retorna a lista de pessoas.
    Filtro de Status:
    - 'TODOS': exibe ativos e inativos.
    - 'ATIVO': exibe somente ativos.
    - 'INATIVO': exibe somente inativos.
    Suporta busca multi-elemento (Razão Social, Nome Fantasia, CPF/CNPJ, E-mail, Telefone, ID).
    """
    termo = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo", "").strip()
    status = request.GET.get("status", "").strip()
    todos = request.GET.get("todos", "false").lower() == "true"

    qs = Pessoas.objects.all()
    qs = _filtrar_por_status(qs, status, todos)

    if tipo:
        qs = qs.filter(tipo=tipo)

    if termo:
        filtro = Q(razao_social__icontains=termo) | \
                 Q(nome_fantasia__icontains=termo) | \
                 Q(cpf_cnpj__icontains=termo) | \
                 Q(email__icontains=termo) | \
                 Q(telefone__icontains=termo)
        if termo.isdigit():
            filtro |= Q(id=int(termo))
        digitos = "".join([c for c in termo if c.isdigit()])
        if digitos and len(digitos) >= 3 and digitos != termo:
            filtro |= Q(cpf_cnpj__icontains=digitos) | Q(telefone__icontains=digitos)
        qs = qs.filter(filtro)

    dados = []
    for p in qs:
        dados.append({
            "id": p.id,
            "razao_social": p.razao_social,
            "nome_fantasia": p.nome_fantasia or "-",
            "cpf_cnpj": p.cpf_cnpj or "-",
            "tipo": p.tipo,
            "tipo_display": p.get_tipo_display(),
            "email": p.email or "-",
            "telefone": p.telefone or "-",
            "status": p.status,
            "data_cadastro": p.data_cadastro.strftime("%d/%m/%Y"),
        })

    return JsonResponse({"sucesso": True, "total": len(dados), "registros": dados})


@never_cache
@csrf_exempt
@login_required(login_url='extrator_fiscal:login')
def api_pessoas_salvar(request):
    """
    Criação ou Edição de Pessoa.
    Regra do Layout (Página 4):
    - No CREATE campo STATUS oculto == ATIVO
    - No UPDATE campo STATUS oculto
    """
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        dados = json.loads(request.body.decode("utf-8")) if request.content_type == "application/json" else request.POST
        pessoa_id = dados.get("id")

        razao_social = dados.get("razao_social", "").strip()
        if not razao_social:
            return JsonResponse({"sucesso": False, "erro": "Razão Social / Nome é obrigatório."}, status=400)

        nome_fantasia = dados.get("nome_fantasia", "").strip()
        cpf_cnpj = dados.get("cpf_cnpj", "").strip()
        tipo = dados.get("tipo", "FORNECEDOR").strip()
        email = dados.get("email", "").strip()
        telefone = dados.get("telefone", "").strip()

        if pessoa_id:
            # UPDATE: Mantém status existente (campo status oculto)
            pessoa = get_object_or_404(Pessoas, id=pessoa_id)
            pessoa.razao_social = razao_social
            pessoa.nome_fantasia = nome_fantasia
            pessoa.cpf_cnpj = cpf_cnpj
            pessoa.tipo = tipo
            pessoa.email = email
            pessoa.telefone = telefone
            pessoa.save()
            msg = f"Pessoa '{pessoa.razao_social}' atualizada com sucesso!"
        else:
            # CREATE: Status oculto == ATIVO
            pessoa = Pessoas.objects.create(
                razao_social=razao_social,
                nome_fantasia=nome_fantasia,
                cpf_cnpj=cpf_cnpj,
                tipo=tipo,
                email=email,
                telefone=telefone,
                status='ATIVO'
            )
            msg = f"Pessoa '{pessoa.razao_social}' cadastrada com sucesso!"

        # Registra mutação na sessão para sincronismo entre instâncias e abas
        registrar_mutacao(request, 'PESSOA', pessoa)

        return JsonResponse({"sucesso": True, "mensagem": msg, "id": pessoa.id})

    except Exception as e:
        return JsonResponse({"sucesso": False, "erro": str(e)}, status=500)


@never_cache
@csrf_exempt
@login_required(login_url='extrator_fiscal:login')
def api_pessoas_inativar(request, id):
    """
    Regra de Negócio:
    - Cadastros não podem ser excluídos.
    - No DELETE altera campo STATUS == INATIVO (exclusão lógica).
    """
    pessoa = get_object_or_404(Pessoas, id=id)
    pessoa.inativar()
    registrar_mutacao(request, 'PESSOA', pessoa)
    return JsonResponse({
        "sucesso": True,
        "mensagem": f"Pessoa '{pessoa.razao_social}' inativada com sucesso!",
        "status": pessoa.status
    })


@never_cache
@csrf_exempt
@login_required(login_url='extrator_fiscal:login')
def api_pessoas_reativar(request, id):
    """Regra de Negócio: Cadastros devem ser possível REATIVAR um registro INATIVO."""
    pessoa = get_object_or_404(Pessoas, id=id)
    pessoa.reativar()
    registrar_mutacao(request, 'PESSOA', pessoa)
    return JsonResponse({
        "sucesso": True,
        "mensagem": f"Pessoa '{pessoa.razao_social}' reativada com sucesso!",
        "status": pessoa.status
    })


# ==============================================================================
# CRUD: MANTER CLASSIFICAÇÃO (TIPO DE RECEITA / TIPO DE DESPESA)
# ==============================================================================

@never_cache
@login_required(login_url='extrator_fiscal:login')
def classificacoes_view(request):
    """Renderiza a tela de gestão de Classificações."""
    context = {
        "pagina_ativa": "classificacoes",
        "usuario_logado": request.user.get_full_name() or request.user.username,
    }
    return render(request, "extrator_fiscal/classificacoes.html", context)


@never_cache
@login_required(login_url='extrator_fiscal:login')
def api_classificacoes_listar(request):
    """Lista classificações de receitas e despesas com busca e filtro por status (Todos/Ativos/Inativos)."""
    termo = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo", "").strip()
    status = request.GET.get("status", "").strip()
    todos = request.GET.get("todos", "false").lower() == "true"

    qs = Classificacao.objects.all()
    qs = _filtrar_por_status(qs, status, todos)

    if tipo:
        qs = qs.filter(tipo=tipo)

    if termo:
        filtro = Q(descricao__icontains=termo) | Q(observacoes__icontains=termo)
        if termo.isdigit():
            filtro |= Q(id=int(termo))
        qs = qs.filter(filtro)

    dados = []
    for c in qs:
        dados.append({
            "id": c.id,
            "descricao": c.descricao,
            "tipo": c.tipo,
            "tipo_display": c.get_tipo_display(),
            "observacoes": c.observacoes or "-",
            "status": c.status,
            "data_cadastro": c.data_cadastro.strftime("%d/%m/%Y"),
        })

    return JsonResponse({"sucesso": True, "total": len(dados), "registros": dados})


@never_cache
@csrf_exempt
@login_required(login_url='extrator_fiscal:login')
def api_classificacoes_salvar(request):
    """Criação ou Edição de Classificação com status oculto."""
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        dados = json.loads(request.body.decode("utf-8")) if request.content_type == "application/json" else request.POST
        class_id = dados.get("id")

        descricao = dados.get("descricao", "").strip()
        if not descricao:
            return JsonResponse({"sucesso": False, "erro": "Descrição é obrigatória."}, status=400)

        tipo = dados.get("tipo", "DESPESA").strip()
        observacoes = dados.get("observacoes", "").strip()

        if class_id:
            c = get_object_or_404(Classificacao, id=class_id)
            c.descricao = descricao
            c.tipo = tipo
            c.observacoes = observacoes
            c.save()
            msg = f"Classificação '{c.descricao}' atualizada com sucesso!"
        else:
            c = Classificacao.objects.create(
                descricao=descricao,
                tipo=tipo,
                observacoes=observacoes,
                status='ATIVO'
            )
            msg = f"Classificação '{c.descricao}' criada com sucesso!"

        # Registra mutação na sessão para sincronismo entre instâncias e abas
        registrar_mutacao(request, 'CLASSIFICACAO', c)

        return JsonResponse({"sucesso": True, "mensagem": msg, "id": c.id})

    except Exception as e:
        return JsonResponse({"sucesso": False, "erro": str(e)}, status=500)


@never_cache
@csrf_exempt
@login_required(login_url='extrator_fiscal:login')
def api_classificacoes_inativar(request, id):
    """Inativação lógica da classificação."""
    c = get_object_or_404(Classificacao, id=id)
    c.inativar()
    registrar_mutacao(request, 'CLASSIFICACAO', c)
    return JsonResponse({
        "sucesso": True,
        "mensagem": f"Classificação '{c.descricao}' inativada com sucesso!",
        "status": c.status
    })


@never_cache
@csrf_exempt
@login_required(login_url='extrator_fiscal:login')
def api_classificacoes_reativar(request, id):
    """Reativação da classificação."""
    c = get_object_or_404(Classificacao, id=id)
    c.reativar()
    registrar_mutacao(request, 'CLASSIFICACAO', c)
    return JsonResponse({
        "sucesso": True,
        "mensagem": f"Classificação '{c.descricao}' reativada com sucesso!",
        "status": c.status
    })


# ==============================================================================
# CRUD: REGISTRAR CONTAS A PAGAR & CONTAS A RECEBER
# ==============================================================================

@never_cache
@login_required(login_url='extrator_fiscal:login')
def contas_pagar_view(request):
    """Renderiza a tela de gestão de Contas a Pagar."""
    pessoas_fornecedores = Pessoas.objects.filter(status='ATIVO').exclude(tipo='CLIENTE')
    pessoas_faturados = Pessoas.objects.filter(status='ATIVO')
    classificacoes_despesas = Classificacao.objects.filter(status='ATIVO', tipo='DESPESA')

    context = {
        "pagina_ativa": "contas_pagar",
        "usuario_logado": request.user.get_full_name() or request.user.username,
        "fornecedores": pessoas_fornecedores,
        "faturados": pessoas_faturados,
        "classificacoes": classificacoes_despesas,
    }
    return render(request, "extrator_fiscal/contas_pagar.html", context)


@never_cache
@login_required(login_url='extrator_fiscal:login')
def contas_receber_view(request):
    """Renderiza a tela de gestão de Contas a Receber."""
    pessoas_clientes = Pessoas.objects.filter(status='ATIVO').exclude(tipo='FORNECEDOR')
    pessoas_faturados = Pessoas.objects.filter(status='ATIVO')
    classificacoes_receitas = Classificacao.objects.filter(status='ATIVO', tipo='RECEITA')

    context = {
        "pagina_ativa": "contas_receber",
        "usuario_logado": request.user.get_full_name() or request.user.username,
        "clientes": pessoas_clientes,
        "faturados": pessoas_faturados,
        "classificacoes": classificacoes_receitas,
    }
    return render(request, "extrator_fiscal/contas_receber.html", context)


def _listar_movimentos(request, tipo_movimento):
    termo = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    todos = request.GET.get("todos", "false").lower() == "true"

    qs = MovimentoContas.objects.filter(tipo=tipo_movimento).select_related('pessoa', 'faturado').prefetch_related('classificacoes', 'parcelas')
    qs = _filtrar_por_status(qs, status, todos)

    if termo:
        filtro = Q(documento_numero__icontains=termo) | \
                 Q(pessoa__razao_social__icontains=termo) | \
                 Q(pessoa__nome_fantasia__icontains=termo) | \
                 Q(pessoa__cpf_cnpj__icontains=termo) | \
                 Q(faturado__razao_social__icontains=termo) | \
                 Q(descricao__icontains=termo)
        if termo.isdigit():
            filtro |= Q(id=int(termo))
        qs = qs.filter(filtro)

    dados = []
    for m in qs:
        classes_str = ", ".join([c.descricao for c in m.classificacoes.all()]) or "Nenhuma"
        parcelas_lista = []
        for p in m.parcelas.all():
            parcelas_lista.append({
                "id": p.id,
                "identificacao": p.identificacao,
                "numero": p.numero_parcela,
                "vencimento": p.data_vencimento.strftime("%d/%m/%Y"),
                "valor": f"{p.valor:.2f}",
                "status_pagamento": p.status_pagamento,
                "status": p.status,
            })

        dados.append({
            "id": m.id,
            "documento_numero": m.documento_numero or "-",
            "serie": m.serie or "-",
            "pessoa_nome": m.pessoa.razao_social if m.pessoa else "-",
            "pessoa_id": m.pessoa.id if m.pessoa else None,
            "faturado_nome": m.faturado.razao_social if m.faturado else "-",
            "data_emissao": m.data_emissao.strftime("%d/%m/%Y"),
            "valor_total": f"{m.valor_total:.2f}",
            "descricao": m.descricao or "-",
            "classificacoes": classes_str,
            "classificacoes_ids": [c.id for c in m.classificacoes.all()],
            "status": m.status,
            "parcelas": parcelas_lista,
            "qtd_parcelas": len(parcelas_lista),
        })

    return JsonResponse({"sucesso": True, "total": len(dados), "registros": dados})


@never_cache
@login_required(login_url='extrator_fiscal:login')
def api_contas_pagar_listar(request):
    return _listar_movimentos(request, 'APAGAR')


@never_cache
@login_required(login_url='extrator_fiscal:login')
def api_contas_receber_listar(request):
    return _listar_movimentos(request, 'ARECEBER')


@never_cache
@csrf_exempt
@login_required(login_url='extrator_fiscal:login')
def api_salvar_movimento(request, tipo_movimento):
    """
    Cria ou atualiza um registro de MovimentoContas e suas Parcelas.
    Regras:
    - Um registro de contas a pagar/receber pode ter uma ou mais classificações.
    - Pode ter uma ou mais parcelas com datas de vencimento distintas.
    - No CREATE/UPDATE campo STATUS oculto == ATIVO.
    """
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        dados = json.loads(request.body.decode("utf-8")) if request.content_type == "application/json" else request.POST
        mov_id = dados.get("id")

        pessoa_id = dados.get("pessoa_id")
        if not pessoa_id:
            return JsonResponse({"sucesso": False, "erro": "Selecione a pessoa (Fornecedor / Cliente)."}, status=400)
        pessoa = get_object_or_404(Pessoas, id=pessoa_id)

        faturado_id = dados.get("faturado_id")
        faturado = Pessoas.objects.filter(id=faturado_id).first() if faturado_id else None

        doc_num = dados.get("documento_numero", "").strip()
        serie = dados.get("serie", "1").strip()

        data_emissao_str = dados.get("data_emissao") or str(date.today())
        try:
            data_emissao = datetime.strptime(data_emissao_str[:10], "%Y-%m-%d").date()
        except Exception:
            data_emissao = date.today()

        valor_total = Decimal(str(dados.get("valor_total", 0)).replace(",", "."))
        descricao = dados.get("descricao", "").strip()

        classificacoes_ids = dados.get("classificacoes", [])
        if isinstance(classificacoes_ids, str):
            classificacoes_ids = [int(x) for x in classificacoes_ids.split(",") if x.strip().isdigit()]

        if mov_id:
            mov = get_object_or_404(MovimentoContas, id=mov_id)
            mov.pessoa = pessoa
            mov.faturado = faturado
            mov.documento_numero = doc_num
            mov.serie = serie
            mov.data_emissao = data_emissao
            mov.valor_total = valor_total
            mov.descricao = descricao
            mov.save()
            msg = f"Movimento #{mov.id} atualizado com sucesso!"
        else:
            mov = MovimentoContas.objects.create(
                tipo=tipo_movimento,
                pessoa=pessoa,
                faturado=faturado,
                documento_numero=doc_num,
                serie=serie,
                data_emissao=data_emissao,
                valor_total=valor_total,
                descricao=descricao,
                status='ATIVO'
            )
            msg = f"Movimento #{mov.id} cadastrado com sucesso!"

        # Atualiza classificações
        if classificacoes_ids:
            mov.classificacoes.set(classificacoes_ids)

        # Atualiza / Cria parcelas
        parcelas_data = dados.get("parcelas", [])
        if parcelas_data:
            # Se for edição, remove as anteriores para recriar conforme especificado
            mov.parcelas.all().delete()
            for idx, p_info in enumerate(parcelas_data, start=1):
                venc_str = p_info.get("data_vencimento") or str(date.today())
                try:
                    venc = datetime.strptime(venc_str[:10], "%Y-%m-%d").date()
                except Exception:
                    venc = date.today()
                vlr = Decimal(str(p_info.get("valor", valor_total)).replace(",", "."))
                ident = p_info.get("identificacao") or f"{idx}/{len(parcelas_data)}" if len(parcelas_data) > 1 else 'ÚNICA'

                ParcelaContas.objects.create(
                    movimento=mov,
                    identificacao=ident,
                    numero_parcela=idx,
                    data_vencimento=venc,
                    valor=vlr,
                    status='ATIVO',
                    status_pagamento=p_info.get("status_pagamento", "PENDENTE")
                )
        elif not mov_id:
            # Parcela única default
            ParcelaContas.objects.create(
                movimento=mov,
                identificacao='ÚNICA',
                numero_parcela=1,
                data_vencimento=data_emissao,
                valor=valor_total,
                status='ATIVO',
                status_pagamento='PENDENTE'
            )

        # Registra mutação na sessão para sincronismo entre instâncias e abas
        registrar_mutacao(request, 'MOVIMENTO', mov)

        return JsonResponse({"sucesso": True, "mensagem": msg, "id": mov.id})

    except Exception as e:
        logger.exception("Erro ao salvar movimento:")
        return JsonResponse({"sucesso": False, "erro": str(e)}, status=500)


@never_cache
@csrf_exempt
@login_required(login_url='extrator_fiscal:login')
def api_contas_pagar_salvar(request):
    return api_salvar_movimento(request, 'APAGAR')


@never_cache
@csrf_exempt
@login_required(login_url='extrator_fiscal:login')
def api_contas_receber_salvar(request):
    return api_salvar_movimento(request, 'ARECEBER')


@never_cache
@csrf_exempt
@login_required(login_url='extrator_fiscal:login')
def api_movimento_inativar(request, id):
    """Inativação lógica do Movimento e de suas Parcelas."""
    mov = get_object_or_404(MovimentoContas, id=id)
    mov.inativar()
    registrar_mutacao(request, 'MOVIMENTO', mov)
    return JsonResponse({
        "sucesso": True,
        "mensagem": f"Movimento #{mov.id} inativado com sucesso!",
        "status": mov.status
    })


@never_cache
@csrf_exempt
@login_required(login_url='extrator_fiscal:login')
def api_movimento_reativar(request, id):
    """Reativação lógica do Movimento e de suas Parcelas."""
    mov = get_object_or_404(MovimentoContas, id=id)
    mov.reativar()
    registrar_mutacao(request, 'MOVIMENTO', mov)
    return JsonResponse({
        "sucesso": True,
        "mensagem": f"Movimento #{mov.id} reativado com sucesso!",
        "status": mov.status
    })


def status_api(request):
    """Retorna o status dos serviços e integrações."""
    tem_chave = bool(os.environ.get("GEMINI_API_KEY") or request.session.get("gemini_api_key"))
    return JsonResponse({
        "status": "online",
        "framework": "Django 6.1.1",
        "linguagem": "Python 3.14.5",
        "etapa": "2 - Manter Pessoas, Classificações, Contas e Integração Fiscal",
        "gemini_configurado": tem_chave,
    })


def api_github_commit(request):
    """
    Retorna os dados da última atualização disponível no GitHub em formato JSON.
    Aceita o parâmetro ?refresh=true para forçar a revalidação imediata junto ao GitHub.
    """
    from .context_processors import obter_info_commit_github
    forcar = request.GET.get("refresh", "").lower() == "true"
    dados = obter_info_commit_github(forcar_atualizacao=forcar)
    return JsonResponse(dados)

