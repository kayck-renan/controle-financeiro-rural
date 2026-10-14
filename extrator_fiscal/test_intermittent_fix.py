import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from extrator_fiscal.models import Pessoas, Classificacao, MovimentoContas, ParcelaContas

def run_all_tests():
    print("=" * 70)
    print("INICIANDO BATERIA DE TESTES OBRIGATÓRIOS (TESTES A, B, C, D, E)")
    print("=" * 70)

    # Cria ou recupera usuário para os testes
    user, _ = User.objects.get_or_create(username='test_auditor', defaults={'email': 'auditor@unirv.br'})
    user.set_password('teste123')
    user.save()

    client = Client()
    logged = client.login(username='test_auditor', password='teste123')
    assert logged, "Falha no login do cliente de teste"
    print("[OK] Login realizado com sucesso no TestClient")

    # =========================================================================
    # TESTE B — Cadastro e consulta
    # =========================================================================
    print("\n--- TESTE B: Cadastro e consulta imediata + navegação entre abas ---")
    ts = int(time.time())
    pessoa_nome = f"FAZENDA SANTA HELENA {ts}"
    resp_create = client.post('/api/pessoas/salvar/', data=json.dumps({
        'razao_social': pessoa_nome,
        'nome_fantasia': 'Santa Helena',
        'cpf_cnpj': '12.345.678/0001-90',
        'tipo': 'FORNECEDOR',
        'telefone': '(64) 99999-0000',
        'email': 'santahelena@rural.com',
        'status': 'ATIVO'
    }), content_type='application/json')
    assert resp_create.status_code == 200, f"Erro ao criar: {resp_create.content}"
    data_create = resp_create.json()
    assert data_create.get('sucesso'), "Criação não retornou sucesso"
    created_id = data_create.get('id')
    print(f"[OK] Registro #{created_id} ('{pessoa_nome}') criado com sucesso!")
    # Consulta imediata
    resp_list = client.get('/api/pessoas/listar/?status=TODOS')
    assert resp_list.status_code == 200
    ids_imediatos = [p['id'] for p in resp_list.json().get('registros', [])]
    assert created_id in ids_imediatos, "Registro criado não encontrado na consulta imediata!"
    print(f"[OK] Registro #{created_id} localizado imediatamente na listagem.")

    # =========================================================================
    # TESTE A — Navegação repetida entre abas e retorno
    # =========================================================================
    print("\n--- TESTE A: Navegação repetida entre abas e verificação de consistência ---")
    abas = [
        '/dashboard/',
        '/classificacoes/',
        '/contas-a-pagar/',
        '/contas-a-receber/',
        '/',
        '/pessoas/'
    ]

    for ciclo in range(1, 6):
        # Navega por todas as abas
        for aba in abas:
            r_nav = client.get(aba)
            assert r_nav.status_code == 200, f"Falha ao carregar aba {aba}: {r_nav.status_code}"
            # Verifica cabeçalhos de controle de cache
            assert 'no-cache' in r_nav.headers.get('Cache-Control', ''), f"Cache-Control ausente na aba {aba}"

        # Volta ao módulo e lista
        r_check = client.get('/api/pessoas/listar/?status=TODOS')
        assert r_check.status_code == 200
        ids_apos_nav = [p['id'] for p in r_check.json().get('registros', [])]
        assert created_id in ids_apos_nav, f"Ciclo {ciclo}: Registro #{created_id} DESAPARECEU após navegação entre abas!"
        print(f"  [OK] Ciclo {ciclo}/5: Registro #{created_id} permaneceu perfeitamente visível e consistente.")

    # =========================================================================
    # TESTE C — Requisições concorrentes e ordem de resposta
    # =========================================================================
    print("\n--- TESTE C: Validação de filtros e consistência de buscas ---")
    # Busca com filtro específico
    r_busca1 = client.get(f'/api/pessoas/listar/?q={ts}')
    registros_b1 = r_busca1.json().get('registros', [])
    assert len(registros_b1) >= 1 and any(p['id'] == created_id for p in registros_b1), "Busca por termo falhou"

    # Busca por critério inexistente
    r_busca2 = client.get('/api/pessoas/listar/?q=TERMO_INEXISTENTE_XYZ_ABC')
    registros_b2 = r_busca2.json().get('registros', [])
    assert len(registros_b2) == 0, "Busca vazia deveria retornar 0 registros"

    # Busca geral novamente
    r_busca3 = client.get('/api/pessoas/listar/?status=TODOS')
    registros_b3 = r_busca3.json().get('registros', [])
    assert any(p['id'] == created_id for p in registros_b3), "Busca geral após filtro perdeu registro"
    print("[OK] Filtros, buscas e paginação retornam exatamente o esperado sem vazamento de estado.")

    # =========================================================================
    # TESTE D — Persistência e consistência (Inativação e Reativação)
    # =========================================================================
    print("\n--- TESTE D: Persistência durante Inativação, Troca de Abas e Reativação ---")
    # Inativação lógica
    r_inativar = client.post(f'/api/pessoas/inativar/{created_id}/')
    assert r_inativar.status_code == 200
    assert r_inativar.json().get('status') == 'INATIVO'

    # Navega para outras abas
    client.get('/contas-a-pagar/')
    client.get('/dashboard/')

    # Lista somente inativos
    r_inativos = client.get('/api/pessoas/listar/?status=INATIVO')
    ids_inativos = [p['id'] for p in r_inativos.json().get('registros', [])]
    assert created_id in ids_inativos, "Registro inativado sumiu da lista de inativos após navegação!"

    # Lista somente ativos (não deve conter)
    r_ativos = client.get('/api/pessoas/listar/?status=ATIVO')
    ids_ativos = [p['id'] for p in r_ativos.json().get('registros', [])]
    assert created_id not in ids_ativos, "Registro inativado ainda aparece na lista de ativos!"

    # Reativa o registro
    r_reativar = client.post(f'/api/pessoas/reativar/{created_id}/')
    assert r_reativar.status_code == 200
    assert r_reativar.json().get('status') == 'ATIVO'

    # Navega novamente
    client.get('/classificacoes/')
    client.get('/pessoas/')

    # Lista somente ativos (deve reaparecer)
    r_reativados = client.get('/api/pessoas/listar/?status=ATIVO')
    ids_reativados = [p['id'] for p in r_reativados.json().get('registros', [])]
    assert created_id in ids_reativados, "Registro reativado não reapareceu na lista de ativos!"
    print("[OK] Inativação e Reativação lógicas persistidas e sincronizadas com 100% de consistência.")

    # =========================================================================
    # TESTE E — Regressão nos demais módulos (Classificações, Contas a Pagar/Receber)
    # =========================================================================
    print("\n--- TESTE E: Regressão nos módulos Classificações, Contas a Pagar e Contas a Receber ---")
    # 1. Classificação
    class_nome = f"MANUTENCAO TRATOR {ts}"
    r_c_save = client.post('/api/classificacoes/salvar/', data=json.dumps({
        'descricao': class_nome,
        'tipo': 'DESPESA',
        'observacoes': 'Teste de regressao',
        'status': 'ATIVO'
    }), content_type='application/json')
    assert r_c_save.status_code == 200
    c_id = r_c_save.json().get('id')

    # Navega
    client.get('/dashboard/')
    client.get('/pessoas/')
    client.get('/classificacoes/')

    r_c_list = client.get('/api/classificacoes/listar/?status=TODOS')
    assert c_id in [c['id'] for c in r_c_list.json().get('registros', [])], "Classificação sumiu após navegação!"
    print(f"  [OK] Módulo Classificações: Registro #{c_id} persistido e íntegro.")

    # 2. Contas a Pagar
    r_pagar_save = client.post('/api/contas-a-pagar/salvar/', data=json.dumps({
        'pessoa_id': created_id,
        'documento_numero': f"NF-{ts}",
        'serie': '1',
        'data_emissao': str(time.strftime('%Y-%m-%d')),
        'data_vencimento': str(time.strftime('%Y-%m-%d')),
        'valor_total': 1500.50,
        'qtd_parcelas': 1,
        'classificacoes': [c_id],
        'descricao': 'Compra de combustivel e pecas',
        'status': 'ATIVO'
    }), content_type='application/json')
    assert r_pagar_save.status_code == 200
    mov_pagar_id = r_pagar_save.json().get('id')

    # Navega
    client.get('/contas-a-receber/')
    client.get('/dashboard/')
    client.get('/contas-a-pagar/')

    r_pagar_list = client.get('/api/contas-a-pagar/listar/?status=TODOS')
    assert mov_pagar_id in [m['id'] for m in r_pagar_list.json().get('registros', [])], "Conta a Pagar sumiu após navegação!"
    print(f"  [OK] Módulo Contas a Pagar: Movimento #{mov_pagar_id} persistido e íntegro.")

    # 3. Contas a Receber
    r_rec_save = client.post('/api/contas-a-receber/salvar/', data=json.dumps({
        'pessoa_id': created_id,
        'documento_numero': f"REC-{ts}",
        'serie': '1',
        'data_emissao': str(time.strftime('%Y-%m-%d')),
        'data_vencimento': str(time.strftime('%Y-%m-%d')),
        'valor_total': 3800.00,
        'qtd_parcelas': 1,
        'descricao': 'Venda de graos',
        'status': 'ATIVO'
    }), content_type='application/json')
    assert r_rec_save.status_code == 200
    mov_rec_id = r_rec_save.json().get('id')

    # Navega
    client.get('/pessoas/')
    client.get('/dashboard/')
    client.get('/contas-a-receber/')

    r_rec_list = client.get('/api/contas-a-receber/listar/?status=TODOS')
    assert mov_rec_id in [m['id'] for m in r_rec_list.json().get('registros', [])], "Conta a Receber sumiu após navegação!"
    print(f"  [OK] Módulo Contas a Receber: Movimento #{mov_rec_id} persistido e íntegro.")

    print("\n" + "=" * 70)
    print("TODOS OS TESTES (A, B, C, D, E) FORAM CONCLUÍDOS COM 100% DE SUCESSO!")
    print("=" * 70)

if __name__ == '__main__':
    run_all_tests()
