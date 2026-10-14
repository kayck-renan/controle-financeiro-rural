from django.urls import path
from . import views

app_name = "extrator_fiscal"

urlpatterns = [
    # Tela Principal / Extrator Fiscal (Etapa 1 + 2)
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard_view, name="dashboard"),

    # Autenticação
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Gestão Segura de Chave da API
    path("api/configurar-chave/", views.configurar_chave_api, name="configurar_chave_api"),

    # Etapa 1: Extração de DANFE (PDF)
    path("api/extrair-nf/", views.extrair_dados, name="extrair_dados"),
    path("api/exemplo/download/", views.download_exemplo, name="download_exemplo"),
    path("api/status/", views.status_api, name="status_api"),
    path("api/github-commit/", views.api_github_commit, name="api_github_commit"),

    # Etapa 2: Consulta e Lançamento de Movimentos
    path("api/consultar-entidades/", views.consultar_entidades_api, name="consultar_entidades_api"),
    path("api/lancar-movimento/", views.lancar_movimento_etapa2, name="lancar_movimento_etapa2"),

    # Etapa 2: Módulo Manter Pessoas
    path("pessoas/", views.pessoas_view, name="pessoas"),
    path("api/pessoas/listar/", views.api_pessoas_listar, name="api_pessoas_listar"),
    path("api/pessoas/salvar/", views.api_pessoas_salvar, name="api_pessoas_salvar"),
    path("api/pessoas/inativar/<int:id>/", views.api_pessoas_inativar, name="api_pessoas_inativar"),
    path("api/pessoas/reativar/<int:id>/", views.api_pessoas_reativar, name="api_pessoas_reativar"),

    # Etapa 2: Módulo Manter Classificações
    path("classificacoes/", views.classificacoes_view, name="classificacoes"),
    path("api/classificacoes/listar/", views.api_classificacoes_listar, name="api_classificacoes_listar"),
    path("api/classificacoes/salvar/", views.api_classificacoes_salvar, name="api_classificacoes_salvar"),
    path("api/classificacoes/inativar/<int:id>/", views.api_classificacoes_inativar, name="api_classificacoes_inativar"),
    path("api/classificacoes/reativar/<int:id>/", views.api_classificacoes_reativar, name="api_classificacoes_reativar"),

    # Etapa 2: Módulo Registrar Contas a Pagar
    path("contas-a-pagar/", views.contas_pagar_view, name="contas_pagar"),
    path("api/contas-a-pagar/listar/", views.api_contas_pagar_listar, name="api_contas_pagar_listar"),
    path("api/contas-a-pagar/salvar/", views.api_contas_pagar_salvar, name="api_contas_pagar_salvar"),

    # Etapa 2: Módulo Registrar Contas a Receber
    path("contas-a-receber/", views.contas_receber_view, name="contas_receber"),
    path("api/contas-a-receber/listar/", views.api_contas_receber_listar, name="api_contas_receber_listar"),
    path("api/contas-a-receber/salvar/", views.api_contas_receber_salvar, name="api_contas_receber_salvar"),

    # Inativação / Reativação de Movimentos de Contas
    path("api/movimentos/inativar/<int:id>/", views.api_movimento_inativar, name="api_movimento_inativar"),
    path("api/movimentos/reativar/<int:id>/", views.api_movimento_reativar, name="api_movimento_reativar"),
]
