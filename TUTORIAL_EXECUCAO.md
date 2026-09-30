# Guia de Execução Local — Sistema de Controle Financeiro Rural
## Avaliação N2 — 1ª Etapa (Entrega: 29/09/2026 • Peso: 35%)

**Autores:** Felipe Lopes Gonçalves e Kayck Renan  
**Instituição:** Universidade de Rio Verde (UniRV)  
**Disciplina:** Projeto Administrativo-Financeiro / Desenvolvimento Orientado a Objetos (DOO)  

---

## 1. O que enviar para o Professor (.zip)

Compacte a pasta do projeto contendo os seguintes arquivos e diretórios essenciais:

```
📁 projeto-financeiro-rural/
├── 📁 config/                       # Configurações centrais do Django (settings, urls, wsgi)
├── 📁 extrator_fiscal/              # Módulo da aplicação (views, gemini_service, rotas)
│   ├── gemini_service.py           # Serviço de IA (Gemini API + extrator semântico local)
│   ├── views.py                    # Endpoints da aplicação
│   └── urls.py                     # Rotas da Etapa 1
├── 📁 templates/                    # Telas HTML (fiel às Figuras 1 e 2)
│   └── extrator_fiscal/index.html
├── 📁 static/                       # Arquivos estáticos (Vanilla CSS e JavaScript)
│   ├── css/style.css
│   └── js/app.js
├── manage.py                       # Utilitário de linha de comando do Django
├── requirements.txt                # Dependências para instalação via pip
├── iniciar_sistema.bat             # Script para inicialização em 1 clique no Windows
├── danfe (ciclano - pecas).pdf     # Nota fiscal de amostra oficial da disciplina
├── PROPOSTA_TECNICA_ETAPA1.md      # Proposta Técnica completa (14 seções solicitadas)
├── TUTORIAL_EXECUCAO.md            # Este guia passo a passo
└── .env.example                    # Exemplo de configuração da chave Gemini
```

> **Dica:** Não é necessário enviar pastas temporárias como `__pycache__` ou bancos SQLite de teste (`db.sqlite3`).

---

## 2. Instruções de Instalação e Execução (Para o Professor)

### Pré-requisitos
* **Python 3.10 ou superior** instalado no computador ([python.org](https://www.python.org/downloads/)).
* Terminal (Prompt de Comando, PowerShell ou Terminal do VS Code).

---

### Método 1: Inicialização em 1 Clique (Recomendado para Windows)
1. Extraia o arquivo `.zip` em qualquer pasta.
2. Dê um **duplo clique** no arquivo:
   👉 **`iniciar_sistema.bat`**
3. O script detecta o Python automaticamente, aplica as migrações e inicia o servidor local.
4. Abra seu navegador em:
   🌐 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

### Método 2: Execução via Linha de Comando (Passo a Passo)

1. **Abrir o terminal na pasta do projeto:**
   ```bash
   cd "caminho/para/pasta_do_projeto"
   ```

2. **(Opcional, mas recomendado) Criar e ativar um ambiente virtual:**
   ```bash
   # Criar ambiente virtual
   python -m venv .venv

   # Ativar no Windows (Prompt de Comando)
   .venv\Scripts\activate.bat

   # Ou ativar no Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   ```

3. **Instalar as dependências do projeto:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar as migrações iniciais:**
   ```bash
   python manage.py migrate
   ```

5. **Iniciar o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

6. **Acessar a aplicação no navegador:**
   Abra: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 3. Roteiro de Demonstração e Testes (Etapa 1)

O sistema foi desenhado para demonstrar com total fidelidade os requisitos da N2:

1. **Carregar o Documento Fiscal (Figura 1):**
   * Você pode clicar no botão **"⚡ Carregar Exemplo: danfe (ciclano - pecas).pdf"** para carregar a nota de teste da disciplina imediatamente com 1 clique;
   * Ou clicar em **"Escolher arquivo"** e selecionar qualquer outro arquivo `.pdf` de nota fiscal.
   * Note que o selo com o nome do arquivo e tamanho em MB é exibido automaticamente.

2. **Acionar a Extração:**
   * Clique no botão **"EXTRAIR DADOS"**.
   * O sistema exibe um indicador animado de processamento com IA.

3. **Verificar os Resultados Extraídos (Figura 2):**
   * **Aba "JSON":** Exibe o payload JSON formatado com sintaxe destacada e o botão funcional **"Copiar JSON"**.
   * **Aba "Visualização Formatada":** Apresenta os cards organizados:
     * **Fornecedor:** *IGUACU MAQUINAS AGRICOLAS LTDA* | CNPJ: *33.656.729/0023-85*
     * **Faturado:** *CICLANO DA SILVA* | CPF: *999.999.999-99*
     * **Nota Fiscal:** Nº *000.084.682*, Série *1*, Emissão *19/09/2025*, Vencimento *17/10/2025*, Valor Total *R$ 3.086,75*.
     * **Classificação da DESPESA:** Enquadrada inteligentemente pela IA na categoria **MANUTENÇÃO E OPERAÇÃO** (com justificativa semântica detalhada com base nos itens: graxa, anéis, rolamentos e materiais de limpeza mecânica).
     * **Tabela de Itens:** Discriminação completa dos 10 produtos da nota.

---

## 4. Configuração da Chave da API Google Gemini (Opcional)

O sistema possui integração nativa com a API do **Google Gemini**:
* **Sem chave informada:** O sistema utiliza um processador semântico local inteligente para garantir que a demonstração e a correção da nota da disciplina funcionem 100% mesmo se o professor estiver sem internet ou sem chave de API.
* **Com chave da API:** O professor pode testar a chamada online diretamente:
  1. Clicando no botão **"⚙️ Configurar Gemini"** no topo da página e colando sua chave da Google AI Studio; ou
  2. Criando um arquivo `.env` na raiz do projeto com o conteúdo:
     ```env
     GEMINI_API_KEY=AIzaSySuaChaveAqui...
     ```
