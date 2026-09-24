from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_ACTIVATION = (
    HTML_HEAD.format(title="Activation — TriBoost")
    + CSS_COMMUN
    + """
<style>
  :root {
    --gold-light: #fff8e1;
    --orange: #f57c00;
    --orange-light: #fff3e0;
  }
  body { background: #f5f5f5; }
  .wrap {
    width: 100%; max-width: 480px;
    background: #fff;
    min-height: 100vh;
    padding: 20px 24px calc(20px + var(--safe-bottom));
    padding-top: var(--safe-top);
    display: flex;
    flex-direction: column;
  }
  .topbar-act {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 20px;
  }
  .back-icon {
    width: 40px; height: 40px; border-radius: 12px;
    background: var(--green-light); color: var(--green);
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    text-decoration: none;
  }
  .amount-card {
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    border-radius: 24px;
    padding: 28px 24px;
    color: #fff;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 30px rgba(46, 125, 50, 0.3);
    margin-bottom: 20px;
  }
  .amount-card::before {
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.1); border-radius: 50%;
  }
  .amount-label {
    font-size: 11px; font-weight: 700; opacity: 0.9;
    text-transform: uppercase; letter-spacing: 1px;
    margin-bottom: 10px;
    position: relative; z-index: 2;
  }
  .amount-value {
    font-size: 44px; font-weight: 900; line-height: 1;
    position: relative; z-index: 2;
    margin-bottom: 6px;
  }
  .amount-value span { font-size: 20px; font-weight: 700; }
  .amount-period {
    font-size: 12px; opacity: 0.85;
    position: relative; z-index: 2;
  }

  /* Infos */
  .info-row {
    display: flex; align-items: center; gap: 12px;
    background: var(--green-light);
    border-radius: 14px;
    padding: 12px 14px;
    margin-bottom: 16px;
    font-size: 12px;
    color: var(--green);
    font-weight: 600;
  }

  /* Formulaire */
  .form-group { margin-bottom: 14px; }
  .form-group label {
    display: block; font-size: 12px;
    font-weight: 700; margin-bottom: 6px;
    color: var(--text-dark);
  }
  .form-group input,
  .form-group select {
    width: 100%;
    height: 52px;
    padding: 0 14px;
    border: 1.5px solid var(--border);
    border-radius: 14px;
    font-size: 16px;
    font-family: inherit;
    color: var(--text-dark);
    outline: none;
    transition: border-color 0.2s;
    background: #fff;
    -webkit-appearance: none;
  }
  .form-group input:focus,
  .form-group select:focus {
    border-color: var(--green);
    box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.12);
  }
  .form-group select {
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23757575' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'/></svg>");
    background-repeat: no-repeat;
    background-position: right 14px center;
    padding-right: 38px;
  }

  /* Avantages */
  .benefits-title {
    font-size: 14px; font-weight: 800;
    margin: 20px 0 12px;
    display: flex; align-items: center; gap: 6px;
  }
  .benefits-list {
    display: flex; flex-direction: column; gap: 8px;
    margin-bottom: 20px;
  }
  .benefit-item {
    display: flex; align-items: center; gap: 10px;
    font-size: 12px;
    color: var(--text-dark);
  }
  .benefit-item .check {
    width: 20px; height: 20px;
    border-radius: 50%;
    background: var(--green-light);
    color: var(--green);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }

  /* Bouton */
  .btn-pay {
    width: 100%;
    height: 56px;
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    color: #fff;
    border: none;
    border-radius: 16px;
    font-weight: 800;
    font-size: 16px;
    font-family: inherit;
    cursor: pointer;
    box-shadow: 0 8px 20px rgba(46, 125, 50, 0.35);
    display: flex; align-items: center; justify-content: center; gap: 8px;
    transition: transform 0.15s;
  }
  .btn-pay:active { transform: scale(0.98); }
  .btn-pay:disabled { opacity: 0.6; cursor: not-allowed; }

  .spinner {
    width: 20px; height: 20px;
    border: 2.5px solid rgba(255,255,255,0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .secure-info {
    text-align: center;
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
  }
</style>
</head>
<body>
<div class="wrap">

  <div class="topbar-act">
    <a href="/dashboard" class="back-icon">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </a>
    <div class="logo" style="font-size:18px;">Tri<span>Boost</span></div>
    <div style="width:40px;"></div>
  </div>

  <div id="errorMsg" class="alert error"></div>
  <div id="successMsg" class="alert success"></div>

  <!-- MONTANT -->
  <div class="amount-card">
    <div class="amount-label">Frais d'activation unique</div>
    <div class="amount-value">3 600 <span>FCFA</span></div>
    <div class="amount-period">Paiement unique · Accès à vie</div>
  </div>

  <div class="info-row">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
    </svg>
    Paiement sécurisé via LeekPay
  </div>

  <!-- FORMULAIRE -->
  <form id="paymentForm" onsubmit="submitPayment(event)">

    <div class="form-group">
      <label>Pays</label>
      <select id="country" required>
        <option value="CM" selected>🇨🇲 Cameroun</option>
        <option value="CI">🇨🇮 Côte d'Ivoire</option>
        <option value="SN">🇸🇳 Sénégal</option>
        <option value="BJ">🇧🇯 Bénin</option>
        <option value="TG">🇹🇬 Togo</option>
        <option value="BF">🇧🇫 Burkina Faso</option>
        <option value="ML">🇲🇱 Mali</option>
        <option value="NE">🇳🇪 Niger</option>
        <option value="GN">🇬🇳 Guinée</option>
        <option value="CD">🇨🇩 RD Congo</option>
        <option value="CG">🇨🇬 Congo</option>
        <option value="GA">🇬🇦 Gabon</option>
        <option value="TD">🇹🇩 Tchad</option>
        <option value="CF">🇨🇫 Centrafrique</option>
        <option value="GQ">🇬🇶 Guinée Équatoriale</option>
      </select>
    </div>

    <div class="form-group">
      <label>Numéro Mobile Money</label>
      <input
        type="tel"
        id="phone"
        required
        placeholder="+237 6XX XXX XXX"
        inputmode="tel"
        autocomplete="tel">
    </div>

    <!-- AVANTAGES -->
    <div class="benefits-title">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
      </svg>
      Ce que vous débloquez
    </div>
    <div class="benefits-list">
      <div class="benefit-item">
        <div class="check">✓</div>
        Système d'affiliation 3 niveaux
      </div>
      <div class="benefit-item">
        <div class="check">✓</div>
        Commissions : 1 500 F / 750 F / 325 F
      </div>
      <div class="benefit-item">
        <div class="check">✓</div>
        Accès au Marché et à la Boutique
      </div>
      <div class="benefit-item">
        <div class="check">✓</div>
        Retraits Mobile Money
      </div>
    </div>

    <!-- BOUTON -->
    <button type="submit" class="btn-pay" id="payBtn">
      <span id="payBtnText">Payer 3 600 FCFA</span>
    </button>

    <div class="secure-info">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
        <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
      </svg>
      Paiement 100% sécurisé · LeekPay
    </div>

  </form>
</div>

"""
    + JS_COMMUN
    + """
<script>
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');

  if (!token || !userId) {
    window.location.href = '/login';
  }

  // Vérifier si déjà activé
  async function checkActivation() {
    try {
      const res = await fetch('/api/auth/profile/' + userId, {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      if (!res.ok) return;
      const data = await res.json();
      if (data.profile?.is_activated) {
        window.location.href = '/dashboard';
      }
    } catch (e) {}
  }
  checkActivation();

  // ===== SOUMISSION DU PAIEMENT =====
  async function submitPayment(e) {
    e.preventDefault();
    vibrate(8);

    const btn = document.getElementById('payBtn');
    const btnText = document.getElementById('payBtnText');
    const errEl = document.getElementById('errorMsg');
    errEl.style.display = 'none';

    const country = document.getElementById('country').value;
    const phone = document.getElementById('phone').value.trim();

    if (!phone || phone.length < 8) {
      errEl.textContent = '⚠ Numéro de téléphone invalide';
      errEl.style.display = 'block';
      return;
    }

    btn.disabled = true;
    btnText.innerHTML = '<div class="spinner"></div>';

    try {
      const res = await fetch('/api/payments/initiate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token,
        },
        body: JSON.stringify({ phone, country }),
      });

      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || 'Erreur de paiement');

      // Rediriger vers LeekPay
      if (data.payment_url) {
        vibrate(15);
        window.location.href = data.payment_url;
      } else {
        throw new Error('URL de paiement manquante');
      }

    } catch (err) {
      vibrate([30, 50, 30]);
      errEl.textContent = '⚠ ' + err.message;
      errEl.style.display = 'block';
      btn.disabled = false;
      btnText.textContent = 'Payer 3 600 FCFA';
    }
  }
</script>
</body>
</html>
"""
)