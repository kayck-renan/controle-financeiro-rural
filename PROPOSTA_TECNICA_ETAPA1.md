# Proposta Técnica Completa de Implementação do Sistema
## Sistema de Controle Financeiro Rural — Avaliação N2 (Etapa 1 e Etapa 2)

**Autores do Projeto:** Felipe Lopes Gonçalves e Kayck Renan  
**Instituição:** Universidade de Rio Verde (UniRV)  
**Disciplina:** Projeto Administrativo-Financeiro / Desenvolvimento Orientado a Objetos (DOO)  
**Data de Emissão da Proposta:** 23/09/2026  
**Documentos Base Analisados:**
1. `DOCUMENTACAOREQUISITOS_FelipeLopes_KayckRenan.pdf` (Documento de Requisitos do Cliente e Especificação Inicial - v1.00)
2. `requisitos.txt` (Pilha Tecnológica Homologada: Linguagens: Python, JavaScript, TypeScript | Frameworks: DJANGO, Node | SGBD: PostGree, MySQL)
3. Arquivo `18. Felipe Lopes Gonçalves e Kayck Renan.pdf` (Folha de Devolutiva / Avaliação e Recomendações do Docente)
4. `PROJETO ADMINISTRATIVO - N2 - Etapa 1.docx.pdf` (Diretrizes Oficiais da Avaliação N2: Etapa 1 e Etapa 2)
5. `danfe (ciclano - pecas).pdf` (Amostra Operacional de Nota Fiscal Eletrônica - DANFE para testes da Etapa 1)

---

### 1. Visão Geral do Sistema

#### 1.1 Objetivo do Sistema
O **Sistema de Controle Financeiro Rural** é uma solução de software corporativa desenvolvida para informatizar, centralizar e simplificar a gestão de contas a pagar, contas a receber, parcelamentos e movimentações financeiras de uma propriedade agropecuária. O objetivo central é eliminar o uso de papéis avulsos e anotações manuais, minimizando drasticamente o risco de erros operacionais através de automação orientada a Inteligência Artificial Generativa (**Google Gemini**).

#### 1.2 Principais Usuários e Perfis
* **Proprietário Rural e Filhos (Beltrano, Fulano e Ciclano):** Gestores operacionais e beneficiários legais da fazenda. Conforme explicitado no documento de requisitos, os produtores rurais possuem pouca escolaridade técnica, o que impõe a necessidade mandatória de interfaces extremamente simples, objetivas, com baixa carga cognitiva, orientadas a "uma ação por vez", mensagens claras e ausência de jargões técnicos de TI. Despesas e receitas podem ser faturadas no CPF de qualquer um dos três sócios.
* **Responsável Financeiro / Operador:** Perfil responsável pela operação do sistema web: carregamento de notas fiscais em PDF, conferência da extração e classificação gerada pela IA, confirmação de lançamentos, baixa/quitação de parcelas e consulta de relatórios consolidados.
* **Serviço de E-mail / Captura Automatizada (Serviço Integrador):** Canal secundário de entrada previsto no documento de requisitos para recebimento direto de faturas anexas por correio eletrônico.

#### 1.3 Funcionalidades Principais
* **Etapa 1 (Foco Imediato - Entrega 29/09/2026 - Peso 35%):** Interface gráfica WEB para upload de documento fiscal em PDF; integração no backend com a API do Google Gemini para leitura e OCR inteligente; extração dos campos obrigatórios (Fornecedor, Faturado, Número da NF, Data de Emissão, Vencimento, Valor Total e Produtos); classificação automática da despesa segundo as categorias do agronegócio; e exibição na tela em formato JSON estruturado e visualização formatada, acompanhado de botão para copiar o JSON.
* **Etapa 2 (Consolidação Operacional - Entrega 28/10/2026 - Peso 45%):** Persistência no banco relacional (PostgreSQL/MySQL); manutenção completa dos cadastros (Fornecedores, Clientes, Faturados, Categorias) com regra mandatória de **inativação lógica (sem exclusão física)** e reativação; controle de Contas a Pagar e a Receber; controle de parcelamentos múltiplos com datas de vencimento distintas; controle de liquidação financeira com suporte a pagamentos parciais; e emissão de relatórios gerenciais consolidados.

#### 1.4 Fluxo Geral de Funcionamento
1. O usuário acessa a aplicação web e faz o upload da nota fiscal (PDF).
2. O backend em **Django** recebe o arquivo em memória e despacha uma solicitação multimodal para a **API do Google Gemini**, injetando as 9 categorias agropecuárias da disciplina.
3. O Gemini processa o layout visual do documento, extrai as entidades fiscais e deduz semanticamente a categoria da despesa com base nos itens discriminados.
4. O backend retorna o payload JSON validado para o frontend, que renderiza instantaneamente as abas de "Visualização Formatada" e "JSON", permitindo a conferência e cópia do código JSON.
5. Na Etapa 2, o usuário valida os dados em tela e confirma a gravação: o Django ORM cria os registros em `FornecedorCliente`, `MovimentoContas` e `MovimentoParcelas`, deixando o título pronto para recebimento de quitações em `MovimentoFinanceiro`.

---

### 2. Requisitos Consolidados

A consolidação abaixo unifica os requisitos de todos os documentos oficiais disponibilizados, rastreando a proveniência exata de cada item.

#### 2.1 Requisitos Funcionais (RF)
* **RF01 - Manter Fornecedores e Clientes:** Cadastrar, listar, consultar, editar, inativar e reativar registros de parceiros comerciais externos (fornecedores de insumos/serviços e clientes compradores). *Origem: DOCUMENTACAOREQUISITOS (RF01), Arquivo 18 (Item i) e PROJETO N2.*
* **RF02 - Manter Faturados:** Cadastrar, listar, consultar, editar, inativar e reativar os dados dos três responsáveis legais da fazenda (o proprietário e os dois filhos: Beltrano, Fulano e Ciclano), associando CPF e nome completo. *Origem: DOCUMENTACAOREQUISITOS (Item 5), Arquivo 18 (Item 7.4) e PROJETO N2.*
* **RF03 - Manter Tipos de Despesas e Receitas:** Cadastrar, parametrizar, inativar e reativar as categorias e subcategorias financeiras da propriedade rural, estruturadas conforme as 9 macrocategorias oficiais da N2. *Origem: DOCUMENTACAOREQUISITOS (RF03), Arquivo 18 (Item ii) e PROJETO N2.*
* **RF04 - Upload de Documento Fiscal (PDF):** Permitir o carregamento de arquivos PDF contendo notas fiscais eletrônicas (DANFE) por meio de interface web intuitiva (com drag & drop e seletor de arquivos). *Origem: DOCUMENTACAOREQUISITOS (RF02), Arquivo 18 (Item vi) e PROJETO N2 (Atividade 1ª Etapa).*
* **RF05 - Extração Inteligente de Dados via LLM (Gemini):** Extrair via IA do arquivo PDF os campos mandatórios: Fornecedor (Razão Social, Nome Fantasia, CNPJ), Faturado (Nome Completo, CPF), Número da Nota Fiscal, Data de Emissão, Descrição dos Produtos, Quantidade de Parcelas, Data de Vencimento e Valor Total. *Origem: PROJETO N2 (Atividade 1ª Etapa) e Arquivo 18 (Item vii).*
* **RF06 - Classificação Automática e Múltipla de Despesas:** Interpretar semanticamente os produtos constantes na nota fiscal através do Gemini e categorizar o lançamento contábil em uma das 9 famílias agropecuárias padronizadas, com estrutura técnica extensível para classificação múltipla/rateio. *Origem: PROJETO N2 (Regras e Classificação da DESPESA).*
* **RF07 - Exibição e Exportação dos Dados Extraídos em JSON:** Apresentar em tela o resultado da extração da Etapa 1 dividido em abas ("Visualização Formatada" e "JSON"), disponibilizando botão com feedback de cópia do JSON para a área de transferência. *Origem: PROJETO N2 (Figuras 1 e 2).*
* **RF08 - Manter Movimento de Contas (A Pagar e A Receber):** Registrar e controlar as contas a pagar e a receber vinculadas a faturas ou lançamentos manuais, associando Fornecedor, Faturado e Tipo de Despesa/Receita. *Origem: DOCUMENTACAOREQUISITOS (RF04, RF05), Arquivo 18 (Item iii) e PROJETO N2.*
* **RF09 - Manter Movimento de Parcelas:** Desdobrar o valor total da conta em uma ou mais parcelas com vencimentos e saldos devedores individuais. *Origem: DOCUMENTACAOREQUISITOS (RF07), Arquivo 18 (Item iv) e PROJETO N2.*
* **RF10 - Manter Movimento Financeiro (Quitação / Baixa):** Registrar as movimentações bancárias/financeiras de pagamento ou recebimento, suportando quitação total ou múltiplos depósitos parciais até a liquidação integral da parcela. *Origem: DOCUMENTACAOREQUISITOS (RF06), Arquivo 18 (Item v) e PROJETO N2.*
* **RF11 - Emitir Relatórios Financeiros:** Gerar relatórios consolidados em tela com filtros por período, faturado, fornecedor e categoria de despesa/receita. *Origem: DOCUMENTACAOREQUISITOS (RF08).*

