from django.db import models
from django.utils import timezone


class Pessoas(models.Model):
    """
    Entidade PESSOAS: Representa Fornecedores, Clientes e Faturados.
    Regras:
    - Não podem ser excluídos fisicamente, apenas inativados (status = INATIVO).
    - Suporta reativação para status = ATIVO.
    """
    TIPO_CHOICES = [
        ('FORNECEDOR', 'Fornecedor'),
        ('CLIENTE', 'Cliente'),
        ('FATURADO', 'Faturado'),
        ('CLIENTE-FORNECEDOR', 'Cliente / Fornecedor'),
    ]

    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
    ]

    razao_social = models.CharField(max_length=255, verbose_name="Razão Social / Nome")
    nome_fantasia = models.CharField(max_length=255, blank=True, default='', verbose_name="Nome Fantasia")
    cpf_cnpj = models.CharField(max_length=30, blank=True, default='', verbose_name="CPF / CNPJ")
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, default='FORNECEDOR', verbose_name="Tipo de Pessoa")
    email = models.CharField(max_length=255, blank=True, default='', verbose_name="E-mail")
    telefone = models.CharField(max_length=50, blank=True, default='', verbose_name="Telefone")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ATIVO', verbose_name="Status")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
        ordering = ['razao_social']

    def __str__(self):
        doc = f" ({self.cpf_cnpj})" if self.cpf_cnpj else ""
        return f"{self.razao_social}{doc} [{self.get_tipo_display()}]"

    def inativar(self):
        self.status = 'INATIVO'
        self.save(update_fields=['status', 'data_atualizacao'])

    def reativar(self):
        self.status = 'ATIVO'
        self.save(update_fields=['status', 'data_atualizacao'])


class Classificacao(models.Model):
    """
    Entidade CLASSIFICACAO: Categorias contábeis de Despesas e Receitas rurais.
    Ex: MANUTENÇÃO E OPERAÇÃO, INSUMOS AGRÍCOLAS, etc.
    Regras:
    - Exclusão lógica (status = INATIVO).
    """
    TIPO_CHOICES = [
        ('DESPESA', 'Despesa'),
        ('RECEITA', 'Receita'),
    ]

    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
    ]

    descricao = models.CharField(max_length=255, verbose_name="Descrição da Classificação")
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='DESPESA', verbose_name="Tipo")
    observacoes = models.TextField(blank=True, default='', verbose_name="Observações / Detalhes")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ATIVO', verbose_name="Status")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    class Meta:
        verbose_name = "Classificação"
        verbose_name_plural = "Classificações"
        ordering = ['descricao']

    def __str__(self):
        return f"{self.descricao} ({self.get_tipo_display()})"

    def inativar(self):
        self.status = 'INATIVO'
        self.save(update_fields=['status'])

    def reativar(self):
        self.status = 'ATIVO'
        self.save(update_fields=['status'])


class MovimentoContas(models.Model):
    """
    Entidade MOVIMENTOCONTAS: Registros financeiros de Contas a Pagar e Contas a Receber.
    Regras:
    - Um registro de contas a pagar pode ser classificado em uma ou mais Tipo de DESPESAS.
    - Um registro de contas a receber pode ser classificado em uma ou mais Tipo de RECEITAS.
    - Um registro pode ter uma ou mais PARCELAS com data de vencimento distinto.
    - Exclusão lógica (status = INATIVO).
    """
    TIPO_CHOICES = [
        ('APAGAR', 'Contas a Pagar'),
        ('ARECEBER', 'Contas a Receber'),
    ]

    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
    ]

    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='APAGAR', verbose_name="Tipo de Movimento")
    pessoa = models.ForeignKey(
        Pessoas,
        on_delete=models.PROTECT,
        related_name='movimentos',
        verbose_name="Pessoa Principal (Fornecedor / Cliente)"
    )
    faturado = models.ForeignKey(
        Pessoas,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movimentos_faturado',
        verbose_name="Faturado (Produtor / Destinatário)"
    )
    documento_numero = models.CharField(max_length=50, blank=True, default='', verbose_name="Nº Documento / NF")
    serie = models.CharField(max_length=20, blank=True, default='1', verbose_name="Série")
    data_emissao = models.DateField(verbose_name="Data de Emissão", default=timezone.now)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor Total (R$)")
    descricao = models.TextField(blank=True, default='', verbose_name="Descrição / Produtos")
    classificacoes = models.ManyToManyField(
        Classificacao,
        related_name='movimentos',
        verbose_name="Classificações Contábeis"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ATIVO', verbose_name="Status")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    class Meta:
        verbose_name = "Movimento de Contas"
        verbose_name_plural = "Movimentos de Contas"
        ordering = ['-data_emissao', '-id']

    def __str__(self):
        doc = f" - NF {self.documento_numero}" if self.documento_numero else ""
        return f"[{self.get_tipo_display()}] #{self.id}{doc} - R$ {self.valor_total} ({self.pessoa.razao_social})"

    def inativar(self):
        self.status = 'INATIVO'
        self.save(update_fields=['status'])
        # Inativa também as parcelas associadas
        self.parcelas.all().update(status='INATIVO')

    def reativar(self):
        self.status = 'ATIVO'
        self.save(update_fields=['status'])
        self.parcelas.all().update(status='ATIVO')


class ParcelaContas(models.Model):
    """
    Entidade PARCELACONTAS: Parcelas vinculadas ao Movimento de Contas.
    Regras:
    - Identificação (ÚNICA ou número da parcela).
    - Data de vencimento e valor individual.
    - Exclusão lógica (status = INATIVO).
    """
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
    ]

    STATUS_PAGAMENTO_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago / Liquidado'),
    ]

    movimento = models.ForeignKey(
        MovimentoContas,
        on_delete=models.CASCADE,
        related_name='parcelas',
        verbose_name="Movimento de Contas"
    )
    identificacao = models.CharField(max_length=50, default='ÚNICA', verbose_name="Identificação da Parcela")
    numero_parcela = models.IntegerField(default=1, verbose_name="Número da Parcela")
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor (R$)")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ATIVO', verbose_name="Status")
    status_pagamento = models.CharField(
        max_length=20,
        choices=STATUS_PAGAMENTO_CHOICES,
        default='PENDENTE',
        verbose_name="Status de Pagamento"
    )
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    class Meta:
        verbose_name = "Parcela de Conta"
        verbose_name_plural = "Parcelas de Contas"
        ordering = ['movimento', 'numero_parcela', 'data_vencimento']

    def __str__(self):
        return f"Parcela {self.identificacao} - Venc: {self.data_vencimento} - R$ {self.valor}"

    def inativar(self):
        self.status = 'INATIVO'
        self.save(update_fields=['status'])

    def reativar(self):
        self.status = 'ATIVO'
        self.save(update_fields=['status'])
