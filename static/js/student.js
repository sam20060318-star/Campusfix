const REQUIRED_FIELDS = ['title', 'location', 'category', 'description'];
const FIELD_LABELS = {
  title: '標題',
  location: '地點',
  category: '分類',
  description: '問題描述',
};
// Stored status values stay in English (assignment wording); the page shows both.
export const STATUS_LABELS = {
  Submitted: '已提交 Submitted',
  'In Progress': '處理中 In Progress',
  Resolved: '已解決 Resolved',
};

export function validateReport(input) {
  const values = {};
  const errors = {};
  for (const field of REQUIRED_FIELDS) {
    values[field] = String(input[field] ?? '').trim();
    if (!values[field]) errors[field] = `請輸入${FIELD_LABELS[field]}。`;
  }
  return { values, errors };
}

export function buildReportUrl(base, filters = {}) {
  const origin = typeof window === 'undefined' ? 'http://localhost/' : window.location.href;
  const url = new URL(base, origin);
  for (const field of ['keyword', 'location']) {
    const value = String(filters[field] ?? '').trim();
    if (value) url.searchParams.set(field, value);
    else url.searchParams.delete(field);
  }
  return url.toString();
}

async function requestJson(url, options = {}) {
  let response;
  try {
    response = await fetch(url, { headers: { Accept: 'application/json', ...options.headers }, ...options });
  } catch (error) {
    if (error.name === 'AbortError') throw error;
    throw new Error('無法連線，請檢查網路後再試一次。');
  }
  const text = await response.text();
  let data = null;
  if (text) {
    try { data = JSON.parse(text); } catch { /* Handle invalid JSON below. */ }
  }
  if (!response.ok) {
    const message = typeof data?.error === 'string' ? data.error : typeof data?.message === 'string' ? data.message : '發生錯誤，請再試一次。';
    throw new Error(message);
  }
  if (data === null) throw new Error('伺服器回應異常，請先查看報修列表再重試。');
  return data;
}

export async function createReport(base, report) {
  return requestJson(base, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify(report),
  });
}