#### 2.2 Requisitos Não Funcionais (RNF)
* **RNF01 - Usabilidade e Simplicidade Cognitiva:** A interface deve possuir poucos elementos na tela, permitindo ao usuário realizar uma ação por vez, reduzindo a complexidade para atender produtores rurais de baixa escolaridade. *Origem: DOCUMENTACAOREQUISITOS (RNF01).*
* **RNF02 - Mensagens de Feedback Acessíveis:** As mensagens de erro, alertas e confirmações devem ser explícitas, simples e em linguagem leiga compreensível. *Origem: DOCUMENTACAOREQUISITOS (RNF02).*
* **RNF03 - Padrão de Navegação Consistente:** As telas de manutenção de cadastros devem obrigatoriamente exibir a listagem dos dados existentes logo na primeira tela. *Origem: DOCUMENTACAOREQUISITOS (RNF03) e Arquivo 18.*
* **RNF04 - Mínima Intervenção Humana (Automação):** O processamento de dados e classificação orçamentária dos documentos fiscais devem ser realizados automaticamente pelo sistema via pipeline LLM. *Origem: DOCUMENTACAOREQUISITOS (RNF04).*
* **RNF05 - Suporte Nativo a Documentos PDF:** O sistema deve suportar ingestão e leitura direta de arquivos PDF padrão DANFE. *Origem: DOCUMENTACAOREQUISITOS (RNF05) e PROJETO N2.*
* **RNF06 - Preservação e Rastreabilidade de Dados:** Garantir integridade histórica e vínculo entre o documento processado e os títulos financeiros gerados. *Origem: DOCUMENTACAOREQUISITOS (RNF06).*
* **RNF07 - Consistência Monetária e Temporal:** Precisão contábil em centavos (utilização de campos numéricos decimais de alta precisão) e controle estrito de prazos de vencimento. *Origem: DOCUMENTACAOREQUISITOS (RNF07).*

#### 2.3 Regras de Negócio (RN)
* **RN01 - Proibição de Exclusão Física (Soft Delete Obrigatório):** Cadastros **não podem ser excluídos** do banco de dados em hipótese alguma. Operações de deleção física são estritamente vedadas. *Origem: PROJETO N2 (Regras de negócios).*
* **RN02 - Inativação e Reativação de Registros:** Cadastros desativados devem ser marcados com status `INATIVO`. O sistema deve disponibilizar funcionalidade explícita para que o usuário possa reativar um registro inativo. *Origem: PROJETO N2 (Regras de negócios).*
* **RN03 - Identificação dos Faturados Rurais:** Os faturados são especificamente os três membros gestores da propriedade: o proprietário e seus dois filhos (Beltrano, Fulano e Ciclano). Toda movimentação financeira deve estar associada a um deles. *Origem: DOCUMENTACAOREQUISITOS (Item 5) e Arquivo 18.*
* **RN04 - Despesa não é Campo Extraído:** A categoria da despesa não consta escrita formalmente na nota fiscal; ela deve ser interpretada e classificada pelo modelo de IA com base na descrição semântica dos produtos adquiridos. *Origem: PROJETO N2 (Página 2).*
* **RN05 - Taxonomia Obrigatória das 9 Categorias Agropecuárias:** A classificação de despesas deve enquadrar-se nas 9 macrocategorias oficiais estabelecidas:
  1. *Insumos Agrícolas* (sementes, fertilizantes, defensivos, corretivos);
  2. *Manutenção e Operação* (combustíveis, lubrificantes, peças, manutenção, pneus, ferramentas);
  3. *Recursos Humanos* (mão de obra temporária, salários, encargos);
  4. *Serviços Operacionais* (frete, colheita terceirizada, secagem, armazenagem, pulverização);
  5. *Infraestrutura e Utilidades* (energia elétrica, arrendamento, construções, reformas, materiais);
  6. *Administrativas* (honorários contábeis/advocatícios, despesas bancárias);
  7. *Seguros e Proteção* (seguro agrícola, seguro de máquinas/veículos, seguro prestamista);
  8. *Impostos e Taxas* (ITR, IPTU, IPVA, INCRA-CCIR);
  9. *Investimentos* (aquisição de máquinas, implementos, veículos, imóveis, infraestrutura rural).  
  *Origem: PROJETO N2 (Páginas 2 e 3).*
* **RN06 - Classificação Múltipla de Contas:** Uma conta a pagar pode ser classificada em um ou mais tipos de despesas (rateio). Uma conta a receber pode ser classificada em um ou mais tipos de receitas. A Etapa 1 opera com uma classificação principal, mantendo a estrutura extensível. *Origem: PROJETO N2.*
* **RN07 - Múltiplas Parcelas com Vencimentos Distintos:** Uma conta a pagar ou receber pode conter uma ou mais parcelas com vencimentos e valores independentes, cuja soma totaliza o valor do documento. *Origem: PROJETO N2 e DOCUMENTACAOREQUISITOS.*
* **RN08 - Quitação e Pagamento Parcial:** Um pagamento pode liquidar uma parcela integralmente ou amortizá-la parcialmente. A parcela só assume o status `QUITADA` quando o somatório das movimentações for igual ao seu valor nominal. Se houver saldo remanescente, a parcela permanece `ABERTA`. *Origem: DOCUMENTACAOREQUISITOS (RF06, Anexo 2).*
* **RN09 - Desacoplamento da Entidade Produtos:** A descrição dos produtos deve ser extraída como texto consolidado para subsidiar a categorização e visualização; **não será criada uma entidade/tabela relacional de `PRODUTOS`** no banco de dados. *Origem: PROJETO N2 (Página 2).*

