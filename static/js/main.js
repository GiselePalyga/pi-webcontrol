/* ============================================================
   Web Control — Main JS
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
  initSidebar();
  initAlerts();
  initNotifications();
  applyMasks();
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

// ============================================================
// LIVE SEARCH — filtragem de tabela no cliente
// ============================================================

/**
 * @param {string} inputId     — id do input de busca
 * @param {string} tbodyId     — id do tbody da tabela
 * @param {string} formId      — id do form de filtros
 * @param {string} emptyMsgId  — id do div de "sem resultados"
 * @param {string} selectId    — id do select de status (auto-submit on change)
 */
function setupLiveSearch(inputId, tbodyId, formId, emptyMsgId, selectId) {
  const input    = document.getElementById(inputId);
  const tbody    = document.getElementById(tbodyId);
  const form     = document.getElementById(formId);
  const emptyMsg = document.getElementById(emptyMsgId);
  const sel      = document.getElementById(selectId);

  // Auto-submit no select
  if (sel) sel.addEventListener('change', () => form && form.submit());

  if (!input || !tbody) return;

  // Debounce: se form existir → auto-submit; senão → filtra localmente
  let timer;
  input.addEventListener('input', function () {
    clearTimeout(timer);
    const term = this.value.trim().toLowerCase();

    // Filtragem local imediata (sem re-request)
    let visible = 0;
    tbody.querySelectorAll('tr').forEach(row => {
      const match = row.textContent.toLowerCase().includes(term);
      row.style.display = match ? '' : 'none';
      if (match) visible++;
    });

    if (emptyMsg) emptyMsg.style.display = visible === 0 ? 'block' : 'none';

    // Após 800ms sem digitar, sincroniza com servidor (para filtros combinados)
    timer = setTimeout(() => {
      if (form && term !== (new URLSearchParams(window.location.search).get(inputId === 'search-input' ? 'busca' : 'busca') || '')) {
        const url = new URL(window.location.href);
        url.searchParams.set('busca', this.value);
        // Mantém outros filtros
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
    const fn = { cnpj: maskCNPJ, telefone: maskTelefone, cep: maskCEP, ncm: maskNCM, cest: maskCEST, data: maskData }[el.dataset.mask];
    if (fn) setupMask(el, fn);
  });
}

function setupMask(el, fn) {
  if (el.value) el.value = fn(el.value);

  el.addEventListener('input', function () {
    const pos = this.selectionStart;
    this.value = fn(this.value);
    try { this.setSelectionRange(pos, pos); } catch (_) {}
  });

  el.addEventListener('keydown', function (e) {
    if (e.key === 'Backspace') {
      const v = this.value;
      if (v.length && /\W/.test(v[v.length - 1])) {
        this.value = v.slice(0, -1);
        e.preventDefault();
      }
    }
  });
}

// Exporta para uso nos templates inline
window.maskCNPJ = maskCNPJ;
window.maskTelefone = maskTelefone;
window.maskCEP = maskCEP;

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
