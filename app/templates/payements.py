from app.templates.shared import CSS_COMMUN, HTML_HEAD, JS_COMMUN

HTML_PAIEMENTS = (
    HTML_HEAD.format(title="Paiements — TriBoost")
    + CSS_COMMUN
    + """
<style>
  :root {
    --gold-light: #fff8e1;
    --orange: #f57c00;
    --orange-light: #fff3e0;
    --blue: #1976d2;
    --blue-light: #e3f2fd;
  }
  body { background: #f5f5f5; }
  .app { width: 100%; max-width: 480px; background: #f5f5f5; min-height: 100vh; padding-bottom: calc(40px + var(--safe-bottom)); padding-top: var(--safe-top); margin: 0 auto; }

  .topbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: #fff; position: sticky; top: 0; z-index: 50; }
  .back-btn { width: 40px; height: 40px; border-radius: 12px; background: var(--green-light); color: var(--green); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; text-decoration: none; }
  .page-title { font-size: 18px; font-weight: 800; color: var(--text-dark); flex: 1; text-align: center; }
  .spacer { width: 40px; }

  .inactive-banner { display: none; margin: 12px 16px; background: linear-gradient(135deg, #fff3e0, #ffe0b2); border: 1.5px solid #ffb74d; border-radius: 16px; padding: 12px 14px; align-items: center; gap: 10px; }
  .inactive-banner.show { display: flex; }
  .inactive-banner .icon { width: 36px; height: 36px; border-radius: 10px; background: #ffe0b2; color: #e65100; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .inactive-banner .text { flex: 1; min-width: 0; }
  .inactive-banner .title { font-size: 12px; font-weight: 800; color: #e65100; }
  .inactive-banner .desc { font-size: 10px; color: #bf360c; }
  .inactive-banner .action { background: #e65100; color: #fff; border: none; padding: 6px 10px; border-radius: 8px; font-size: 10px; font-weight: 700; cursor: pointer; flex-shrink: 0; }

  /* ===== SOLDE ===== */
  .balance-card { margin: 16px; background: linear-gradient(135deg, var(--green), var(--green-dark)); border-radius: 20px; padding: 20px; color: #fff; position: relative; overflow: hidden; box-shadow: 0 8px 20px rgba(46, 125, 50, 0.3); }
  .balance-card::before { content: ''; position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: rgba(255,255,255,0.1); border-radius: 50%; }
  .balance-label { font-size: 11px; font-weight: 700; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px; position: relative; z-index: 2; }
  .balance-value { font-size: 32px; font-weight: 900; margin: 8px 0 4px; position: relative; z-index: 2; line-height: 1; }
  .balance-value span { font-size: 16px; font-weight: 600; }
  .balance-sub { font-size: 12px; opacity: 0.85; position: relative; z-index: 2; }

  /* ===== TABS ===== */
  .tabs { display: flex; gap: 8px; padding: 0 16px; margin-bottom: 16px; }
  .tab { flex: 1; background: #fff; border: 1.5px solid var(--border); color: var(--text-muted); padding: 12px 8px; border-radius: 14px; font-size: 13px; font-weight: 700; font-family: inherit; cursor: pointer; transition: all 0.2s; display: flex; flex-direction: column; align-items: center; gap: 4px; }
  .tab .icon { font-size: 20px; }
  .tab.active { background: var(--green); color: #fff; border-color: var(--green); box-shadow: 0 4px 10px rgba(46, 125, 50, 0.25); }
  .tab-content { display: none; }
  .tab-content.active { display: block; }

  /* ===== FORM CARD ===== */
  .form-card { margin: 0 16px 16px; background: #fff; border-radius: 20px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
  .form-card h3 { font-size: 15px; font-weight: 800; margin-bottom: 16px; display: flex; align-items: center; gap: 6px; color: var(--text-dark); }

  .form-group { margin-bottom: 14px; }
  .form-group label { display: block; font-size: 12px; font-weight: 700; margin-bottom: 6px; color: var(--text-dark); }
  .form-group input, .form-group select { width: 100%; padding: 12px 14px; border: 1.5px solid var(--border); border-radius: 12px; font-size: 15px; font-family: inherit; color: var(--text-dark); outline: none; background: #fff; transition: border-color 0.2s; -webkit-appearance: none; }
  .form-group input:focus, .form-group select:focus { border-color: var(--green); }
  .form-group select { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23757575' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'/></svg>"); background-repeat: no-repeat; background-position: right 14px center; padding-right: 38px; }

  /* Montants rapides */
  .quick-amounts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 10px; }
  .qa-btn { background: #f5f5f5; border: 1.5px solid transparent; color: var(--text-dark); padding: 10px; border-radius: 10px; font-size: 13px; font-weight: 700; font-family: inherit; cursor: pointer; transition: all 0.2s; }
  .qa-btn.active { background: var(--green-light); border-color: var(--green); color: var(--green); }

  .info-min { background: #fff8e1; border-left: 3px solid var(--gold); border-radius: 10px; padding: 10px 12px; font-size: 11px; color: #6d4c00; margin-bottom: 14px; line-height: 1.5; }

  .btn-primary { width: 100%; background: linear-gradient(135deg, var(--green), var(--green-dark)); color: #fff; border: none; padding: 16px; border-radius: 14px; font-weight: 800; font-size: 15px; font-family: inherit; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; box-shadow: 0 4px 14px rgba(46, 125, 50, 0.3); transition: transform 0.15s; }
  .btn-primary:active { transform: scale(0.98); }
  .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
  .btn-primary.gold { background: linear-gradient(135deg, var(--gold), #f57c00); color: #212121; box-shadow: 0 4px 14px rgba(245, 124, 0, 0.3); }

  .spinner { width: 18px; height: 18px; border: 2.5px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.8s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* ===== LISTES ===== */
  .section-title { font-size: 14px; font-weight: 800; margin: 16px 16px 10px; color: var(--text-dark); display: flex; justify-content: space-between; align-items: center; }
  .section-title .right { font-size: 11px; color: var(--text-muted); font-weight: 600; }

  .history-list { padding: 0 16px; display: flex; flex-direction: column; gap: 8px; }
  .history-item { background: #fff; border-radius: 14px; padding: 14px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
  .hi-icon { width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }
  .hi-icon.withdraw { background: var(--orange-light); color: var(--orange); }
  .hi-icon.recharge { background: var(--blue-light); color: var(--blue); }
  .hi-icon.green { background: var(--green-light); color: var(--green); }
  .hi-icon.red { background: var(--red-light); color: var(--red); }
  .hi-icon.yellow { background: #fff8e1; color: #f9a825; }
  .hi-info { flex: 1; min-width: 0; }
  .hi-title { font-size: 13px; font-weight: 700; color: var(--text-dark); margin-bottom: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .hi-meta { font-size: 11px; color: var(--text-muted); display: flex; gap: 8px; }
  .hi-badge { font-size: 10px; font-weight: 800; padding: 2px 8px; border-radius: 6px; text-transform: uppercase; }
  .hi-badge.pending { background: #fff3e0; color: #e65100; }
  .hi-badge.completed { background: var(--green-light); color: var(--green); }
  .hi-badge.rejected, .hi-badge.failed { background: var(--red-light); color: var(--red); }
  .hi-amount { font-size: 15px; font-weight: 900; white-space: nowrap; }
  .hi-amount.negative { color: var(--orange); }
  .hi-amount.positive { color: var(--green); }

  .empty-state { text-align: center; padding: 40px 20px; color: var(--text-muted); }
  .empty-state .icon { width: 64px; height: 64px; margin: 0 auto 12px; border-radius: 50%; background: var(--green-light); color: var(--green); display: flex; align-items: center; justify-content: center; }
  .empty-state h3 { font-size: 14px; font-weight: 700; color: var(--text-dark); margin-bottom: 4px; }
  .empty-state p { font-size: 12px; line-height: 1.5; }

  .skel-card { background: #fff; border-radius: 14px; padding: 14px; animation: pulse 1.4s infinite; }
  .skel-line { height: 12px; background: #f0f0f0; border-radius: 6px; margin-bottom: 8px; }
  .skel-line.short { width: 60%; }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }
</style>
</head>
<body>

<div class="app">
  <header class="topbar">
    <a href="/dashboard" class="back-btn">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
    </a>
    <div class="page-title">Paiements</div>
    <div class="spacer"></div>
  </header>

  <div class="inactive-banner" id="inactiveBanner">
    <div class="icon">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
    </div>
    <div class="text">
      <div class="title">Lecture seule</div>
      <div class="desc">Activez pour retirer ou recharger</div>
    </div>
    <button class="action" onclick="location.href='/activation'">Activer</button>
  </div>

  <!-- SOLDE -->
  <div class="balance-card">
    <div class="balance-label">Solde disponible</div>
    <div class="balance-value" id="walletBalance">- <span>FCFA</span></div>
    <div class="balance-sub">Frais de retrait : 2% · Minimum : 2 000 F</div>
  </div>

  <!-- TABS -->
  <div class="tabs">
    <button class="tab active" data-tab="withdraw">
      <span class="icon">💸</span>
      Retrait
    </button>
    <button class="tab" data-tab="recharge">
      <span class="icon">💰</span>
      Recharge
    </button>
    <button class="tab" data-tab="history">
      <span class="icon">📜</span>
      Historique
    </button>
  </div>

  <!-- TAB RETRAIT -->
  <div class="tab-content active" id="tab-withdraw">
    <div class="form-card">
      <h3>💸 Demander un retrait</h3>
      <div class="info-min">
        ⚠️ Minimum 2 000 F · Frais 2% · Traitement sous 24-72h
      </div>

      <div id="withdrawError" class="alert error" style="display:none;"></div>

      <form id="withdrawForm" onsubmit="submitWithdraw(event)">
        <div class="form-group">
          <label>Pays *</label>
          <select id="wCountry" required>
            <option value="">-- Choisir un pays --</option>
            <option value="CM">🇨🇲 Cameroun</option>
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
          <label>Opérateur *</label>
          <select id="wOperator" required disabled>
            <option value="">-- Choisir d'abord un pays --</option>
          </select>
        </div>

        <div class="form-group">
          <label>Numéro de téléphone *</label>
          <input type="tel" id="wPhone" required placeholder="+237 6XX XXX XXX" inputmode="tel">
        </div>

        <div class="form-group">
          <label>Nom complet du bénéficiaire *</label>
          <input type="text" id="wName" required maxlength="80" placeholder="Ex : Abdoula Diallo">
        </div>

        <div class="form-group">
          <label>Montant à retirer (FCFA) *</label>
          <div class="quick-amounts">
            <button type="button" class="qa-btn" data-amount="2000">2 000</button>
            <button type="button" class="qa-btn" data-amount="5000">5 000</button>
            <button type="button" class="qa-btn" data-amount="10000">10 000</button>
          </div>
          <input type="number" id="wAmount" required min="2000" step="500" placeholder="Minimum 2 000">
        </div>

        <div class="info-min" id="feeInfo" style="display:none;">
          Montant reçu : <strong id="netAmount">-</strong> F (frais 2%)
        </div>

        <button type="submit" class="btn-primary" id="withdrawBtn">
          <span>💸 Demander le retrait</span>
        </button>
      </form>
    </div>
  </div>

  <!-- TAB RECHARGE -->
  <div class="tab-content" id="tab-recharge">
    <div class="form-card">
      <h3>💰 Recharger mon wallet</h3>
      <div class="info-min">
        💡 Minimum 1 000 F · Paiement sécurisé via LeekPay
      </div>

      <div id="rechargeError" class="alert error" style="display:none;"></div>

      <form id="rechargeForm" onsubmit="submitRecharge(event)">
        <div class="form-group">
          <label>Pays *</label>
          <select id="rCountry" required>
            <option value="">-- Choisir un pays --</option>
            <option value="CM">🇨🇲 Cameroun</option>
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
          <label>Opérateur *</label>
          <select id="rOperator" required disabled>
            <option value="">-- Choisir d'abord un pays --</option>
          </select>
        </div>

        <div class="form-group">
          <label>Numéro de téléphone *</label>
          <input type="tel" id="rPhone" required placeholder="+237 6XX XXX XXX" inputmode="tel">
        </div>

        <div class="form-group">
          <label>Nom complet *</label>
          <input type="text" id="rName" required maxlength="80" placeholder="Ex : Abdoula Diallo">
        </div>

        <div class="form-group">
          <label>Montant à recharger (FCFA) *</label>
          <div class="quick-amounts">
            <button type="button" class="qa-btn" data-amount="1000">1 000</button>
            <button type="button" class="qa-btn" data-amount="3600">3 600</button>
            <button type="button" class="qa-btn" data-amount="5000">5 000</button>
          </div>
          <input type="number" id="rAmount" required min="1000" step="500" placeholder="Minimum 1 000">
        </div>

        <button type="submit" class="btn-primary gold" id="rechargeBtn">
          <span>💰 Recharger maintenant</span>
        </button>
      </form>
    </div>
  </div>

  <!-- TAB HISTORIQUE -->
  <div class="tab-content" id="tab-history">
    <div class="section-title"><span>💸 Retraits</span></div>
    <div class="history-list" id="withdrawalsList">
      <div class="skel-card"><div class="skel-line short"></div><div class="skel-line"></div></div>
    </div>

    <div class="section-title"><span>💰 Recharges</span></div>
    <div class="history-list" id="rechargesList">
      <div class="skel-card"><div class="skel-line short"></div><div class="skel-line"></div></div>
    </div>
  </div>

  <div style="height: 32px;"></div>
</div>

"""
    + JS_COMMUN
    + """
<script>
  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');

  if (!token || !userId) window.location.href = '/login';

  let isActivated = false;

  // Mapping pays → opérateurs
  const OPERATORS = {
    CM: [['mtn', '📱 MTN Mobile Money'], ['orange', '🟠 Orange Money']],
    CI: [['mtn', '📱 MTN'], ['orange', '🟠 Orange'], ['moov', '🔵 Moov'], ['wave', '🌊 Wave']],
    SN: [['orange', '🟠 Orange'], ['free', '🔵 Free'], ['wave', '🌊 Wave']],
    BJ: [['mtn', '📱 MTN'], ['moov', '🔵 Moov']],
    TG: [['togocom', '🔵 Togocom'], ['moov', '🟣 Moov']],
    BF: [['orange', '🟠 Orange'], ['moov', '🔵 Moov']],
    ML: [['orange', '🟠 Orange'], ['moov', '🔵 Moov']],
    NE: [['airtel', '🔴 Airtel'], ['orange', '🟠 Orange']],
    GN: [['orange', '🟠 Orange'], ['mtn', '📱 MTN']],
    CD: [['vodacom', '🔴 Vodacom'], ['airtel', '🔴 Airtel'], ['orange', '🟠 Orange']],
    CG: [['mtn', '📱 MTN'], ['airtel', '🔴 Airtel']],
    GA: [['airtel', '🔴 Airtel'], ['moov', '🔵 Moov']],
    TD: [['airtel', '🔴 Airtel'], ['tigo', '🔵 Tigo']],
    CF: [['orange', '🟠 Orange'], ['telecel', '🔵 Telecel']],
    GQ: [['orange', '🟠 Orange'], ['muni', '🔵 Muni']],
  };

  // ===== PROFIL =====
  async function loadProfile() {
    try {
      const res = await fetch('/api/auth/profile/' + userId + '?t=' + Date.now(), {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      if (!res.ok) return;
      const data = await res.json();
      const raw = data.profile?.is_activated;
      isActivated = (raw === true || raw === "true" || raw === 1 || raw === "1");
      if (!isActivated) document.getElementById('inactiveBanner').classList.add('show');

      const balance = Number(data.profile?.wallet_balance || 0);
      document.getElementById('walletBalance').innerHTML =
        balance.toLocaleString('fr-FR') + ' <span>FCFA</span>';
    } catch (e) {}
  }

  // ===== PAYS → OPÉRATEURS =====
  function setupCountryOperator(countryId, operatorId) {
    const countrySel = document.getElementById(countryId);
    const operatorSel = document.getElementById(operatorId);

    countrySel.addEventListener('change', function() {
      const code = this.value;
      operatorSel.innerHTML = '<option value="">-- Choisir un opérateur --</option>';

      if (OPERATORS[code]) {
        operatorSel.disabled = false;
        OPERATORS[code].forEach(([val, label]) => {
          const opt = document.createElement('option');
          opt.value = val;
          opt.textContent = label;
          operatorSel.appendChild(opt);
        });
      } else {
        operatorSel.disabled = true;
      }
    });
  }

  setupCountryOperator('wCountry', 'wOperator');
  setupCountryOperator('rCountry', 'rOperator');

  // ===== MONTANTS RAPIDES =====
  document.querySelectorAll('.qa-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const parent = this.closest('.form-group');
      parent.querySelectorAll('.qa-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      const input = parent.querySelector('input[type="number"]');
      input.value = this.dataset.amount;
      input.dispatchEvent(new Event('input'));
      vibrate(5);
    });
  });

  // ===== CALCUL FRAIS RETRAIT =====
  document.getElementById('wAmount').addEventListener('input', function() {
    const amount = parseFloat(this.value) || 0;
    const info = document.getElementById('feeInfo');
    if (amount >= 2000) {
      const fee = amount * 0.02;
      const net = amount - fee;
      document.getElementById('netAmount').textContent = net.toFixed(0);
      info.style.display = 'block';
    } else {
      info.style.display = 'none';
    }
  });

  // ===== SOUMETTRE RETRAIT =====
  async function submitWithdraw(e) {
    e.preventDefault();
    if (!isActivated) { showInactiveToast(); return; }

    const btn = document.getElementById('withdrawBtn');
    const errEl = document.getElementById('withdrawError');
    errEl.style.display = 'none';

    const payload = {
      country: document.getElementById('wCountry').value,
      operator: document.getElementById('wOperator').value,
      phone: document.getElementById('wPhone').value.trim(),
      full_name: document.getElementById('wName').value.trim(),
      amount: parseFloat(document.getElementById('wAmount').value) || 0,
    };

    if (!payload.country || !payload.operator || !payload.phone || !payload.full_name) {
      errEl.textContent = '⚠ Tous les champs sont obligatoires';
      errEl.style.display = 'block';
      return;
    }
    if (payload.amount < 2000) {
      errEl.textContent = '⚠ Montant minimum : 2 000 FCFA';
      errEl.style.display = 'block';
      return;
    }

    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div>';

    try {
      const res = await fetch('/api/payments/withdraw', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');

      vibrate(30);
      showToast('✅ Demande envoyée ! Traitement 24-72h');
      document.getElementById('withdrawForm').reset();
      document.getElementById('wOperator').disabled = true;
      document.getElementById('wOperator').innerHTML = '<option value="">-- Choisir d\\'abord un pays --</option>';
      document.getElementById('feeInfo').style.display = 'none';
      document.querySelectorAll('.qa-btn').forEach(b => b.classList.remove('active'));

      loadProfile();
      loadWithdrawals();
      setTimeout(() => {
        document.querySelector('[data-tab="history"]').click();
      }, 800);

    } catch (err) {
      errEl.textContent = '⚠ ' + err.message;
      errEl.style.display = 'block';
      btn.disabled = false;
      btn.innerHTML = '<span>💸 Demander le retrait</span>';
    }
  }

  // ===== SOUMETTRE RECHARGE =====
  async function submitRecharge(e) {
    e.preventDefault();
    if (!isActivated) { showInactiveToast(); return; }

    const btn = document.getElementById('rechargeBtn');
    const errEl = document.getElementById('rechargeError');
    errEl.style.display = 'none';

    const payload = {
      country: document.getElementById('rCountry').value,
      operator: document.getElementById('rOperator').value,
      phone: document.getElementById('rPhone').value.trim(),
      full_name: document.getElementById('rName').value.trim(),
      amount: parseFloat(document.getElementById('rAmount').value) || 0,
    };

    if (!payload.country || !payload.operator || !payload.phone || !payload.full_name) {
      errEl.textContent = '⚠ Tous les champs sont obligatoires';
      errEl.style.display = 'block';
      return;
    }
    if (payload.amount < 1000) {
      errEl.textContent = '⚠ Montant minimum : 1 000 FCFA';
      errEl.style.display = 'block';
      return;
    }

    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div>';

    try {
      const res = await fetch('/api/payments/recharge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erreur');

      if (data.payment_url) {
        vibrate(20);
        showToast('✅ Redirection vers LeekPay...');
        setTimeout(() => window.location.href = data.payment_url, 800);
      } else {
        throw new Error('URL de paiement manquante');
      }

    } catch (err) {
      errEl.textContent = '⚠ ' + err.message;
      errEl.style.display = 'block';
      btn.disabled = false;
      btn.innerHTML = '<span>💰 Recharger maintenant</span>';
    }
  }

  // ===== CHARGER HISTORIQUES =====
  async function loadWithdrawals() {
    const list = document.getElementById('withdrawalsList');
    try {
      const res = await fetch('/api/payments/withdrawals?t=' + Date.now(), {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      const data = await res.json();
      const items = data.withdrawals || [];

      if (items.length === 0) {
        list.innerHTML = '<div class="empty-state"><div class="icon">💸</div><h3>Aucun retrait</h3><p>Vos retraits apparaîtront ici.</p></div>';
        return;
      }

      list.innerHTML = items.map(w => {
        const statusLabel = {pending: 'En attente', processing: 'Traitement', completed: 'Complété', rejected: 'Rejeté'}[w.status] || w.status;
        const icon = w.status === 'completed' ? 'green' : w.status === 'rejected' ? 'red' : 'yellow';
        return `
          <div class="history-item">
            <div class="hi-icon ${icon}">💸</div>
            <div class="hi-info">
              <div class="hi-title">${escapeHtml(w.operator)} · ${escapeHtml(w.phone)}</div>
              <div class="hi-meta">
                <span>${formatDate(w.created_at)}</span>
                <span class="hi-badge ${w.status}">${statusLabel}</span>
              </div>
            </div>
            <div class="hi-amount negative">-${Number(w.amount).toLocaleString('fr-FR')} F</div>
          </div>
        `;
      }).join('');
    } catch (e) {
      list.innerHTML = '<div class="empty-state"><h3>Erreur</h3></div>';
    }
  }

  async function loadRecharges() {
    const list = document.getElementById('rechargesList');
    try {
      const res = await fetch('/api/payments/recharges?t=' + Date.now(), {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      const data = await res.json();
      const items = data.recharges || [];

      if (items.length === 0) {
        list.innerHTML = '<div class="empty-state"><div class="icon">💰</div><h3>Aucune recharge</h3><p>Vos recharges apparaîtront ici.</p></div>';
        return;
      }

      list.innerHTML = items.map(r => {
        const statusLabel = {pending: 'En attente', completed: 'Complété', failed: 'Échoué', cancelled: 'Annulé'}[r.status] || r.status;
        const icon = r.status === 'completed' ? 'green' : r.status === 'pending' ? 'yellow' : 'red';
        return `
          <div class="history-item">
            <div class="hi-icon recharge">💰</div>
            <div class="hi-info">
              <div class="hi-title">${escapeHtml(r.operator)} · ${escapeHtml(r.phone)}</div>
              <div class="hi-meta">
                <span>${formatDate(r.created_at)}</span>
                <span class="hi-badge ${r.status}">${statusLabel}</span>
              </div>
            </div>
            <div class="hi-amount positive">+${Number(r.amount).toLocaleString('fr-FR')} F</div>
          </div>
        `;
      }).join('');
    } catch (e) {
      list.innerHTML = '<div class="empty-state"><h3>Erreur</h3></div>';
    }
  }

  // ===== TABS =====
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      document.getElementById('tab-' + this.dataset.tab).classList.add('active');
      vibrate(5);

      if (this.dataset.tab === 'history') {
        loadWithdrawals();
        loadRecharges();
      }
    });
  });

  // ===== HELPERS =====
  function escapeHtml(s) {
    if (!s) return '';
    return String(s).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
  }

  function formatDate(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    const diff = (Date.now() - d) / 1000;
    if (diff < 3600) return Math.floor(diff / 60) + ' min';
    if (diff < 86400) return Math.floor(diff / 3600) + 'h';
    if (diff < 604800) return Math.floor(diff / 86400) + 'j';
    return d.toLocaleDateString('fr-FR');
  }

  function showInactiveToast() {
    vibrate([20, 40, 20]);
    const t = document.createElement('div');
    t.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,#e65100,#bf360c);color:#fff;padding:16px 20px;border-radius:16px;font-size:13px;font-weight:600;z-index:10000;box-shadow:0 10px 30px rgba(230,81,0,0.5);max-width:340px;text-align:center;line-height:1.5;';
    t.innerHTML = '<div><strong>Compte non activé</strong></div><button onclick="location.href=\\'/activation\\'" style="margin-top:12px;background:#fff;color:#e65100;border:none;padding:10px 20px;border-radius:10px;font-weight:800;font-size:13px;cursor:pointer;font-family:inherit;width:100%;">Activer</button>';
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 5000);
  }

  function showToast(msg) {
    const t = document.createElement('div');
    t.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,#2e7d32,#1b5e20);color:#fff;padding:14px 20px;border-radius:14px;font-size:13px;font-weight:700;z-index:10001;box-shadow:0 8px 24px rgba(0,0,0,0.3);max-width:340px;text-align:center;';
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
  }

  // ===== INIT =====
  (async () => {
    await loadProfile();
    loadWithdrawals();
    loadRecharges();
  })();
</script>
</body>
</html>
"""
)