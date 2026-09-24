from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

# ============================================================
# 54 PAYS D'AFRIQUE AVEC DRAPEAUX
# ============================================================
AFRICAN_COUNTRIES = [
    ("DZ", "🇩🇿", "Algérie"),
    ("AO", "🇦🇴", "Angola"),
    ("BJ", "🇧🇯", "Bénin"),
    ("BW", "🇧🇼", "Botswana"),
    ("BF", "🇧🇫", "Burkina Faso"),
    ("BI", "🇧🇮", "Burundi"),
    ("CM", "🇨🇲", "Cameroun"),
    ("CV", "🇨🇻", "Cap-Vert"),
    ("CF", "🇨🇫", "République Centrafricaine"),
    ("TD", "🇹🇩", "Tchad"),
    ("KM", "🇰🇲", "Comores"),
    ("CG", "🇨🇬", "Congo-Brazzaville"),
    ("CD", "🇨🇩", "Congo-Kinshasa (RDC)"),
    ("CI", "🇨🇮", "Côte d'Ivoire"),
    ("DJ", "🇩🇯", "Djibouti"),
    ("EG", "🇪🇬", "Égypte"),
    ("GQ", "🇬🇶", "Guinée Équatoriale"),
    ("ER", "🇪🇷", "Érythrée"),
    ("SZ", "🇸🇿", "Eswatini"),
    ("ET", "🇪🇹", "Éthiopie"),
    ("GA", "🇬🇦", "Gabon"),
    ("GM", "🇬🇲", "Gambie"),
    ("GH", "🇬🇭", "Ghana"),
    ("GN", "🇬🇳", "Guinée"),
    ("GW", "🇬🇼", "Guinée-Bissau"),
    ("KE", "🇰🇪", "Kenya"),
    ("LS", "🇱🇸", "Lesotho"),
    ("LR", "🇱🇷", "Liberia"),
    ("LY", "🇱🇾", "Libye"),
    ("MG", "🇲🇬", "Madagascar"),
    ("MW", "🇲🇼", "Malawi"),
    ("ML", "🇲🇱", "Mali"),
    ("MR", "🇲🇷", "Mauritanie"),
    ("MU", "🇲🇺", "Maurice"),
    ("MA", "🇲🇦", "Maroc"),
    ("MZ", "🇲🇿", "Mozambique"),
    ("NA", "🇳🇦", "Namibie"),
    ("NE", "🇳🇪", "Niger"),
    ("NG", "🇳🇬", "Nigeria"),
    ("RW", "🇷🇼", "Rwanda"),
    ("ST", "🇸🇹", "Sao Tomé-et-Principe"),
    ("SN", "🇸🇳", "Sénégal"),
    ("SC", "🇸🇨", "Seychelles"),
    ("SL", "🇸🇱", "Sierra Leone"),
    ("SO", "🇸🇴", "Somalie"),
    ("ZA", "🇿🇦", "Afrique du Sud"),
    ("SS", "🇸🇸", "Soudan du Sud"),
    ("SD", "🇸🇩", "Soudan"),
    ("TZ", "🇹🇿", "Tanzanie"),
    ("TG", "🇹🇬", "Togo"),
    ("TN", "🇹🇳", "Tunisie"),
    ("UG", "🇺🇬", "Ouganda"),
    ("ZM", "🇿🇲", "Zambie"),
    ("ZW", "🇿🇼", "Zimbabwe"),
]


def _country_options() -> str:
    """Génère les <option> avec drapeau + nom."""
    return "\n".join(
        f'        <option value="{code}">{flag} {name}</option>'
        for code, flag, name in AFRICAN_COUNTRIES
    )


