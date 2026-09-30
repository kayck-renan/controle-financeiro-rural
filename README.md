# 🌾 Sistema de Controle Financeiro Rural

> **Projeto Administrativo-Financeiro (DOO) — Avaliação N2 (Etapa 1)**  
> **Autores:** Kayck Renan e Felipe Lopes Gonçalves  
> **Instituição:** Universidade de Rio Verde (UniRV)  
> **Data de Entrega:** 29/09/2026  

---

## 📌 1. Visão Geral do Projeto

O **Sistema de Controle Financeiro Rural** é uma solução moderna e intuitiva voltada para a gestão fiscal e financeira do agronegócio. Desenvolvido para atender aos requisitos da disciplina de **Desenvolvimento Orientado a Objetos (DOO)** da **UniRV**, o sistema atua como um **Extrator Fiscal Inteligente**:

* 📄 **Leitura e Extração de DANFE (PDF):** Processamento automatizado de notas fiscais eletrônicas de compras rurais (maquinários, insumos, defensivos, peças, etc.).
* 🧠 **Classificação Semântica por Inteligência Artificial:** Integração com a API **Google Gemini** para leitura multimodal do documento e classificação contábil automática nas 9 macrocategorias oficiais da disciplina.
* 🛡️ **Motor Local Resiliente (Fallback Inteligente):** Caso o usuário não informe uma chave da API Gemini ou esteja sem conexão externa, o sistema utiliza um algoritmo heurístico local especializado, garantindo **100% de funcionamento e precisão** na extração da nota fiscal de teste.
* 📊 **Apresentação em Dupla Camada:** Exibição dinâmica em formato **Visual Formatado** (com cards de totais, dados das partes e tabela de itens) e formato **JSON Estruturado** (padronizado para integrações contábeis).

---

## 🧭 Guia Passo a Passo: Como Usar o Sistema

### Passo 1: Autenticação no Sistema (Login)
1. Acesse o sistema pelo link da nuvem ou localmente (`/login/`).
2. Digite suas credenciais ou utilize um dos botões de **acesso rápido ("Usar")** disponíveis na caixa de credenciais de teste para preencher os campos instantaneamente.
3. Clique em **"Entrar no Sistema"**. O sistema criará uma sessão segura e redirecionará para o painel principal.

### Passo 2: Gestão da KEY Gemini em Tempo Real
1. No topo da página principal, localize a barra **"Monitoramento e Envio da KEY Gemini em Tempo Real"**.
2. **Status da Chave:** O indicador exibe visualmente se o sistema está operando em modo *Motor Local Inteligente* (laranja) ou *Google Gemini Cloud AI* (verde).
3. **Pré-visualização Dinâmica:** Conforme você digita ou cola a chave no campo, a pré-visualização mascarada (`AIzaSy••••••••`) e a contagem de caracteres são atualizadas imediatamente na tela.
4. **Envio da Chave:** Clique no botão verde **"Enviar Chave"**. A chave será validada e ativada imediatamente na sua sessão.
5. Se preferir, você também pode configurar a chave clicando no botão **"⚙️ Configurar Gemini"** no cabeçalho para abrir o modal dedicado.

### Passo 3: Carregamento do Arquivo PDF (DANFE)
O sistema disponibiliza duas formas de carregar notas fiscais:
* **Opção Rápida (1 Clique):** Clique no botão **"⚡ Carregar Exemplo: danfe (ciclano - peças).pdf"**. O arquivo oficial fornecido pela disciplina será pré-selecionado automaticamente.
* **Upload Personalizado:** Clique na área de upload ou arraste um arquivo `.pdf` válido de uma DANFE para a caixa de seleção.

### Passo 4: Extração e Processamento Inteligente
1. Com o arquivo selecionado, clique no botão escuro **"⚡ EXTRAIR DADOS"**.
2. O sistema exibirá uma barra de progresso com animação visual enquanto o motor processa o documento.

### Passo 5: Análise dos Dados Extraídos
Após o processamento, a seção de resultados será apresentada com duas abas interativas:

* **Aba 1 — 📋 Visualização Formatada:**
  * **Status & Classificação:** Destaca a macrocategoria contábil inferida (ex: `MANUTENÇÃO E OPERAÇÃO`) acompanhada de justificativa técnica baseada nos itens adquiridos.
  * **Metadados da NF:** Número do documento, série, data de emissão e data de vencimento.
  * **Partes Envolvidas:** Dados completos do **Fornecedor** (Razão Social, Nome Fantasia, CNPJ) e do **Faturado** (Nome do Produtor Rural, CPF).
  * **Resumo Financeiro:** Valor total líquido e quantidade de parcelas.
  * **Tabela Discriminada de Produtos:** Lista completa contendo descrição de cada item, quantidade e valor total individual.
