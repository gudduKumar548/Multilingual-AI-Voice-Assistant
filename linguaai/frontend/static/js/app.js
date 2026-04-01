function showPage(name) {
  document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
  document.getElementById('page-' + name).classList.remove('hidden');
}

function initApp() {
  const token    = localStorage.getItem('lingua_token');
  const username = localStorage.getItem('lingua_user');

  if (token && username) {
    document.getElementById('nav-username').textContent = username;
    document.getElementById('nav-actions').classList.add('hidden');
    document.getElementById('nav-user-bar').classList.remove('hidden');
    showPage('assistant');
    checkBackendStatus();
  } else {
    showPage('register');
  }
}

document.addEventListener('DOMContentLoaded', initApp);
