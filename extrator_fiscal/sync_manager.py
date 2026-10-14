import logging
from decimal import Decimal
from datetime import datetime, date
from django.db import connection

logger = logging.getLogger(__name__)

def registrar_mutacao(request, tipo_entidade, obj):
    """
    Registra uma alteração (criação, edição, inativação ou reativação) na sessão do usuário.
    Como a sessão utiliza cookies assinados (signed_cookies), essa lista viaja com o navegador
    para qualquer instância serverless (Vercel) ou ambiente local, garantindo sincronismo total.
    """
    if not hasattr(request, 'session'):
        return

    try:
        from .models import Pessoas, Classificacao, MovimentoContas

        dados = {}
        if tipo_entidade == 'PESSOA':
            dados = {
                'tipo_entidade': 'PESSOA',
                'id': obj.id,
                'razao_social': obj.razao_social,
                'nome_fantasia': obj.nome_fantasia or '',
                'cpf_cnpj': obj.cpf_cnpj or '',
                'tipo': obj.tipo,
                'email': obj.email or '',
                'telefone': obj.telefone or '',
                'status': obj.status,
            }
        elif tipo_entidade == 'CLASSIFICACAO':
            dados = {
                'tipo_entidade': 'CLASSIFICACAO',
                'id': obj.id,
                'descricao': obj.descricao,
                'tipo': obj.tipo,
                'observacoes': obj.observacoes or '',
                'status': obj.status,
            }
        elif tipo_entidade == 'MOVIMENTO':
            class_ids = list(obj.classificacoes.values_list('id', flat=True)) if hasattr(obj, 'classificacoes') else []
            parcelas_lista = []
            if hasattr(obj, 'parcelas'):
                for p in obj.parcelas.all():
                    parcelas_lista.append({
                        'identificacao': p.identificacao,
                        'numero_parcela': p.numero_parcela,
                        'data_vencimento': str(p.data_vencimento),
                        'valor': str(p.valor),
                        'status': p.status,
                        'status_pagamento': p.status_pagamento,
                    })

            dados = {
                'tipo_entidade': 'MOVIMENTO',
                'id': obj.id,
                'tipo': obj.tipo,
                'pessoa_id': obj.pessoa_id,
                'faturado_id': obj.faturado_id,
                'documento_numero': obj.documento_numero or '',
                'serie': obj.serie or '1',
                'data_emissao': str(obj.data_emissao),
                'valor_total': str(obj.valor_total),
                'descricao': obj.descricao or '',
                'status': obj.status,
                'classificacoes': class_ids,
                'parcelas': parcelas_lista,
            }

        if not dados:
            return

        mutacoes = request.session.get('rural_sync_mutations', [])
        # Atualiza mutação existente para o mesmo tipo e id ou adiciona nova
        atualizado = False
        for i, m in enumerate(mutacoes):
            if m.get('tipo_entidade') == tipo_entidade and m.get('id') == obj.id:
                mutacoes[i] = dados
                atualizado = True
                break
        if not atualizado:
            mutacoes.append(dados)

        # Limita às 100 alterações mais recentes para manter o cookie leve e seguro
        request.session['rural_sync_mutations'] = mutacoes[-100:]
        request.session.modified = True

    except Exception as e:
        logger.warning("Falha ao registrar mutação para sincronismo: %s", str(e))


