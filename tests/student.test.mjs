import test from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';

// Surface a missing implementation as a normal assertion during the initial red run.
const student = await import('../static/js/student.js').catch((error) => {
  if (error.code === 'ERR_MODULE_NOT_FOUND') return {};
  throw error;
});

test('blank fields are rejected and an error identifies each missing field', () => {
  assert.equal(typeof student.validateReport, 'function', 'validation must exist');
  const result = student.validateReport({ title: '  ', location: '', category: '', description: '' });
  assert.deepEqual(Object.keys(result.errors).sort(), ['category', 'description', 'location', 'title']);
});

test('a valid report is trimmed without changing its meaning', () => {
  assert.equal(typeof student.validateReport, 'function');
  const result = student.validateReport({ title: ' Broken projector ', location: ' A101 ', category: ' Equipment ', description: ' Will not start. ' });
  assert.deepEqual(result.errors, {});
  assert.deepEqual(result.values, { title: 'Broken projector', location: 'A101', category: 'Equipment', description: 'Will not start.' });
});

test('keyword and location are both encoded in the search URL', () => {
  assert.equal(typeof student.buildReportUrl, 'function');
  const url = student.buildReportUrl('http://127.0.0.1/api/reports', { keyword: ' Wi-Fi & power ', location: ' A 101 ' });
  const parsed = new URL(url);
  assert.equal(parsed.searchParams.get('keyword'), 'Wi-Fi & power');
  assert.equal(parsed.searchParams.get('location'), 'A 101');
});

test('a successful submission sends exactly the four fields and returns the server ID', async (t) => {
  assert.equal(typeof student.createReport, 'function');
  const report = { title: 'Projector', location: 'A101', category: 'Equipment', description: 'No image' };
  let received;
  const server = http.createServer(async (req, res) => {
    let body = '';
    for await (const chunk of req) body += chunk;
    received = { path: req.url, method: req.method, body: JSON.parse(body) };
    res.writeHead(201, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ ...report, id: 42, status: 'Submitted' }));
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  t.after(() => server.close());
  const result = await student.createReport(`http://127.0.0.1:${server.address().port}/api/reports`, report);
  assert.deepEqual(received, { path: '/api/reports', method: 'POST', body: report });
  assert.equal(result.id, 42);
  assert.equal(result.status, 'Submitted');
});

test('an unsuccessful submission surfaces the server error', async (t) => {
  assert.equal(typeof student.createReport, 'function');
  const server = http.createServer((req, res) => {
    res.writeHead(400, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ error: 'Location is required.' }));
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  t.after(() => server.close());
  await assert.rejects(student.createReport(`http://127.0.0.1:${server.address().port}/api/reports`, { title: 'Test' }), /Location is required/);
});

// ---- Staff page (S6): the browser-side check mirrors the server rule ----
const staff = await import('../static/js/staff.js');

test('resolving without a note, or with only spaces, is blocked before sending', () => {
  assert.match(staff.validateStatusUpdate('Resolved', '').error, /處理備註/);
  assert.match(staff.validateStatusUpdate('Resolved', '   \n ').error, /處理備註/);
});

test('a valid status update sends the trimmed note only when resolving', () => {
  assert.deepEqual(staff.validateStatusUpdate('Resolved', ' Lamp replaced. ').body, { status: 'Resolved', resolution_note: 'Lamp replaced.' });
  assert.deepEqual(staff.validateStatusUpdate('In Progress', 'ignored').body, { status: 'In Progress' });
  assert.ok(staff.validateStatusUpdate('Closed', 'x').error);
});
