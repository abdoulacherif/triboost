from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_LOGIN = (
    HTML_HEAD.format(title="Connexion — TriBoost")
    + CSS_COMMUN
    + """
</head>
<body>
<div class="progress-bar" id="progressBar"></div>
<div class="wrap">

  <div class="logo">Tri<span>Boost</span></div>
  <div class="subtitle">Connectez-vous à votre compte</div>

  <div id="errorMsg" class="alert error"></div>
  <div id="successMsg" class="alert success"></div>

  <form id="loginForm" autocomplete="on" novalidate>

    <div class="form-group">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required
        placeholder="vous@exemple.com" inputmode="email"
        autocomplete="email" autocapitalize="off" autocorrect="off"
        spellcheck="false" enterkeyhint="next">
    </div>

    <div class="form-group">
      <label for="password">Mot de passe</label>
      <input type="password" id="password" name="password" required
        placeholder="••••••••" autocomplete="current-password" enterkeyhint="go">
      <button type="button" class="pw-toggle" onclick="togglePassword('password')" aria-label="Afficher">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
          <circle cx="12" cy="12" r="3"></circle>
        </svg>
      </button>
    </div>

    <button type="submit" class="btn-primary" id="loginBtn">
      <span>Se connecter</span>
    </button>

  </form>

  <div class="footer">
    Pas de compte ? <a href="/register">Inscrivez-vous</a>
  </div>
</div>
"""
    + JS_COMMUN
    + """
<script>
  const form = document.getElementById('loginForm');
  const btn = document.getElementById('loginBtn');

  setTimeout(() => document.getElementById('email').focus(), 300);

  if (localStorage.getItem('access_token')) {
    window.location.href = '/dashboard';
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    vibrate(8);
    document.getElementById('errorMsg').style.display = 'none';
    document.getElementById('successMsg').style.display = 'none';

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    if (!email || !password) {
      showError('Veuillez remplir tous les champs');
      return;
    }

    setButtonLoading(btn, true);
    showProgress();

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || 'Identifiants invalides');

      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      localStorage.setItem('user_email', data.user.email);
      if (data.user.full_name) localStorage.setItem('user_name', data.user.full_name);

      vibrate(20);
      showSuccess('Connexion réussie ! Redirection...');
      setTimeout(() => window.location.href = '/dashboard', 700);

    } catch (err) {
      hideProgress();
      vibrate([30, 50, 30]);
      showError(err.message);
      setButtonLoading(btn, false, 'Se connecter');
    }
  });
</script>
</body>
</html>
"""
)