#### 2.4 Requisitos Técnicos e Ferramentas Homologadas (`requisitos.txt`)
* **Linguagens Disponíveis:** Python, JavaScript, TypeScript.
* **Frameworks Disponíveis:** DJANGO / Flash (com exclusão formal do Flask, adotando **Django** como framework Python principal), Node.
* **SGBD Disponíveis:** PostGree (PostgreSQL), MySQL.
* **Tecnologia de IA:** Google Gemini API (recomendada oficialmente no documento da N2).

---

### 3. Matriz de Validação dos Requisitos x Ferramentas

| Requisito | Ferramenta / Tecnologia | Pode atender? | Como será atendido | Limitações / Observações |
| :--- | :--- | :--- | :--- | :--- |
| **RF01 - Manter Fornecedor/Cliente** | Python + Django + PostgreSQL (PostGree) | **Atende diretamente** | Modelo `FornecedorCliente` no Django ORM, Class-Based Views (CBVs), formulários com validação e rotas REST. | Requer sobrescrever o método `.delete()` para aplicar `status = 'INATIVO'`. |
| **RF02 - Manter Faturado** | Python + Django + PostgreSQL | **Atende diretamente** | Modelo específico vinculado a `FornecedorCliente` ou especialização com validação de CPF dos três sócios rurais. | Cadastros restritos inicialmente a Beltrano, Fulano e Ciclano. |
| **RF03 - Manter Tipos Despesa/Receita** | Python + Django + PostgreSQL | **Atende diretamente** | Modelo `DespesasReceitas` com as 9 macrocategorias oficiais pré-carregadas via fixtures/migrations do Django. | Cadastros devem permitir inclusão de novas subcategorias sem quebrar o histórico. |
| **RF04 - Upload de PDF (Etapa 1)** | Frontend Web Vanilla + Django Views | **Atende diretamente** | Formulário web `enctype="multipart/form-data"`, componente de drag-and-drop e recepção em `request.FILES['pdf_file']`. | Validação de extensão `.pdf` e limite de tamanho (10MB) no backend Django. |
| **RF05 - Extração de Dados da NF** | API Google Gemini + Python SDK (`google-genai`) | **Atende com configuração** | O Django despacha o payload binário do PDF diretamente à API Gemini utilizando *Structured Outputs* (Pydantic / JSON Schema). | Depende de chave de API (`GEMINI_API_KEY`) e conexão externa de internet. |
| **RF06 - Classificação Inteligente de Despesas** | Prompt Engineering + Gemini API | **Atende com desenvolvimento adicional** | Injeção no `system_instruction` da tabela de categorias e regras da N2, instruindo a IA a mapear os itens adquiridos para a macrocategoria adequada. | Exige fallback para notas que contenham itens de naturezas mistas. |
| **RF07 - Exibição em Tela (JSON e Formatado)** | JavaScript Vanilla + CSS3 + Django Template | **Atende diretamente** | Interface web responsiva renderizando JSON identado com botão "Copiar JSON" e painel formatado (Figuras 1 e 2 da N2). | Sem dependências externas pesadas no cliente; carregamento instantâneo. |
| **RF08 - Manter Movimento de Contas** | Django ORM + PostgreSQL | **Atende diretamente** | Modelo `MovimentoContas` com FKs para Faturado, Fornecedor e Tipo de Despesa/Receita. | Unicidade composta (Número NF + Fornecedor) para evitar duplicidades. |
| **RF09 - Manter Movimento de Parcelas** | Django ORM + PostgreSQL | **Atende diretamente** | Modelo `MovimentoParcelas` relacionado (1:N) a `MovimentoContas`. Geração automática de parcelas com vencimentos distintos. | Na Etapa 1 opera com 1 parcela, já modelado no banco para $N$ parcelas. |
| **RF10 - Movimento Financeiro (Quitação)** | Django ORM + PostgreSQL | **Atende diretamente** | Transações atômicas (`transaction.atomic`) para registrar o pagamento em `MovimentoFinanceiro` e abater o saldo da parcela. | Impede baixa de valor superior ao saldo sem confirmação explícita. |
| **RF11 - Emitir Relatórios** | Django ORM Aggregations + SQL | **Atende com desenvolvimento adicional** | Métodos agregadores (`annotate`, `aggregate`, `Sum`) agrupando por período, categoria e faturado. | Relatórios em tela cumprem perfeitamente a exigência documental. |
| **RN01 / RN02 - Soft Delete (Inativação/Reativação)** | Django ORM | **Atende diretamente** | Campo `status = models.CharField(default='ATIVO')`. Sobrescrita do método `delete()` nos models para executar `update(status='INATIVO')`. | `objects.filter(status='ATIVO')` encapsulado em um `ActiveManager` customizado. |
| **RN04 - Inferência Semântica de Despesa** | Google Gemini API | **Atende diretamente** | Capacidade nativa de raciocínio da LLM multimodal correlacionando a descrição dos produtos às macrocategorias agropecuárias. | Requer parametrização precisa no prompt com exemplos do documento oficial. |
| **RNF01 - Poucos elementos de tela** | HTML5 / CSS3 Vanilla | **Atende diretamente** | Interface limpa com cards modulares, botões de alto contraste e fluxo guiado para baixa escolaridade. | Design focado em clareza, evitando poluição visual. |
| **Captura por E-mail (Doc Requisitos)** | Python (`imaplib` / `email`) | **Necessita de ferramenta adicional** | Script em background (`management command` do Django) para varredura de caixa postal IMAP e download de anexos PDF. | Opcional para o escopo web principal da N2. |

---

