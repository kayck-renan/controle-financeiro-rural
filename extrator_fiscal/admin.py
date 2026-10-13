from django.contrib import admin
from .models import Pessoas, Classificacao, MovimentoContas, ParcelaContas


@admin.register(Pessoas)
class PessoasAdmin(admin.ModelAdmin):
    list_display = ('id', 'razao_social', 'cpf_cnpj', 'tipo', 'status', 'data_cadastro')
    list_filter = ('tipo', 'status')
    search_fields = ('razao_social', 'nome_fantasia', 'cpf_cnpj')


@admin.register(Classificacao)
class ClassificacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'tipo', 'status', 'data_cadastro')
    list_filter = ('tipo', 'status')
    search_fields = ('descricao',)


class ParcelaContasInline(admin.TabularInline):
    model = ParcelaContas
    extra = 1


@admin.register(MovimentoContas)
class MovimentoContasAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'pessoa', 'documento_numero', 'valor_total', 'data_emissao', 'status')
    list_filter = ('tipo', 'status')
    search_fields = ('documento_numero', 'pessoa__razao_social')
    filter_horizontal = ('classificacoes',)
    inlines = [ParcelaContasInline]


@admin.register(ParcelaContas)
class ParcelaContasAdmin(admin.ModelAdmin):
    list_display = ('id', 'movimento', 'identificacao', 'data_vencimento', 'valor', 'status_pagamento', 'status')
    list_filter = ('status', 'status_pagamento')