HTML_REGISTER = (
    HTML_HEAD.format(title="Inscription — TriBoost")
    + CSS_COMMUN
    + """
<style>
  /* SELECT custom (compatible Android) */
  .form-group select {
    width: 100%;
    height: 52px;
    padding: 0 40px 0 16px;
    border: 1.5px solid var(--border);
    border-radius: 14px;
    font-size: 16px;
    font-family: inherit;
    background: #fff;
    color: var(--text-dark);
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
    -webkit-appearance: none;
    appearance: none;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23757575' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'/></svg>");
    background-repeat: no-repeat;
    background-position: right 14px center;
    cursor: pointer;
  }
  .form-group select:focus {
    border-color: var(--green);
    box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.12);
  }
  .form-group select option {
    font-size: 16px;
    padding: 10px;
  }

  /* Bandeau drapeau du pays sélectionné */
  .country-preview {
    display: none;
    align-items: center;
    gap: 10px;
    background: var(--green-light);
    color: var(--green);
    padding: 10px 14px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 600;
    margin-top: 8px;
    animation: popIn 0.3s ease-out;
  }
  .country-preview.show { display: flex; }
  .country-preview .flag {
    font-size: 22px;
    line-height: 1;
  }
  @keyframes popIn {
    from { transform: scale(0.9); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
  }

  /* Champ code parrainage */
  .referral-field {
    background: linear-gradient(135deg, #fff8e1, #fffde7);
    border: 1.5px solid var(--gold);
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 18px;
  }
  .referral-field .field-label {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    font-weight: 700;
    color: #6d4c00;
    margin-bottom: 8px;
  }
  .referral-field .field-label .badge-optional {
    background: rgba(0,0,0,0.08);
    color: #6d4c00;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 6px;
    font-weight: 600;
  }
  .referral-input-wrap {
    position: relative;
  }
  .referral-input-wrap input {
    width: 100%;
    height: 48px;
    padding: 0 44px 0 14px;
    border: 1.5px solid #ffe082;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-family: 'Courier New', monospace;
    background: #fff;
    color: #6d4c00;
    outline: none;
    transition: border-color 0.2s;
  }
  .referral-input-wrap input:focus {
    border-color: var(--gold);
    box-shadow: 0 0 0 3px rgba(251, 192, 45, 0.2);
  }
  .referral-input-wrap input::placeholder {
    color: #bcaaa4;
    font-weight: 400;
    letter-spacing: normal;
    text-transform: none;
    font-family: inherit;
  }
  .referral-status {
    position: absolute;
    right: 14px;
    top: 50%;
    transform: translateY(-50%);
    display: none;
    align-items: center;
    justify-content: center;
  }
  .referral-status.show { display: flex; }
  .referral-status .check {
    color: var(--green);
    animation: popIn 0.3s ease-out;
  }
  .referral-status .cross {
    color: var(--red);
    animation: popIn 0.3s ease-out;
  }
  .referral-status .loading {
    width: 18px;
    height: 18px;
    border: 2px solid #ffe082;
    border-top-color: var(--gold);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  .referral-help {
    font-size: 11px;
    color: #8d6e63;
    margin-top: 6px;
    line-height: 1.4;
  }
  .referral-success {
    background: var(--green-light);
    color: var(--green);
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    margin-top: 8px;
    display: none;
    font-weight: 600;
  }
  .referral-success.show { display: block; }
</style>
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

  <div id="errorMsg" class="alert error"></div>
  <div id="successMsg" class="alert success"></div>

  <form id="registerForm" autocomplete="on" novalidate>

    <!-- Nom complet -->
    <div class="form-group">
      <label for="fullName">Nom complet</label>
      <input type="text" id="fullName" name="name" required
        placeholder="Ex : Abdoula Diallo"
        autocomplete="name" autocapitalize="words" enterkeyhint="next">
    </div>

    <!-- Email -->
    <div class="form-group">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required
        placeholder="vous@exemple.com" inputmode="email"
        autocomplete="email" autocapitalize="off" autocorrect="off"
        spellcheck="false" enterkeyhint="next">
    </div>

    <!-- Téléphone -->
    <div class="form-group">
      <label for="phone">Numéro Mobile Money</label>
      <input type="tel" id="phone" name="phone" required
        placeholder="+237 6XX XXX XXX"
        inputmode="tel" autocomplete="tel" enterkeyhint="next">
    </div>

    <!-- PAYS avec drapeaux -->
    <div class="form-group">
      <label for="country">Pays</label>
      <select id="country" name="country" required>
        <option value="" disabled selected>-- Sélectionnez votre pays --</option>
""" + _country_options() + """
      </select>
      <div class="country-preview" id="countryPreview">
        <span class="flag" id="countryFlag"></span>
        <span id="countryName"></span>
      </div>
    </div>

    <!-- CODE PARRAINAGE -->
    <div class="referral-field">
      <div class="field-label">
        🎁 Code de parrainage
        <span class="badge-optional">optionnel</span>
      </div>
      <div class="referral-input-wrap">
        <input type="text" id="referralCode" name="referral_code"
          placeholder="Ex : TB4A7B9C"
          maxlength="10"
          autocapitalize="characters"
          autocorrect="off"
          spellcheck="false"
          enterkeyhint="next">
        <div class="referral-status" id="refStatus"></div>
      </div>
      <div class="referral-help">
        Entrez le code d'un ami pour qu'il gagne des commissions.
      </div>
      <div class="referral-success" id="refSuccess"></div>
    </div>

    <!-- Mot de passe -->
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
  const countrySelect = document.getElementById('country');
  const countryPreview = document.getElementById('countryPreview');
  const countryFlag = document.getElementById('countryFlag');
  const countryName = document.getElementById('countryName');
  const refInput = document.getElementById('referralCode');
  const refStatus = document.getElementById('refStatus');
  const refSuccess = document.getElementById('refSuccess');

  // ===== APERÇU DU PAYS SÉLECTIONNÉ =====
  countrySelect.addEventListener('change', (e) => {
    const selectedOption = e.target.options[e.target.selectedIndex];
    const text = selectedOption.textContent.trim();
    const parts = text.split(' ');
    const flag = parts[0];
    const name = parts.slice(1).join(' ');

    countryFlag.textContent = flag;
    countryName.textContent = name;
    countryPreview.classList.add('show');
    vibrate(8);
  });

  // ===== RÉCUPÉRER CODE PARRAIN DEPUIS URL =====
  const urlParams = new URLSearchParams(window.location.search);
  const urlRefCode = urlParams.get('ref');
  const storedRefCode = localStorage.getItem('referral_code');
  const initialRefCode = (urlRefCode || storedRefCode || '').toUpperCase().trim();

  if (initialRefCode) {
    refInput.value = initialRefCode;
    localStorage.setItem('referral_code', initialRefCode);
    verifyReferralCode(initialRefCode);
  }

  // ===== VÉRIFICATION EN TEMPS RÉEL =====
  let verifyTimeout = null;

  refInput.addEventListener('input', (e) => {
    e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
    const code = e.target.value.trim();

    clearTimeout(verifyTimeout);
    refStatus.classList.remove('show');
    refSuccess.classList.remove('show');

    if (code.length < 4) return;

    verifyTimeout = setTimeout(() => verifyReferralCode(code), 500);
  });

  refInput.addEventListener('blur', () => {
    const code = refInput.value.trim();
    if (code.length >= 4) verifyReferralCode(code);
  });

  async function verifyReferralCode(code) {
    if (!code || code.length < 4) return;

    refStatus.innerHTML = '<div class="loading"></div>';
    refStatus.classList.add('show');
    refSuccess.classList.remove('show');

    try {
      const res = await fetch('/api/auth/check-referral/' + encodeURIComponent(code));
      const data = await res.json();

      if (data.valid) {
        refStatus.innerHTML = '<svg class="check" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
        refSuccess.textContent = '✓ Parrain : ' + (data.full_name || 'Utilisateur TriBoost');
        refSuccess.style.background = 'var(--green-light)';
        refSuccess.style.color = 'var(--green)';
        refSuccess.classList.add('show');
        vibrate(10);
      } else {
        refStatus.innerHTML = '<svg class="cross" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>';
        refSuccess.textContent = '⚠ Code introuvable';
        refSuccess.style.background = 'var(--red-light)';
        refSuccess.style.color = 'var(--red)';
        refSuccess.classList.add('show');
      }
    } catch (err) {
      refStatus.classList.remove('show');
    }
  }

  // ===== AUTO-FOCUS =====
  setTimeout(() => document.getElementById('fullName').focus(), 300);

  // ===== SUBMIT =====
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    vibrate(8);
    document.getElementById('errorMsg').style.display = 'none';
    document.getElementById('successMsg').style.display = 'none';

    const fullName = document.getElementById('fullName').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const country = countrySelect.value;
    const referralCode = refInput.value.trim();
    const password = document.getElementById('password').value;

    if (!fullName || !email || !phone || !country || !password) {
      showError('Veuillez remplir tous les champs obligatoires');
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
          country: country,
          referral_code: referralCode || null
        })
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || "Erreur lors de l'inscription");

      localStorage.removeItem('referral_code');
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