### 4. Análise das Recomendações do Arquivo `18.`

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               AVALIAÇÃO DO ARQUIVO 18 PELO DOCENTE                              │
├──────────────────────────┬──────────────────────┬────────────────────────────────────────────────┤
│ Item Avaliado            │ Situação Identificada│ Ação Corretiva Obrigatória                     │
├──────────────────────────┼──────────────────────┼────────────────────────────────────────────────┤
│ 1. Capa e Formatação     │ Em desacordo         │ Ajustar capa, identificação institucional UniRV│
│ 2. Lista de Funções      │ Incompleta/Desacordo │ Adotar nomenclatura e funções do professor     │
│ 3. Casos de Uso (Geral)  │ Quantidade em falta  │ Alinhar 1 caso de uso por RF com protótipo     │
│ 4. Modelo ER             │ Entidades incorretas │ Implementar as 5 entidades e FKs exatas        │
│ 5. Diagrama de Sequência │ Falta padrão OO      │ Utilizar instâncias de classes e objetos       │
│ 6. Diagrama de Gantt     │ Não usou ferramenta  │ Modelar cronograma no GanttProject             │
│ 7. Especificação de C.U. │ Faltam protótipos    │ Inserir protótipo e listagem na primeira tela  │
└──────────────────────────┴──────────────────────┴────────────────────────────────────────────────┘
```

#### 4.1 Recomendação sobre Lista de Funções
* **O que propõe:** Substituir a lista original pelas 7 funções padronizadas:
  1. *Manter Fornecedor/Cliente*
  2. *Manter Despesas/Receitas*
  3. *Manter MovimentoContas (a pagar ou receber)*
  4. *Manter MovimentoParcelas (associado a MovimentoContas)*
  5. *Manter MovimentoFinanceiro (quitação)*
  6. *Fazer upload do documento*
  7. *Extrair dados do documento*
* **Relação aos requisitos existentes:** Alinha a nomenclatura dos requisitos iniciais aos padrões acadêmicos de DOO e ERPs contábeis. Decompõe o antigo "Receber Documentos" em duas ações operacionais claras: upload e extração.
* **Compatibilidade com as ferramentas:** 100% compatível com a arquitetura Django e PostgreSQL.
* **Decisão:** **INCORPORADA INTEGRALMENTE AO PROJETO.**

#### 4.2 Recomendação sobre Diagrama de Casos de Uso e Detalhamento
* **O que propõe:** Posicionar os atores nas bordas e os casos de uso no centro, garantindo correspondência 1:1 exata com a lista de funções e detalhamento rigoroso do campo "Dependências".
* **Relação aos requisitos existentes:** Corrige inconsistências de rastreabilidade entre o escopo e o detalhamento técnico.
* **Decisão:** **INCORPORADA INTEGRALMENTE AO PROJETO.**

#### 4.3 Recomendação sobre Diagrama Entidade-Relacionamento (DER)
* **O que propõe:** O professor rejeitou a estrutura inicial solta e exigiu as seguintes 5 entidades interligadas:
  * Entidade `Fornecedor/Cliente`
  * Entidade `Despesas/Receitas`
  * Entidade `MovimentoContas` (com FK para `Despesas/Receitas`, FK para `Fornecedor/Cliente` como fornecedor e FK para `Fornecedor/Cliente` como faturado)
  * Entidade `MovimentoParcelas` (com FK para `MovimentoContas`)
  * Entidade `MovimentoFinanceiro` (com FK para `MovimentoParcelas`)
* **Relação aos requisitos existentes:** Modela perfeitamente o ciclo contábil de contas a pagar/receber e suas liquidações.
* **Compatibilidade com as ferramentas:** Mapeamento perfeito para Models do Django ORM no PostgreSQL/MySQL.
* **Decisão:** **INCORPORADA INTEGRALMENTE AO PROJETO.**

#### 4.4 Recomendação sobre Diagrama de Sequência Orientado a Objetos
* **O que propõe:** As linhas de vida devem representar classes e instâncias de software (`:UploadView`, `:GeminiService`, `:ContaController`, `:MovimentoContaRepository`), mantendo a última mensagem retornando ao Ator.
* **Decisão:** **INCORPORADA INTEGRALMENTE AO PROJETO.**

#### 4.5 Recomendação sobre Diagrama de Gantt
* **O que propõe:** Utilizar obrigatoriamente o software oficial **GanttProject** para modelar o cronograma com predecessoras e marcos da N2 (Etapa 1: 29/09 e Etapa 2: 28/10).
* **Decisão:** **INCORPORADA AO PLANO DE DESENVOLVIMENTO.**

#### 4.6 Recomendação sobre Especificação de Casos de Uso com Protótipos
* **O que propõe:** Inserir um protótipo de tela ao final de cada especificação de RF, sendo obrigatório que todo caso de uso de "MANTER" apresente a listagem dos dados cadastrados logo na primeira tela.
* **Decisão:** **INCORPORADA INTEGRALMENTE AO PROJETO.**

---

### 5. Arquitetura Proposta

Em estrita consonância com `requisitos.txt` (autorizando Python, JavaScript, TypeScript, DJANGO, Node e PostgreSQL/MySQL), a arquitetura adotada fundamenta-se no ecossistema **Python + DJANGO + PostgreSQL (PostGree)** no backend e **HTML5 + Vanilla CSS3 + JavaScript** no frontend.

#### 5.1 Diagrama da Arquitetura em Camadas
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   CAMADA DE APRESENTAÇÃO                               │
│  [ Navegador Web / Cliente ]                                                           │
│  • Interface Gráfica Web Responsiva (HTML5, Vanilla CSS3, JavaScript ES6)              │
│  • Componente de Upload de PDF (Drag & Drop e Seletor de Arquivos)                     │
│  • Painel de Exibição com Abas ("Visualização Formatada" e "JSON" com Syntax High)     │
│  • Botão de Ação Rápida "Copiar JSON" com feedback de cópia                            │
│  • Telas de Manutenção com Listagem Inicial (Grid de Ativos e Inativos)                │
└───────────────────────────────────────────▲────────────────────────────────────────────┘
                                            │ HTTP / JSON REST / Multipart
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│                             CAMADA DE SERVIÇOS E API (BACKEND)                         │
│  [ Django Web Framework - Python 3.11+ ]                                               │
│  • Django URLs e Class-Based Views (CBVs)                                              │
│  • Módulo de Extração da Etapa 1:                                                      │
│    - `InvoiceExtractView`: Tratamento do upload (`request.FILES`)                      │
│    - `GeminiExtractionService`: Orquestração do prompt multimodal e JSON Schema        │
│  • Módulos da Etapa 2:                                                                 │
│    - `FinanceiroService`: Regras de negócio de contas, parcelas e baixas               │
│    - Django ORM Models: Soft delete (`status`), transações ACID e integridade          │
└─────────────────────▲─────────────────────────────────────────────▲────────────────────┘
                      │                                             │
      JSON Payload    │                                             │ SQL Queries / ACID
┌─────────────────────▼──────────────────────────┐    ┌─────────────▼────────────────────┐
│           INTEGRAÇÃO EXTERNA (LLM)             │    │    CAMADA DE PERSISTÊNCIA (SGBD) │
│  [ Google Gemini API (v1beta / google-genai) ] │    │  [ PostgreSQL (PostGree) / MySQL]│
│  • Modelo: `gemini-1.5-flash` ou `2.0-flash`   │    │  • Transações ACID               │
│  • Vision & Document Analysis Nativa           │    │  • Integridade Referencial (FKs) │
│  • Structured Outputs (Pydantic / JSON Schema) │    │  • Soft Delete com Índices       │
│  • Prompt contextual com as 9 categorias agro  │    │  • 5 Tabelas do Arquivo 18       │
└────────────────────────────────────────────────┘    └──────────────────────────────────┘
```

#### 5.2 Justificativa Técnica de Cada Escolha Arquitetural
* **Back-end (Python com Django):**
  * *Por que escolher:* Django é o framework Python corporativo autorizado em `requisitos.txt`. É amplamente consagrado pela robustez, maturidade arquitetural e aderência ao paradigma de Desenvolvimento Orientado a Objetos (DOO). O Django possui um ORM integrado completo com migrations seguras, permitindo implementar facilmente as regras de negócio de inativação lógica (`soft delete`) e integridade referencial. Além disso, o Python é a linguagem primária para integração com o SDK oficial da API do Google Gemini (`google-genai`), garantindo suporte nativo a Structured Outputs e visão computacional multimodal sem a necessidade de bibliotecas de terceiros instáveis.
