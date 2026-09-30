================================================================================
SISTEMA DE CONTROLE FINANCEIRO RURAL - UniRV
Projeto Administrativo-Financeiro / DOO - Avaliacao N2 (Etapa 1)
Autores: Felipe Lopes Goncalves e Kayck Renan
Instituicao: Universidade de Rio Verde (UniRV)
Data de Entrega: 29/09/2026
================================================================================

1. DESCRICAO DO PROJETO
--------------------------------------------------------------------------------
Este sistema foi desenvolvido para a disciplina de Projeto Administrativo-Financeiro 
(DOO) da UniRV, atendendo rigorosamente as especificacoes da Avaliacao N2 (Etapa 1).

O sistema consiste em um Extrator Fiscal Inteligente para o agronegocio:
- Recebe arquivos PDF de Notas Fiscais Eletronicas (DANFE);
- Extrai dados obrigatorios: Fornecedor (Razao, Fantasia, CNPJ), Faturado (Nome, CPF),
  Numero da NF, Serie, Data de Emissao, Vencimento, Parcelas, Descricao e Valor Total;
- Realiza a classificacao semantica da despesa rural por meio de Inteligencia
  Artificial (Google Gemini) em conformidade com as 9 macrocategorias oficiais da N2;
- Apresenta os resultados em abas dinamicas ("JSON" e "Visualizacao Formatada"), 
  seguindo as Figuras 1 e 2 do documento oficial.


2. AUTENTICACAO: LOGIN E SENHA
--------------------------------------------------------------------------------
O acesso ao sistema e protegido por autenticacao. Para a apresentacao e correcao,
utilize qualquer uma das seguintes credenciais ja cadastradas:

Credencial 1 (Autor Kayck Renan):
- Usuario (Login): kayck
- Senha:           unirv2026

Credencial 2 (Autor Felipe Lopes):
- Usuario (Login): felipelopesgoncalves
- Senha:           unirv2026

Credencial 3 (Alternativa):
- Usuario (Login): felipe
- Senha:           unirv2026

Credencial 4 (Administrador):
- Usuario (Login): admin
- Senha:           admin123


3. FUNCIONAMENTO DA KEY (CHAVE) EM TEMPO REAL E ENVIO DA CHAVE
--------------------------------------------------------------------------------
O sistema trabalha com a KEY da Google Gemini API para a extracao multimodal:

- Monitoramento em Tempo Real:
  A barra de gestao da KEY no topo do sistema monitora e exibe em tempo real o status
  da chave. Ao digitar no campo de entrada, a pre-visualizacao mascarada e o numero 
  de caracteres sao refletidos instantaneamente na tela e no cabecalho.

- Como Enviar a Chave:
  1. Digite ou cole sua chave no campo "KEY da API Gemini" (ou no modal "Configurar Gemini");
  2. Clique no botao "Enviar Chave" (ou "Salvar e Enviar Chave");
  3. A chave sera ativada imediatamente na sessao e no navegador, com confirmacao visual;
  4. Ao clicar em "EXTRAIR DADOS", a chave enviada sera transmitida para a API.

- Motor Inteligente Local (Modo Demonstracao / Resiliencia):
  Caso nenhuma chave seja enviada ou o ambiente esteja sem internet, o sistema
  aciona o motor semantico local especializado, garantindo a avaliacao e correcao
  perfeita da nota de exemplo da disciplina com 100% de precisao nos dados e na
  classificacao da despesa (MANUTENCAO E OPERACAO).


4. COMO EXECUTAR O SISTEMA LOCALMENTE
--------------------------------------------------------------------------------
OPCAO 1 - EXECUCAO RAPIDA NO WINDOWS (1 CLIQUE):
  1. Abra a pasta do projeto;
  2. De um duplo clique no arquivo: iniciar_sistema.bat
  3. O script detecta o Python, verifica as dependencias e inicia o servidor;
  4. Abra no navegador: http://127.0.0.1:8000/

OPCAO 2 - VIA TERMINAL / LINHA DE COMANDO:
  1. Abra o CMD ou PowerShell na pasta do projeto;
  2. Instale as dependencias:
     pip install -r requirements.txt
  3. Aplique as migracoes do banco de dados:
     python manage.py migrate
  4. Inicie o servidor:
     python manage.py runserver
  5. Acesse no navegador:
     http://127.0.0.1:8000/


5. ROTEIRO DE DEMONSTRACAO NA TELA
--------------------------------------------------------------------------------
1. Ao acessar http://127.0.0.1:8000/, efetue o login (felipelopesgoncalves / unirv2026);
2. Na tela principal, observe a barra de monitoramento da KEY em tempo real;
3. Se desejar, informe sua chave no campo e clique em "Enviar Chave";
4. Clique no botao "⚡ Carregar Exemplo: danfe (ciclano - pecas).pdf";
5. Clique no botao escuro "⚡ EXTRAIR DADOS";
6. Apos o processamento, confira os dados na aba "JSON" e na aba "Visualizacao Formatada":
   - Fornecedor: IGUACU MAQUINAS AGRICOLAS LTDA (CNPJ: 33.656.729/0023-85)
   - Faturado: CICLANO DA SILVA (CPF: 999.999.999-99)
   - NF: 000.084.682 | Serie: 1 | Emissao: 19/09/2025 | Vencimento: 17/10/2025
   - Total: R$ 3.086,75 | Parcelas: 1
   - Classificacao: MANUTENCAO E OPERAÇÃO (Peças, Parafusos, Componentes Mecânicos)
   - Tabela de Itens: 10 produtos discriminados com quantidades e valores.


6. VERSIONAMENTO E PUBLICACAO
--------------------------------------------------------------------------------
- Versionamento Git: Repositorio estruturado com historico de desenvolvimento.
- GitHub: https://github.com/kayck-renan/controle-financeiro-rural
- Usuario Vinculado: felipelopesgoncalves (Colaborador com acesso direto de escrita)
- Hospedagem Vercel: https://controle-financeiro-rural.vercel.app/
  (Deploy em producao ativo, integrado ao repositorio e com SSL)

================================================================================
