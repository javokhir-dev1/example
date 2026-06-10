// ---- Data ----
const users = [];
let currentUser = null;

// ---- DOM ----
const authContainer = document.getElementById('authContainer');
const dashboardContainer = document.getElementById('dashboardContainer');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const formTitle = document.getElementById('formTitle');
const formSubtitle = document.getElementById('formSubtitle');
const switchLink = document.getElementById('switchLink');
const switchText = document.getElementById('switchText');
const messageBox = document.getElementById('message');
const logoutBtn = document.getElementById('logoutBtn');

let isLogin = true;

// ---- Helpers ----

function genId() {
  return 'U-' + Math.random().toString(36).substring(2, 7).toUpperCase();
}

function formatDate(d) {
  return new Date(d).toLocaleDateString('uz-UZ', {
    year: 'numeric', month: 'short', day: 'numeric',
  });
}

function showMsg(text, type) {
  messageBox.textContent = text;
  messageBox.className = `msg ${type}`;
}

function hideMsg() {
  messageBox.className = 'msg hidden';
}

function toast(text, type) {
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.textContent = text;
  document.getElementById('toastContainer').appendChild(el);
  setTimeout(() => {
    el.style.animation = 'fadeOut 0.3s ease forwards';
    setTimeout(() => el.remove(), 300);
  }, 2500);
}

// ---- Views ----

function showAuth() {
  authContainer.classList.remove('hidden');
  dashboardContainer.classList.add('hidden');
}

function showDashboard() {
  authContainer.classList.add('hidden');
  dashboardContainer.classList.remove('hidden');

  const u = currentUser;
  document.getElementById('welcomeMsg').textContent = `${u.email} hisobiga kirildi`;
  document.getElementById('userId').textContent = u.id;
  document.getElementById('userEmail').textContent = u.email;
  document.getElementById('userDate').textContent = formatDate(u.createdAt);

  renderTable();
}

function renderTable() {
  const tbody = document.getElementById('usersBody');
  const count = document.getElementById('userCount');
  tbody.innerHTML = '';
  count.textContent = users.length;

  users.forEach(u => {
    const tr = document.createElement('tr');
    if (currentUser && u.id === currentUser.id) tr.classList.add('current');
    tr.innerHTML = `
      <td>${u.id}</td>
      <td>${u.email}</td>
      <td>${formatDate(u.createdAt)}</td>
    `;
    tbody.appendChild(tr);
  });
}

// ---- Toggle login/register ----

switchLink.addEventListener('click', (e) => {
  e.preventDefault();
  hideMsg();
  isLogin = !isLogin;

  if (isLogin) {
    loginForm.classList.remove('hidden');
    registerForm.classList.add('hidden');
    formTitle.textContent = 'Kirish';
    formSubtitle.textContent = 'Email va parolingizni kiriting';
    switchText.textContent = "Akkauntingiz yo'qmi?";
    switchLink.textContent = "Ro'yxatdan o'ting";
  } else {
    loginForm.classList.add('hidden');
    registerForm.classList.remove('hidden');
    formTitle.textContent = "Ro'yxatdan o'tish";
    formSubtitle.textContent = 'Email va parol kiriting';
    switchText.textContent = 'Akkauntingiz bormi?';
    switchLink.textContent = 'Kiring';
  }
});

// ---- Login ----

loginForm.addEventListener('submit', (e) => {
  e.preventDefault();
  hideMsg();

  const email = document.getElementById('loginEmail').value.trim();
  const password = document.getElementById('loginPassword').value;

  if (!email || !password) {
    showMsg("Barcha maydonlarni to'ldiring", 'error');
    return;
  }

  const user = users.find(u => u.email === email && u.password === password);

  if (!user) {
    showMsg("Email yoki parol noto'g'ri", 'error');
    return;
  }

  currentUser = user;
  loginForm.reset();
  toast('Muvaffaqiyatli kirdingiz!', 'success');
  showDashboard();
});

// ---- Register ----

registerForm.addEventListener('submit', (e) => {
  e.preventDefault();
  hideMsg();

  const email = document.getElementById('regEmail').value.trim();
  const password = document.getElementById('regPassword').value;

  if (!email || !password) {
    showMsg("Barcha maydonlarni to'ldiring", 'error');
    return;
  }

  if (password.length < 6) {
    showMsg('Parol kamida 6 ta belgi', 'error');
    return;
  }

  if (users.find(u => u.email === email)) {
    showMsg("Bu email allaqachon ro'yxatdan o'tgan", 'error');
    return;
  }

  users.push({
    id: genId(),
    email,
    password,
    createdAt: new Date(),
  });

  registerForm.reset();
  toast("Ro'yxatdan o'tdingiz! Endi kiring.", 'success');

  // login sahifasiga o'tkazish
  isLogin = true;
  loginForm.classList.remove('hidden');
  registerForm.classList.add('hidden');
  formTitle.textContent = 'Kirish';
  formSubtitle.textContent = 'Email va parolingizni kiriting';
  switchText.textContent = "Akkauntingiz yo'qmi?";
  switchLink.textContent = "Ro'yxatdan o'ting";
});

// ---- Logout ----

logoutBtn.addEventListener('click', () => {
  currentUser = null;
  toast('Tizimdan chiqdingiz', 'error');
  showAuth();
});

// ---- Demo user ----
users.push({
  id: genId(),
  email: 'demo@email.com',
  password: '123456',
  createdAt: new Date(),
});