* **Front-end (HTML5 / Vanilla CSS3 / JavaScript):**
  * *Por que escolher:* Atende com máxima fidelidade ao requisito não funcional de simplicidade cognitiva (RNF01) e aos modelos de interface das Figuras 1 e 2 do documento oficial da N2. A ausência de frameworks de cliente complexos (como React ou Angular) elimina etapas morosas de empacotamento (build), reduz o tempo de carregamento para redes rurais de menor largura de banda e permite focar diretamente na usabilidade com botões visíveis, abas dinâmicas e cópia de JSON.
* **Banco de Dados (PostgreSQL / PostGree):**
  * *Por que escolher:* Autorizado expressamente em `requisitos.txt`. O PostgreSQL é a escolha padrão da indústria contábil e financeira para garantir conformidade ACID estrita, tipos monetários exatos (`NUMERIC(15,2)`), chaves estrangeiras rígidas e consultas analíticas para relatórios consolidados.
* **Alternativa Técnica Avaliada (Node.js + TypeScript):**
  * O ecossistema Node com TypeScript também está autorizado em `requisitos.txt`. Contudo, o Django em Python foi priorizado como solução principal devido à sinergia direta e imediata com as ferramentas de IA generativa do Google, permitindo implementar tanto a Etapa 1 quanto a Etapa 2 com menor atrito e maior coesão técnica.

---

### 6. Fluxo das Principais Funcionalidades

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           FLUXO DE EXTRAÇÃO INTELIGENTE (ETAPA 1)                                │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
 [Usuário]               [Frontend Web]             [Backend Django]            [Google Gemini API]
     │                          │                          │                             │
     │ 1. Seleciona PDF         │                          │                             │
     │─────────────────────────>│                          │                             │
     │ 2. Clica "Extrair Dados" │                          │                             │
     │─────────────────────────>│ 3. POST /api/extrair-nf/ │                             │
     │                          │    (multipart/pdf)       │                             │
     │                          │─────────────────────────>│ 4. Valida buffer PDF        │
     │                          │                          │    Monta Prompt + Schema    │
     │                          │                          │ 5. Envia documento binário  │
     │                          │                          │────────────────────────────>│
     │                          │                          │                             │ 6. Executa OCR,
     │                          │                          │                             │    extrai entidades,
     │                          │                          │                             │    classifica despesa
     │                          │                          │ 7. Retorna JSON estruturado │
     │                          │                          │<────────────────────────────│
     │                          │ 8. HTTP 200 OK           │                             │
     │                          │    (Payload JSON)        │                             │
     │                          │<─────────────────────────│                             │
     │ 9. Renderiza abas:       │                          │                             │
     │    - Dados Formatados    │                          │                             │
     │    - JSON + Copiar JSON  │                          │                             │
     │<─────────────────────────│                          │                             │
```

#### 6.1 Fluxo 1: Extração de Dados da Nota Fiscal via IA (Atividade da 1ª Etapa)
* **Ator:** Responsável Financeiro.
* **Pré-condições:** Aplicação em execução, `GEMINI_API_KEY` configurada no ambiente e arquivo PDF da nota fiscal (DANFE) selecionado.
* **Entrada:** Arquivo no formato `.pdf` (ex.: `danfe (ciclano - pecas).pdf`).
* **Processamento:**
  1. O usuário anexa o PDF na interface web e clica no botão **EXTRAIR DADOS**.
  2. O frontend despacha o arquivo via requisição assíncrona (`POST`) para a view do Django (`/api/extrair-nf/`).
  3. A view do Django lê o arquivo a partir de `request.FILES['pdf_file']` em buffer de memória (`io.BytesIO`), sem persistir arquivos desnecessários em disco.
  4. O serviço `GeminiExtractionService` aciona o modelo Gemini com o PDF e o System Instruction parametrizado com as 9 macrocategorias agropecuárias e regras de classificação.
  5. A IA lê o documento, extrai os campos mandatórios (Fornecedor, Faturado, NF, Emissão, Vencimento, Valor Total, Itens) e infere a categoria da despesa com base nos produtos.
  6. A LLM retorna os dados estritamente no formato do JSON Schema solicitado.
  7. O Django sanitiza os campos e responde HTTP 200 com o JSON.
* **Validações:** Validação de extensão `.pdf`, verificação do tamanho máximo (10 MB) e checagem de integridade contra o schema de saída.
* **Persistência:** Na 1ª Etapa, os dados não exigem persistência em banco; são mantidos em tela para visualização e cópia imediata.
* **Saída:** Apresentação dinâmica nas abas "Visualização Formatada" e "JSON", acompanhada do botão "Copiar JSON".
* **Exceções:**
  * *Arquivo Inválido:* Alerta: "Por favor, selecione um arquivo no formato PDF válido."
  * *Falha de Conectividade com a IA:* HTTP 503 com mensagem amigável: "Não foi possível conectar ao serviço de inteligência artificial. Verifique a chave de API e tente novamente."

#### 6.2 Fluxo 2: Manutenção de Cadastros com Inativação Lógica (Etapa 2)
* **Ator:** Responsável Financeiro.
* **Pré-condições:** Usuário autenticado e banco de dados conectado.
* **Processamento:**
  1. Ao abrir qualquer menu de cadastro, o sistema exibe imediatamente a **listagem inicial** dos registros já cadastrados com filtros de "Ativos" e "Inativos".
  2. Para novos cadastros, o usuário clica em "Novo", preenche o formulário e clica em "Salvar" (status inicial `ATIVO`).
  3. Para desativar um registro, o usuário clica em "Inativar" (o Django executa soft delete: `status = 'INATIVO'`).
  4. Ao filtrar por inativos, o sistema disponibiliza o botão "Reativar" para restaurar o registro a `ATIVO`.
* **Validações:** Unicidade de CNPJ/CPF e dígitos verificadores. Comandos `DELETE` físicos são bloqueados no ORM.

#### 6.3 Fluxo 3: Registro de Contas, Parcelamento e Quitação Financeira (Etapa 2)
* **Ator:** Responsável Financeiro.
* **Processamento:**
  1. O usuário confirma os dados extraídos de uma nota ou insere manualmente um novo título a pagar/receber.
  2. O Django cria a conta em `MovimentoContas` e gera automaticamente os registros em `MovimentoParcelas` com base na quantidade de parcelas e prazos de vencimento informados.
  3. Ao ocorrer um pagamento, o usuário localiza a parcela em aberto e informa o valor amortizado e data de liquidação.
  4. O sistema insere um registro em `MovimentoFinanceiro` e subtrai o valor do saldo devedor da parcela.
  5. Se o saldo devedor for zerado, a parcela é marcada como `QUITADA`; caso contrário, permanece `ABERTA` com o saldo atualizado.

---

### 7. Modelagem dos Dados

A modelagem de dados foi estruturada para satisfazer integralmente as exigências do **Arquivo 18** e as regras de soft delete da **N2**:

```
  ┌────────────────────────┐                   ┌────────────────────────┐
  │   FornecedorCliente    │                   │    DespesasReceitas    │
  ├────────────────────────┤                   ├────────────────────────┤
  │ PK id_pessoa           │                   │ PK id_categoria        │
  │    tipo_pessoa         │                   │    descricao           │
  │    razao_social_nome   │                   │    natureza (DESP/REC) │
  │    nome_fantasia       │                   │    macro_categoria     │
  │    documento_cpf_cnpj  │                   │    status (ATIVO/INAT) │
  │    status (ATIVO/INAT) │                   └───────────▲────────────┘
  └───────────▲────────────┘                               │
              │                                            │
              ├─────────────────────────┐                  │ 1
              │ 1 (Como Fornecedor)     │ 1 (Como Faturado)│
              │                         │                  │
              │         ┌───────────────┴──────────────────┴┐
              │         │          MovimentoContas          │
              │         ├───────────────────────────────────┤
              │         │ PK id_conta                       │
              └────────>│ FK id_fornecedor_cliente          │
                        │ FK id_faturado                    │
                        │ FK id_despesa_receita             │
                        │    numero_documento_nf            │
                        │    data_emissao                   │
                        │    valor_total                    │
                        │    natureza (PAGAR / RECEBER)     │
                        │    status_conta (ABERTA/QUITADA)  │
                        │    status_registro (ATIVO/INATIVO)│
                        │    descricao_produtos             │
                        └─────────────────▲─────────────────┘
                                          │ 1
                                          │
                                          │ N
                        ┌─────────────────┴─────────────────┐
                        │         MovimentoParcelas         │
                        ├───────────────────────────────────┤
                        │ PK id_parcela                     │
                        │ FK id_conta                       │
                        │    numero_parcela                 │
                        │    data_vencimento                │
                        │    valor_parcela                  │
                        │    saldo_devedor                  │
                        │    status_parcela (ABERTA/QUITADA)│
                        └─────────────────▲─────────────────┘
                                          │ 1
                                          │
                                          │ N
                        ┌─────────────────┴─────────────────┐
                        │        MovimentoFinanceiro        │
                        ├───────────────────────────────────┤
                        │ PK id_movimento                   │
                        │ FK id_parcela                     │
                        │    data_pagamento                 │
                        │    valor_pago                     │
                        │    forma_pagamento                │
                        │    observacao                     │
                        └───────────────────────────────────┘
