# 🌾 Sistema de Controle Financeiro Rural

> **Projeto Administrativo-Financeiro (DOO) — Avaliação N2 (Etapa 1 & Etapa 2)**  
> **Autores:** Kayck Renan e Felipe Lopes Gonçalves  
> **Instituição:** Universidade de Rio Verde (UniRV)  
> **Data de Entrega:** Outubro/2026  

---

## 📌 1. Visão Geral do Projeto

O **Sistema de Controle Financeiro Rural** é uma solução ERP completa voltada para a gestão fiscal e financeira do agronegócio, desenvolvida para a disciplina de **Desenvolvimento Orientado a Objetos (DOO)** da **UniRV**:

* 📄 **Extrator Fiscal Inteligente (1ª Etapa):** Leitura de DANFE (PDF), extração de dados e classificação semântica nas 9 macrocategorias oficiais com a API Google Gemini (e motor local resiliente).
* 🔍 **Análise e Consulta no Banco de Dados (2ª Etapa):** Ao concluir a extração da nota fiscal, o sistema consulta automaticamente se o **Fornecedor**, **Faturado** e a **Despesa** já existem no banco de dados e exibe o status em tela (`EXISTE – ID: XX` ou `NÃO EXISTE`).
* 💾 **Lançamento Automático em 1 Clique (2ª Etapa):** Cria automaticamente novo fornecedor, faturado, despesa e registra o Movimento de Contas e suas Parcelas.
* 👥 **Módulo Manter Pessoas:** Gestão completa de Fornecedores, Clientes e Faturados com busca multi-elemento, botão "Todos (Ativos)" e exclusão lógica (inativação/reativação).
* 🏷️ **Módulo Manter Classificações:** Gestão das 9 macrocategorias de Despesas e Receitas rurais.
* 💳 **Módulo Registrar Contas a Pagar & Contas a Receber:** Suporte a múltiplas classificações por movimento e parcelamento com datas de vencimento distintas.
* 🔒 **Segurança da Chave da API (LLM):** A chave do Gemini é mascarada e protegida, nunca sendo exposta em texto plano na interface.
* 🐙 **Código da Última Atualização no GitHub:** Exibido em destaque no cabeçalho e na tela principal do sistema.

---

## 🔑 Credenciais e Dados de Entrega (Solicitação do Docente)

- **Link Hospedagem (Produção):** [https://controle-financeiro-rural.vercel.app/](https://controle-financeiro-rural.vercel.app/)
- **Repositório GitHub:** [https://github.com/kayck-renan/controle-financeiro-rural](https://github.com/kayck-renan/controle-financeiro-rural)
- **Código da Última Atualização no GitHub:** Exibido dinamicamente na tela principal do projeto.
- **Key (LLM):** `AIzaSyDemoUniRV2026RuralFinancasKey99`

| Usuário (Login) | Senha | Perfil |
| :--- | :--- | :--- |
| `kayck` | `unirv2026` | Kayck Renan (Autor / Desenvolvedor) |
| `felipelopesgoncalves` | `unirv2026` | Felipe Lopes Gonçalves (Autor) |
| `admin` | `admin123` | Administrador |

---

## 🧭 Módulos do Sistema e Regras de Negócio (Etapa 2)

### 1. Extrator Fiscal & Análise no Banco de Dados
- Upload de DANFE ou clique em **"⚡ Carregar Exemplo"**.
- Extração de produtos, valores, emitente e destinatário.
- **Painel de Análise (2ª Etapa):** Consulta em tempo real no banco:
  - FORNECEDOR: `EXISTE – ID: 1` ou `NÃO EXISTE`
  - FATURADO: `EXISTE – ID: 2` ou `NÃO EXISTE`
  - DESPESA: `EXISTE – ID: 2` ou `NÃO EXISTE`
- **Botão de Ação:** Lança o movimento e parcelas com um clique, criando as entidades inexistentes.

### 2. Manter Pessoas (`/pessoas/`)
- Cadastro de Fornecedores, Clientes e Faturados.
- Regras de negócio da disciplina:
  - Tabela inicia vazia.
  - Carrega com busca multi-elemento ou botão **"Todos (Ativos)"** (filtra `status = ATIVO`).
  - Cadastros não são excluídos fisicamente: apenas **INATIVADOS** (exclusão lógica).
  - É possível **REATIVAR** um registro inativo.
  - No CREATE: campo `status` oculto == `ATIVO`.
  - No UPDATE: campo `status` oculto.
  - No DELETE: altera campo `status == INATIVO`.

### 3. Manter Classificações (`/classificacoes/`)
- 9 Macrocategorias oficiais da N2 de Despesas + Tipos de Receitas.
- Inativação e reativação lógica.

### 4. Registrar Contas a Pagar (`/contas-a-pagar/`) & Contas a Receber (`/contas-a-receber/`)
- Múltiplas classificações por movimento.
- Múltiplas parcelas com datas de vencimento distintas.
- Inativação e reativação lógica.

---

## 💻 Como Rodar Localmente

1. Execute o script de 1 clique:
   ```cmd
   iniciar_sistema.bat
   ```
2. Acesse: `http://127.0.0.1:8000/`
