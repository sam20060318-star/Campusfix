const form = document.querySelector('#login-form');
const feedback = document.querySelector('#login-feedback');
const button = document.querySelector('#login-button');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  feedback.hidden = true;
  const data = new FormData(form);
  const username = String(data.get('username') ?? '').trim();
  const password = String(data.get('password') ?? '');
  if (!username || !password) {
    feedback.textContent = '請輸入帳號和密碼。';
    feedback.hidden = false;
    return;
  }
  button.disabled = true;
  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const result = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(result.error || '登入失敗，請再試一次。');
    if (result.role === 'staff') window.location.assign('/staff');
    else throw new Error(`已用 ${result.username} 登入，但這不是 Staff 帳號，不能管理報修。`);
  } catch (error) {
    feedback.textContent = error instanceof TypeError ? '無法連線，請再試一次。' : error.message;
    feedback.hidden = false;
  } finally {
    button.disabled = false;
  }
});