```

#### 7.2 Definição dos Django Models e Integridade Referencial

```python
# models.py (Estrutura Django ORM)
from django.db import models

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='ATIVO')

class FornecedorCliente(models.Model):
    TIPO_CHOICES = [('FORNECEDOR', 'Fornecedor'), ('CLIENTE', 'Cliente'), ('FATURADO', 'Faturado')]
    tipo_cadastro = models.CharField(max_length=20, choices=TIPO_CHOICES)
    razao_social_nome = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True)
    documento_cpf_cnpj = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=10, default='ATIVO')
    criado_em = models.DateTimeField(auto_now_add=True)
    
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        self.status = 'INATIVO'
        self.save()

class DespesasReceitas(models.Model):
    NATUREZA_CHOICES = [('DESPESA', 'Despesa'), ('RECEITA', 'Receita')]
    descricao = models.CharField(max_length=150)
    natureza = models.CharField(max_length=10, choices=NATUREZA_CHOICES)
    macro_categoria = models.CharField(max_length=100) # As 9 categorias oficiais da N2
    status = models.CharField(max_length=10, default='ATIVO')

    def delete(self, *args, **kwargs):
        self.status = 'INATIVO'
        self.save()

class MovimentoContas(models.Model):
    NATUREZA_CONTA = [('PAGAR', 'A Pagar'), ('RECEBER', 'A Receber')]
    STATUS_CONTA = [('ABERTA', 'Aberta'), ('PARCIAL', 'Parcialmente Paga'), ('QUITADA', 'Quitada')]
    
    fornecedor_cliente = models.ForeignKey(FornecedorCliente, on_delete=models.RESTRICT, related_name='contas_fornecedor')
    faturado = models.ForeignKey(FornecedorCliente, on_delete=models.RESTRICT, related_name='contas_faturado')
    despesa_receita = models.ForeignKey(DespesasReceitas, on_delete=models.RESTRICT)
    numero_documento_nf = models.CharField(max_length=50, blank=True, null=True)
    data_emissao = models.DateField()
    valor_total = models.DecimalField(max_digits=15, decimal_places=2)
    natureza = models.CharField(max_length=10, choices=NATUREZA_CONTA)
    status_conta = models.CharField(max_length=20, choices=STATUS_CONTA, default='ABERTA')
    status_registro = models.CharField(max_length=10, default='ATIVO')
    descricao_produtos = models.TextField(blank=True, null=True) # RN09: Sem entidade Produtos

class MovimentoParcelas(models.Model):
    STATUS_PARCELA = [('ABERTA', 'Aberta'), ('QUITADA', 'Quitada')]
    conta = models.ForeignKey(MovimentoContas, on_delete=models.RESTRICT, related_name='parcelas')
    numero_parcela = models.PositiveIntegerField(default=1)
    data_vencimento = models.DateField()
    valor_parcela = models.DecimalField(max_digits=15, decimal_places=2)
    saldo_devedor = models.DecimalField(max_digits=15, decimal_places=2)
    status_parcela = models.CharField(max_length=20, choices=STATUS_PARCELA, default='ABERTA')

class MovimentoFinanceiro(models.Model):
    parcela = models.ForeignKey(MovimentoParcelas, on_delete=models.RESTRICT, related_name='movimentacoes')
    data_pagamento = models.DateField()
    valor_pago = models.DecimalField(max_digits=15, decimal_places=2)
    forma_pagamento = models.CharField(max_length=50, blank=True, null=True)
    observacao = models.CharField(max_length=255, blank=True, null=True)
