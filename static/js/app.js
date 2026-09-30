document.addEventListener('DOMContentLoaded', () => {
  // Elementos do DOM - Arquivo & Upload
  const fileInput = document.getElementById('file-input');
  const dropzone = document.getElementById('dropzone');
  const fileNameDisplay = document.getElementById('file-name-display');
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

  // Elementos de Gestão da KEY em Tempo Real
  const keyLivePill = document.getElementById('key-live-pill');
  const pillText = document.getElementById('pill-text');
  const barStatusTag = document.getElementById('bar-status-tag');
  const barLiveFeedback = document.getElementById('bar-live-feedback');
  const barApiKeyInput = document.getElementById('bar-api-key-input');
  const btnToggleBarEye = document.getElementById('btn-toggle-bar-eye');
  const btnEnviarChave = document.getElementById('btn-enviar-chave');
  const btnDemoKey = document.getElementById('btn-demo-key');
  const btnLimparChaveBar = document.getElementById('btn-limpar-chave-bar');
  const typingLiveIndicator = document.getElementById('typing-live-indicator');
  const typingLiveText = document.getElementById('typing-live-text');

  // Modal de Configuração da Chave
  const btnToggleConfig = document.getElementById('btn-toggle-config');
  const modalConfig = document.getElementById('modal-config');
  const btnCloseConfig = document.getElementById('btn-close-config');
  const inputApiKey = document.getElementById('input-api-key');
  const btnToggleModalEye = document.getElementById('btn-toggle-modal-eye');
  const modalRealtimeKeyPreview = document.getElementById('modal-realtime-key-preview');
  const btnSaveKey = document.getElementById('btn-save-key');
  const btnModalDemoKey = document.getElementById('btn-modal-demo-key');
  const btnClearKey = document.getElementById('btn-clear-key');

  const DEMO_API_KEY = 'AIzaSyDemoUniRV2026RuralFinancasKey99';

  let currentFile = null;
  let useSampleMode = false;
  let lastExtractedData = null;

  // =========================================================================
  // GESTÃO E MONITORAMENTO DA KEY EM TEMPO REAL
  // =========================================================================

  function mascararChave(key) {
    if (!key) return '';
    if (key.length <= 10) return '••••••••';
    return key.substring(0, 6) + '••••••••' + key.substring(key.length - 4);
  }

  // Atualiza todos os indicadores da KEY em tempo real na interface
  function atualizarStatusKeyInterface(key, modoServidor = null) {
    const temChave = Boolean(key && key.trim());
    const mascara = temChave ? mascararChave(key.trim()) : null;

    if (temChave) {
      // Header pill
      if (keyLivePill) {
        keyLivePill.classList.add('active');
        pillText.textContent = `🔑 Chave: ${mascara}`;
      }
      // Barra principal
      if (barStatusTag) {
        barStatusTag.className = 'status-tag active';
        barStatusTag.textContent = '✓ CHAVE ATIVA (Online)';
      }
      if (barLiveFeedback) {
        barLiveFeedback.innerHTML = `Chave configurada: <strong>${mascara}</strong> (${key.trim().length} caracteres). Pronto para chamadas à API Gemini.`;
      }
    } else {
      // Header pill
      if (keyLivePill) {
        keyLivePill.classList.remove('active');
        pillText.textContent = '🔑 Modo Local (Sem Chave)';
      }
      // Barra principal
      if (barStatusTag) {
        barStatusTag.className = 'status-tag local';
        barStatusTag.textContent = 'Modo Local Ativo';
      }
      if (barLiveFeedback) {
        barLiveFeedback.textContent = 'Nenhuma chave externa enviada. O sistema processará com o motor semântico inteligente local.';
      }
    }
  }

  // Inicialização da chave a partir de localStorage e backend
  const savedLocalKey = localStorage.getItem('gemini_api_key') || '';
  if (savedLocalKey) {
    if (barApiKeyInput) barApiKeyInput.value = savedLocalKey;
    if (inputApiKey) inputApiKey.value = savedLocalKey;
    atualizarStatusKeyInterface(savedLocalKey);
  }

  // Consulta status inicial no backend
  fetch('/api/configurar-chave/')
    .then(res => res.json())
    .then(data => {
      if (data.configurada && !savedLocalKey) {
        atualizarStatusKeyInterface(data.chave_mascarada);
      } else if (savedLocalKey) {
        atualizarStatusKeyInterface(savedLocalKey);
      } else {
        atualizarStatusKeyInterface('');
      }
    })
    .catch(() => {
      atualizarStatusKeyInterface(savedLocalKey);
    });

  // Digitação em tempo real na Barra
  if (barApiKeyInput) {
    barApiKeyInput.addEventListener('input', (e) => {
      const val = e.target.value.trim();
      if (inputApiKey) inputApiKey.value = val;

      if (val.length > 0) {
        typingLiveIndicator.classList.remove('hidden');
        typingLiveText.textContent = `KEY em tempo real: ${mascararChave(val)} (${val.length} caracteres)`;
      } else {
        typingLiveIndicator.classList.add('hidden');
      }
    });
  }

  // Digitação em tempo real no Modal
  if (inputApiKey) {
    inputApiKey.addEventListener('input', (e) => {
      const val = e.target.value.trim();
      if (barApiKeyInput) barApiKeyInput.value = val;

      if (val.length > 0) {
        modalRealtimeKeyPreview.textContent = `Pré-visualização: ${mascararChave(val)} (${val.length} caracteres)`;
      } else {
        modalRealtimeKeyPreview.textContent = 'Digite a chave para pré-visualizar em tempo real...';
      }
    });
  }

  // Alternar visibilidade da senha (olho)
  function toggleVisibilidadeInput(inputEl, btnEl) {
    if (inputEl.type === 'password') {
      inputEl.type = 'text';
      btnEl.textContent = '🔒';
    } else {
      inputEl.type = 'password';
      btnEl.textContent = '👁️';
    }
  }

  if (btnToggleBarEye && barApiKeyInput) {
    btnToggleBarEye.addEventListener('click', () => {
      toggleVisibilidadeInput(barApiKeyInput, btnToggleBarEye);
    });
  }

  if (btnToggleModalEye && inputApiKey) {
    btnToggleModalEye.addEventListener('click', () => {
      toggleVisibilidadeInput(inputApiKey, btnToggleModalEye);
    });
  }

  // ENVIAR CHAVE - Processa o envio e ativação imediata
  async function enviarChave(chave) {
    const val = (chave || '').trim();

    if (val) {
      localStorage.setItem('gemini_api_key', val);
    } else {
      localStorage.removeItem('gemini_api_key');
    }

    // Sincroniza campos
    if (barApiKeyInput) barApiKeyInput.value = val;
    if (inputApiKey) inputApiKey.value = val;
    if (typingLiveIndicator) typingLiveIndicator.classList.add('hidden');

    atualizarStatusKeyInterface(val);

    try {
      const resp = await fetch('/api/configurar-chave/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_key: val })
      });
      const data = await resp.json();
      showToast(data.mensagem || (val ? 'CHAVE enviada com sucesso!' : 'Chave removida.'));
    } catch (err) {
      showToast(val ? 'CHAVE salva no navegador com sucesso!' : 'Chave limpa.');
    }
  }

  if (btnEnviarChave) {
    btnEnviarChave.addEventListener('click', () => {
      const val = barApiKeyInput ? barApiKeyInput.value : '';
      enviarChave(val);
    });
  }

  if (btnDemoKey) {
    btnDemoKey.addEventListener('click', () => {
      enviarChave(DEMO_API_KEY);
      showToast('Chave de Demonstração UniRV preenchida e ativada em tempo real!');
    });
  }

  if (btnModalDemoKey) {
    btnModalDemoKey.addEventListener('click', () => {
      enviarChave(DEMO_API_KEY);
      modalConfig.classList.add('hidden');
      showToast('Chave de Demonstração UniRV ativada em tempo real!');
    });
  }

  if (btnLimparChaveBar) {
    btnLimparChaveBar.addEventListener('click', () => {
      enviarChave('');
    });
  }

  if (btnSaveKey) {
    btnSaveKey.addEventListener('click', () => {
      const val = inputApiKey ? inputApiKey.value : '';
      enviarChave(val);
      modalConfig.classList.add('hidden');
    });
  }

  if (btnClearKey) {
    btnClearKey.addEventListener('click', () => {
      enviarChave('');
      modalConfig.classList.add('hidden');
    });
  }

  // =========================================================================
  // MODAL DE CONFIGURAÇÃO
  // =========================================================================
  if (btnToggleConfig) {
    btnToggleConfig.addEventListener('click', () => {
      modalConfig.classList.remove('hidden');
      const val = localStorage.getItem('gemini_api_key') || '';
      if (inputApiKey) {
        inputApiKey.value = val;
        if (val) {
          modalRealtimeKeyPreview.textContent = `Pré-visualização: ${mascararChave(val)} (${val.length} caracteres)`;
        } else {
          modalRealtimeKeyPreview.textContent = 'Digite a chave para pré-visualizar em tempo real...';
        }
      }
    });
  }

  if (btnCloseConfig) {
    btnCloseConfig.addEventListener('click', () => {
      modalConfig.classList.add('hidden');
    });
  }

  if (modalConfig) {
    modalConfig.addEventListener('click', (e) => {
      if (e.target === modalConfig) {
        modalConfig.classList.add('hidden');
      }
    });
  }

  // =========================================================================
  // MANIPULAÇÃO DE ARQUIVOS (PDF) E DROPZONE
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
      alert('Por favor, selecione um arquivo em formato PDF.');
      return;
    }

    currentFile = file;
    useSampleMode = false;
    const sizeInMB = (file.size / (1024 * 1024)).toFixed(2);

    fileNameDisplay.textContent = file.name;
    badgeFileName.textContent = file.name;
    badgeFileSize.textContent = `${sizeInMB} MB`;

    fileSelectedBadge.classList.remove('hidden');
    btnExtrair.removeAttribute('disabled');
  }

  if (btnUseSample) {
    btnUseSample.addEventListener('click', () => {
      useSampleMode = true;
      currentFile = null;
      if (fileInput) fileInput.value = '';

      const sampleName = 'danfe (ciclano - pecas).pdf';
      fileNameDisplay.textContent = sampleName;
      badgeFileName.textContent = sampleName;
      badgeFileSize.textContent = '0.01 MB';

      fileSelectedBadge.classList.remove('hidden');
      btnExtrair.removeAttribute('disabled');
      showToast('Nota fiscal de teste carregada!');
    });
  }

  if (btnRemoveFile) {
    btnRemoveFile.addEventListener('click', () => {
      currentFile = null;
      useSampleMode = false;
      if (fileInput) fileInput.value = '';
      fileNameDisplay.textContent = 'Nenhum arquivo escolhido';
      fileSelectedBadge.classList.add('hidden');
      btnExtrair.setAttribute('disabled', 'true');
      resultsSection.classList.add('hidden');
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
      const targetId = btn.getAttribute('data-target');
      const targetContent = document.getElementById(targetId);
      if (targetContent) targetContent.classList.add('active');
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
      loadingIndicator.classList.remove('hidden');
      resultsSection.classList.add('hidden');

      const formData = new FormData();
      if (useSampleMode) {
        formData.append('usar_exemplo', 'true');
      } else if (currentFile) {
        formData.append('pdf_file', currentFile);
      }

      // Envia a KEY ativa informada pelo usuário
      const activeKey = localStorage.getItem('gemini_api_key') || (barApiKeyInput ? barApiKeyInput.value.trim() : '');
      if (activeKey) {
        formData.append('api_key', activeKey);
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
        renderizarResultados(data);

        loadingIndicator.classList.add('hidden');
        resultsSection.classList.remove('hidden');
        btnExtrair.removeAttribute('disabled');

        resultsSection.scrollIntoView({ behavior: 'smooth' });

      } catch (err) {
        console.error(err);
        loadingIndicator.classList.add('hidden');
        btnExtrair.removeAttribute('disabled');
        alert(`Falha na extração de dados: ${err.message}`);
      }
    });
  }

  // =========================================================================
  // RENDERIZAÇÃO DOS RESULTADOS EXTRAÍDOS
  // =========================================================================
  function renderizarResultados(data) {
    // 1. Badge de modo de extração
    if (data._extracao_modo && modeText) {
      modeText.textContent = data._extracao_modo;
    }

    // JSON limpo (sem chaves de controle com _)
    const cleanJson = {};
    for (const key in data) {
      if (!key.startsWith('_')) {
        cleanJson[key] = data[key];
      }
    }

    // 2. Aba JSON
    if (jsonCodeDisplay) {
      jsonCodeDisplay.textContent = JSON.stringify(cleanJson, null, 2);
    }

    // 3. Aba Visualização Formatada
    // Fornecedor
    setText('disp-fornecedor-razao', data.fornecedor?.razaoSocial || data.fornecedor?.razao_social || 'Não identificado');
    setText('disp-fornecedor-fantasia', data.fornecedor?.fantasia || data.fornecedor?.nome_fantasia || 'Não informado');
    setText('disp-fornecedor-cnpj', data.fornecedor?.cnpj || 'Não informado');

    // Faturado
    setText('disp-faturado-nome', data.faturado?.nomeCompleto || data.faturado?.nome_completo || 'Não identificado');
    setText('disp-faturado-cpf', data.faturado?.cpf || 'Não informado');

    // Dados da NF
    setText('disp-nf-numero', data.numero || data.numero_nota_fiscal || '000.000');
    setText('disp-nf-serie', data.serie || '1');
    setText('disp-nf-emissao', formatarData(data.dataEmissao || data.data_emissao));
    setText('disp-nf-vencimento', formatarData(data.dataVencimento || data.data_vencimento));
    setText('disp-nf-parcelas', `${data.quantidadeParcelas || data.quantidade_parcelas || 1} parcela(s)`);

    // Valor Total
    const valor = Number(data.valorTotal || data.valor_total || 0);
    setText('disp-nf-total', formatarMoeda(valor));

    // Classificação da Despesa
    const categoria = data.classificacaoDespesa || data.classificacao_despesa || 'OUTRAS';
    setText('disp-classificacao-tag', categoria);

    const subcat = data.detalhesClassificacao?.subcategoria || 'Geral';
    setText('disp-subcategoria', subcat);

    const justificativa = data.justificativaClassificacao || data.detalhesClassificacao?.justificativa || 'Classificação semântica automática.';
    setText('disp-justificativa', justificativa);

    // Tabela de Produtos
    const tbody = document.getElementById('products-table-body');
    if (tbody) {
      tbody.innerHTML = '';
      const produtos = data.produtos || [];

      if (produtos.length === 0 && data.descricaoProdutos) {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${data.descricaoProdutos}</td>
          <td style="text-align: center;">1</td>
          <td style="text-align: right; font-family: var(--font-mono);">${formatarMoeda(valor)}</td>
        `;
        tbody.appendChild(row);
      } else {
        produtos.forEach(prod => {
          const row = document.createElement('tr');
          const valProd = Number(prod.valorTotal || prod.valor || 0);
          row.innerHTML = `
            <td><strong>${prod.descricao || prod.nome || 'Item sem descrição'}</strong></td>
            <td style="text-align: center; font-family: var(--font-mono);">${prod.quantidade || 1}</td>
            <td style="text-align: right; font-family: var(--font-mono); font-weight: 500;">${formatarMoeda(valProd)}</td>
          `;
          tbody.appendChild(row);
        });
      }
    }
  }

  function setText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
  }

  function formatarMoeda(valor) {
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  }

  function formatarData(dataStr) {
    if (!dataStr) return '-';
    if (dataStr.includes('/')) return dataStr;
    const partes = dataStr.split('-');
    if (partes.length === 3) {
      return `${partes[2]}/${partes[1]}/${partes[0]}`;
    }
    return dataStr;
  }

  // =========================================================================
  // COPIAR JSON
  // =========================================================================
  if (btnCopyJson) {
    btnCopyJson.addEventListener('click', async () => {
      const code = jsonCodeDisplay.textContent;
      try {
        await navigator.clipboard.writeText(code);
        copyBtnText.textContent = 'Copiado!';
        showToast('JSON copiado para a área de transferência!');
        setTimeout(() => {
          copyBtnText.textContent = 'Copiar JSON';
        }, 2500);
      } catch (err) {
        showToast('Falha ao copiar.');
      }
    });
  }

  // =========================================================================
  // TOAST NOTIFICATION
  // =========================================================================
  function showToast(mensagem) {
    if (!toast) return;
    toast.textContent = mensagem;
    toast.classList.remove('hidden');
    setTimeout(() => {
      toast.classList.add('hidden');
    }, 3200);
  }
});
