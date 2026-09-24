from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_REGISTER = (
    HTML_HEAD.format(title="Inscription — TriBoost")
    + CSS_COMMUN
    + """
</head>
<body>
<div class="progress-bar" id="progressBar"></div>

<a href="/login" class="back-btn" aria-label="Retour">
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="15 18 9 12 15 6"></polyline>
  </svg>
</a>

<div class="wrap">
  <div class="logo">Tri<span>Boost</span></div>
  <div class="subtitle">Créez votre compte gratuit</div>

  <div class="referral-info" id="refInfo" style="display:none;">
    🎁 Parrainé par <span id="refCode"></span>
  </div>

  <div id="errorMsg" class="alert error"></div>
  <div id="successMsg" class="alert success"></div>

  <form id="registerForm" autocomplete="on" novalidate>

    <div class="form-group">
      <label for="fullName">Nom complet</label>
      <input type="text" id="fullName" name="name" required
        placeholder="Ex : Abdoula Diallo"
        autocomplete="name" autocapitalize="words" enterkeyhint="next">
    </div>

    <div class="form-group">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required
        placeholder="vous@exemple.com" inputmode="email"
        autocomplete="email" autocapitalize="off" autocorrect="off"
        spellcheck="false" enterkeyhint="next">
    </div>

    <div class="form-group">
      <label for="phone">Numéro Mobile Money</label>
      <input type="tel" id="phone" name="phone" required
        placeholder="+237 6XX XXX XXX"
        inputmode="tel" autocomplete="tel" enterkeyhint="next">
    </div>

    <div class="form-group">
      <label for="password">Mot de passe (min. 6 caractères)</label>
      <input type="password" id="password" name="new-password"
        minlength="6" required placeholder="••••••••"
        autocomplete="new-password" enterkeyhint="go">
      <button type="button" class="pw-toggle" onclick="togglePassword('password')" aria-label="Afficher">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
          <circle cx="12" cy="12" r="3"></circle>
        </svg>
      </button>
    </div>

    <button type="submit" class="btn-primary" id="registerBtn">
      <span>Créer mon compte</span>
    </button>

  </form>

  <div class="footer">
    Déjà inscrit ? <a href="/login">Se connecter</a>
  </div>
</div>
"""
    + JS_COMMUN
    + """
<script>
  const form = document.getElementById('registerForm');
  const btn = document.getElementById('registerBtn');

  const urlParams = new URLSearchParams(window.location.search);
  const refCode = urlParams.get('ref') || localStorage.getItem('referral_code');
  if (refCode) {
    document.getElementById('refInfo').style.display = 'block';
    document.getElementById('refCode').textContent = refCode;
    localStorage.setItem('referral_code', refCode);
  }

  setTimeout(() => document.getElementById('fullName').focus(), 300);

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    vibrate(8);
    document.getElementById('errorMsg').style.display = 'none';
    document.getElementById('successMsg').style.display = 'none';

    const fullName = document.getElementById('fullName').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const password = document.getElementById('password').value;

    if (!fullName || !email || !phone || !password) {
      showError('Veuillez remplir tous les champs');
      return;
    }
    if (password.length < 6) {
      showError('Le mot de passe doit contenir au moins 6 caractères');
      return;
    }

    setButtonLoading(btn, true);
    showProgress();

    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email, password,
          full_name: fullName,
          phone: phone,
          referral_code: refCode || null
        })
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || "Erreur lors de l'inscription");

      vibrate(20);
      hideProgress();
      showSuccess('Compte créé ! Vérifiez votre email.');
      setTimeout(() => window.location.href = '/login', 2000);

    } catch (err) {
      hideProgress();
      vibrate([30, 50, 30]);
      showError(err.message);
      setButtonLoading(btn, false, 'Créer mon compte');
    }
  });
</script>
</body>
</html>
"""
)