```

---

### 8. Casos de Uso com Protótipos de Tela

Atendendo rigorosamente à determinação do Arquivo 18 (*"Espera-se: um protótipo ao final de cada RF; sendo MANTER listagem na primeira tela"*):

#### UC01 - Manter Fornecedor/Cliente
* **Código:** UC01
* **Nome:** Manter Fornecedor e Cliente
* **Objetivo:** Consultar, incluir, alterar, inativar e reativar parceiros comerciais da propriedade rural.
* **Protótipo (Listagem Inicial na 1ª Tela):**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SISTEMA DE CONTROLE FINANCEIRO RURAL               [ Menu ]  [ Sair ]      │
├─────────────────────────────────────────────────────────────────────────────┤
│  Cadastros > Fornecedores e Clientes                                        │
│                                                                             │
│  [ Filtro: (•) Ativos  ( ) Inativos ]     [ Buscar: ________________ ]      │
│                                                     [ + Novo Cadastro ]     │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Razão Social / Nome      │ CNPJ / CPF         │ Tipo       │ Ações     │  │
│  ├──────────────────────────┼────────────────────┼────────────┼───────────┤  │
│  │ Iguaçu Máquinas Agrícolas│ 33.656.729/0023-85 │ Fornecedor │ [✏️] [🚫] │  │
│  │ Grãos do Vale Ltda       │ 01.234.567/0001-89 │ Cliente    │ [✏️] [🚫] │  │
│  │ Adubos & Fertilizantes   │ 10.987.654/0001-32 │ Fornecedor │ [✏️] [🚫] │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│  Legenda: [✏️] Editar  [🚫] Inativar  [🔄] Reativar                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### UC02 - Manter Faturado
* **Código:** UC02
* **Nome:** Manter Faturado (Sócios Gestores)
* **Objetivo:** Manter os dados cadastrais dos três responsáveis da fazenda (Beltrano, Fulano e Ciclano).
* **Protótipo (Listagem Inicial na 1ª Tela):**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Cadastros > Faturados da Propriedade (Responsáveis)                        │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Nome Completo            │ CPF                │ Status     │ Ações     │  │
│  ├──────────────────────────┼────────────────────┼────────────┼───────────┤  │
│  │ Ciclano da Silva         │ 999.999.999-99     │ ATIVO      │ [✏️] [🚫] │  │
│  │ Fulano da Silva          │ 888.888.888-88     │ ATIVO      │ [✏️] [🚫] │  │
│  │ Beltrano da Silva        │ 777.777.777-77     │ ATIVO      │ [✏️] [🚫] │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### UC04_05 - Upload e Extração Inteligente de Nota Fiscal (Atividade da 1ª Etapa)
* **Código:** UC04_05
* **Nome:** Extração de Dados de Nota Fiscal com IA
* **Objetivo:** Fazer upload de uma nota fiscal em PDF e receber os dados extraídos e a classificação em JSON e exibição formatada.
* **Atores:** Responsável Financeiro.
* **Protótipo Oficial (Conforme Figuras 1 e 2 do Documento Oficial da N2):**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Extração de Dados de Nota Fiscal                      │
│             Carregue um PDF de nota fiscal e extraia os dados usando IA     │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  ⬆ Upload do PDF                                                      │  │
│  │  Selecione o arquivo PDF da nota fiscal                               │  │
│  │  [ Escolher arquivo ]  danfe (ciclano - pecas).pdf  (0.01 MB)          │  │
│  │                                                                       │  │
│  │  [                   ⚡ EXTRAIR DADOS COM IA                        ] │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  Dados Extraídos                                                            │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  [ Visualização Formatada ]  [ (•) JSON ]                             │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │  {> Dados em JSON                                     [ 📋 Copiar JSON]│  │
│  │  {                                                                    │  │
│  │    "fornecedor": {                                                    │  │
│  │      "razao_social": "IGUACU MAQUINAS AGRICOLAS LTDA",                │  │
│  │      "nome_fantasia": "IGUACU MAQUINAS AGRICOLAS",                    │  │
│  │      "cnpj": "33.656.729/0023-85"                                     │  │
│  │    },                                                                 │  │
│  │    "faturado": {                                                      │  │
│  │      "nome_completo": "CICLANO DA SILVA",                             │  │
│  │      "cpf": "999.999.999-99"                                          │  │
│  │    },                                                                 │  │
│  │    "numero_nota": "000.084.682",                                      │  │
│  │    "data_emissao": "2025-09-19",                                      │  │
│  │    "quantidade_parcelas": 1,                                          │  │
│  │    "data_vencimento": "2025-10-17",                                   │  │
│  │    "valor_total": 3086.75,                                            │  │
│  │    "classificacao_despesa": "MANUTENÇÃO E OPERAÇÃO",                  │  │
│  │    "produtos": "GRAXA DE POLIUREIA, ANEL O, KIT DA BUCHA, ROLAMENTO..."│  │
│  │  }                                                                    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### UC06 - Manter Movimento de Contas e Parcelas (Etapa 2)
* **Protótipo (Listagem Inicial na 1ª Tela):**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Movimentações > Contas a Pagar e Receber                                   │
│  [ Filtrar: (•) A Pagar  ( ) A Receber ]              [ + Nova Conta ]      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ NF / Doc   │ Fornecedor / Cliente │ Faturado │ Vencimento │ Total (R$)│  │
│  ├────────────┼──────────────────────┼──────────┼────────────┼───────────┤  │
│  │ 000.084.682│ Iguaçu Máquinas      │ Ciclano  │ 17/10/2025 │  3.086,75 │  │
│  │ Contrato 12│ Grãos do Vale        │ Beltrano │ 10/11/2025 │ 45.000,00 │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### UC07 - Baixa e Quitação Financeira (Etapa 2)
* **Protótipo (Listagem Inicial na 1ª Tela):**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Financeiro > Quitação de Parcelas em Aberto                                │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Parcela │ Vencimento │ Valor Orig. │ Saldo Devedor │ Status │ Ação     │  │
│  ├─────────┼────────────┼─────────────┼───────────────┼────────┼──────────┤  │
│  │ 084682/1│ 17/10/2025 │ R$ 3.086,75 │ R$ 3.086,75   │ ABERTA │[Pagar/Baixa]│
│  │ Trator/1│ 10/03/2026 │ R$ 15.000,00│ R$  7.000,00  │ ABERTA │[Pagar/Baixa]│
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 9. Requisitos que Não Podem ser Atendidos com as Ferramentas Atuais

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             ANÁLISE DE GAPS E LIMITAÇÕES TÉCNICAS                                │
├──────────────────────────┬─────────────────────────────┬─────────────────────────────────────────┤
│ Requisito sem Suporte    │ Natureza do Impedimento     │ Alternativa Técnica Adotada             │
├──────────────────────────┼─────────────────────────────┼─────────────────────────────────────────┤
│ 1. Leitura/OCR de PDF    │ Django e PostgreSQL não têm │ Integração direta com Google Gemini     │
│    inteligente           │ recursos de visão computac. │ API (Vision multimodal) via Python.     │
│ 2. Dedução semântica da  │ Não é um campo textual      │ Prompt engineering estruturado no Gemini│
│    categoria de despesa  │ explícito na nota fiscal.   │ com as 9 macrocategorias do agronegócio.│
│ 3. Captura por E-mail    │ Fora do ciclo de vida       │ Management Command em Python executando │
│    (mencionado no base)  │ de requisições HTTP normais.│ rotina via protocolo IMAP (`imaplib`).  │
│ 4. Cronograma Oficial    │ Ferramentas web não geram   │ Utilização do software desktop gratuito │
│    do Projeto            │ diagramas de precedência.   │ GanttProject conforme exigido pelo prof.│
└──────────────────────────┴─────────────────────────────┴─────────────────────────────────────────┘
```

1. **Extração de Dados Não Estruturados de PDF (RF05):**
   * Nem o Django nem o banco de dados possuem OCR nativo capaz de decodificar tabelas fiscais de PDFs digitalizados. A alternativa adotada é a **API do Google Gemini**, recomendada expressamente pela disciplina.
2. **Classificação Contextual de Despesas (RF06 / RN04):**
   * A categoria da despesa não existe escrita na nota. Expressões regulares ou buscas estáticas falhariam facilmente. A alternativa é utilizar a capacidade de raciocínio da IA generativa informando a taxonomia rural completa no prompt de sistema.
3. **Recebimento de Documentos por E-mail:**
   * Caso o cliente demande no futuro o recebimento automático de notas por e-mail (além do upload web da N2), implementa-se um `management command` customizado no Django que roda periodicamente e utiliza o módulo nativo `imaplib` do Python.

---

### 10. Lacunas e Inconsistências entre os Documentos

* **Exclusão Física x Inativação Lógica:** Enquanto a documentação inicial pressupunha exclusão comum, as regras oficiais da N2 impõem a proibição expressa de exclusão de cadastros e a obrigatoriedade de inativação/reativação. O sistema adota a inativação lógica (`Soft Delete`) via Django ORM.
* **Categorias de Despesa:** O documento de requisitos inicial continha apenas duas categorias (*Insumos* e *Operacionais*), ao passo que a especificação oficial da N2 estabeleceu **9 macrocategorias agrícolas completas**. A proposta técnica incorpora integralmente as 9 categorias da N2.
* **Entidade Produtos:** O documento inicial deixava em aberto o cadastro de itens, mas a diretriz da N2 cravou que **não será necessário criar a entidade PRODUTOS**. Os itens são persistidos como texto consolidado em `MovimentoContas`.
* **Nomenclatura Relacional:** A devoluçao do Arquivo 18 determinou a substituição da modelagem anterior pela estrutura padronizada com `MovimentoContas`, `MovimentoParcelas` e `MovimentoFinanceiro`.

