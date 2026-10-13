from django.test import TestCase, Client
from django.contrib.auth.models import User
from decimal import Decimal
import json

from .models import Pessoas, Classificacao, MovimentoContas, ParcelaContas


class Etapa2BusinessRulesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password123')
        self.client = Client()
        self.client.login(username='tester', password='password123')

        # Cria entidades de teste
        self.fornecedor = Pessoas.objects.create(
            razao_social='IGUAÇU MAQUINAS AGRICOLAS LTDA',
            cpf_cnpj='33.656.729/0023-85',
            tipo='CLIENTE-FORNECEDOR',
            status='ATIVO'
        )
        self.faturado = Pessoas.objects.create(
            razao_social='CICLANO DA SILVA',
            cpf_cnpj='999.999.999-99',
            tipo='FATURADO',
            status='ATIVO'
        )
        self.despesa1 = Classificacao.objects.create(
            descricao='MANUTENÇÃO E OPERAÇÃO',
            tipo='DESPESA',
            status='ATIVO'
        )
        self.despesa2 = Classificacao.objects.create(
            descricao='INSUMOS AGRÍCOLAS',
            tipo='DESPESA',
            status='ATIVO'
        )

    def test_regra_inativacao_e_reativacao(self):
        """Regra: Cadastros não podem ser excluídos fisicamente, apenas INATIVADOS e REATIVADOS."""
        p = self.fornecedor
        p.inativar()
        self.assertEqual(p.status, 'INATIVO')

        p.reativar()
        self.assertEqual(p.status, 'ATIVO')

    def test_consulta_entidades_existentes_e_inexistentes(self):
        """Atividade 2ª Etapa: Consultar no BD se Fornecedor, Faturado e Despesa existem ou não."""
        payload = {
            'fornecedor': {'razaoSocial': 'IGUAÇU MAQUINAS AGRICOLAS LTDA', 'cnpj': '33.656.729/0023-85'},
            'faturado': {'nomeCompleto': 'CICLANO DA SILVA', 'cpf': '999.999.999-99'},
            'classificacaoDespesa': 'MANUTENÇÃO E OPERAÇÃO'
        }
        res = self.client.post('/api/consultar-entidades/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        dados = res.json()
        self.assertTrue(dados['fornecedor']['existe'])
        self.assertTrue(dados['faturado']['existe'])
        self.assertTrue(dados['despesa']['existe'])

    def test_lancar_movimento_automatico_etapa2(self):
        """Regra da 2ª Etapa: Executar os 5 passos de lançamento e registro no Banco de Dados."""
        payload = {
            'fornecedor': {'razaoSocial': 'NOVA AGROPECUARIA LTDA', 'cnpj': '11.222.333/0001-44'},
            'faturado': {'nomeCompleto': 'PRODUTOR NOVO', 'cpf': '123.456.789-00'},
            'classificacaoDespesa': 'SEGUROS E PROTEÇÃO',
            'numero': '000.123.456',
            'serie': '1',
            'dataEmissao': '2026-10-10',
            'dataVencimento': '2026-11-10',
            'valorTotal': 5000.00,
            'quantidadeParcelas': 2,
            'descricaoProdutos': 'Apólice de Seguro Agrícola de Safra'
        }
        res = self.client.post('/api/lancar-movimento/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        dados = res.json()
        self.assertTrue(dados['sucesso'])

        # Verifica se o fornecedor novo foi criado (Passo 1)
        self.assertTrue(Pessoas.objects.filter(razao_social='NOVA AGROPECUARIA LTDA').exists())
        # Verifica se o faturado novo foi criado (Passo 2)
        self.assertTrue(Pessoas.objects.filter(razao_social='PRODUTOR NOVO').exists())
        # Verifica se a nova despesa foi criada (Passo 3)
        self.assertTrue(Classificacao.objects.filter(descricao='SEGUROS E PROTEÇÃO').exists())
        # Verifica o movimento e suas parcelas (Passo 4)
        mov_id = dados['detalhes']['movimento_id']
        mov = MovimentoContas.objects.get(id=mov_id)
        self.assertEqual(mov.valor_total, Decimal('5000.00'))
        self.assertEqual(mov.parcelas.count(), 2)

    def test_multiplas_classificacoes_e_parcelas(self):
        """Regra: Contas a pagar/receber com mais de uma classificação e parcelas."""
        mov = MovimentoContas.objects.create(
            tipo='APAGAR',
            pessoa=self.fornecedor,
            documento_numero='NF-999',
            data_emissao='2026-10-01',
            valor_total=Decimal('2000.00')
        )
        mov.classificacoes.add(self.despesa1, self.despesa2)
        self.assertEqual(mov.classificacoes.count(), 2)
