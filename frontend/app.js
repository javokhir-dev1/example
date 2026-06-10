const API = 'http://localhost:5000/api/auth';

// ---- DOM elementlar ----
const authContainer = document.getElementById('authContainer');
const profileContainer = document.getElementById('profileContainer');

const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const formTitle = document.getElementById('formTitle');
const formSubtitle = document.getElementById('formSubtitle');

const toggleLink = document.getElementById('toggleLink');
const toggleText = document.getElementById('toggleText');
const messageBox = document.getElementById('message');

const logoutBtn = document.getElementById('logoutBtn');

// ---- State ----
let isLoginView = true;

// ---- Helpers ----

function showMessage(text, type) {
  messageBox.textContent = text;
  messageBox.className = `message ${type}`;
}

function clearMessage() {
  messageBox.textContent = '';
  messageBox.className = 'message hidden';
}

function saveTokens(tokens) {
  localStorage.setItem('accessToken', tokens.accessToken);
  localStorage.setItem('refreshToken', tokens.refreshToken);
}

function getAccessToken() {
  return localStorage.getItem('accessToken');
}

function getRefreshToken() {
  return localStorage.getItem('refreshToken');
}

function clearTokens() {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('uz-UZ', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

async function request(url, options = {}) {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  return res.json();
}

// ---- View toggling ----

function showAuth() {
  authContainer.classList.remove('hidden');
  profileContainer.classList.add('hidden');
}

function showProfile() {
  authContainer.classList.add('hidden');
  profileContainer.classList.remove('hidden');
}

toggleLink.addEventListener('click', (e) => {
  e.preventDefault();
  clearMessage();
  isLoginView = !isLoginView;

  if (isLoginView) {
    loginForm.classList.remove('hidden');
    registerForm.classList.add('hidden');
    formTitle.textContent = 'Kirish';
    formSubtitle.textContent = "Tizimga kirish uchun ma'lumotlaringizni kiriting";
    toggleText.textContent = "Akkauntingiz yo'qmi?";
    toggleLink.textContent = "Ro'yxatdan o'ting";
  } else {
    loginForm.classList.add('hidden');
    registerForm.classList.remove('hidden');
    formTitle.textContent = "Ro'yxatdan o'tish";
    formSubtitle.textContent = 'Yangi akkount yarating';
    toggleText.textContent = 'Akkauntingiz bormi?';
    toggleLink.textContent = 'Kiring';
  }
});

// ---- Login ----

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearMessage();

  const email = document.getElementById('loginEmail').value.trim();
  const password = document.getElementById('loginPassword').value;
  const btn = document.getElementById('loginBtn');

  btn.disabled = true;
  btn.textContent = 'Kutilmoqda...';

  try {
    const data = await request(`${API}/login`, {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });

    if (data.success) {
      saveTokens(data.data.tokens);
      loginForm.reset();
      await loadProfile();
    } else {
      const msg = data.errors ? data.errors.join(', ') : data.message;
      showMessage(msg, 'error');
    }
  } catch {
    showMessage('Serverga ulanib bo\'lmadi', 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Kirish';
  }
});

// ---- Register ----

registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearMessage();

  const username = document.getElementById('regUsername').value.trim();
  const email = document.getElementById('regEmail').value.trim();
  const password = document.getElementById('regPassword').value;
  const btn = document.getElementById('regBtn');

  btn.disabled = true;
  btn.textContent = 'Kutilmoqda...';

  try {
    const data = await request(`${API}/register`, {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    });

    if (data.success) {
      saveTokens(data.data.tokens);
      registerForm.reset();
      await loadProfile();
    } else {
      const msg = data.errors ? data.errors.join(', ') : data.message;
      showMessage(msg, 'error');
    }
  } catch {
    showMessage('Serverga ulanib bo\'lmadi', 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = "Ro'yxatdan o'tish";
  }
});

// ---- Profile ----

async function loadProfile() {
  const token = getAccessToken();
  if (!token) {
    showAuth();
    return;
  }

  try {
    let data = await request(`${API}/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    // Agar token expired bo'lsa — refresh qilamiz
    if (!data.success && data.message && data.message.includes('tugagan')) {
      const refreshed = await tryRefresh();
      if (!refreshed) {
        showAuth();
        return;
      }
      data = await request(`${API}/me`, {
        headers: { Authorization: `Bearer ${getAccessToken()}` },
      });
    }

    if (data.success) {
      const user = data.data.user;
      document.getElementById('profileId').textContent = user.id;
      document.getElementById('profileUsername').textContent = user.username;
      document.getElementById('profileEmail').textContent = user.email;
      document.getElementById('profileDate').textContent = formatDate(user.created_at);
      showProfile();
    } else {
      clearTokens();
      showAuth();
    }
  } catch {
    clearTokens();
    showAuth();
  }
}

async function tryRefresh() {
  const refreshToken = getRefreshToken();
  if (!refreshToken) return false;

  try {
    const data = await request(`${API}/refresh`, {
      method: 'POST',
      body: JSON.stringify({ refreshToken }),
    });

    if (data.success) {
      saveTokens(data.data.tokens);
      return true;
    }
  } catch {
    // ignore
  }

  clearTokens();
  return false;
}

// ---- Logout ----

logoutBtn.addEventListener('click', async () => {
  const refreshToken = getRefreshToken();

  try {
    await request(`${API}/logout`, {
      method: 'POST',
      body: JSON.stringify({ refreshToken }),
    });
  } catch {
    // ignore
  }

  clearTokens();
  showAuth();
});

// ---- Init ----
// Sahifa ochilganda token bor-yo'qligini tekshiramiz
loadProfile();