---

### 11. Plano de Desenvolvimento Estruturado

```
CRONOGRAMA GERAL DO PROJETO:
[23/09] ────> [29/09/2026] ───────────────────────────> [28/10/2026]
   │                 │                                         │
   ├─ Definição      └─ ENTREGA ETAPA 1 (35%)                  └─ ENTREGA ETAPA 2 (45%)
   │  Técnica           • Upload Web de PDF                       • Banco de Dados PostgreSQL
   │  e Arquitetura     • Integração com Gemini API               • CRUDs com Inativação
   │                    • Extração de dados da NF                 • Contas a Pagar / Receber
   │                    • Classificação inteligente               • Parcelamentos e Baixas
   │                    • Exibição em tela (JSON + Formatado)     • Relatórios Financeiros
```

#### Fase 1: Entrega da Etapa 1 (Prazo: 29/09/2026 - Peso: 35%)
* **Sprint 1.1 - Preparação do Projeto Django e SDK Gemini (Dia 1):**
  * Inicialização do projeto Django e configuração do app `extrator_fiscal`.
  * Instalação e teste do SDK `google-genai` com chave de API em `.env`.
* **Sprint 1.2 - Serviço de Extração e Engenharia de Prompt (Dias 2 e 3):**
  * Implementação da classe `GeminiExtractionService` com envio multimodal de PDF em buffer de memória.
  * Validação com o arquivo de teste `danfe (ciclano - pecas).pdf` (garantindo extração de Iguaçu Máquinas, Ciclano da Silva, R$ 3.086,75 e classificação em "MANUTENÇÃO E OPERAÇÃO").
* **Sprint 1.3 - Construção da Interface Web (Dias 4 e 5):**
  * Criação da interface gráfica web com componente de upload de PDF, botão "EXTRAIR DADOS", indicador de progresso e abas com botão de cópia de JSON.
* **Sprint 1.4 - Homologação e Fechamento da 1ª Etapa (Dia 6 - até 29/09):**
  * Teste do fluxo completo e empacotamento para apresentação.

#### Fase 2: Entrega da Etapa 2 (Prazo: 28/10/2026 - Peso: 45%)
* **Sprint 2.1 - Banco de Dados e Models Django (Semana 1):**
  * Criação e migração das 5 tabelas no PostgreSQL/MySQL (`FornecedorCliente`, `DespesasReceitas`, `MovimentoContas`, `MovimentoParcelas`, `MovimentoFinanceiro`).
* **Sprint 2.2 - Módulos de Manutenção de Cadastros (Semana 2):**
  * Telas de cadastro com listagem inicial e botões de inativar/reativar.
* **Sprint 2.3 - Módulo de Contas a Pagar e Parcelamentos (Semana 3):**
  * Integração da extração da Etapa 1 com a gravação de títulos e parcelas no banco de dados.
* **Sprint 2.4 - Módulo Financeiro e Relatórios (Semana 4):**
  * Baixa e quitação parcial de parcelas e relatórios gerenciais em tela.
* **Sprint 2.5 - Documentação Final e GanttProject (Até 28/10):**
  * Atualização da documentação acadêmica e cronograma oficial no GanttProject.

---

### 12. Escopo do Produto Mínimo Viável (MVP)

* **Essencial para o MVP (Etapa 1 - Entrega Imediata):**
  * Interface gráfica web intuitiva para upload da nota fiscal (PDF).
  * Backend Django consumindo a API Google Gemini com System Instruction especializado no agronegócio.
  * Extração completa de Fornecedor, Faturado, NF, Emissão, Vencimento, Valor Total e Produtos.
  * Classificação automática precisa da despesa na macrocategoria adequada.
  * Painel de dados com abas ("Visualização Formatada" e "JSON") e botão funcional "Copiar JSON".
* **Importante para a Versão Final (Etapa 2):**
  * Banco de dados PostgreSQL configurado.
  * Cadastros com controle estrito de inativação lógica e reativação.
  * Gerenciamento de Contas a Pagar/Receber, Parcelamentos e Baixas Financeiras.
* **Opcional / Melhorias Futuras:**
  * Coleta automática de notas fiscais via IMAP (e-mail).
  * Exportação de relatórios em planilhas Excel e PDF.

---

### 13. Análise e Matriz de Riscos Técnicos

| Risco Técnico Identificado | Probabilidade / Impacto | Estratégia Prática de Mitigação |
| :--- | :--- | :--- |
| **1. Latência ou Indisponibilidade da API Gemini** | Média / Alto | Implementar timeouts adequados, feedback visual imediato no frontend ("Processando nota fiscal com IA...") e tratamento gracioso de erros HTTP no Django. |
| **2. Exaustão de Quotas da API** | Baixa / Alto | Uso do modelo otimizado `gemini-1.5-flash` ou `gemini-2.0-flash`, que oferecem alta velocidade e limite generoso de requisições gratuitas. |
| **3. Inconsistência na Classificação de Despesas** | Média / Médio | Parametrização detalhada das 9 famílias rurais com exemplos concretos de insumos e peças no System Instruction da LLM. |
| **4. Exclusão Inadvertida de Registros no Banco** | Baixa / Alto | Bloqueio de comandos `DELETE` físicos através da sobrescrita do método `delete()` dos Models no Django ORM, forçando soft delete. |
| **5. Discrepâncias em Valores Monetários** | Média / Alto | Uso exclusivo de campos `DecimalField` no Django e `NUMERIC(15,2)` no banco de dados para evitar erros de ponto flutuante. |
| **6. Dificuldade Operacional pelos Produtores** | Alta / Alto | Cumprimento rigoroso do RNF01: botões destacados, telas sem acúmulo de dados, mensagens diretas em linguagem simples. |

---

### 14. Conclusão Técnica

1. **Aderência aos Requisitos Obrigatórios:** A proposta técnica utiliza estritamente as ferramentas permitidas em `requisitos.txt`: **Python + DJANGO + PostgreSQL (PostGree)** no backend, em conjunto com **HTML5 + Vanilla CSS3 + JavaScript** no frontend e a **API do Google Gemini** recomendada oficialmente no documento da N2. O uso do Flask foi integralmente descartado.
2. **Entrega da Etapa 1:** A solução técnica para a 1ª Etapa está plenamente definida, com arquitetura pronta para execução: upload da nota em PDF via interface web, acionamento do Gemini pelo Django e retorno estruturado em JSON com classificação inteligente da despesa rural, perfeitamente validado com o arquivo `danfe (ciclano - pecas).pdf`.
3. **Conformidade com a Devolutiva do Professor:** Todas as 7 recomendações do Arquivo 18 foram incorporadas (nova lista de funções, DER com 5 tabelas e chaves estrangeiras, padrão orientado a objetos, cronograma em GanttProject e especificação de casos de uso com listagem inicial na primeira tela e protótipos visuais).
