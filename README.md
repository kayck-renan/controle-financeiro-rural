# 🌾 Sistema de Controle Financeiro Rural

> **Projeto Administrativo-Financeiro (DOO) — Avaliação N2 (Etapa 1 & Etapa 2)**  
> **Autores:** Kayck Renan e Felipe Lopes Gonçalves  
> **Instituição:** Universidade de Rio Verde (UniRV)  
> **Data de Entrega:** Outubro/2026  

### 🌐 Links Oficiais do Projeto (Critério de Avaliação N2)
- **Aplicação Publicada (Produção na Vercel):** [https://controle-financeiro-rural.vercel.app](https://controle-financeiro-rural.vercel.app)
- **Repositório no GitHub:** [https://github.com/kayck-renan/controle-financeiro-rural](https://github.com/kayck-renan/controle-financeiro-rural)

---

## 📌 1. Visão Geral do Projeto

O **Sistema de Controle Financeiro Rural** é uma solução ERP completa voltada para a gestão fiscal e financeira do agronegócio, desenvolvida para a disciplina de **Desenvolvimento Orientado a Objetos (DOO)** da **UniRV**:

* 📄 **Extrator Fiscal Inteligente (1ª Etapa):** Leitura de DANFE (PDF), extração de dados e classificação semântica nas 9 macrocategorias oficiais com a API Google Gemini (e motor local resiliente).
* 🔍 **Análise e Consulta no Banco de Dados (2ª Etapa):** Ao concluir a extração da nota fiscal, o sistema consulta automaticamente se o **Fornecedor**, **Faturado** e a **Despesa** já existem no banco de dados e exibe o status em tela (`EXISTE – ID: XX` ou `NÃO EXISTE`).
* 💾 **Lançamento Automático em 1 Clique (2ª Etapa):** Cria automaticamente novo fornecedor, faturado, despesa e registra o Movimento de Contas e suas Parcelas.
* 👥 **Módulo Manter Pessoas:** Gestão completa de Fornecedores, Clientes e Faturados com busca multi-elemento, filtro de status em 3 estados (Todos, Somente ativos, Somente inativos), botão "Listar Registros", exclusão lógica (inativação/reativação) e validação em tempo real de CPF/CNPJ e Telefone.
* 🏷️ **Módulo Manter Classificações:** Gestão das 9 macrocategorias de Despesas e Receitas rurais com limites de caracteres.
* 💳 **Módulo Registrar Contas a Pagar & Contas a Receber:** Suporte a múltiplas classificações por movimento e parcelamento com datas de vencimento distintas.
* 🌓 **Alternador de Tema (Modo Claro & Modo Escuro):** Botão intuitivo no cabeçalho com transições suaves e persistência da preferência do usuário via `localStorage`.
* 🔒 **Segurança da Chave da API (LLM) & Autenticação:** A chave do Gemini permanece confidencial e protegida, nunca exposta na interface do site. A autenticação utiliza cookies criptograficamente assinados resilientes a ambientes serverless (Vercel).
* 🐙 **Código da Última Atualização no GitHub:** Exibido em destaque no cabeçalho e na tela principal do sistema.

---

## 🔑 Credenciais e Dados de Entrega (Solicitação do Docente)

- **Link Hospedagem (Produção):** [https://controle-financeiro-rural.vercel.app/](https://controle-financeiro-rural.vercel.app/)
- **Repositório GitHub:** [https://github.com/kayck-renan/controle-financeiro-rural](https://github.com/kayck-renan/controle-financeiro-rural)
- **Código da Última Atualização no GitHub:** Exibido dinamicamente no cabeçalho e páginas do sistema.
- **Key Confidencial da API Gemini (LLM):** `AIzaSyDemoUniRV2026RuralFinancasKey99`

| Usuário (Login) | Senha | Perfil |
| :--- | :--- | :--- |
| `kayck` | `unirv2026` | Kayck Renan (Autor / Desenvolvedor) |
| `felipelopesgoncalves` | `unirv2026` | Felipe Lopes Gonçalves (Autor) |
| `felipe` | `unirv2026` | Felipe Lopes Gonçalves (Acesso Rápido) |
| `admin` | `admin123` | Administrador do Sistema |

> **Nota de Segurança:** As credenciais de acesso foram removidas da tela inicial de login por boas práticas de conformidade e segurança da informação, ficando documentadas com exclusividade neste arquivo e no repositório.

---

## 🎨 Modernização do Frontend & Novas Funcionalidades

1. **Modo Claro / Modo Escuro (Dark/Light Mode):**
   - Alternância em 1 clique através do botão no cabeçalho (`☀️ Modo Claro` / `🌙 Modo Escuro`).
   - Cores refinadas no padrão Tailwind/Slate moderno, com alto contraste, legibilidade e efeitos de profundidade.
   - Detecção automática da preferência do sistema operacional e persistência da escolha do usuário no navegador.

2. **Formatação Automática e Validação dos Campos de Cadastro:**
   - **CPF / CNPJ:** Máscara dinâmica inteligente (formata como CPF até 11 dígitos `000.000.000-00` ou CNPJ até 14 dígitos `00.000.000/0000-00`), com limite estrito de 18 caracteres. Validação dos dígitos verificadores oficiais com feedback visual em tempo real (verde para válido, vermelho para inválido).
   - **Telefone:** Máscara contínua `(00) 0000-0000` ou `(00) 00000-0000` com limite de 15 caracteres.
   - **E-mail:** Validação de sintaxe e domínio com indicador instantâneo de conformidade.
   - **Limites de Caracteres (`maxlength`):** Aplicados em todos os campos de formulário do sistema para prevenir estouros de dados.

3. **Navegação Resiliente (Sessão Serverless na Vercel):**
   - Configuração de sessão baseada em `signed_cookies` (`SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'`).
   - Resolução definitiva do bug de redirecionamento para login ao navegar entre os itens do menu lateral no ambiente da Vercel.

---

## 🧭 Módulos do Sistema e Regras de Negócio (Etapa 2)

### 1. Extrator Fiscal & Análise no Banco de Dados (`/`)
- Upload de DANFE em PDF ou clique em **"⚡ Carregar Exemplo"**.
- Extração automática de produtos, valores, emitente e destinatário.
- **Painel de Análise (2ª Etapa):** Consulta em tempo real no banco:
  - FORNECEDOR: `EXISTE – ID: XX` ou `NÃO EXISTE`
  - FATURADO: `EXISTE – ID: XX` ou `NÃO EXISTE`
  - DESPESA: `EXISTE – ID: XX` ou `NÃO EXISTE`
- **Botão de Lançamento em 1 Clique:** Cria automaticamente as entidades inexistentes e lança o movimento com suas respectivas parcelas no banco de dados.

### 2. Manter Pessoas (`/pessoas/`)
- Cadastro e edição de Fornecedores, Clientes e Faturados.
- Regras de negócio da disciplina:
  - Tabela de registros inicia vazia.
  - Carrega com busca multi-elemento ou botão **"Listar Registros"** com filtro de status configurável (**Todos**, **Somente ativos** ou **Somente inativos**).
  - Cadastros nunca são excluídos fisicamente: apenas **INATIVADOS** (exclusão lógica).
  - É possível **REATIVAR** registros previamente inativados.
  - No CREATE: campo `status` oculto == `ATIVO`.
  - No UPDATE: campo `status` oculto.
  - No DELETE: altera o campo `status` para `INATIVO`.

### 3. Manter Classificações (`/classificacoes/`)
- 9 Macrocategorias oficiais da N2 de Despesas + Classificações de Receitas.
- Inativação e reativação lógica.

### 4. Registrar Contas a Pagar (`/contas-a-pagar/`) & Contas a Receber (`/contas-a-receber/`)
- Múltiplas classificações por movimento financeiro.
- Múltiplas parcelas com datas de vencimento distintas.
- Inativação e reativação lógica.

---

## 💻 Como Rodar Localmente

1. Execute o script de 1 clique:
   ```cmd
   iniciar_sistema.bat
   ```
2. Abra o navegador em:
   ```
   http://127.0.0.1:8000/
   ```
