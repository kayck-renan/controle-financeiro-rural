document.addEventListener('DOMContentLoaded', () => {
  // =========================================================================
  // ALTERNÂNCIA DE TEMA (CLARO / ESCURO)
  // =========================================================================
  const btnThemeToggle = document.getElementById('btn-theme-toggle');
  const themeToggleText = document.getElementById('theme-toggle-text');

  function aplicarTema(tema) {
    document.documentElement.setAttribute('data-theme', tema);
    document.body.setAttribute('data-theme', tema);
    try {
      localStorage.setItem('rural_theme', tema);
    } catch (e) {}
    if (themeToggleText) {
      themeToggleText.textContent = tema === 'dark' ? 'Modo Escuro' : 'Modo Claro';
    }
  }

  const temaInicial = document.documentElement.getAttribute('data-theme') || 'light';
  aplicarTema(temaInicial);

  if (btnThemeToggle) {
    btnThemeToggle.addEventListener('click', () => {
      const temaAtual = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
      const novoTema = temaAtual === 'dark' ? 'light' : 'dark';
      aplicarTema(novoTema);
    });
  }

  // =========================================================================
  // MENU LATERAL RESPONSIVO (MOBILE OFFCANVAS)
  // =========================================================================
  const btnSidebarToggle = document.getElementById('btn-sidebar-toggle');
  const appSidebar = document.getElementById('app-sidebar');
  const sidebarBackdrop = document.getElementById('sidebar-backdrop');

  function toggleSidebar(open) {
    if (!appSidebar) return;
    const shouldOpen = open !== undefined ? open : !appSidebar.classList.contains('open');
    if (shouldOpen) {
      appSidebar.classList.add('open');
      if (sidebarBackdrop) sidebarBackdrop.classList.add('show');
    } else {
      appSidebar.classList.remove('open');
      if (sidebarBackdrop) sidebarBackdrop.classList.remove('show');
    }
  }

  if (btnSidebarToggle) {
    btnSidebarToggle.addEventListener('click', () => toggleSidebar());
  }
  if (sidebarBackdrop) {
    sidebarBackdrop.addEventListener('click', () => toggleSidebar(false));
  }
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && appSidebar && appSidebar.classList.contains('open')) {
      toggleSidebar(false);
    }
  });

  // Elementos do DOM - Arquivo & Upload
  const fileInput = document.getElementById('file-input');
  const dropzone = document.getElementById('dropzone');
  const fileSelectedBadge = document.getElementById('file-selected-badge');
  const badgeFileName = document.getElementById('badge-file-name');
  const badgeFileSize = document.getElementById('badge-file-size');
  const btnRemoveFile = document.getElementById('btn-remove-file');
  const btnExtrair = document.getElementById('btn-extrair');
  const btnUseSample = document.getElementById('btn-use-sample');
  const loadingIndicator = document.getElementById('loading-indicator');
  const resultsSection = document.getElementById('results-section');
  const jsonCodeDisplay = document.getElementById('json-code-display');
  const btnCopyJson = document.getElementById('btn-copy-json');
  const copyBtnText = document.getElementById('copy-btn-text');
  const toast = document.getElementById('toast');
  const extractionModeBadge = document.getElementById('extraction-mode-badge');
  const modeText = document.getElementById('mode-text');

  // Abas
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  // Elementos de Gestão Segura da KEY (Oculta)
  const keyLivePill = document.getElementById('key-live-pill');
  const pillText = document.getElementById('pill-text');
  const barStatusTag = document.getElementById('bar-status-tag');
  const barLiveFeedback = document.getElementById('bar-live-feedback');
  const barApiKeyInput = document.getElementById('bar-api-key-input');
  const btnEnviarChave = document.getElementById('btn-enviar-chave');
  const btnLimparChaveBar = document.getElementById('btn-limpar-chave-bar');

  // Modal de Configuração da Chave
  const btnToggleConfig = document.getElementById('btn-toggle-config');
  const modalConfig = document.getElementById('modal-config');
  const btnCloseConfig = document.getElementById('btn-close-config');
  const inputApiKey = document.getElementById('input-api-key');
  const btnSaveKey = document.getElementById('btn-save-key');
  const btnClearKey = document.getElementById('btn-clear-key');

  // Elementos da Análise no Banco de Dados (2ª Etapa)
  const analiseFornNome = document.getElementById('analise-forn-nome');
  const analiseFornDoc = document.getElementById('analise-forn-doc');
  const pillFornStatus = document.getElementById('pill-forn-status');

  const analiseFatNome = document.getElementById('analise-fat-nome');
  const analiseFatDoc = document.getElementById('analise-fat-doc');
  const pillFatStatus = document.getElementById('pill-fat-status');

  const analiseDespNome = document.getElementById('analise-desp-nome');
  const pillDespStatus = document.getElementById('pill-desp-status');

  const btnLancarMovimento = document.getElementById('btn-lancar-movimento-etapa2');
  const boxSucessoLancamento = document.getElementById('box-sucesso-lancamento');
  const msgSucessoDetalhes = document.getElementById('msg-sucesso-detalhes');

  let currentFile = null;
  let useSampleMode = false;
  let lastExtractedData = null;

  // =========================================================================
  // GESTÃO SEGURA DA CHAVE GEMINI (OCULTA POR SEGURANÇA)
  // =========================================================================

  function atualizarStatusKeyInterface(ativo) {
    const barIndicatorDot = document.getElementById('bar-indicator-dot');
    if (ativo) {
      if (keyLivePill) {
        keyLivePill.classList.add('active');
        if (pillText) pillText.textContent = 'Chave Protegida (Ativa)';
      }
      if (barStatusTag) {
        barStatusTag.className = 'badge badge-success';
        barStatusTag.textContent = 'Chave Ativa';
      }
      if (barIndicatorDot) {
        barIndicatorDot.className = 'status-indicator-dot active';
      }
      if (barLiveFeedback) {
        barLiveFeedback.textContent = 'Chave da API ativada no ambiente seguro. Oculta contra visualização indevida.';
      }
    } else {
      if (keyLivePill) {
        keyLivePill.classList.remove('active');
        if (pillText) pillText.textContent = 'Modo Local';
      }
      if (barStatusTag) {
        barStatusTag.className = 'badge badge-neutral';
        barStatusTag.textContent = 'Modo Local';
      }
      if (barIndicatorDot) {
        barIndicatorDot.className = 'status-indicator-dot';
      }
      if (barLiveFeedback) {
        barLiveFeedback.textContent = 'Nenhuma chave ativa. O sistema opera com o motor semântico inteligente local.';
      }
    }
  }

  // Verifica status seguro inicial no backend
  fetch('/api/configurar-chave/')
    .then(res => res.json())
    .then(data => {
      atualizarStatusKeyInterface(data.status === 'configurada');
    })
    .catch(() => {
      atualizarStatusKeyInterface(false);
    });

  // Salvar Chave com Mascaramento Total
  async function salvarChaveSegura(chave) {
    const val = (chave || '').trim();
    try {
      const resp = await fetch('/api/configurar-chave/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_key: val })
      });
      const data = await resp.json();
      atualizarStatusKeyInterface(Boolean(val));
      if (barApiKeyInput) barApiKeyInput.value = '';
      if (inputApiKey) inputApiKey.value = '';
      showToast(data.mensagem || (val ? 'Chave salva com sucesso!' : 'Chave removida.'));
    } catch (err) {
      showToast('Erro ao atualizar chave.');
    }
  }

  if (btnEnviarChave) {
    btnEnviarChave.addEventListener('click', () => {
      const val = barApiKeyInput ? barApiKeyInput.value : '';
      if (val) salvarChaveSegura(val);
    });
  }

  if (btnLimparChaveBar) {
    btnLimparChaveBar.addEventListener('click', () => {
      salvarChaveSegura('');
    });
  }

  if (btnSaveKey) {
    btnSaveKey.addEventListener('click', () => {
      const val = inputApiKey ? inputApiKey.value : '';
      salvarChaveSegura(val);
      if (modalConfig) modalConfig.classList.add('hidden');
    });
  }

  if (btnClearKey) {
    btnClearKey.addEventListener('click', () => {
      salvarChaveSegura('');
      if (modalConfig) modalConfig.classList.add('hidden');
    });
  }

  // Modal de Configuração
  if (btnToggleConfig && modalConfig) {
    btnToggleConfig.addEventListener('click', () => {
      modalConfig.classList.remove('hidden');
    });
  }

  if (btnCloseConfig && modalConfig) {
    btnCloseConfig.addEventListener('click', () => {
      modalConfig.classList.add('hidden');
    });
  }

  if (modalConfig) {
    modalConfig.addEventListener('click', (e) => {
      if (e.target === modalConfig) modalConfig.classList.add('hidden');
    });
  }

  // =========================================================================
  // ARQUIVOS (PDF) E DROPZONE
  // =========================================================================
  if (dropzone) {
    dropzone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => {
      dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropzone.classList.remove('dragover');
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        handleFileSelected(e.dataTransfer.files[0]);
      }
    });

    dropzone.addEventListener('click', (e) => {
      if (e.target.closest('#btn-remove-file')) return;
      if (fileInput) fileInput.click();
    });
  }

  if (fileInput) {
    fileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files.length > 0) {
        handleFileSelected(e.target.files[0]);
      }
    });
  }

  function handleFileSelected(file) {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      alert('Por favor, selecione exclusivamente um arquivo no formato PDF.');
      return;
    }

    currentFile = file;
    useSampleMode = false;

    if (badgeFileName) badgeFileName.textContent = file.name;
    if (badgeFileSize) badgeFileSize.textContent = formatBytes(file.size);
    if (fileSelectedBadge) fileSelectedBadge.classList.remove('hidden');
    if (btnExtrair) btnExtrair.removeAttribute('disabled');
  }

  if (btnUseSample) {
    btnUseSample.addEventListener('click', () => {
      currentFile = null;
      useSampleMode = true;

      if (badgeFileName) badgeFileName.textContent = 'danfe (ciclano - pecas).pdf (Arquivo de Demonstração)';
      if (badgeFileSize) badgeFileSize.textContent = '7.5 KB';
      if (fileSelectedBadge) fileSelectedBadge.classList.remove('hidden');
      if (btnExtrair) btnExtrair.removeAttribute('disabled');

      showToast('Arquivo de teste oficial selecionado com sucesso!');
    });
  }

  if (btnRemoveFile) {
    btnRemoveFile.addEventListener('click', (e) => {
      e.stopPropagation();
      currentFile = null;
      useSampleMode = false;
      if (fileInput) fileInput.value = '';
      if (fileSelectedBadge) fileSelectedBadge.classList.add('hidden');
      if (btnExtrair) btnExtrair.setAttribute('disabled', 'true');
      if (resultsSection) resultsSection.classList.add('hidden');
    });
  }

  // =========================================================================
  // ABAS (FORMATADA E JSON)
  // =========================================================================
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const tabTarget = btn.getAttribute('data-tab');
      const content = document.getElementById(tabTarget);
      if (content) content.classList.add('active');
    });
  });

  // =========================================================================
  // EXTRAÇÃO DE DADOS (POST /api/extrair-nf/)
  // =========================================================================
  if (btnExtrair) {
    btnExtrair.addEventListener('click', async () => {
      if (!currentFile && !useSampleMode) {
        alert('Selecione uma nota fiscal em PDF primeiro.');
        return;
      }

      btnExtrair.setAttribute('disabled', 'true');
      if (loadingIndicator) loadingIndicator.classList.remove('hidden');
      if (resultsSection) resultsSection.classList.add('hidden');
      if (boxSucessoLancamento) boxSucessoLancamento.classList.add('hidden');

      const formData = new FormData();
      if (useSampleMode) {
        formData.append('usar_exemplo', 'true');
      } else if (currentFile) {
        formData.append('pdf_file', currentFile);
      }

      try {
        const response = await fetch('/api/extrair-nf/', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.erro || `Erro HTTP ${response.status}`);
        }

        const data = await response.json();
        lastExtractedData = data;

        // Renderiza campos da 1ª etapa
        renderizarCamposEtapa1(data);

        // Dispara a consulta de banco de dados da 2ª Etapa
        await consultarEntidadesEtapa2(data);

        if (loadingIndicator) loadingIndicator.classList.add('hidden');
        if (resultsSection) resultsSection.classList.remove('hidden');
        btnExtrair.removeAttribute('disabled');

        resultsSection.scrollIntoView({ behavior: 'smooth' });

      } catch (err) {
        console.error(err);
        if (loadingIndicator) loadingIndicator.classList.add('hidden');
        btnExtrair.removeAttribute('disabled');
        alert(`Falha no processamento: ${err.message}`);
      }
    });
  }

  // =========================================================================
  // ETAPA 2: CONSULTA NO BANCO DE DADOS (CONFORME PÁGINA 2 DO PDF)
  // =========================================================================
  async function consultarEntidadesEtapa2(data) {
    try {
      const payload = {
        fornecedor_razao: data.fornecedor?.razaoSocial || data.fornecedor?.razao_social || '',
        fornecedor_cnpj: data.fornecedor?.cnpj || '',
        faturado_nome: data.faturado?.nomeCompleto || data.faturado?.nome_completo || '',
        faturado_cpf: data.faturado?.cpf || '',
        despesa_descricao: data.classificacaoDespesa || data.classificacao_despesa || ''
      };

      const res = await fetch('/api/consultar-entidades/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const consulta = await res.json();

      // 1. Fornecedor
      if (analiseFornNome) analiseFornNome.textContent = consulta.fornecedor.nome;
      if (analiseFornDoc) analiseFornDoc.textContent = `CNPJ: ${consulta.fornecedor.documento || 'Não informado'}`;
      if (pillFornStatus) {
        pillFornStatus.textContent = consulta.fornecedor.status_texto;
        pillFornStatus.className = `analysis-status-pill ${consulta.fornecedor.existe ? 'existe' : 'nao-existe'}`;
      }

      // 2. Faturado
      if (analiseFatNome) analiseFatNome.textContent = consulta.faturado.nome;
      if (analiseFatDoc) analiseFatDoc.textContent = `CPF: ${consulta.faturado.documento || 'Não informado'}`;
      if (pillFatStatus) {
        pillFatStatus.textContent = consulta.faturado.status_texto;
        pillFatStatus.className = `analysis-status-pill ${consulta.faturado.existe ? 'existe' : 'nao-existe'}`;
      }

      // 3. Despesa
      if (analiseDespNome) analiseDespNome.textContent = consulta.despesa.descricao;
      if (pillDespStatus) {
        pillDespStatus.textContent = consulta.despesa.status_texto;
        pillDespStatus.className = `analysis-status-pill ${consulta.despesa.existe ? 'existe' : 'nao-existe'}`;
      }

    } catch (e) {
      console.error('Erro na consulta de entidades:', e);
    }
  }

  // =========================================================================
  // ETAPA 2: BOTÃO LANÇAR MOVIMENTO NO BANCO DE DADOS
  // =========================================================================
  if (btnLancarMovimento) {
    btnLancarMovimento.addEventListener('click', async () => {
      if (!lastExtractedData) {
        alert('Nenhum dado extraído disponível para lançamento.');
        return;
      }

      btnLancarMovimento.setAttribute('disabled', 'true');
      btnLancarMovimento.textContent = 'Gravando no Banco de Dados...';

      try {
        const res = await fetch('/api/lancar-movimento/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(lastExtractedData)
        });
        const resp = await res.json();

        if (resp.sucesso) {
          showToast(resp.mensagem);
          if (boxSucessoLancamento) {
            boxSucessoLancamento.classList.remove('hidden');
            if (msgSucessoDetalhes) {
              const det = resp.detalhes;
              msgSucessoDetalhes.innerHTML = `
                Movimento <strong>#${det.movimento_id}</strong> (Tipo: ${det.tipo}) cadastrado com sucesso!<br>
                Fornecedor: <strong>${det.fornecedor.razao_social}</strong> (ID: ${det.fornecedor.id}) | 
                Faturado: <strong>${det.faturado.razao_social}</strong> (ID: ${det.faturado.id})<br>
                Despesa: <strong>${det.despesa.descricao}</strong> (ID: ${det.despesa.id}) | 
                Total: <strong>R$ ${det.valor_total}</strong> (${det.parcelas.length} parcela(s)).
              `;
            }
            boxSucessoLancamento.scrollIntoView({ behavior: 'smooth' });
          }

          // Atualiza status das pills para EXISTE
          if (pillFornStatus) {
            pillFornStatus.textContent = `EXISTE – ID: ${resp.detalhes.fornecedor.id}`;
            pillFornStatus.className = 'analysis-status-pill existe';
          }
          if (pillFatStatus) {
            pillFatStatus.textContent = `EXISTE – ID: ${resp.detalhes.faturado.id}`;
            pillFatStatus.className = 'analysis-status-pill existe';
          }
          if (pillDespStatus) {
            pillDespStatus.textContent = `EXISTE – ID: ${resp.detalhes.despesa.id}`;
            pillDespStatus.className = 'analysis-status-pill existe';
          }

        } else {
          alert(resp.erro || 'Erro ao lançar movimento');
        }

      } catch (err) {
        alert('Falha na comunicação ao lançar movimento');
      } finally {
        btnLancarMovimento.removeAttribute('disabled');
        btnLancarMovimento.innerHTML = '<span>Lançar Movimento e Parcelas no Banco de Dados</span>';
      }
    });
  }

  // =========================================================================
  // RENDERIZAÇÃO DE CAMPOS (ETAPA 1)
  // =========================================================================
  function renderizarCamposEtapa1(data) {
    if (data._extracao_modo && modeText) {
      modeText.textContent = data._extracao_modo;
    }

    const cleanJson = {};
    for (const key in data) {
      if (!key.startsWith('_')) cleanJson[key] = data[key];
    }
    if (jsonCodeDisplay) {
      jsonCodeDisplay.textContent = JSON.stringify(cleanJson, null, 2);
    }

    // Metadados
    setText('card-numero-nf', data.numero || '000.000');
    setText('card-serie', data.serie || '1');
    setText('card-emissao', formatarData(data.dataEmissao));
    setText('card-vencimento', formatarData(data.dataVencimento));

    // Fornecedor
    setText('card-fornecedor-razao', data.fornecedor?.razaoSocial || 'Não identificado');
    setText('card-fornecedor-fantasia', data.fornecedor?.fantasia || '-');
    setText('card-fornecedor-cnpj', data.fornecedor?.cnpj || '-');

    // Faturado
    setText('card-faturado-nome', data.faturado?.nomeCompleto || 'Não identificado');
    setText('card-faturado-cpf', data.faturado?.cpf || '-');

    // Classificação
    setText('card-classificacao', data.classificacaoDespesa || 'MANUTENÇÃO E OPERAÇÃO');
    setText('card-justificativa', data.justificativaClassificacao || 'Inferência semântica realizada com sucesso.');

    // Valores e Parcelas
    const valor = Number(data.valorTotal || 0);
    setText('card-valor-total', formatarMoeda(valor));
    setText('card-parcelas', `${data.quantidadeParcelas || 1} parcela(s)`);

    // Tabela de Produtos
    const tbody = document.getElementById('products-table-body');
    const productsCount = document.getElementById('products-count');
    if (tbody) {
      tbody.innerHTML = '';
      const produtos = data.produtos || [];
      if (productsCount) productsCount.textContent = `${produtos.length} itens`;

      if (produtos.length === 0 && data.descricaoProdutos) {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>1</td>
          <td>${data.descricaoProdutos}</td>
          <td style="text-align: center;">1</td>
          <td style="text-align: right; font-family: var(--font-mono);">${formatarMoeda(valor)}</td>
        `;
        tbody.appendChild(row);
      } else {
        produtos.forEach((p, idx) => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${idx + 1}</td>
            <td><strong>${p.descricao || 'Item sem descrição'}</strong></td>
            <td style="text-align: center;">${p.quantidade || 1}</td>
            <td style="text-align: right; font-family: var(--font-mono);">${formatarMoeda(p.valorTotal || 0)}</td>
          `;
          tbody.appendChild(row);
        });
      }
    }
  }

  // =========================================================================
  // COPIAR JSON & UTILITÁRIOS
  // =========================================================================
  if (btnCopyJson && jsonCodeDisplay) {
    btnCopyJson.addEventListener('click', () => {
      navigator.clipboard.writeText(jsonCodeDisplay.textContent)
        .then(() => {
          if (copyBtnText) copyBtnText.textContent = '✓ Copiado!';
          showToast('JSON copiado para a área de transferência!');
          setTimeout(() => {
            if (copyBtnText) copyBtnText.textContent = '📋 Copiar JSON';
          }, 2500);
        })
        .catch(() => alert('Falha ao copiar JSON.'));
    });
  }

  function setText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
  }

  function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);
  }

  function formatarData(dataStr) {
    if (!dataStr) return '-';
    try {
      const [ano, mes, dia] = dataStr.substring(0, 10).split('-');
      if (ano && mes && dia) return `${dia}/${mes}/${ano}`;
    } catch (e) {}
    return dataStr;
  }

  function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }

  window.showToast = function(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.remove('hidden');
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.classList.add('hidden'), 300);
    }, 3500);
  };

  // =========================================================================
  // ATUALIZAÇÃO DO STATUS DO GITHUB SOB DEMANDA
  // =========================================================================
  const btnRefreshCommit = document.getElementById('btn-refresh-github-commit');
  if (btnRefreshCommit) {
    btnRefreshCommit.addEventListener('click', async () => {
      btnRefreshCommit.classList.add('spinning');
      btnRefreshCommit.setAttribute('disabled', 'true');
      try {
        const res = await fetch('/api/github-commit/?refresh=true');
        const data = await res.json();

        const hashEl = document.getElementById('github-commit-hash');
        const dateEl = document.getElementById('github-commit-date');
        const msgEl = document.getElementById('github-commit-msg');
        const pillEl = document.getElementById('github-commit-pill');
        const fallbackNote = document.getElementById('github-fallback-note');

        if (hashEl) hashEl.textContent = `#${data.git_commit_hash}`;
        if (dateEl) dateEl.textContent = `em ${data.git_commit_date}`;
        if (msgEl) {
          msgEl.textContent = data.git_commit_message || 'Atualização recente no repositório.';
          msgEl.setAttribute('title', data.git_commit_message || '');
        }
        if (pillEl) {
          pillEl.setAttribute('href', data.git_commit_url || data.git_repo_url);
          if (data.git_sucesso) {
            pillEl.classList.remove('error');
            if (fallbackNote) fallbackNote.style.display = 'none';
          } else {
            pillEl.classList.add('error');
            if (fallbackNote) {
              fallbackNote.textContent = `(${data.git_erro_msg || 'Dados locais'})`;
              fallbackNote.style.display = 'inline';
            }
          }
        }
        showToast(data.git_sucesso ? 'Dados do GitHub atualizados com sucesso!' : 'Status do GitHub recarregado.');
      } catch (err) {
        showToast('Não foi possível sincronizar com o GitHub no momento.');
      } finally {
        setTimeout(() => {
          btnRefreshCommit.classList.remove('spinning');
          btnRefreshCommit.removeAttribute('disabled');
        }, 400);
      }
    });
  }
});

