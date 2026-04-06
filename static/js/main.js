/* ============================================================
   Web Control — Main JS
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
  initSidebar();
  initAlerts();
  initNotifications();
  applyMasks();
  initDecimalSubmit();
});

// ── Sidebar mobile ────────────────────────────────────────────
function initSidebar() {
  const toggle  = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  if (!toggle || !sidebar) return;

  let overlay = document.querySelector('.sidebar-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);
  }
  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    overlay.classList.toggle('active');
  });
  overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
  });
}

// ── Auto-dismiss alerts ───────────────────────────────────────
function initAlerts() {
  document.querySelectorAll('.alert.fade.show').forEach(el => {
    setTimeout(() => bootstrap.Alert.getOrCreateInstance(el)?.close(), 5000);
  });
}

// ── Notificações dropdown ─────────────────────────────────────
function initNotifications() {
  const btn  = document.getElementById('notifBtn');
  const drop = document.getElementById('notifDropdown');
  if (!btn || !drop) return;

  btn.addEventListener('click', e => {
    e.stopPropagation();
    drop.classList.toggle('open');
  });
  document.addEventListener('click', e => {
    if (!drop.contains(e.target) && e.target !== btn) drop.classList.remove('open');
  });
}

// ── Converte vírgula → ponto antes de enviar formulários ──────
function initDecimalSubmit() {
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function () {
      this.querySelectorAll('[data-mask="decimal"], [data-mask="quantidade"]').forEach(el => {
        // Remove tudo exceto dígitos e vírgula/ponto, depois normaliza
        el.value = el.value.replace(/[^\d,]/g, '').replace(',', '.');
      });
    });
  });
}

// ============================================================
// LIVE SEARCH — filtragem de tabela no cliente
// ============================================================
function setupLiveSearch(inputId, tbodyId, formId, emptyMsgId, selectId) {
  const input    = document.getElementById(inputId);
  const tbody    = document.getElementById(tbodyId);
  const form     = document.getElementById(formId);
  const emptyMsg = document.getElementById(emptyMsgId);
  const sel      = document.getElementById(selectId);

  if (sel) sel.addEventListener('change', () => form && form.submit());
  if (!input || !tbody) return;

  let timer;
  input.addEventListener('input', function () {
    clearTimeout(timer);
    const term = this.value.trim().toLowerCase();

    let visible = 0;
    tbody.querySelectorAll('tr').forEach(row => {
      const match = row.textContent.toLowerCase().includes(term);
      row.style.display = match ? '' : 'none';
      if (match) visible++;
    });

    if (emptyMsg) emptyMsg.style.display = visible === 0 ? 'block' : 'none';

    timer = setTimeout(() => {
      if (form) {
        const url = new URL(window.location.href);
        url.searchParams.set('busca', this.value);
        window.history.replaceState({}, '', url);
      }
    }, 800);
  });
}

// ============================================================
// MÁSCARAS
// ============================================================

function applyMasks() {
  document.querySelectorAll('[data-mask]').forEach(el => {
    const fn = {
      cnpj:       maskCNPJ,
      telefone:   maskTelefone,
      cep:        maskCEP,
      ncm:        maskNCM,
      cest:       maskCEST,
      data:       maskData,
      decimal:    v => maskDecimal(v, 2),
      quantidade: v => maskDecimal(v, 3),
    }[el.dataset.mask];
    if (fn) setupMask(el, fn);
  });
}

// Preserva a posição do cursor contando dígitos antes dele
function setupMask(el, fn) {
  if (el.value) el.value = fn(el.value);

  el.addEventListener('input', function () {
    const raw    = this.value;
    const cursor = this.selectionStart;

    // Conta quantos "dígitos úteis" existiam antes do cursor
    const digitsBeforeCursor = raw.slice(0, cursor).replace(/[^\d]/g, '').length;

    this.value = fn(raw);

    // Reposiciona o cursor após o mesmo número de dígitos na string mascarada
    let count = 0;
    let newPos = this.value.length;
    for (let i = 0; i < this.value.length; i++) {
      if (/\d/.test(this.value[i])) count++;
      if (count === digitsBeforeCursor) { newPos = i + 1; break; }
    }
    try { this.setSelectionRange(newPos, newPos); } catch (_) {}
  });

  el.addEventListener('keydown', function (e) {
    if (e.key === 'Backspace') {
      const v = this.value;
      // Se o último char for separador, apaga ele também
      if (v.length && /[.\-/()\s]/.test(v[v.length - 1])) {
        this.value = v.slice(0, -1);
        e.preventDefault();
      }
    }
  });
}

// Exporta para uso nos templates inline
window.maskCNPJ     = maskCNPJ;
window.maskTelefone = maskTelefone;
window.maskCEP      = maskCEP;
window.maskDecimal  = maskDecimal;

function maskCNPJ(v) {
  v = v.replace(/\D/g, '').slice(0, 14);
  if (v.length <=  2) return v;
  if (v.length <=  5) return `${v.slice(0,2)}.${v.slice(2)}`;
  if (v.length <=  8) return `${v.slice(0,2)}.${v.slice(2,5)}.${v.slice(5)}`;
  if (v.length <= 12) return `${v.slice(0,2)}.${v.slice(2,5)}.${v.slice(5,8)}/${v.slice(8)}`;
  return `${v.slice(0,2)}.${v.slice(2,5)}.${v.slice(5,8)}/${v.slice(8,12)}-${v.slice(12)}`;
}

function maskTelefone(v) {
  v = v.replace(/\D/g, '').slice(0, 11);
  if (!v.length) return '';
  if (v.length <=  2) return `(${v}`;
  if (v.length <=  6) return `(${v.slice(0,2)}) ${v.slice(2)}`;
  if (v.length <= 10) return `(${v.slice(0,2)}) ${v.slice(2,6)}-${v.slice(6)}`;
  return `(${v.slice(0,2)}) ${v.slice(2,7)}-${v.slice(7)}`;
}

function maskCEP(v) {
  v = v.replace(/\D/g, '').slice(0, 8);
  if (v.length <= 5) return v;
  return `${v.slice(0,5)}-${v.slice(5)}`;
}

function maskNCM(v) {
  v = v.replace(/\D/g, '').slice(0, 8);
  if (v.length <= 4) return v;
  if (v.length <= 6) return `${v.slice(0,4)}.${v.slice(4)}`;
  return `${v.slice(0,4)}.${v.slice(4,6)}.${v.slice(6)}`;
}

function maskCEST(v) {
  v = v.replace(/\D/g, '').slice(0, 7);
  if (v.length <= 2) return v;
  if (v.length <= 5) return `${v.slice(0,2)}.${v.slice(2)}`;
  return `${v.slice(0,2)}.${v.slice(2,5)}.${v.slice(5)}`;
}

function maskData(v) {
  v = v.replace(/\D/g, '').slice(0, 8);
  if (v.length <= 2) return v;
  if (v.length <= 4) return `${v.slice(0,2)}/${v.slice(2)}`;
  return `${v.slice(0,2)}/${v.slice(2,4)}/${v.slice(4)}`;
}

// Máscara decimal: aceita dígitos e uma vírgula, limita casas decimais
function maskDecimal(v, casas) {
  // Mantém apenas dígitos e vírgula (ou ponto → converte para vírgula)
  v = v.replace(/[^\d,\.]/g, '').replace('.', ',');

  const partes = v.split(',');
  let inteiro   = partes[0] || '';
  let decimal   = partes.length > 1 ? partes.slice(1).join('').slice(0, casas) : null;

  if (decimal !== null) {
    return `${inteiro},${decimal}`;
  }
  return inteiro;
}
