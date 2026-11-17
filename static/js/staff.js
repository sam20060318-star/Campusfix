// Staff management page. The server checks the staff role on every update;
// this script only presents the result.

const STATUSES = ['Submitted', 'In Progress', 'Resolved'];
// Stored status values stay in English (assignment wording); the page shows both.
const STATUS_LABELS = {
  Submitted: '已提交 Submitted',
  'In Progress': '處理中 In Progress',
  Resolved: '已解決 Resolved',
};

// Jira CF-9｜S6 填寫備註後結案
export function validateStatusUpdate(status, note) {
  if (!STATUSES.includes(status)) return { error: '請選擇有效的狀態。' };
  const trimmed = String(note ?? '').trim();
  if (status === 'Resolved' && !trimmed) return { error: '結案時必須填寫處理備註。' };
  return { body: status === 'Resolved' ? { status, resolution_note: trimmed } : { status } };
}

function setupStaffPage() {
  const apiBase = (document.body.dataset.apiBase || '/api/reports').replace(/\/$/, '');
  const $ = (selector) => document.querySelector(selector);
  const list = $('#report-list');
  const listState = $('#list-state');
  const resultsCount = $('#results-count');
  const filterForm = $('#filter-form');
  const statusForm = $('#status-form');
  const statusSelect = $('#status');
  const noteField = $('#note-field');
  const noteInput = $('#resolution_note');
  const noteError = $('#note-error');
  const saveButton = $('#save-button');
  const saveFeedback = $('#save-feedback');
  let currentFilters = {};
  // selectedId: the report whose details are shown and that "儲存狀態" will update.
  // activeId: the report the staff member clicked last (may still be loading).
  // selectSequence: only the response to the latest click may change the form.
  let selectedId = null;
  let activeId = null;
  let selectSequence = 0;
  let loadSequence = 0;

  function el(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined && text !== null) element.textContent = String(text);
    return element;
  }

  function statusBadge(status) {
    const normalized = String(status).toLowerCase().replace(/[^a-z]+/g, '-');
    return el('span', `status-badge status-${normalized}`, STATUS_LABELS[status] || status);
  }

  async function requestJson(url, options = {}) {
    let response;
    try {
      response = await fetch(url, { ...options, headers: { Accept: 'application/json', ...options.headers } });
    } catch {
      throw new Error('無法連線，請檢查網路後再試一次。');
    }
    const data = await response.json().catch(() => null);
    if (response.status === 401) {
      window.location.assign('/login');
      throw new Error('登入已失效，請重新登入。');
    }
    if (!response.ok) throw new Error(typeof data?.error === 'string' ? data.error : '發生錯誤，請再試一次。');
    return data;
  }

  function setListMessage(message, kind = '') {
    listState.textContent = message;
    listState.className = `list-state ${kind}`.trim();
    listState.hidden = !message;
  }

  function renderRow(report) {
    const item = el('li', 'report-item');
    const button = el('button', 'staff-row');
    button.type = 'button';
    button.dataset.reportId = report.id;
    if (report.id === activeId) button.setAttribute('aria-current', 'true');
    const main = el('span', 'report-main');
    const meta = el('span', 'report-meta');
    meta.append(el('span', 'report-id', `#${report.id}`), el('span', 'meta-dot', '•'), el('span', '', report.location));
    main.append(meta, el('span', 'report-title', report.title));
    button.append(main, statusBadge(report.status));
    button.addEventListener('click', () => selectReport(report.id));
    item.append(button);
    return item;
  }

  // Jira CF-7｜S4 Staff 查看報修
  async function loadReports(filters = currentFilters) {
    currentFilters = { ...filters };
    const sequence = ++loadSequence;
    list.setAttribute('aria-busy', 'true');
    const url = new URL(apiBase, window.location.href);
    for (const field of ['keyword', 'location']) {
      const value = String(filters[field] ?? '').trim();
      if (value) url.searchParams.set(field, value);
    }
    try {
      const reports = await requestJson(url);
      if (sequence !== loadSequence) return;
      resultsCount.textContent = `${reports.length} 筆報修`;
      list.replaceChildren(...reports.map(renderRow));
      setListMessage(reports.length ? '' : '找不到報修。', 'empty');
    } catch (error) {
      if (sequence !== loadSequence) return;
      resultsCount.textContent = '無法取得';
      list.replaceChildren();
      setListMessage(error.message, 'error');
    } finally {
      if (sequence === loadSequence) list.setAttribute('aria-busy', 'false');
    }
  }

  function toggleNote() {
    noteField.hidden = statusSelect.value !== 'Resolved';
    noteError.textContent = '';
    noteInput.removeAttribute('aria-invalid');
  }

  function showReport(report) {
    selectedId = report.id;
    $('#manage-hint').textContent = '檢視報修內容後，記錄處理進度。';
    $('#manage-id').textContent = `報修 #${report.id}`;
    $('#manage-status').replaceChildren(statusBadge(report.status));
    $('#manage-report-title').textContent = report.title;
    const fields = $('#manage-fields');
    fields.replaceChildren();
    const rows = [['地點', report.location], ['分類', report.category], ['問題描述', report.description]];
    if (report.resolution_note) rows.push(['處理備註', report.resolution_note]);
    for (const [label, value] of rows) {
      const wrap = el('div', 'detail-field');
      wrap.append(el('dt', '', label), el('dd', '', value));
      fields.append(wrap);
    }
    statusSelect.value = report.status;
    noteInput.value = report.resolution_note || '';
    toggleNote();
    $('#manage-content').hidden = false;
    highlightRow(report.id);
  }

  function highlightRow(id) {
    for (const row of list.querySelectorAll('.staff-row')) {
      if (Number(row.dataset.reportId) === id) row.setAttribute('aria-current', 'true');
      else row.removeAttribute('aria-current');
    }
  }

  // Jira CF-7｜S4 Staff 查看報修
  // Bug CM-59｜快速切換報修時只接受最後一次點選的回應
  async function selectReport(id) {
    const sequence = ++selectSequence;
    activeId = id;
    // Until the new report has loaded, nothing is selected, so the form cannot save to the previous report.
    selectedId = null;
    highlightRow(id);
    saveFeedback.hidden = true;
    $('#manage-content').hidden = true;
    $('#manage-hint').textContent = `正在載入報修 #${id}…`;
    try {
      const report = await requestJson(`${apiBase}/${encodeURIComponent(id)}`);
      if (sequence !== selectSequence) return; // a newer click won; ignore this late response
      showReport(report);
    } catch (error) {
      if (sequence !== selectSequence) return;
      $('#manage-hint').textContent = error.message;
    }
  }

  statusSelect.addEventListener('change', toggleNote);
  noteInput.addEventListener('input', () => { noteError.textContent = ''; noteInput.removeAttribute('aria-invalid'); });

  // Jira CF-8｜S5 更新報修狀態
  statusForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (selectedId === null) return;
    saveFeedback.hidden = true;
    const { body, error } = validateStatusUpdate(statusSelect.value, noteInput.value);
    if (error) {
      noteError.textContent = error;
      noteInput.setAttribute('aria-invalid', 'true');
      noteInput.focus();
      return;
    }
    const targetId = selectedId;
    const sequence = selectSequence;
    saveButton.disabled = true;
    try {
      const report = await requestJson(`${apiBase}/${encodeURIComponent(targetId)}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      // If staff opened another report while saving, keep showing that one.
      if (sequence === selectSequence) showReport(report);
      saveFeedback.className = 'form-feedback success';
      saveFeedback.textContent = `已儲存。報修 #${report.id} 目前狀態：${STATUS_LABELS[report.status] || report.status}。`;
      await loadReports();
    } catch (requestError) {
      saveFeedback.className = 'form-feedback error';
      saveFeedback.textContent = requestError.message;
    } finally {
      saveFeedback.hidden = false;
      saveButton.disabled = false;
    }
  });

  filterForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(filterForm);
    loadReports({ keyword: data.get('keyword'), location: data.get('location') });
  });
  $('#clear-filters').addEventListener('click', () => { filterForm.reset(); loadReports({}); });
  $('#retry-list').addEventListener('click', () => loadReports());
  $('#logout-button').addEventListener('click', async () => {
    await fetch('/api/logout', { method: 'POST' }).catch(() => {});
    window.location.assign('/login');
  });

  loadReports({});
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setupStaffPage);
  else setupStaffPage();
}
