/**
 * validators.js - Funções globais de validação e formatação automática de campos
 * Sistema de Controle Financeiro Rural - UniRV
 */

const RuralValidators = {
  // Limpa caracteres deixando apenas dígitos numéricos
  somenteDigitos(str) {
    if (!str) return '';
    return str.toString().replace(/\D/g, '');
  },

  // Validação oficial do CPF (Dígitos verificadores + sequências inválidas)
  validarCpf(cpf) {
    const limpo = this.somenteDigitos(cpf);
    if (limpo.length !== 11) return false;
    
    // Elimina sequências iguais conhecidas (ex: 00000000000, 11111111111)
    if (/^(\d)\1{10}$/.test(limpo)) return false;

    // Primeiro dígito verificador
    let soma = 0;
    for (let i = 0; i < 9; i++) {
      soma += parseInt(limpo.charAt(i), 10) * (10 - i);
    }
    let resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(limpo.charAt(9), 10)) return false;

    // Segundo dígito verificador
    soma = 0;
    for (let i = 0; i < 10; i++) {
      soma += parseInt(limpo.charAt(i), 10) * (11 - i);
    }
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(limpo.charAt(10), 10)) return false;

    return true;
  },

  // Validação oficial do CNPJ (Dígitos verificadores + sequências inválidas)
  validarCnpj(cnpj) {
    const limpo = this.somenteDigitos(cnpj);
    if (limpo.length !== 14) return false;
    
    // Elimina sequências conhecidas
    if (/^(\d)\1{13}$/.test(limpo)) return false;

    // Primeiro dígito
    let tamanho = limpo.length - 2;
    let numeros = limpo.substring(0, tamanho);
    const digitos = limpo.substring(tamanho);
    let soma = 0;
    let pos = tamanho - 7;
    for (let i = tamanho; i >= 1; i--) {
      soma += parseInt(numeros.charAt(tamanho - i), 10) * pos--;
      if (pos < 2) pos = 9;
    }
    let resultado = soma % 11 < 2 ? 0 : 11 - (soma % 11);
    if (resultado !== parseInt(digitos.charAt(0), 10)) return false;

    // Segundo dígito
    tamanho = tamanho + 1;
    numeros = limpo.substring(0, tamanho);
    soma = 0;
    pos = tamanho - 7;
    for (let i = tamanho; i >= 1; i--) {
      soma += parseInt(numeros.charAt(tamanho - i), 10) * pos--;
      if (pos < 2) pos = 9;
    }
    resultado = soma % 11 < 2 ? 0 : 11 - (soma % 11);
    if (resultado !== parseInt(digitos.charAt(1), 10)) return false;

    return true;
  },

  // Formata automaticamente CPF (000.000.000-00) ou CNPJ (00.000.000/0000-00)
  formatarCpfCnpj(valor) {
    const digitos = this.somenteDigitos(valor).substring(0, 14);
    if (digitos.length <= 11) {
      // Formato CPF
      return digitos
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    } else {
      // Formato CNPJ
      return digitos
        .replace(/^(\d{2})(\d)/, '$1.$2')
        .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
        .replace(/\.(\d{3})(\d)/, '.$1/$2')
        .replace(/(\d{4})(\d{1,2})$/, '$1-$2');
    }
  },

  // Formata automaticamente Telefone: (00) 0000-0000 ou (00) 00000-0000
  formatarTelefone(valor) {
    const digitos = this.somenteDigitos(valor).substring(0, 11);
    if (digitos.length <= 10) {
      // Fixo ou 8 dígitos
      return digitos
        .replace(/^(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{4})(\d{1,4})$/, '$1-$2');
    } else {
      // Celular com 9 dígitos
      return digitos
        .replace(/^(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{5})(\d{1,4})$/, '$1-$2');
    }
  },

  // Valida e-mail com regex padrão
  validarEmail(email) {
    if (!email) return true; // campo opcional
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  },

  // Aplica máscara contínua em campo CPF/CNPJ com feedback de validação em tempo real
  aplicarMascaraCpfCnpj(inputEl, feedbackEl = null) {
    if (!inputEl) return;
    inputEl.setAttribute('maxLength', '18');
    inputEl.setAttribute('autocomplete', 'off');

    const atualizar = () => {
      const pos = inputEl.selectionStart;
      const originalLen = inputEl.value.length;
      inputEl.value = this.formatarCpfCnpj(inputEl.value);

      const digitos = this.somenteDigitos(inputEl.value);
      if (feedbackEl) {
        feedbackEl.innerHTML = '';
        inputEl.classList.remove('input-error', 'input-success');

        if (digitos.length === 11) {
          if (this.validarCpf(digitos)) {
            inputEl.classList.add('input-success');
            feedbackEl.innerHTML = '<span class="text-success">✓ CPF válido</span>';
          } else {
            inputEl.classList.add('input-error');
            feedbackEl.innerHTML = '<span class="text-danger">⚠ CPF inválido (dígitos verificadores incorretos)</span>';
          }
        } else if (digitos.length === 14) {
          if (this.validarCnpj(digitos)) {
            inputEl.classList.add('input-success');
            feedbackEl.innerHTML = '<span class="text-success">✓ CNPJ válido</span>';
          } else {
            inputEl.classList.add('input-error');
            feedbackEl.innerHTML = '<span class="text-danger">⚠ CNPJ inválido (dígitos verificadores incorretos)</span>';
          }
        } else if (digitos.length > 0 && digitos.length < 11) {
          feedbackEl.innerHTML = `<span class="text-muted">Digitando CPF (${digitos.length}/11)...</span>`;
        } else if (digitos.length > 11 && digitos.length < 14) {
          feedbackEl.innerHTML = `<span class="text-muted">Digitando CNPJ (${digitos.length}/14)...</span>`;
        }
      }
    };

    inputEl.addEventListener('input', atualizar);
    inputEl.addEventListener('blur', atualizar);
    if (inputEl.value) atualizar();
  },

  // Aplica máscara contínua em campo Telefone
  aplicarMascaraTelefone(inputEl) {
    if (!inputEl) return;
    inputEl.setAttribute('maxLength', '15');
    inputEl.setAttribute('type', 'tel');

    inputEl.addEventListener('input', () => {
      inputEl.value = this.formatarTelefone(inputEl.value);
    });
  }
};

window.RuralValidators = RuralValidators;
