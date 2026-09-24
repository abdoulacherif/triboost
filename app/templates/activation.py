from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_ACTIVATION = (
    HTML_HEAD.format(title="Activation — TriBoost")
    + CSS_COMMUN
    + """
<style>
  .wrap { justify-content: flex-start; padding-top: 20px; }
  .topbar-act {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 24px;
  }
  .back-icon {
    width: 40px; height: 40px; border-radius: 12px;
    background: var(--green-light); color: var(--green);
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
  }
  .activation-title {
    font-size: 24px; font-weight: 800;
    text-align: center; margin-bottom: 8px;
  }
  .activation-sub {
    text-align: center; color: var(--text-muted);
    font-size: 14px; margin-bottom: 28px; line-height: 1.5;
  }

  /* Carte montant */
  .amount-card {
    background: linear-gradient(135deg, var(--green), var(--green-dark));
    border-radius: 24px;
    padding: 32px 24px;
    color: #fff;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 30px rgba(46, 125, 50, 0.3);
    margin-bottom: 24px;
  }
  .amount-card::before {
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.1); border-radius: 50%;
  }
  .amount-card::after {
    content: ''; position: absolute; bottom: -50px; left: -50px;
    width: 150px; height: 150px;
    background: rgba(251, 192, 45, 0.2); border-radius: 50%;
  }
  .amount-label {
    font-size: 12px; font-weight: 700; opacity: 0.9;
    text-transform: uppercase; letter-spacing: 1px;
    margin-bottom: 12px;
    position: relative; z-index: 2;
  }
  .amount-value {
    font-size: 52px; font-weight: 900; line-height: 1;
    position: relative; z-index: 2;
    margin-bottom: 6px;
  }
  .amount-value span {
    font-size: 22px; font-weight: 700;
  }
  .amount-period {
    font-size: 13px; opacity: 0.85;
    position: relative; z-index: 2;
  }

  /* Avantages */
  .benefits-title {
    font-size: 15px; font-weight: 800;
    margin-bottom: 14px;
    display: flex; align-items: center; gap: 8px;
  }
  .benefits-list {
    display: flex; flex-direction: column; gap: 12px;
    margin-bottom: 28px;
  }
  .benefit-item {
    display: flex; align-items: center; gap: 14px;
    background: #fff;
    border: 1px solid var(--border);
    padding: 14px;
    border-radius: 16px;
  }
  .benefit-icon {
    width: 40px; height: 40px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .benefit-text {
    flex: 1;
  }
  .benefit-text .title {
    font-size: 14px; font-weight: 700;
    margin-bottom: 2px;
  }
  .benefit-text .desc {
    font-size: 12px; color: var(--text-muted);
  }

  .bi-green { background: var(--green-light); color: var(--green); }
  .bi-gold  { background: #fff8e1; color: #f9a825; }
  .bi-red   { background: var(--red-light); color: var(--red); }
  .bi-blue  { background: #e3f2fd; color: #1976d2; }

  /* Méthode de paiement */
  .payment-methods {
    display: flex; flex-direction: column; gap: 10px;
    margin-bottom: 20px;
  }
  .payment-option {
    display: flex; align-items: center; gap: 14px;
    background: #fff;
    border: 2px solid var(--border);
    padding: 14px 16px;
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
  }
  .payment-option.selected {
    border-color: var(--green);
    background: var(--green-light);
  }
  .payment-option input {
    display: none;
  }
  .payment-radio {
    width: 22px; height: 22px;
    border-radius: 50%;
    border: 2px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    transition: 0.2s;
  }
  .payment-option.selected .payment-radio {
    border-color: var(--green);
  }
  .payment-option.selected .payment-radio::after {
    content: '';
    width: 12px; height: 12px;
    border-radius: 50%;
    background: var(--green);
  }
  .payment-logo {
    font-size: 22px;
    flex-shrink: 0;
  }
  .payment-info {
    flex: 1;
  }
  .payment-info .title {
    font-size: 14px; font-weight: 700;
  }
  .payment-info .desc {
    font-size: 11px; color: var(--text-muted);
  }

  /* Info solde actuel */
  .balance-info {
    background: #fff8e1;
    border: 1.5px solid var(--gold);
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
  }
  .balance-info .label {
    color: #6d4c00;
    font-weight: 600;
  }
  .balance-info .value {
    color: #6d4c00;
    font-weight: 800;
    font-size: 16px;
  }

  /* Badge status */
  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 700;
  }
  .status-badge.inactive {
    background: #fff3e0;
    color: #e65100;
  }
  .status-badge.active {
    background: var(--green-light);
    color: var(--green);
  }
</style>
</head>
<body>
<div class="progress-bar" id="progressBar"></div>

<div class="wrap">

  <div class="topbar-act">
    <button class="back-icon" onclick="location.href='/dashboard'">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </button>
    <div class="logo" style="font-size:18px;">Tri<span>Boost</span></div>
    <div style="width:40px;"></div>
  </div>

  <div id="errorMsg" class="alert error"></div>
  <div id="successMsg" class="alert success"></div>

  <!-- Carte montant -->
  <div class="amount-card">
    <div class="amount-label">Frais d'activation unique</div>
    <div class="amount-value">3 600 <span>FCFA</span></div>
    <div class="amount-period">Paiement unique · Accès à vie</div>
  </div>

  <!-- Avantages -->
  <div class="benefits-title">✨ Ce que vous débloquez</div>
  <div class="benefits-list">

    <div class="benefit-item">
      <div class="benefit-icon bi-green">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
      </div>
      <div class="benefit-text">
        <div class="title">Système d'affiliation 3 niveaux</div>
        <div class="desc">Gagnez sur vos filleuls directs et indirects</div>
      </div>
    </div>

    <div class="benefit-item">
      <div class="benefit-icon bi-gold">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
          <polyline points="17 6 23 6 23 12"></polyline>
        </svg>
      </div>
      <div class="benefit-text">
        <div class="title">Commissions sur les ventes</div>
        <div class="desc">40% N1 · 15% N2 · 5% N3</div>
      </div>
    </div>

    <div class="benefit-item">
      <div class="benefit-icon bi-blue">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
          <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
        </svg>
      </div>
      <div class="benefit-text">
        <div class="title">Accès au Shop & Marché</div>
        <div class="desc">Achetez, vendez et touchez des bonus</div>
      </div>
    </div>

    <div class="benefit-item">
      <div class="benefit-icon bi-red">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
          <line x1="1" y1="10" x2="23" y2="10"></line>
        </svg>
      </div>
      <div class="benefit-text">
        <div class="title">Retraits Mobile Money</div>
        <div class="desc">MTN MoMo · Orange Money · Banque</div>
      </div>
    </div>

  </div>

  <!-- Solde actuel -->
  <div class="balance-info">
    <span class="label">Solde actuel du compte</span>
    <span class="value" id="currentBalance">0 FCFA</span>
  </div>

  <!-- Méthodes de paiement -->
  <div class="benefits-title">💳 Méthode de paiement</div>
  <div class="payment-methods">

    <div class="payment-option selected" onclick="selectPayment(this, 'mtn')">
      <div class="payment-radio"></div>
      <div class="payment-logo">📱</div>
      <div class="payment-info">
        <div class="title">MTN Mobile Money</div>
        <div class="desc">Paiement via *126#</div>
      </div>
      <input type="radio" name="payment" value="mtn" checked>
    </div>

    <div class="payment-option" onclick="selectPayment(this, 'orange')">
      <div class="payment-radio"></div>
      <div class="payment-logo">🟠</div>
      <div class="payment-info">
        <div class="title">Orange Money</div>
        <div class="desc">Paiement via #150#</div>
      </div>
      <input type="radio" name="payment" value="orange">
    </div>

    <div class="payment-option" onclick="selectPayment(this, 'wallet')">
      <div class="payment-radio"></div>
      <div class="payment-logo">💰</div>
      <div class="payment-info">
        <div class="title">Solde TriBoost</div>
        <div class="desc">Utiliser votre solde disponible</div>
      </div>
      <input type="radio" name="payment" value="wallet">
    </div>

  </div>

  <button type="button" class="btn-primary" id="activateBtn" onclick="activateAccount()">
    <span>Payer 3 600 FCFA et activer</span>
  </button>

  <div class="footer" style="margin-top:20px; font-size:12px;">
    Une fois activé, votre compte est actif <strong>à vie</strong>.<br>
    Aucun frais mensuel.
  </div>

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

  let selectedMethod = 'mtn';

  // ===== VÉRIFIER SI DÉJÀ ACTIVÉ =====
  async function checkActivation() {
    try {
      const res = await fetch('/api/auth/profile/' + userId, {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      if (!res.ok) return;
      const data = await res.json();
      const profile = data.profile;

      if (profile.wallet_balance) {
        document.getElementById('currentBalance').textContent =
          Number(profile.wallet_balance).toLocaleString('fr-FR') + ' FCFA';
      }

      if (profile.is_activated) {
        // Déjà activé → rediriger
        showSuccess('Votre compte est déjà activé ! Redirection...');
        setTimeout(() => window.location.href = '/dashboard', 1200);
      }
    } catch (err) {
      console.error(err);
    }
  }
  checkActivation();

  // ===== SÉLECTION MÉTHODE =====
  function selectPayment(el, method) {
    document.querySelectorAll('.payment-option').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
    el.querySelector('input').checked = true;
    selectedMethod = method;
    vibrate(8);
  }

  // ===== ACTIVER =====
  async function activateAccount() {
    const btn = document.getElementById('activateBtn');
    vibrate(10);
    setButtonLoading(btn, true);
    showProgress();
    document.getElementById('errorMsg').style.display = 'none';
    document.getElementById('successMsg').style.display = 'none';

    try {
      const res = await fetch('/api/auth/activate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token,
        },
        body: JSON.stringify({
          payment_method: selectedMethod,
          payment_reference: 'TRIBOOST-' + Date.now(),
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || 'Erreur lors de l\\'activation');
      }

      vibrate(30);
      hideProgress();
      showSuccess('🎉 Compte activé ! Redirection...');
      setTimeout(() => window.location.href = '/dashboard', 1500);

    } catch (err) {
      hideProgress();
      vibrate([30, 50, 30]);
      showError(err.message);
      setButtonLoading(btn, false, 'Payer 3 600 FCFA et activer');
    }
  }
</script>
</body>
</html>
"""
)