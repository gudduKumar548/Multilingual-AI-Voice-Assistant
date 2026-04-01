function showAlert(id, msg, type = 'error') {
  const el = document.getElementById(id);
  el.className = `alert alert-${type}`;
  el.textContent = msg;
  el.classList.remove('hidden');
}

function hideAlert(id) {
  document.getElementById(id).classList.add('hidden');
}

async function doRegister() {
  hideAlert('register-alert');
  const username = document.getElementById('reg-username').value.trim();
  const email    = document.getElementById('reg-email').value.trim();
  const password = document.getElementById('reg-password').value;

  if (!username || !email || !password) {
    return showAlert('register-alert', 'Please fill all fields.');
  }

  try {
    const { ok, data } = await API.register(username, email, password);
    if (!ok) return showAlert('register-alert', data.detail || 'Registration failed.');
    loginSuccess(data.access_token, data.username);
  } catch {
    showAlert('register-alert', 'Cannot connect to backend. Is it running on port 8000?');
  }
}

async function doLogin() {
  hideAlert('login-alert');
  const username = document.getElementById('login-username').value.trim();
  const password = document.getElementById('login-password').value;

  if (!username || !password) {
    return showAlert('login-alert', 'Please fill all fields.');
  }

  try {
    const { ok, data } = await API.login(username, password);
    if (!ok) return showAlert('login-alert', data.detail || 'Login failed.');
    loginSuccess(data.access_token, data.username);
  } catch {
    showAlert('login-alert', 'Cannot connect to backend. Is it running on port 8000?');
  }
}

function loginSuccess(token, username) {
  localStorage.setItem('lingua_token', token);
  localStorage.setItem('lingua_user', username);
  document.getElementById('nav-username').textContent = username;
  document.getElementById('nav-actions').classList.add('hidden');
  document.getElementById('nav-user-bar').classList.remove('hidden');
  showPage('assistant');
  checkBackendStatus();
}

function logout() {
  localStorage.removeItem('lingua_token');
  localStorage.removeItem('lingua_user');
  document.getElementById('nav-actions').classList.remove('hidden');
  document.getElementById('nav-user-bar').classList.add('hidden');
  window.conversationHistory = [];
  showPage('register');
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('reg-password')?.addEventListener('keydown', e => { if (e.key === 'Enter') doRegister(); });
  document.getElementById('login-password')?.addEventListener('keydown', e => { if (e.key === 'Enter') doLogin(); });
});
