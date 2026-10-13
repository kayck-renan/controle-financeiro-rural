================================================================================
SISTEMA DE CONTROLE FINANCEIRO RURAL - UNIRV
Projeto Administrativo-Financeiro / DOO - Avaliacao N2 (Etapa 1 e Etapa 2)
Autores: Kayck Renan e Felipe Lopes Goncalves
Instituicao: Universidade de Rio Verde (UniRV)
Data de Entrega: Outubro/2026
================================================================================

1. DADOS DE ACESSO E ENTREGA (SOLICITACAO DO PROFESSOR)
--------------------------------------------------------------------------------
- Link Hospedagem:
  https://controle-financeiro-rural.vercel.app/

- Login:
  kayck   (ou: felipelopesgoncalves)

- Senha:
  unirv2026

- Key (LLM):
  AIzaSyDemoUniRV2026RuralFinancasKey99

- Codigo Ultima Atualizacao no GitHub:
  Commit: 0d8427b (Exibido no cabecalho e na tela principal do projeto)
  Repositorio: https://github.com/kayck-renan/controle-financeiro-rural


2. CREDENCIAIS DE DEMONSTRACAO CADASTRADAS NO BANCO
--------------------------------------------------------------------------------
| Usuario (Login)       | Senha     | Perfil / Nome Exibido          |
| :-------------------- | :-------- | :----------------------------- |
| kayck                 | unirv2026 | Kayck Renan (Autor/Dev)        |
| felipelopesgoncalves  | unirv2026 | Felipe Lopes Gonçalves (Autor)  |
| felipe                | unirv2026 | Felipe (Acesso Alternativo)    |
| admin                 | admin123  | Administrador Geral             |


3. ESCOPO E FUNCIONALIDADES DA ETAPA 2 (CONFORME EDITAL N2)
--------------------------------------------------------------------------------
O sistema evoluiu da extracao de DANFE para um ERP Financeiro Rural completo:

A. MODULO MANTER PESSOAS (/pessoas/):
   - MANTER FORNECEDOR
   - MANTER CLIENTE
   - MANTER FATURADO
   - Regras de Negocio Atendidas:
     * Cadastros nao podem ser excluidos.
     * Exclusao logica implementada: STATUS = INATIVO.
     * Reativacao permitida: STATUS volta para ATIVO.
     * Layout da disciplina: Tabela inicia vazia, busca multi-elemento ou
       botao TODOS (que carrega apenas registros com status = ATIVO).
     * No CREATE: campo STATUS oculto == ATIVO.
     * No UPDATE: campo STATUS oculto.
     * No DELETE: altera campo STATUS == INATIVO.

B. MODULO MANTER CLASSIFICACAO (/classificacoes/):
   - MANTER TIPO DE DESPESA (9 Macrocategorias oficiais da N2)
   - MANTER TIPO DE RECEITA (Venda de Graos, Hortifruti, Servicos)
   - Regras de negocio, busca, botao TODOS e inativacao logica.

C. MODULO REGISTRAR CONTAS (/contas-a-pagar/ e /contas-a-receber/):
   - REGISTRAR CONTAS A PAGAR:
     * Pode ser classificado em UMA OU MAIS tipos de DESPESAS.
     * Suporta UMA OU MAIS PARCELAS com datas de vencimento distintas.
   - REGISTRAR CONTAS A RECEBER:
     * Pode ser classificado em UMA OU MAIS tipos de RECEITAS.
     * Suporta UMA OU MAIS PARCELAS com datas de vencimento distintas.

D. ATIVIDADE DA 2ª ETAPA INTEGRADA AO EXTRATOR FISCAL:
   - Apos a extracao da DANFE (PDF), o sistema consulta o Banco de Dados e informa:
     * FORNECEDOR: Existe ou Nao Existe (com ID exibido em tela)
     * FATURADO:   Existe ou Nao Existe (com ID exibido em tela)
     * DESPESA:    Existe ou Nao Existe (com ID exibido em tela)
   - Botao de Lancamento em 1 Clique que executa automaticamente:
     1. Cria o novo fornecedor (se for o caso)
     2. Cria o novo faturado (se for o caso)
     3. Cria a nova despesa (se for o caso)
     4. Cria o registro do MOVIMENTO e suas PARCELAS
     5. Notifica o usuario de sucesso com os IDs gerados.

E. SEGURANCA DA CHAVE (LLM):
   - A chave da API Google Gemini fica oculta e mascarada na interface (••••••••),
     garantindo a privacidade e protecao contra visualizacao indevida.
   - O codigo da ultima atualizacao no GitHub e renderizado dinamicamente no topo.


4. COMO EXECUTAR O SISTEMA LOCALMENTE
--------------------------------------------------------------------------------
1. Abra a pasta do projeto no Windows;
2. De um duplo clique no arquivo: iniciar_sistema.bat
3. O script detecta o Python, aplica as migracoes e inicia o servidor;
4. Acesse no navegador: http://127.0.0.1:8000/


5. LINKS E VERSIONAMENTO
--------------------------------------------------------------------------------
- Link do Site (Producao):
  https://controle-financeiro-rural.vercel.app/

- Repositorio no GitHub:
  https://github.com/kayck-renan/controle-financeiro-rural

================================================================================
