// Regression test for the staff page "late response" bug (optional, needs Playwright).
//
// Bug: staff clicks #1, then #2. If #1's details arrive later, the page switched back to #1
// and "儲存狀態" updated #1 instead of #2.
//
// Setup once:   npm install --no-save playwright
//               npx playwright install chromium
// Run:          node tests/e2e_staff_race.cjs
// It starts its own server on a temporary database, so your real data is not touched.

const { chromium } = require('playwright');
const { spawn } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const assert = require('node:assert/strict');

const PORT = 5099;
const BASE = `http://127.0.0.1:${PORT}`;
const ROOT = path.resolve(__dirname, '..');
const PYTHON = process.env.PYTHON || 'python';

async function waitForServer() {
  for (let i = 0; i < 100; i += 1) {
    try { if ((await fetch(`${BASE}/api/reports`)).ok) return; } catch { /* not up yet */ }
    await new Promise((r) => setTimeout(r, 100));
  }
  throw new Error('server did not start');
}

(async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'campusfix-'));
  const server = spawn(PYTHON, [path.join(ROOT, 'app.py'), '--port', String(PORT), '--seed-demo'],
    { env: { ...process.env, CAMPUSFIX_DB: path.join(dir, 'test.db') }, stdio: 'ignore' });
  const browser = await chromium.launch();
  let failed = false;
  try {
    await waitForServer();
    const page = await (await browser.newContext()).newPage();
    await page.goto(`${BASE}/login`);
    await page.fill('#username', 'staff');
    await page.fill('#password', 'staff123');
    await page.click('#login-button');
    await page.waitForURL('**/staff');
    await page.waitForSelector('.staff-row');

    // Make the details of #1 arrive 1.5 seconds late.
    await page.route('**/api/reports/1', async (route) => {
      if (route.request().method() === 'GET') await new Promise((r) => setTimeout(r, 1500));
      route.continue();
    });
    await page.click('.staff-row[data-report-id="1"]');
    await page.click('.staff-row[data-report-id="2"]');
    await page.waitForTimeout(2000); // let the late #1 response arrive

    assert.equal(await page.textContent('#manage-id'), '報修 #2', 'the last clicked report (#2) must stay shown');
    await page.selectOption('#status', 'In Progress');
    await page.click('#save-button');
    await page.waitForSelector('#save-feedback.success');

    const statusOf = async (id) => (await (await fetch(`${BASE}/api/reports/${id}`)).json()).status;
    assert.equal(await statusOf(2), 'In Progress', '#2 must be updated');
    assert.equal(await statusOf(1), 'Submitted', '#1 must not change');
    console.log('PASS  staff page keeps the last clicked report and saves to it');
  } catch (error) {
    failed = true;
    console.error('FAIL ', error.message);
  } finally {
    await browser.close();
    server.kill();
  }
  process.exit(failed ? 1 : 0);
})();