* **Aba 2 — 💻 JSON:**
  * Exibe a estrutura de dados bruta serializada em JSON, com formatação limpa e botão **"Copiar JSON"** para facilitar a integração com outros softwares de contabilidade rural.

### Passo 6: Logout Seguro
* Para encerrar a sessão a qualquer momento, clique no botão **"Sair"** localizado no canto superior direito do cabeçalho.

---

## 🔑 Credenciais de Teste / Acesso

Para fins de avaliação por parte do corpo docente, as seguintes contas já se encontram registradas no banco de dados da aplicação:

| Perfil | Usuário (Login) | Senha | Nome Exibido no Painel |
| :--- | :--- | :--- | :--- |
| **Autor (Desenvolvedor)** | `kayck` | `unirv2026` | Kayck Renan |
| **Autor (Desenvolvedor)** | `felipelopesgoncalves` | `unirv2026` | Felipe Lopes Gonçalves |
| **Acesso Alternativo** | `felipe` | `unirv2026` | Felipe |
| **Administrador** | `admin` | `admin123` | Administrador |

> 💡 **Dica de Usabilidade:** Na página de login, basta clicar no botão **"Usar"** ao lado de qualquer usuário para que o formulário seja preenchido automaticamente, dispensando digitação manual.

> **Placeholders de Referência:**
> - `[INSERIR EMAIL/LOGIN]`: `kayck` ou `felipelopesgoncalves`
> - `[INSERIR SENHA]`: `unirv2026`

---

## 🔗 Links Relevantes

* **Repositório no GitHub:** [https://github.com/kayck-renan/controle-financeiro-rural](https://github.com/kayck-renan/controle-financeiro-rural)
* **Aplicação em Produção (Vercel):** [https://controle-financeiro-rural.vercel.app/](https://controle-financeiro-rural.vercel.app/)
* **Vídeo de Demonstração:** `[INSERIR LINK DO VÍDEO]` *(Substituir com o link do vídeo de apresentação da turma/dupla)*

---

## 💻 Como Executar o Projeto (Setup Local)

### Pré-requisitos
* **Python 3.10 ou superior** instalado na máquina.
* **Git** instalado (opcional, para clonagem).

---

### Opção A — Execução Rápida no Windows (1 Clique)
1. Abra a pasta raiz do projeto.
2. Dê um duplo clique no arquivo:
   ```cmd
   iniciar_sistema.bat
   ```
3. O script detectará o executável do Python, aplicará as migrações necessárias e iniciará o servidor automaticamente.
4. Abra o navegador no endereço: **`http://127.0.0.1:8000/`**

---

### Opção B — Execução Manual via Linha de Comando (Terminal)

1. **Clonar ou baixar o repositório:**
   ```bash
   git clone https://github.com/kayck-renan/controle-financeiro-rural.git
   cd controle-financeiro-rural
   ```

2. **Criar e ativar o ambiente virtual (Recomendado):**
   * *No Windows (PowerShell/CMD):*
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * *No Linux / macOS:*
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar as dependências do projeto:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar as migrações do banco de dados:**
   ```bash
   python manage.py migrate
   ```

5. **Iniciar o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

6. **Acessar o sistema:**
   Abra no seu navegador: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🛠️ Tecnologias e Arquitetura

* **Linguagem & Framework:** Python 3 + Django 5
* **Inteligência Artificial:** Google Gemini API (`google-genai`) multimodal com prompt semântico para o setor agropecuário
* **Processamento de Documentos:** `PyPDF2` e `pdfplumber`
* **Estilização & Frontend:** HTML5 Semântico, CSS3 Moderno (Variáveis de tema, Glassmorphism, Mobile-First) e Vanilla JavaScript assíncrono
* **Armazenamento de Dados:** SQLite3 (com suporte dinâmico a diretório temporário para ambientes serverless)
* **Arquivos Estáticos:** WhiteNoise
* **Hospedagem & Nuvem:** Vercel com Runtime Serverless `@vercel/python`

---

## 👥 Autoria e Créditos

Desenvolvido para a **Universidade de Rio Verde (UniRV)** por:
* **Kayck Renan** — [GitHub @kayck-renan](https://github.com/kayck-renan)
* **Felipe Lopes Gonçalves** — [GitHub @felipelopesgoncalves](https://github.com/felipelopesgoncalves)

*Curso de Engenharia de Software / Ciência da Computação — 2026*