function setupStudentPage() {
  const body = document.body;
  const apiBase = (body.dataset.apiBase || '/api/reports').replace(/\/$/, '');
  const form = document.querySelector('#report-form');
  const filterForm = document.querySelector('#filter-form');
  const list = document.querySelector('#report-list');
  const listState = document.querySelector('#list-state');
  const resultsCount = document.querySelector('#results-count');
  const submitButton = document.querySelector('#submit-button');
  const submitFeedback = document.querySelector('#submit-feedback');
  const dialog = document.querySelector('#detail-dialog');
  const detailContent = document.querySelector('#detail-content');
  const detailState = document.querySelector('#detail-state');
  const clearFiltersButton = document.querySelector('#clear-filters');
  let loadSequence = 0;
  let currentFilters = {};

  if (body.dataset.preview === 'true') document.querySelector('#preview-banner').hidden = false;

  // Suggest locations that are already stored so filters use the same saved values.
  async function loadLocations() {
    const datalist = document.querySelector('#known-locations');
    if (!datalist || !body.dataset.locationsUrl) return;
    try {
      const locations = await requestJson(body.dataset.locationsUrl);
      if (!Array.isArray(locations)) return;
      datalist.replaceChildren(...locations.map((value) => {
        const option = document.createElement('option');
        option.value = String(value);
        return option;
      }));
    } catch { /* Suggestions are optional; the page works without them. */ }
  }

  function makeElement(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined && text !== null) element.textContent = String(text);
    return element;
  }

  function statusElement(value) {
    const status = typeof value === 'string' && value.trim() ? value : '狀態未知';
    const normalized = status.toLowerCase().replace(/[^a-z]+/g, '-');
    return makeElement('span', `status-badge status-${normalized}`, STATUS_LABELS[status] || status);
  }

  function clearFieldErrors() {
    for (const field of REQUIRED_FIELDS) {
      form.elements[field].removeAttribute('aria-invalid');
      document.querySelector(`#${field}-error`).textContent = '';
    }
  }

  function displayFieldErrors(errors) {
    clearFieldErrors();
    for (const [field, message] of Object.entries(errors)) {
      form.elements[field].setAttribute('aria-invalid', 'true');
      document.querySelector(`#${field}-error`).textContent = message;
    }
    const firstInvalid = REQUIRED_FIELDS.find((field) => errors[field]);
    if (firstInvalid) form.elements[firstInvalid].focus();
  }

  function setListMessage(message, kind = '') {
    listState.textContent = message;
    listState.className = `list-state ${kind}`.trim();
    listState.hidden = !message;
  }

  function renderReport(report) {
    const item = makeElement('li', 'report-item');
    const left = makeElement('div', 'report-main');
    const meta = makeElement('div', 'report-meta');
    meta.append(makeElement('span', 'report-id', report.id == null ? '報修' : `#${report.id}`));
    if (report.category) meta.append(makeElement('span', 'meta-dot', '•'), makeElement('span', '', report.category));
    const title = makeElement('h3', 'report-title', report.title || '未命名報修');
    const description = makeElement('p', 'report-description', report.description || '未提供描述。');
    const location = makeElement('p', 'report-location');
    location.append(makeElement('span', 'location-icon', '⌖'), makeElement('span', '', report.location || '未提供地點'));
    left.append(meta, title, description, location);

    const right = makeElement('div', 'report-actions');
    right.append(statusElement(report.status));
    const view = makeElement('button', 'view-button', '查看詳情');
    view.type = 'button';
    view.setAttribute('aria-label', `查看「${report.title || '報修'}」的詳情`);
    if (report.id == null || report.id === '') {
      view.disabled = true;
      view.title = '這筆報修沒有編號。';
    } else {
      view.addEventListener('click', () => showDetails(report.id));
    }
    right.append(view);
    item.append(left, right);
    return item;
  }

  async function loadReports(filters = {}) {
    currentFilters = { ...filters };
    const sequence = ++loadSequence;
    list.setAttribute('aria-busy', 'true');
    resultsCount.textContent = '載入中…';
    setListMessage('正在載入報修…');
    list.replaceChildren();
    try {
      const data = await requestJson(buildReportUrl(apiBase, filters));
      if (sequence !== loadSequence) return;
      const reports = Array.isArray(data) ? data : data?.reports;
      if (!Array.isArray(reports)) throw new Error('無法顯示報修，請再試一次。');
      const safeReports = reports.filter((report) => report && typeof report === 'object');
      resultsCount.textContent = `${safeReports.length} 筆報修`;
      const filtered = Boolean(String(filters.keyword ?? '').trim() || String(filters.location ?? '').trim());
      if (!safeReports.length) setListMessage(filtered ? '找不到符合的報修。請換個關鍵字或地點，或清除條件。' : '目前還沒有報修，成為第一個回報問題的人吧。', 'empty');
      else {
        setListMessage('');
        list.replaceChildren(...safeReports.map(renderReport));
      }
    } catch (error) {
      if (sequence !== loadSequence) return;
      resultsCount.textContent = '無法取得';
      setListMessage(error.message || '無法載入報修，請再試一次。', 'error');
    } finally {
      if (sequence === loadSequence) list.setAttribute('aria-busy', 'false');
    }
  }

  function detailField(container, label, value) {
    const wrap = makeElement('div', 'detail-field');
    wrap.append(makeElement('dt', '', label), makeElement('dd', '', value == null || value === '' ? '未提供' : value));
    container.append(wrap);
  }

  async function showDetails(id) {
    detailContent.replaceChildren();
    detailState.textContent = '正在載入報修…';
    if (typeof dialog.showModal === 'function') dialog.showModal();
    else dialog.setAttribute('open', '');
    try {
      const data = await requestJson(`${apiBase}/${encodeURIComponent(id)}`);
      if (!dialog.open) return;
      const report = data?.report || data;
      if (!report || typeof report !== 'object' || Array.isArray(report)) throw new Error('無法取得報修詳情。');
      detailState.textContent = '';
      const top = makeElement('div', 'detail-top');
      top.append(makeElement('span', 'detail-id', report.id == null ? '報修' : `報修 #${report.id}`), statusElement(report.status));
      const heading = makeElement('h3', 'detail-title', report.title || '未命名報修');
      const details = makeElement('dl', 'detail-grid');
      detailField(details, '地點', report.location);
      detailField(details, '分類', report.category);
      detailField(details, '問題描述', report.description);
      if (report.resolution_note) detailField(details, '處理備註', report.resolution_note);
      detailContent.append(top, heading, details);
    } catch (error) {
      if (dialog.open) detailState.textContent = error.message || '無法取得報修詳情。';
    }
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    submitFeedback.hidden = true;
    submitFeedback.textContent = '';
    const input = Object.fromEntries(new FormData(form).entries());
    const { values, errors } = validateReport(input);
    displayFieldErrors(errors);
    if (Object.keys(errors).length) return;
    submitButton.disabled = true;
    submitButton.textContent = '送出中…';
    try {
      const data = await createReport(apiBase, values);
      const report = data?.report || data;
      form.reset();
      clearFieldErrors();
      submitFeedback.className = 'form-feedback success';
      const reference = report?.id == null ? '' : `報修編號 #${report.id}。`;
      const status = typeof report?.status === 'string' && report.status ? `狀態：${STATUS_LABELS[report.status] || report.status}。` : '';
      submitFeedback.textContent = `報修已送出。${reference}${status}`;
      submitFeedback.hidden = false;
      // New reports should be visible even if a previous search was active.
      filterForm.reset();
      loadLocations();
      await loadReports({});
    } catch (error) {
      submitFeedback.className = 'form-feedback error';
      submitFeedback.textContent = error.message || '報修無法送出，請再試一次。';
      submitFeedback.hidden = false;
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = '送出報修';
    }
  });

  for (const field of REQUIRED_FIELDS) {
    form.elements[field].addEventListener('input', () => {
      form.elements[field].removeAttribute('aria-invalid');
      document.querySelector(`#${field}-error`).textContent = '';
    });
  }

  filterForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(filterForm);
    loadReports({ keyword: data.get('keyword'), location: data.get('location') });
  });
  clearFiltersButton.addEventListener('click', () => { filterForm.reset(); loadReports({}); });
  document.querySelector('#retry-list').addEventListener('click', () => loadReports(currentFilters));
  document.querySelector('#close-dialog').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });
  loadLocations();
  loadReports();
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setupStudentPage);
  else setupStudentPage();
}