def sincronizar_banco_da_sessao(request):
    """
    Aplica as mutações registradas na sessão no banco SQLite da instância atual.
    Isso elimina o problema de isolamento entre lambdas efêmeras no Vercel e
    garante persistência e consistência total entre trocas de abas.
    """
    if not hasattr(request, 'session'):
        return

    mutacoes = request.session.get('rural_sync_mutations')
    if not mutacoes:
        return

    try:
        from .models import Pessoas, Classificacao, MovimentoContas, ParcelaContas

        modificou = False

        # 1. Aplica Pessoas e Classificações primeiro (são dependências de Movimentos)
        for m in mutacoes:
            tipo = m.get('tipo_entidade')
            rec_id = m.get('id')
            if not rec_id:
                continue

            if tipo == 'PESSOA':
                obj = Pessoas.objects.filter(id=rec_id).first()
                if not obj or obj.status != m.get('status') or obj.razao_social != m.get('razao_social'):
                    Pessoas.objects.update_or_create(
                        id=rec_id,
                        defaults={
                            'razao_social': m.get('razao_social', ''),
                            'nome_fantasia': m.get('nome_fantasia', ''),
                            'cpf_cnpj': m.get('cpf_cnpj', ''),
                            'tipo': m.get('tipo', 'FORNECEDOR'),
                            'email': m.get('email', ''),
                            'telefone': m.get('telefone', ''),
                            'status': m.get('status', 'ATIVO'),
                        }
                    )
                    modificou = True

            elif tipo == 'CLASSIFICACAO':
                obj = Classificacao.objects.filter(id=rec_id).first()
                if not obj or obj.status != m.get('status') or obj.descricao != m.get('descricao'):
                    Classificacao.objects.update_or_create(
                        id=rec_id,
                        defaults={
                            'descricao': m.get('descricao', ''),
                            'tipo': m.get('tipo', 'DESPESA'),
                            'observacoes': m.get('observacoes', ''),
                            'status': m.get('status', 'ATIVO'),
                        }
                    )
                    modificou = True

        # 2. Aplica MovimentoContas e suas Parcelas
        for m in mutacoes:
            if m.get('tipo_entidade') != 'MOVIMENTO':
                continue

            rec_id = m.get('id')
            if not rec_id:
                continue

            pessoa_id = m.get('pessoa_id')
            if not pessoa_id or not Pessoas.objects.filter(id=pessoa_id).exists():
                continue

            faturado_id = m.get('faturado_id')
            faturado = Pessoas.objects.filter(id=faturado_id).first() if faturado_id else None

            data_emissao_val = m.get('data_emissao')
            if data_emissao_val:
                try:
                    data_emissao = datetime.strptime(data_emissao_val[:10], "%Y-%m-%d").date()
                except Exception:
                    data_emissao = date.today()
            else:
                data_emissao = date.today()

            valor_total_val = Decimal(str(m.get('valor_total', 0)).replace(',', '.'))

            mov, created = MovimentoContas.objects.update_or_create(
                id=rec_id,
                defaults={
                    'tipo': m.get('tipo', 'APAGAR'),
                    'pessoa_id': pessoa_id,
                    'faturado': faturado,
                    'documento_numero': m.get('documento_numero', ''),
                    'serie': m.get('serie', '1'),
                    'data_emissao': data_emissao,
                    'valor_total': valor_total_val,
                    'descricao': m.get('descricao', ''),
                    'status': m.get('status', 'ATIVO'),
                }
            )

            # Classificações associadas
            class_ids = m.get('classificacoes', [])
            if class_ids:
                mov.classificacoes.set(class_ids)

            # Parcelas
            parcelas_data = m.get('parcelas', [])
            if parcelas_data:
                # Recria parcelas se o movimento acabou de ser inserido ou atualizado
                if created or mov.parcelas.count() != len(parcelas_data):
                    mov.parcelas.all().delete()
                    for idx, p_info in enumerate(parcelas_data, start=1):
                        venc_str = p_info.get('data_vencimento')
                        try:
                            venc = datetime.strptime(venc_str[:10], "%Y-%m-%d").date() if venc_str else data_emissao
                        except Exception:
                            venc = data_emissao
                        vlr = Decimal(str(p_info.get('valor', valor_total_val)).replace(',', '.'))
                        ParcelaContas.objects.create(
                            movimento=mov,
                            identificacao=p_info.get('identificacao', f"{idx}/{len(parcelas_data)}"),
                            numero_parcela=p_info.get('numero_parcela', idx),
                            data_vencimento=venc,
                            valor=vlr,
                            status=p_info.get('status', 'ATIVO'),
                            status_pagamento=p_info.get('status_pagamento', 'PENDENTE')
                        )
            modificou = True

        # Ajusta sequência do SQLite se aplicável para evitar colisões de IDs futuros
        if modificou and connection.vendor == 'sqlite':
            with connection.cursor() as cursor:
                try:
                    cursor.execute("""
                        UPDATE sqlite_sequence
                        SET seq = (SELECT MAX(id) FROM extrator_fiscal_pessoas)
                        WHERE name = 'extrator_fiscal_pessoas' AND EXISTS (SELECT 1 FROM extrator_fiscal_pessoas);
                    """)
                    cursor.execute("""
                        UPDATE sqlite_sequence
                        SET seq = (SELECT MAX(id) FROM extrator_fiscal_classificacao)
                        WHERE name = 'extrator_fiscal_classificacao' AND EXISTS (SELECT 1 FROM extrator_fiscal_classificacao);
                    """)
                    cursor.execute("""
                        UPDATE sqlite_sequence
                        SET seq = (SELECT MAX(id) FROM extrator_fiscal_movimentocontas)
                        WHERE name = 'extrator_fiscal_movimentocontas' AND EXISTS (SELECT 1 FROM extrator_fiscal_movimentocontas);
                    """)
                except Exception:
                    pass

    except Exception as e:
        logger.warning("Falha na sincronização do banco a partir da sessão: %s", str(e))
